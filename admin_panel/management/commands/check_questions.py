from django.core.management.base import BaseCommand
from content.models import Question
from subjects.models import Subject, ClassLevel, Topic


class Command(BaseCommand):
    help = 'Check the current state of questions in the database'

    def handle(self, *args, **options):
        # Check questions
        total_questions = Question.objects.count()
        active_questions = Question.objects.filter(is_active=True).count()

        self.stdout.write(f"Total Questions: {total_questions}")
        self.stdout.write(f"Active Questions: {active_questions}")

        if total_questions > 0:
            self.stdout.write("\nQuestions by Subject:")
            for subject in Subject.objects.filter(is_active=True):
                subject_questions = Question.objects.filter(
                    topic__class_level__subject=subject,
                    is_active=True
                ).count()
                self.stdout.write(f"  {subject.name}: {subject_questions} questions")

                # Show levels and topics with questions
                for level in subject.classlevels.filter(is_active=True):
                    level_questions = Question.objects.filter(
                        topic__class_level=level,
                        is_active=True
                    ).count()
                    if level_questions > 0:
                        self.stdout.write(f"    {level.name}: {level_questions} questions")

                        for topic in level.topics.filter(is_active=True):
                            topic_questions = Question.objects.filter(
                                topic=topic,
                                is_active=True
                            ).count()
                            if topic_questions > 0:
                                self.stdout.write(f"      {topic.title}: {topic_questions} questions")

        # Check subjects and topics
        self.stdout.write(f"\nSubjects: {Subject.objects.filter(is_active=True).count()}")
        self.stdout.write(f"Class Levels: {ClassLevel.objects.filter(is_active=True).count()}")
        self.stdout.write(f"Topics: {Topic.objects.filter(is_active=True).count()}")

        # Check question types
        self.stdout.write("\nQuestion Types:")
        for qt in Question.objects.values('question_type').distinct():
            count = Question.objects.filter(question_type=qt['question_type'], is_active=True).count()
            self.stdout.write(f"  {qt['question_type']}: {count} questions")

        # Show recent questions with types and choices
        recent_questions = Question.objects.filter(is_active=True).order_by('-created_at')[:5]
        if recent_questions:
            self.stdout.write("\nRecent Questions:")
            for q in recent_questions:
                choice_count = q.answer_choices.count()
                self.stdout.write(f"  {q.question_type}: {q.question_text[:50]}... (Choices: {choice_count})")
