from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from progress.models import UserProgress
from django.db.models import Count

User = get_user_model()


class Command(BaseCommand):
    help = 'Clean up duplicate progress records'

    def handle(self, *args, **options):
        self.stdout.write('Cleaning up duplicate UserProgress records...')
        
        # Find duplicates
        duplicates = UserProgress.objects.values('user', 'class_level').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        cleaned_count = 0
        for duplicate in duplicates:
            # Get all records for this user/class_level combination
            records = UserProgress.objects.filter(
                user_id=duplicate['user'],
                class_level_id=duplicate['class_level']
            ).order_by('-updated_at')
            
            # Keep the most recent one, delete the rest
            records_to_delete = records[1:]
            for record in records_to_delete:
                self.stdout.write(f'  - Deleting duplicate: {record}')
                record.delete()
                cleaned_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Cleaned up {cleaned_count} duplicate records')
        )
        
        # Update all remaining progress records
        self.stdout.write('Updating progress calculations...')
        for progress in UserProgress.objects.all():
            progress.update_progress()
        
        self.stdout.write(
            self.style.SUCCESS('Progress cleanup completed!')
        )
