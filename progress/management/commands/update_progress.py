from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from progress.models import UserProgress, TopicProgress
from subjects.models import ClassLevel, Subject

User = get_user_model()


class Command(BaseCommand):
    help = 'Update user progress calculations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-id',
            type=int,
            help='Update progress for specific user ID',
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all progress and recalculate',
        )

    def handle(self, *args, **options):
        if options['user_id']:
            try:
                user = User.objects.get(id=options['user_id'])
                self.update_user_progress(user, options['reset'])
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User with ID {options["user_id"]} does not exist')
                )
        else:
            # Update all users
            users = User.objects.filter(is_active=True)
            for user in users:
                self.update_user_progress(user, options['reset'])

    def update_user_progress(self, user, reset=False):
        self.stdout.write(f'Updating progress for user: {user.email}')
        
        if reset:
            # Reset progress
            UserProgress.objects.filter(user=user).delete()
            TopicProgress.objects.filter(user=user).delete()
            self.stdout.write(f'  - Reset all progress for {user.email}')

        # Get user's current grade subjects
        current_grade = user.current_class_level or 1
        subjects = Subject.objects.filter(
            classlevels__level_number=current_grade,
            is_active=True
        ).distinct()

        for subject in subjects:
            try:
                class_level = ClassLevel.objects.get(
                    subject=subject,
                    level_number=current_grade
                )
                
                # Create or get user progress
                progress, created = UserProgress.objects.get_or_create(
                    user=user,
                    class_level=class_level,
                    defaults={
                        'is_started': False
                    }
                )
                
                # Update progress calculations
                progress.update_progress()
                
                if created:
                    self.stdout.write(f'  - Created progress for {subject.name}')
                else:
                    self.stdout.write(f'  - Updated progress for {subject.name}: {progress.completion_percentage:.1f}%')
                    
            except ClassLevel.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'  - No class level found for {subject.name} at grade {current_grade}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated progress for {user.email}')
        )
