from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from progress.models import UserProgress, TopicProgress
from content.models import Quiz
from subjects.models import Topic

User = get_user_model()


class Command(BaseCommand):
    help = 'Debug progress tracking issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Debug specific user by email',
        )

    def handle(self, *args, **options):
        if options['user_email']:
            try:
                user = User.objects.get(email=options['user_email'])
                self.debug_user_progress(user)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User with email {options["user_email"]} does not exist')
                )
        else:
            # Debug all users
            users = User.objects.filter(is_active=True)
            for user in users:
                self.debug_user_progress(user)
                self.stdout.write('---')

    def debug_user_progress(self, user):
        self.stdout.write(f'DEBUG: User {user.email} (Grade {user.current_class_level})')
        
        # Check UserProgress records
        user_progress = UserProgress.objects.filter(user=user)
        self.stdout.write(f'  UserProgress records: {user_progress.count()}')
        for progress in user_progress:
            self.stdout.write(f'    - {progress.class_level.subject.name}: {progress.completion_percentage:.1f}% ({progress.topics_completed}/{progress.total_topics})')
        
        # Check TopicProgress records
        topic_progress = TopicProgress.objects.filter(user=user)
        self.stdout.write(f'  TopicProgress records: {topic_progress.count()}')
        for progress in topic_progress:
            status = "✓ Completed" if progress.is_completed else "○ In Progress" if progress.is_started else "- Not Started"
            self.stdout.write(f'    - {progress.topic.title}: {status} (Quiz: {progress.best_quiz_score}%)')
        
        # Check Quiz records
        quizzes = Quiz.objects.filter(user=user, is_completed=True)
        self.stdout.write(f'  Completed Quizzes: {quizzes.count()}')
        for quiz in quizzes:
            self.stdout.write(f'    - {quiz.topic.title}: {quiz.percentage}% (Attempt #{quiz.attempt_number})')
        
        # Check available topics for user's grade
        available_topics = Topic.objects.filter(
            class_level__level_number=user.current_class_level,
            is_active=True
        )
        self.stdout.write(f'  Available Topics for Grade {user.current_class_level}: {available_topics.count()}')
        for topic in available_topics[:5]:  # Show first 5
            self.stdout.write(f'    - {topic.title} ({topic.class_level.subject.name})')
        if available_topics.count() > 5:
            self.stdout.write(f'    ... and {available_topics.count() - 5} more')
