from django.core.management.base import BaseCommand
from django.db import transaction
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Quiz, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Clear existing data and populate database with real GES curriculum'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-all',
            action='store_true',
            help='Clear all existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear_all']:
            self.clear_existing_data()

        self.populate_curriculum()
        self.stdout.write(
            self.style.SUCCESS('Successfully populated GES curriculum!')
        )

    def clear_existing_data(self):
        """Clear all existing curriculum data"""
        self.stdout.write('Clearing existing data...')

        # Clear in reverse order of dependencies
        AnswerChoice.objects.all().delete()
        Question.objects.all().delete()
        Quiz.objects.all().delete()
        StudyNote.objects.all().delete()
        Topic.objects.all().delete()
        ClassLevel.objects.all().delete()
        Subject.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

    @transaction.atomic
    def populate_curriculum(self):
        """Populate with real GES curriculum"""
        self.stdout.write('Populating GES curriculum...')

        # Create subjects
        subjects_data = [
            {
                'name': 'English Language',
                'description': 'Develop reading, writing, speaking and listening skills in English.',
                'icon': 'fas fa-book-open',
                'color': '#3B82F6',
                'order': 1
            },
            {
                'name': 'Mathematics',
                'description': 'Build strong mathematical foundations and problem-solving skills.',
                'icon': 'fas fa-calculator',
                'color': '#10B981',
                'order': 2
            },
            {
                'name': 'Science',
                'description': 'Explore the natural world through scientific inquiry and discovery.',
                'icon': 'fas fa-flask',
                'color': '#8B5CF6',
                'order': 3
            },
            {
                'name': 'Social Studies',
                'description': 'Understand society, culture, and civic responsibilities.',
                'icon': 'fas fa-globe-africa',
                'color': '#F59E0B',
                'order': 4
            },
            {
                'name': 'Ghanaian Language',
                'description': 'Learn and appreciate local Ghanaian languages and culture.',
                'icon': 'fas fa-language',
                'color': '#EF4444',
                'order': 5
            },
            {
                'name': 'Religious and Moral Education',
                'description': 'Develop moral values and understanding of religious principles.',
                'icon': 'fas fa-heart',
                'color': '#EC4899',
                'order': 6
            }
        ]

        subjects = {}
        for subject_data in subjects_data:
            subject = Subject.objects.create(**subject_data)
            subjects[subject.name] = subject
            self.stdout.write(f'Created subject: {subject.name}')

        # Create class levels and topics
        self.create_primary_curriculum(subjects)
        self.create_jhs_curriculum(subjects)
        self.create_shs_curriculum(subjects)

    def create_primary_curriculum(self, subjects):
        """Create Primary 1-6 curriculum"""
        self.stdout.write('Creating Primary curriculum...')

        # Primary levels
        primary_levels = [
            (1, 'Primary 1'), (2, 'Primary 2'), (3, 'Primary 3'),
            (4, 'Primary 4'), (5, 'Primary 5'), (6, 'Primary 6')
        ]

        for level_num, level_name in primary_levels:
            # English Language
            english_level = ClassLevel.objects.create(
                subject=subjects['English Language'],
                name=level_name,
                level_number=level_num,
                description=f'English Language curriculum for {level_name}'
            )

            english_topics = [
                'Letters and Sounds', 'Reading and Comprehension',
                'Writing Skills', 'Speaking and Listening', 'Grammar Basics'
            ]

            for i, topic_name in enumerate(english_topics, 1):
                Topic.objects.create(
                    class_level=english_level,
                    title=topic_name,
                    description=f'{topic_name} for {level_name}',
                    order=i
                )

            # Mathematics
            math_level = ClassLevel.objects.create(
                subject=subjects['Mathematics'],
                name=level_name,
                level_number=level_num,
                description=f'Mathematics curriculum for {level_name}'
            )

            math_topics = [
                'Numbers and Counting', 'Basic Operations',
                'Shapes and Patterns', 'Measurement', 'Problem Solving'
            ]

            for i, topic_name in enumerate(math_topics, 1):
                Topic.objects.create(
                    class_level=math_level,
                    title=topic_name,
                    description=f'{topic_name} for {level_name}',
                    order=i
                )

            # Science
            science_level = ClassLevel.objects.create(
                subject=subjects['Science'],
                name=level_name,
                level_number=level_num,
                description=f'Science curriculum for {level_name}'
            )

            science_topics = [
                'Living Things', 'Non-Living Things',
                'Our Environment', 'Health and Safety', 'Simple Experiments'
            ]

            for i, topic_name in enumerate(science_topics, 1):
                Topic.objects.create(
                    class_level=science_level,
                    title=topic_name,
                    description=f'{topic_name} for {level_name}',
                    order=i
                )

    def create_jhs_curriculum(self, subjects):
        """Create JHS 1-3 curriculum"""
        self.stdout.write('Creating JHS curriculum...')

        jhs_levels = [(7, 'JHS 1'), (8, 'JHS 2'), (9, 'JHS 3')]

        for level_num, level_name in jhs_levels:
            # English Language
            english_level = ClassLevel.objects.create(
                subject=subjects['English Language'],
                name=level_name,
                level_number=level_num,
                description=f'English Language curriculum for {level_name}'
            )

            english_topics = [
                'Literature and Poetry', 'Essay Writing',
                'Grammar and Usage', 'Comprehension Skills', 'Oral Communication'
            ]

            for i, topic_name in enumerate(english_topics, 1):
                Topic.objects.create(
                    class_level=english_level,
                    title=topic_name,
                    description=f'{topic_name} for {level_name}',
                    order=i
                )

            # Mathematics
            math_level = ClassLevel.objects.create(
                subject=subjects['Mathematics'],
                name=level_name,
                level_number=level_num,
                description=f'Mathematics curriculum for {level_name}'
            )

            math_topics = [
                'Algebra Basics', 'Geometry',
                'Statistics', 'Trigonometry', 'Problem Solving'
            ]

            for i, topic_name in enumerate(math_topics, 1):
                Topic.objects.create(
                    class_level=math_level,
                    title=topic_name,
                    description=f'{topic_name} for {level_name}',
                    order=i
                )

    def create_shs_curriculum(self, subjects):
        """Create SHS 1-3 curriculum"""
        self.stdout.write('Creating SHS curriculum...')

        shs_levels = [(10, 'SHS 1'), (11, 'SHS 2'), (12, 'SHS 3')]

        for level_num, level_name in shs_levels:
            # English Language
            english_level = ClassLevel.objects.create(
                subject=subjects['English Language'],
                name=level_name,
                level_number=level_num,
                description=f'English Language curriculum for {level_name}'
            )

            english_topics = [
                'Advanced Literature', 'Academic Writing',
                'Critical Analysis', 'Research Skills', 'Public Speaking'
            ]

            for i, topic_name in enumerate(english_topics, 1):
                Topic.objects.create(
                    class_level=english_level,
                    title=topic_name,
                    description=f'{topic_name} for {level_name}',
                    order=i
                )
