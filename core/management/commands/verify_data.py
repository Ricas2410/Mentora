from django.core.management.base import BaseCommand
from subjects.models import Subject, ClassLevel, Topic


class Command(BaseCommand):
    help = 'Verify the populated educational data'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Verifying populated data...')
        self.stdout.write('=' * 60)
        
        # Check subjects
        subjects = Subject.objects.all().order_by('order')
        self.stdout.write(f'\n📚 Total Subjects: {subjects.count()}')
        
        for subject in subjects:
            class_levels = subject.classlevels.filter(is_active=True)
            total_topics = sum(level.topics.filter(is_active=True).count() for level in class_levels)
            
            self.stdout.write(f'  ✅ {subject.name}:')
            self.stdout.write(f'     - Class Levels: {class_levels.count()}')
            self.stdout.write(f'     - Total Topics: {total_topics}')
            self.stdout.write(f'     - Color: {subject.color}')
            self.stdout.write(f'     - Icon: {subject.icon}')
            
            # Show sample topics for first few grades
            for level in class_levels[:3]:  # Show first 3 grades
                topics = level.topics.filter(is_active=True)[:2]  # Show first 2 topics
                if topics:
                    self.stdout.write(f'       Grade {level.level_number} sample topics:')
                    for topic in topics:
                        self.stdout.write(f'         - {topic.title}')
            
            self.stdout.write('')
        
        # Summary statistics
        total_class_levels = ClassLevel.objects.filter(is_active=True).count()
        total_topics = Topic.objects.filter(is_active=True).count()
        
        self.stdout.write('📊 Summary Statistics:')
        self.stdout.write(f'  - Total Subjects: {subjects.count()}')
        self.stdout.write(f'  - Total Class Levels: {total_class_levels}')
        self.stdout.write(f'  - Total Topics: {total_topics}')
        self.stdout.write(f'  - Average Topics per Subject: {total_topics / subjects.count():.1f}')
        
        self.stdout.write('\n🎉 Data verification completed!')
