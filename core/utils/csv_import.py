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

    def __init__(self, import_type, file_content, user=None, import_mode='strict'):
        self.import_type = import_type
        self.file_content = file_content
        self.user = user
        self.import_mode = import_mode  # 'strict' or 'partial'
        self.log = None
        self.errors = []
        self.successful_rows = 0
        self.failed_rows = 0
        self.skipped_rows = []  # For partial import mode

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
        """Get preview data for CSV import with graceful handling"""
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
                question_type = row.get('question_type', '').strip().lower()
                valid_question_types = ['multiple_choice', 'fill_blank', 'true_false', 'short_answer']

                if not question_type:
                    row_validation['issues'].append("Missing question type")
                    row_validation['status'] = 'error'
                elif question_type not in valid_question_types:
                    # Handle common variations and provide helpful suggestions
                    suggestions = {
                        'mc': 'multiple_choice',
                        'multiple': 'multiple_choice',
                        'choice': 'multiple_choice',
                        'mcq': 'multiple_choice',
                        'fill': 'fill_blank',
                        'blank': 'fill_blank',
                        'tf': 'true_false',
                        'boolean': 'true_false',
                        'short': 'short_answer',
                        'essay': 'short_answer',
                        'text': 'short_answer'
                    }

                    suggestion = suggestions.get(question_type, None)
                    if suggestion:
                        row_validation['issues'].append(f"Invalid question type: '{question_type}'. Did you mean '{suggestion}'?")
                    else:
                        row_validation['issues'].append(f"Invalid question type: '{question_type}'. Must be one of: {', '.join(valid_question_types)}")
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

                # Check if entities exist (show as warnings since we auto-create them)
                try:
                    subject_name = row.get('subject_name', '').strip()
                    class_level_name = row.get('class_level_name', '').strip()

                    if subject_name:
                        from subjects.models import Subject, ClassLevel
                        subject = Subject.objects.filter(name__iexact=subject_name).first()
                        if not subject:
                            row_validation['warnings'].append(f"Subject '{subject_name}' will be auto-created")
                        elif class_level_name:
                            class_level = ClassLevel.objects.filter(
                                subject=subject,
                                name__iexact=class_level_name
                            ).first()
                            if not class_level:
                                row_validation['warnings'].append(f"Class level '{class_level_name}' will be auto-created in {subject_name}")
                except:
                    pass

                if row_validation['issues'] or row_validation['warnings']:
                    preview_data['validation_results'].append(row_validation)

            # Summary statistics
            error_count = sum(1 for result in preview_data['validation_results'] if result['status'] == 'error')
            warning_count = sum(1 for result in preview_data['validation_results'] if result['warnings'])
            valid_rows = len(csv_data) - error_count

            preview_data['summary'] = {
                'total_rows': len(csv_data),
                'rows_with_errors': error_count,
                'rows_with_warnings': warning_count,
                'valid_rows': valid_rows,
                'estimated_success_rate': max(0, valid_rows / len(csv_data) * 100) if csv_data else 0
            }

            return preview_data

        except Exception as e:
            raise ValueError(f"Failed to generate preview: {str(e)}")

    def import_questions(self, csv_data):
        """Optimized bulk import of questions from CSV with proper hierarchy validation"""
        required_fields = ['subject_name', 'class_level_name', 'topic_title', 'question_text', 'question_type']

        print(f"🚀 Starting optimized bulk import of {len(csv_data)} questions...")

        # Pre-process and validate all data first
        validated_data = []
        subjects_cache = {}
        class_levels_cache = {}
        topics_cache = {}

        # Phase 1: Validate and prepare all data
        for row_num, row in enumerate(csv_data, 1):
            try:
                # Validate required fields
                missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
                if missing_fields:
                    available_fields = list(row.keys())
                    raise ValueError(f"Missing required fields: {', '.join(missing_fields)}. Available fields: {', '.join(available_fields)}")

                # Validate question type and required fields
                question_type = row.get('question_type', '').strip().lower()
                valid_question_types = ['multiple_choice', 'fill_blank', 'true_false', 'short_answer']

                if not question_type:
                    raise ValueError("Missing question type field")
                elif question_type not in valid_question_types:
                    # Handle common variations and provide helpful suggestions
                    suggestions = {
                        'mc': 'multiple_choice',
                        'multiple': 'multiple_choice',
                        'choice': 'multiple_choice',
                        'mcq': 'multiple_choice',
                        'fill': 'fill_blank',
                        'blank': 'fill_blank',
                        'tf': 'true_false',
                        'boolean': 'true_false',
                        'short': 'short_answer',
                        'essay': 'short_answer',
                        'text': 'short_answer'
                    }

                    suggestion = suggestions.get(question_type, None)
                    if suggestion:
                        raise ValueError(f"Invalid question type: '{question_type}'. Did you mean '{suggestion}'? Valid types: {', '.join(valid_question_types)}")
                    else:
                        raise ValueError(f"Invalid question type: '{question_type}'. Must be one of: {', '.join(valid_question_types)}")

                # Store validated row data
                validated_data.append({
                    'row_num': row_num,
                    'subject_name': row['subject_name'].strip(),
                    'class_level_name': row['class_level_name'].strip(),
                    'topic_title': row['topic_title'].strip(),
                    'question_text': row['question_text'].strip(),
                    'question_type': question_type,
                    'correct_answer': row.get('correct_answer', '').strip(),
                    'explanation': row.get('explanation', '').strip(),
                    'difficulty': row.get('difficulty', 'medium').lower(),
                    'points': int(row.get('points', 1)),
                    'time_limit': int(row.get('time_limit', 45)),
                    'choice_a': row.get('choice_a', '').strip(),
                    'choice_b': row.get('choice_b', '').strip(),
                    'choice_c': row.get('choice_c', '').strip(),
                    'choice_d': row.get('choice_d', '').strip(),
                })

            except Exception as e:
                self.failed_rows += 1
                error_msg = f"Row {row_num}: {str(e)}"
                if self.import_mode == 'partial':
                    self.skipped_rows.append({
                        'row_number': row_num,
                        'error': str(e),
                        'data': dict(row)
                    })
                    if self.log:
                        self.log.add_warning(f"Skipped {error_msg}")
                else:
                    self.errors.append(error_msg)
                    if self.log:
                        self.log.add_error(error_msg)

        print(f"📋 Validated {len(validated_data)} questions, {self.failed_rows} failed validation")

        # Phase 2: Bulk create hierarchy (subjects, class levels, topics)
        if self.log:
            self.log.add_info("Phase 2: Creating hierarchy (subjects, class levels, topics)")
        self._bulk_create_hierarchy(validated_data, subjects_cache, class_levels_cache, topics_cache)

        # Phase 3: Bulk create questions and answer choices
        if self.log:
            self.log.add_info("Phase 3: Bulk creating questions and answer choices")
        self._bulk_create_questions(validated_data, topics_cache)

    def _bulk_create_hierarchy(self, validated_data, subjects_cache, class_levels_cache, topics_cache):
        """Bulk create subjects, class levels, and topics"""
        print("🏗️ Creating hierarchy (subjects, class levels, topics)...")

        # Collect unique hierarchy items
        unique_subjects = set()
        unique_class_levels = set()
        unique_topics = set()

        for data in validated_data:
            unique_subjects.add(data['subject_name'])
            unique_class_levels.add((data['subject_name'], data['class_level_name']))
            unique_topics.add((data['subject_name'], data['class_level_name'], data['topic_title']))

        # Bulk create subjects
        existing_subjects = {s.name.lower(): s for s in Subject.objects.all()}
        subjects_to_create = []

        for subject_name in unique_subjects:
            if subject_name.lower() not in existing_subjects:
                subjects_to_create.append(Subject(
                    name=subject_name,
                    description=f"Auto-created subject for {subject_name}",
                    icon='📚',
                    color='#3B82F6',
                    order=len(existing_subjects) + len(subjects_to_create) + 1,
                    is_active=True
                ))

        if subjects_to_create:
            Subject.objects.bulk_create(subjects_to_create)
            print(f"✅ Created {len(subjects_to_create)} new subjects")
            if self.log:
                self.log.add_info(f"Created {len(subjects_to_create)} new subjects: {[s.name for s in subjects_to_create]}")

        # Refresh subjects cache
        for subject in Subject.objects.all():
            subjects_cache[subject.name.lower()] = subject

        # Bulk create class levels
        existing_class_levels = {(cl.subject.name.lower(), cl.name.lower()): cl for cl in ClassLevel.objects.select_related('subject')}
        class_levels_to_create = []

        for subject_name, class_level_name in unique_class_levels:
            key = (subject_name.lower(), class_level_name.lower())
            if key not in existing_class_levels:
                subject = subjects_cache[subject_name.lower()]

                # Extract level number from name
                import re
                level_match = re.search(r'\d+', class_level_name)
                level_number = int(level_match.group()) if level_match else ClassLevel.objects.filter(subject=subject).count() + 1

                class_levels_to_create.append(ClassLevel(
                    subject=subject,
                    name=class_level_name,
                    level_number=level_number,
                    description=f"Auto-created class level for {class_level_name}",
                    pass_percentage=60,
                    is_active=True
                ))

        if class_levels_to_create:
            ClassLevel.objects.bulk_create(class_levels_to_create)
            print(f"✅ Created {len(class_levels_to_create)} new class levels")

        # Refresh class levels cache
        for class_level in ClassLevel.objects.select_related('subject'):
            key = (class_level.subject.name.lower(), class_level.name.lower())
            class_levels_cache[key] = class_level

        # Bulk create topics
        existing_topics = {(t.class_level.subject.name.lower(), t.class_level.name.lower(), t.title.lower()): t
                          for t in Topic.objects.select_related('class_level__subject')}
        topics_to_create = []

        for subject_name, class_level_name, topic_title in unique_topics:
            key = (subject_name.lower(), class_level_name.lower(), topic_title.lower())
            if key not in existing_topics:
                class_level = class_levels_cache[(subject_name.lower(), class_level_name.lower())]

                topics_to_create.append(Topic(
                    class_level=class_level,
                    title=topic_title,
                    description=f"Auto-created topic for {topic_title}",
                    order=Topic.objects.filter(class_level=class_level).count() + 1,
                    difficulty_level='beginner',
                    estimated_duration=30,
                    is_active=True
                ))

        if topics_to_create:
            Topic.objects.bulk_create(topics_to_create)
            print(f"✅ Created {len(topics_to_create)} new topics")

        # Refresh topics cache
        for topic in Topic.objects.select_related('class_level__subject'):
            key = (topic.class_level.subject.name.lower(), topic.class_level.name.lower(), topic.title.lower())
            topics_cache[key] = topic
    def _bulk_create_questions(self, validated_data, topics_cache):
        """Bulk create questions and answer choices"""
        print(f"📝 Bulk creating {len(validated_data)} questions...")

        questions_to_create = []
        answer_choices_to_create = []

        # Prepare questions for bulk creation
        for data in validated_data:
            try:
                # Get topic from cache
                topic_key = (data['subject_name'].lower(), data['class_level_name'].lower(), data['topic_title'].lower())
                topic = topics_cache.get(topic_key)

                if not topic:
                    raise ValueError(f"Topic not found: {data['topic_title']}")

                # Validate question type specific requirements
                if data['question_type'] == 'multiple_choice':
                    if not data['correct_answer']:
                        raise ValueError("Multiple choice questions require 'correct_answer' field (a, b, c, or d)")
                    if data['correct_answer'].lower() not in ['a', 'b', 'c', 'd']:
                        raise ValueError("Multiple choice 'correct_answer' must be a, b, c, or d")

                    # Check if at least 2 choices are provided
                    choices_provided = sum(1 for choice in [data['choice_a'], data['choice_b'], data['choice_c'], data['choice_d']] if choice)
                    if choices_provided < 2:
                        raise ValueError("Multiple choice questions require at least 2 answer choices")

                elif data['question_type'] in ['fill_blank', 'short_answer']:
                    if not data['correct_answer']:
                        raise ValueError(f"{data['question_type']} questions require 'correct_answer' field")

                elif data['question_type'] == 'true_false':
                    if data['correct_answer'].lower() not in ['true', 'false', 't', 'f', '1', '0']:
                        raise ValueError("True/False questions require 'correct_answer' to be true/false, t/f, or 1/0")

                # Create question object (not saved yet)
                question = Question(
                    topic=topic,
                    question_text=data['question_text'],
                    question_type=data['question_type'],
                    correct_answer=data['correct_answer'],
                    explanation=data['explanation'],
                    difficulty=data['difficulty'],
                    points=data['points'],
                    time_limit=data['time_limit'],
                    created_by=self.user
                )

                questions_to_create.append((question, data))

            except Exception as e:
                self.failed_rows += 1
                error_msg = f"Row {data['row_num']}: {str(e)}"
                if self.import_mode == 'partial':
                    self.skipped_rows.append({
                        'row_number': data['row_num'],
                        'error': str(e),
                        'data': data
                    })
                    if self.log:
                        self.log.add_warning(f"Skipped {error_msg}")
                else:
                    self.errors.append(error_msg)
                    if self.log:
                        self.log.add_error(error_msg)

        # Bulk create questions in chunks for better performance
        chunk_size = 500  # Process 500 questions at a time
        total_chunks = (len(questions_to_create) + chunk_size - 1) // chunk_size

        for chunk_num in range(total_chunks):
            start_idx = chunk_num * chunk_size
            end_idx = min(start_idx + chunk_size, len(questions_to_create))
            chunk = questions_to_create[start_idx:end_idx]

            print(f"📦 Processing chunk {chunk_num + 1}/{total_chunks} ({len(chunk)} questions)")

            try:
                with transaction.atomic():
                    # Extract just the question objects for bulk_create
                    questions_only = [item[0] for item in chunk]
                    created_questions = Question.objects.bulk_create(questions_only)

                    # Create answer choices for multiple choice questions
                    choices_batch = []
                    for i, (question, data) in enumerate(chunk):
                        created_question = created_questions[i]

                        if data['question_type'] == 'multiple_choice':
                            choices = [
                                ('a', data['choice_a']),
                                ('b', data['choice_b']),
                                ('c', data['choice_c']),
                                ('d', data['choice_d'])
                            ]

                            for choice_value, choice_text in choices:
                                if choice_text:
                                    choices_batch.append(AnswerChoice(
                                        question=created_question,
                                        choice_text=choice_text,
                                        is_correct=(choice_value == data['correct_answer'].lower()),
                                        order=ord(choice_value) - ord('a')
                                    ))

                    # Bulk create answer choices
                    if choices_batch:
                        AnswerChoice.objects.bulk_create(choices_batch)

                    self.successful_rows += len(chunk)
                    print(f"✅ Successfully created {len(chunk)} questions with answer choices")

                    if self.log:
                        self.log.add_info(f"Chunk {chunk_num + 1}/{total_chunks}: Created {len(chunk)} questions")

            except Exception as e:
                # Handle chunk failure
                print(f"❌ Error creating chunk {chunk_num + 1}: {str(e)}")
                if self.log:
                    self.log.add_error(f"Chunk {chunk_num + 1} failed: {str(e)}")

                # Add failed questions to error tracking
                for question, data in chunk:
                    self.failed_rows += 1
                    error_msg = f"Row {data['row_num']}: Chunk creation failed - {str(e)}"
                    self.errors.append(error_msg)

        print(f"🎉 Bulk import completed! {self.successful_rows} questions created successfully")

        # Update log status and return results
        if self.log:
            if self.failed_rows == 0 and len(self.skipped_rows) == 0:
                self.log.status = 'completed'
                self.log.success_message = f"Successfully imported {self.successful_rows} questions"
            else:
                self.log.status = 'completed_with_errors'
                if self.import_mode == 'partial':
                    self.log.success_message = f"Successfully imported {self.successful_rows} questions, skipped {len(self.skipped_rows)} with errors"
                else:
                    self.log.error_message = f"Imported {self.successful_rows} questions, {self.failed_rows} failed"

            self.log.successful_rows = self.successful_rows
            self.log.failed_rows = self.failed_rows if self.import_mode == 'strict' else len(self.skipped_rows)
            self.log.save()

        return {
            'success': True,
            'total_processed': self.successful_rows + self.failed_rows + len(self.skipped_rows),
            'successful_rows': self.successful_rows,
            'failed_rows': self.failed_rows,
            'skipped_rows': len(self.skipped_rows),
            'errors': self.errors,
            'skipped_details': self.skipped_rows,
            'import_mode': self.import_mode
        }

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
