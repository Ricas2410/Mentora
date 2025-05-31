from django.core.management.base import BaseCommand
from django.db import transaction
from subjects.models import Subject


class Command(BaseCommand):
    help = 'Update Computer Science subject name to ICT'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making actual changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        self.stdout.write(
            self.style.SUCCESS('🔍 Searching for Computer Science subject...')
        )
        
        try:
            # Find Computer Science subject (case-insensitive search)
            computer_science_subjects = Subject.objects.filter(
                name__icontains='computer science'
            )
            
            if not computer_science_subjects.exists():
                self.stdout.write(
                    self.style.WARNING('❌ No "Computer Science" subject found in database.')
                )
                
                # Show all subjects for reference
                all_subjects = Subject.objects.all().order_by('name')
                if all_subjects.exists():
                    self.stdout.write('\n📋 Current subjects in database:')
                    for subject in all_subjects:
                        self.stdout.write(f'  - {subject.name} (ID: {subject.id})')
                else:
                    self.stdout.write('📋 No subjects found in database.')
                return
            
            # Process each Computer Science subject found
            for subject in computer_science_subjects:
                self.stdout.write(f'\n📍 Found subject: "{subject.name}" (ID: {subject.id})')
                
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(f'🔄 [DRY RUN] Would change "{subject.name}" to "ICT"')
                    )
                    
                    # Show related data
                    class_levels = subject.classlevels.all()
                    if class_levels.exists():
                        self.stdout.write(f'📚 This subject has {class_levels.count()} grade levels:')
                        for level in class_levels:
                            topics_count = level.topics.count()
                            self.stdout.write(f'  - Grade {level.level_number}: {topics_count} topics')
                    else:
                        self.stdout.write('📚 This subject has no grade levels.')
                        
                else:
                    # Actually update the subject
                    with transaction.atomic():
                        old_name = subject.name
                        subject.name = 'ICT'
                        subject.save()
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Successfully changed "{old_name}" to "ICT"')
                        )
                        
                        # Show related data
                        class_levels = subject.classlevels.all()
                        if class_levels.exists():
                            self.stdout.write(f'📚 Updated subject has {class_levels.count()} grade levels:')
                            for level in class_levels:
                                topics_count = level.topics.count()
                                self.stdout.write(f'  - Grade {level.level_number}: {topics_count} topics')
                        
            if dry_run:
                self.stdout.write(
                    self.style.WARNING('\n🔍 This was a dry run. No changes were made.')
                )
                self.stdout.write(
                    'To actually make the changes, run: python manage.py update_subject_name'
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('\n🎉 Subject name update completed successfully!')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error updating subject: {str(e)}')
            )
            raise
