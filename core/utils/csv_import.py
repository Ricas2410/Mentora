import csv
import io
from django.db import transaction
from django.core.exceptions import ValidationError
from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice, StudyNote
from core.models import CSVImportLog


class CSVImporter:
    """
    Utility class for importing educational content from CSV files
    """

    def __init__(self, import_type, file_content, user=None):
        self.import_type = import_type
        self.file_content = file_content
        self.user = user
        self.log = None
        self.errors = []
        self.successful_rows = 0
        self.failed_rows = 0

    def import_data(self):
        """Main import method"""
        try:
            # Create import log
            self.log = CSVImportLog.objects.create(
                import_type=self.import_type,
                file_name=f"{self.import_type}_import.csv",
                imported_by=self.user,
                status='processing'
            )

            # Parse CSV
            csv_data = self.parse_csv()
            self.log.total_rows = len(csv_data)
            self.log.save()

            # Add diagnostic information for questions import
            if self.import_type == 'questions':
                self._add_diagnostic_info()

            # Import questions only
            if self.import_type == 'questions':
                self.import_questions(csv_data)
            else:
                raise ValueError(f"Unsupported import type: {self.import_type}")

            # Update log
            self.log.successful_rows = self.successful_rows
            self.log.failed_rows = self.failed_rows

            if self.failed_rows == 0:
                self.log.status = 'completed'
            elif self.successful_rows > 0:
                self.log.status = 'partial'
            else:
                self.log.status = 'failed'

            if self.errors:
                self.log.error_log = '\n'.join(self.errors)

            self.log.mark_completed()

            return {
                'success': True,
                'total_rows': self.log.total_rows,
                'successful_rows': self.successful_rows,
                'failed_rows': self.failed_rows,
                'errors': self.errors
            }

        except Exception as e:
            if self.log:
                self.log.status = 'failed'
                self.log.add_error(str(e))
                self.log.mark_completed()

            return {
                'success': False,
                'error': str(e),
                'errors': self.errors
            }

    def _add_diagnostic_info(self):
        """Add diagnostic information to help with troubleshooting"""
        # Get available subjects, levels, and topics
        subjects = list(Subject.objects.filter(is_active=True).values_list('name', flat=True))
        levels = list(ClassLevel.objects.filter(is_active=True).select_related('subject').values_list('name', 'subject__name'))
        topics = list(Topic.objects.filter(is_active=True).select_related('class_level__subject').values_list('title', 'class_level__name', 'class_level__subject__name'))

        diagnostic_info = f"""
DIAGNOSTIC INFORMATION:
Available Subjects: {', '.join(subjects) if subjects else 'None'}
Available Class Levels: {', '.join([f'{level[0]} ({level[1]})' for level in levels]) if levels else 'None'}
Available Topics: {', '.join([f'{topic[0]} ({topic[1]} - {topic[2]})' for topic in topics[:10]]) if topics else 'None'}
{f'... and {len(topics) - 10} more topics' if len(topics) > 10 else ''}
"""

        if self.log:
            self.log.add_error(diagnostic_info)

    def parse_csv(self):
        """Parse CSV content"""
        try:
            # Handle both string and bytes
            if isinstance(self.file_content, bytes):
                content = self.file_content.decode('utf-8')
            else:
                content = self.file_content

            # Parse CSV
            csv_reader = csv.DictReader(io.StringIO(content))
            return list(csv_reader)

        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {str(e)}")

    def get_preview_data(self):
        """Get preview data for CSV import"""
        try:
            csv_data = self.parse_csv()

            preview_data = {
                'total_rows': len(csv_data),
                'headers': list(csv_data[0].keys()) if csv_data else [],
                'sample_rows': csv_data,  # Show all rows for preview
                'validation_results': [],
                'warnings': [],
                'errors': []
            }

            # Validate each row and collect issues
            required_fields = ['subject_name', 'class_level_name', 'topic_title', 'question_text', 'question_type']

            for row_num, row in enumerate(csv_data[:20], 1):  # Check first 20 rows for validation
                row_validation = {
                    'row_number': row_num,
                    'issues': [],
                    'warnings': [],
                    'status': 'valid'
                }

                # Check required fields
                missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
                if missing_fields:
                    row_validation['issues'].append(f"Missing required fields: {', '.join(missing_fields)}")
                    row_validation['status'] = 'error'

                # Validate question type
                question_type = row.get('question_type', '').lower()
                if question_type and question_type not in ['multiple_choice', 'fill_blank', 'true_false', 'short_answer']:
                    row_validation['issues'].append(f"Invalid question type: {question_type}")
                    row_validation['status'] = 'error'

                # Check question type specific requirements
                if question_type == 'multiple_choice':
                    if not row.get('correct_answer'):
                        row_validation['issues'].append("Multiple choice questions require 'correct_answer' field")
                        row_validation['status'] = 'error'
                    elif row.get('correct_answer', '').lower() not in ['a', 'b', 'c', 'd']:
                        row_validation['issues'].append("Multiple choice 'correct_answer' must be a, b, c, or d")
                        row_validation['status'] = 'error'

                    # Check choices
                    choices_provided = sum(1 for choice in ['choice_a', 'choice_b', 'choice_c', 'choice_d'] if row.get(choice, '').strip())
                    if choices_provided < 2:
                        row_validation['warnings'].append("Multiple choice questions should have at least 2 answer choices")

                elif question_type in ['fill_blank', 'short_answer']:
                    if not row.get('correct_answer'):
                        row_validation['issues'].append(f"{question_type} questions require 'correct_answer' field")
                        row_validation['status'] = 'error'

                elif question_type == 'true_false':
                    correct_answer = row.get('correct_answer', '').lower()
                    if correct_answer not in ['true', 'false', 't', 'f', '1', '0']:
                        row_validation['issues'].append("True/False questions require 'correct_answer' to be true/false, t/f, or 1/0")
                        row_validation['status'] = 'error'

                # Check if entities exist
                try:
                    subject_name = row.get('subject_name', '').strip()
                    if subject_name:
                        from subjects.models import Subject
                        if not Subject.objects.filter(name__iexact=subject_name).exists():
                            row_validation['warnings'].append(f"Subject '{subject_name}' does not exist")
                except:
                    pass

                if row_validation['issues'] or row_validation['warnings']:
                    preview_data['validation_results'].append(row_validation)

            # Summary statistics
            error_count = sum(1 for result in preview_data['validation_results'] if result['status'] == 'error')
            warning_count = sum(1 for result in preview_data['validation_results'] if result['warnings'])

            preview_data['summary'] = {
                'total_rows': len(csv_data),
                'rows_with_errors': error_count,
                'rows_with_warnings': warning_count,
                'estimated_success_rate': max(0, (len(csv_data) - error_count) / len(csv_data) * 100) if csv_data else 0
            }

            return preview_data

        except Exception as e:
            raise ValueError(f"Failed to generate preview: {str(e)}")

    def import_questions(self, csv_data):
        """Import questions from CSV with proper hierarchy validation"""
        required_fields = ['subject_name', 'class_level_name', 'topic_title', 'question_text', 'question_type']

        for row_num, row in enumerate(csv_data, 1):
            try:
                # Validate required fields
                missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
                if missing_fields:
                    available_fields = list(row.keys())
                    raise ValueError(f"Missing required fields: {', '.join(missing_fields)}. Available fields: {', '.join(available_fields)}")

                # Validate question type and required fields
                question_type = row['question_type'].lower()
                if question_type not in ['multiple_choice', 'fill_blank', 'true_false', 'short_answer']:
                    raise ValueError(f"Invalid question type: {question_type}. Must be one of: multiple_choice, fill_blank, true_false, short_answer")

                # Find subject
                subject = Subject.objects.filter(name__iexact=row['subject_name']).first()
                if not subject:
                    raise ValueError(f"Subject '{row['subject_name']}' not found. Please create the subject first.")

                # Find class level within the subject
                class_level = ClassLevel.objects.filter(
                    subject=subject,
                    name__iexact=row['class_level_name']
                ).first()
                if not class_level:
                    raise ValueError(f"Class level '{row['class_level_name']}' not found in subject '{subject.name}'. Please create the class level first.")

                # Find or create topic within the class level
                topic = Topic.objects.filter(
                    class_level=class_level,
                    title__iexact=row['topic_title']
                ).first()
                if not topic:
                    # Auto-create missing topic
                    topic = Topic.objects.create(
                        class_level=class_level,
                        title=row['topic_title'].strip(),
                        description=f"Auto-created topic for {row['topic_title']}",
                        order=Topic.objects.filter(class_level=class_level).count() + 1,
                        difficulty_level='beginner',
                        estimated_duration=30,
                        is_active=True
                    )
                    self.log.add_info(f"Auto-created topic: '{topic.title}' in {subject.name} - {class_level.name}")

                # Validate question type specific requirements
                if question_type == 'multiple_choice':
                    if not row.get('correct_answer'):
                        raise ValueError("Multiple choice questions require 'correct_answer' field (a, b, c, or d)")
                    if row['correct_answer'].lower() not in ['a', 'b', 'c', 'd']:
                        raise ValueError("Multiple choice 'correct_answer' must be a, b, c, or d")

                    # Check if at least 2 choices are provided
                    choices_provided = sum(1 for choice in ['choice_a', 'choice_b', 'choice_c', 'choice_d'] if row.get(choice, '').strip())
                    if choices_provided < 2:
                        raise ValueError("Multiple choice questions require at least 2 answer choices")

                elif question_type in ['fill_blank', 'short_answer']:
                    if not row.get('correct_answer'):
                        raise ValueError(f"{question_type} questions require 'correct_answer' field")

                elif question_type == 'true_false':
                    if row.get('correct_answer', '').lower() not in ['true', 'false', 't', 'f', '1', '0']:
                        raise ValueError("True/False questions require 'correct_answer' to be true/false, t/f, or 1/0")

                with transaction.atomic():
                    # Create question
                    question = Question.objects.create(
                        topic=topic,
                        question_text=row['question_text'].strip(),
                        question_type=question_type,
                        correct_answer=row.get('correct_answer', '').strip(),
                        explanation=row.get('explanation', '').strip(),
                        difficulty=row.get('difficulty', 'medium').lower(),
                        points=int(row.get('points', 1)),
                        time_limit=int(row.get('time_limit', 45)),
                        created_by=self.user
                    )

                    # Create answer choices for multiple choice questions
                    if question.question_type == 'multiple_choice':
                        choices = [
                            ('a', row.get('choice_a', '').strip()),
                            ('b', row.get('choice_b', '').strip()),
                            ('c', row.get('choice_c', '').strip()),
                            ('d', row.get('choice_d', '').strip())
                        ]

                        for choice_value, choice_text in choices:
                            if choice_text:
                                AnswerChoice.objects.create(
                                    question=question,
                                    choice_text=choice_text,
                                    is_correct=(choice_value == row['correct_answer'].lower()),
                                    order=ord(choice_value) - ord('a')
                                )

                self.successful_rows += 1

            except Exception as e:
                self.failed_rows += 1
                error_msg = f"Row {row_num}: {str(e)}"
                self.errors.append(error_msg)
                if self.log:
                    self.log.add_error(error_msg)

    def import_study_notes(self, csv_data):
        """Import study notes from CSV with proper hierarchy validation"""
        required_fields = ['subject_name', 'class_level_name', 'topic_title', 'note_title', 'content']

        for row_num, row in enumerate(csv_data, 1):
            try:
                # Validate required fields
                missing_fields = [field for field in required_fields if not row.get(field)]
                if missing_fields:
                    raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

                # Find subject
                subject = Subject.objects.filter(name__iexact=row['subject_name']).first()
                if not subject:
                    raise ValueError(f"Subject '{row['subject_name']}' not found. Please create the subject first.")

                # Find class level within the subject
                class_level = ClassLevel.objects.filter(
                    subject=subject,
                    name__iexact=row['class_level_name']
                ).first()
                if not class_level:
                    raise ValueError(f"Class level '{row['class_level_name']}' not found in subject '{subject.name}'. Please create the class level first.")

                # Find or create topic within the class level
                topic = Topic.objects.filter(
                    class_level=class_level,
                    title__iexact=row['topic_title']
                ).first()
                if not topic:
                    # Auto-create missing topic
                    topic = Topic.objects.create(
                        class_level=class_level,
                        title=row['topic_title'].strip(),
                        description=f"Auto-created topic for {row['topic_title']}",
                        order=Topic.objects.filter(class_level=class_level).count() + 1,
                        difficulty_level='beginner',
                        estimated_duration=30,
                        is_active=True
                    )
                    self.log.add_info(f"Auto-created topic: '{topic.title}' in {subject.name} - {class_level.name}")

                # Create study note
                StudyNote.objects.create(
                    topic=topic,
                    title=row['note_title'].strip(),
                    content=row['content'].strip(),
                    order=int(row.get('order', 1)),
                    created_by=self.user
                )

                self.successful_rows += 1

            except Exception as e:
                self.failed_rows += 1
                error_msg = f"Row {row_num}: {str(e)}"
                self.errors.append(error_msg)
                if self.log:
                    self.log.add_error(error_msg)

    def import_subjects(self, csv_data):
        """Import subjects from CSV"""
        required_fields = ['name', 'description']

        for row_num, row in enumerate(csv_data, 1):
            try:
                # Validate required fields
                missing_fields = [field for field in required_fields if not row.get(field)]
                if missing_fields:
                    raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

                # Create or update subject
                subject, created = Subject.objects.get_or_create(
                    name=row['name'],
                    defaults={
                        'description': row['description'],
                        'icon': row.get('icon', '📚'),
                        'color': row.get('color', '#3B82F6'),
                        'order': int(row.get('order', 1))
                    }
                )

                if not created:
                    # Update existing subject
                    subject.description = row['description']
                    subject.icon = row.get('icon', subject.icon)
                    subject.color = row.get('color', subject.color)
                    subject.order = int(row.get('order', subject.order))
                    subject.save()

                self.successful_rows += 1

            except Exception as e:
                self.failed_rows += 1
                error_msg = f"Row {row_num}: {str(e)}"
                self.errors.append(error_msg)
                if self.log:
                    self.log.add_error(error_msg)

    def import_class_levels(self, csv_data):
        """Import class levels from CSV"""
        required_fields = ['subject_name', 'name', 'level_number']

        for row_num, row in enumerate(csv_data, 1):
            try:
                # Validate required fields
                missing_fields = [field for field in required_fields if not row.get(field)]
                if missing_fields:
                    raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

                # Find subject
                subject = Subject.objects.filter(name__iexact=row['subject_name']).first()
                if not subject:
                    raise ValueError(f"Subject '{row['subject_name']}' not found. Please create the subject first.")

                # Validate level number
                try:
                    level_number = int(row['level_number'])
                except ValueError:
                    raise ValueError(f"Invalid level_number: {row['level_number']}. Must be a number.")

                # Create or update class level
                class_level, created = ClassLevel.objects.get_or_create(
                    subject=subject,
                    level_number=level_number,
                    defaults={
                        'name': row['name'],
                        'description': row.get('description', ''),
                        'pass_percentage': int(row.get('pass_percentage', 60))
                    }
                )

                if not created:
                    # Update existing class level
                    class_level.name = row['name']
                    class_level.description = row.get('description', class_level.description)
                    class_level.pass_percentage = int(row.get('pass_percentage', class_level.pass_percentage))
                    class_level.save()

                self.successful_rows += 1

            except Exception as e:
                self.failed_rows += 1
                error_msg = f"Row {row_num}: {str(e)}"
                self.errors.append(error_msg)
                if self.log:
                    self.log.add_error(error_msg)

    def import_topics(self, csv_data):
        """Import topics from CSV"""
        required_fields = ['subject_name', 'level_name', 'title', 'description']

        for row_num, row in enumerate(csv_data, 1):
            try:
                # Validate required fields
                missing_fields = [field for field in required_fields if not row.get(field)]
                if missing_fields:
                    raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

                # Find subject and level
                subject = Subject.objects.filter(name__icontains=row['subject_name']).first()
                if not subject:
                    raise ValueError(f"Subject not found: {row['subject_name']}")

                level = ClassLevel.objects.filter(
                    subject=subject,
                    name__icontains=row['level_name']
                ).first()
                if not level:
                    raise ValueError(f"Level not found: {row['level_name']}")

                # Create topic
                Topic.objects.create(
                    class_level=level,
                    title=row['title'],
                    description=row['description'],
                    order=int(row.get('order', 1)),
                    estimated_duration=int(row.get('estimated_duration', 30)),
                    difficulty_level=row.get('difficulty_level', 'beginner')
                )

                self.successful_rows += 1

            except Exception as e:
                self.failed_rows += 1
                error_msg = f"Row {row_num}: {str(e)}"
                self.errors.append(error_msg)
                if self.log:
                    self.log.add_error(error_msg)


def get_csv_template(import_type):
    """Get CSV template for questions import"""
    if import_type == 'questions':
        return [
            'subject_name', 'class_level_name', 'topic_title', 'question_text', 'question_type',
            'correct_answer', 'explanation', 'difficulty', 'points', 'time_limit',
            'choice_a', 'choice_b', 'choice_c', 'choice_d'
        ]
    return []
