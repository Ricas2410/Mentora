from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from content.models import Quiz
from progress.models import TopicProgress
from admin_panel.utils import get_quiz_settings

User = get_user_model()


class Command(BaseCommand):
    help = 'Sync existing quiz results with progress tracking'

    def handle(self, *args, **options):
        quiz_settings = get_quiz_settings()
        passing_score = quiz_settings['minimum_pass_percentage']
        
        self.stdout.write('Syncing quiz results with progress tracking...')
        
        # Get all completed quizzes
        quizzes = Quiz.objects.filter(is_completed=True).select_related('user', 'topic')
        
        synced_count = 0
        for quiz in quizzes:
            # Get or create topic progress
            topic_progress, created = TopicProgress.objects.get_or_create(
                user=quiz.user,
                topic=quiz.topic,
                defaults={
                    'is_started': True,
                    'started_at': quiz.started_at
                }
            )
            
            # Update quiz score if this is better
            if quiz.percentage > topic_progress.best_quiz_score:
                topic_progress.best_quiz_score = quiz.percentage
                topic_progress.quiz_completed = True
                
                # Check if topic should be completed
                if quiz.percentage >= passing_score:
                    topic_progress.is_completed = True
                    if not topic_progress.completed_at:
                        topic_progress.completed_at = quiz.completed_at
                
                # Mark as started if not already
                if not topic_progress.is_started:
                    topic_progress.is_started = True
                    topic_progress.started_at = quiz.started_at
                
                topic_progress.save()
                synced_count += 1
                
                self.stdout.write(f'  - Synced {quiz.user.email} - {quiz.topic.title}: {quiz.percentage}%')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully synced {synced_count} quiz results')
        )
        
        # Update all user progress
        self.stdout.write('Updating user progress calculations...')
        from progress.models import UserProgress
        
        for progress in UserProgress.objects.all():
            progress.update_progress()
        
        self.stdout.write(
            self.style.SUCCESS('Progress sync completed!')
        )
