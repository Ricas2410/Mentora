from django.core.management.base import BaseCommand
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Show content in the database for Primary 1 English Letters and Sounds'

    def handle(self, *args, **options):
        try:
            # Get Letters and Sounds topic
            english = Subject.objects.get(name='English Language')
            primary_1 = ClassLevel.objects.get(subject=english, level_number=1)
            letters_topic = Topic.objects.get(class_level=primary_1, title='Letters and Sounds')

            self.stdout.write(self.style.SUCCESS(f"\n=== TOPIC: {letters_topic.title} ==="))
            self.stdout.write(f"Description: {letters_topic.description}")
            self.stdout.write(f"Duration: {letters_topic.estimated_duration} minutes")
            self.stdout.write(f"Difficulty: {letters_topic.difficulty_level}")

            # Show study notes
            notes = StudyNote.objects.filter(topic=letters_topic)
            self.stdout.write(self.style.SUCCESS(f"\n=== STUDY NOTES ({notes.count()}) ==="))
            for note in notes:
                self.stdout.write(f"\nTitle: {note.title}")
                self.stdout.write(f"Content length: {len(note.content)} characters")
                self.stdout.write(f"First 200 characters:")
                self.stdout.write(f"{note.content[:200]}...")

            # Show questions
            questions = Question.objects.filter(topic=letters_topic)
            self.stdout.write(self.style.SUCCESS(f"\n=== QUIZ QUESTIONS ({questions.count()}) ==="))
            for i, question in enumerate(questions, 1):
                self.stdout.write(f"\n{i}. {question.question_text}")
                choices = AnswerChoice.objects.filter(question=question)
                for choice in choices:
                    marker = "✓" if choice.is_correct else " "
                    self.stdout.write(f"   {marker} {choice.choice_text}")
                if question.explanation:
                    self.stdout.write(f"   Explanation: {question.explanation}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
