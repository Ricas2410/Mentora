from django.core.management.base import BaseCommand
from django.db import transaction
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice
import uuid


class Command(BaseCommand):
    help = 'Populate the database with comprehensive educational data for production'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        self.stdout.write('🚀 Starting to populate production data...')
        
        if options['clear']:
            self.clear_existing_data()
        
        with transaction.atomic():
            # Create subjects with comprehensive content
            self.create_subjects()
            
            # Create comprehensive content for each subject
            self.create_english_content()
            self.create_mathematics_content()
            self.create_science_content()
            self.create_social_studies_content()
            self.create_ict_content()
            self.create_french_content()
            
        self.stdout.write(
            self.style.SUCCESS('🎉 Successfully populated production data!')
        )

    def clear_existing_data(self):
        """Clear existing educational data"""
        self.stdout.write('🧹 Clearing existing data...')
        
        # Clear in reverse dependency order
        AnswerChoice.objects.all().delete()
        Question.objects.all().delete()
        StudyNote.objects.all().delete()
        Topic.objects.all().delete()
        ClassLevel.objects.all().delete()
        Subject.objects.all().delete()
        
        self.stdout.write('✅ Existing data cleared')

    def create_subjects(self):
        """Create main subjects"""
        self.stdout.write('📚 Creating subjects...')
        
        subjects_data = [
            {
                'name': 'English Language',
                'description': 'Comprehensive English language learning covering reading, writing, grammar, and literature',
                'icon': 'fas fa-book-open',
                'color': '#EF4444',
                'order': 1
            },
            {
                'name': 'Mathematics',
                'description': 'Mathematical concepts from basic arithmetic to advanced problem solving',
                'icon': 'fas fa-calculator',
                'color': '#3B82F6',
                'order': 2
            },
            {
                'name': 'Science',
                'description': 'Natural sciences including biology, chemistry, physics, and environmental science',
                'icon': 'fas fa-flask',
                'color': '#10B981',
                'order': 3
            },
            {
                'name': 'Social Studies',
                'description': 'History, geography, civics, and cultural studies',
                'icon': 'fas fa-globe-africa',
                'color': '#F59E0B',
                'order': 4
            },
            {
                'name': 'Information Technology',
                'description': 'Computer literacy, digital skills, and technology applications',
                'icon': 'fas fa-laptop-code',
                'color': '#8B5CF6',
                'order': 5
            },
            {
                'name': 'French',
                'description': 'French language learning for beginners to intermediate levels',
                'icon': 'fas fa-language',
                'color': '#EC4899',
                'order': 6
            }
        ]
        
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                defaults=subject_data
            )
            if created:
                self.stdout.write(f'✅ Created subject: {subject.name}')
            else:
                self.stdout.write(f'📝 Subject already exists: {subject.name}')

    def create_class_levels_for_subject(self, subject, grades):
        """Create class levels for a subject"""
        for grade in grades:
            # Determine pass percentage based on grade level
            if grade <= 3:
                pass_percentage = 60  # Lower primary
            elif grade <= 6:
                pass_percentage = 65  # Upper primary
            elif grade <= 9:
                pass_percentage = 70  # Junior high
            else:
                pass_percentage = 75  # Senior high
            
            class_level, created = ClassLevel.objects.get_or_create(
                subject=subject,
                level_number=grade,
                defaults={
                    'name': f'Grade {grade}',
                    'description': f'{subject.name} curriculum for Grade {grade}',
                    'pass_percentage': pass_percentage,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'  ✅ Created class level: {class_level.name}')

    def create_english_content(self):
        """Create comprehensive English content"""
        self.stdout.write('📖 Creating English content...')
        
        subject = Subject.objects.get(name='English Language')
        
        # Create class levels (Grades 1-12)
        self.create_class_levels_for_subject(subject, range(1, 13))
        
        # English topics by grade level
        english_topics = {
            1: [
                ('Alphabet and Phonics', 'Learning letters, sounds, and basic phonics'),
                ('Simple Words', 'Reading and writing simple three-letter words'),
                ('Basic Sentences', 'Forming simple sentences with subject and verb'),
                ('Story Time', 'Listening to and understanding simple stories'),
            ],
            2: [
                ('Reading Comprehension', 'Understanding short passages and stories'),
                ('Spelling Patterns', 'Common spelling patterns and word families'),
                ('Grammar Basics', 'Nouns, verbs, and adjectives'),
                ('Creative Writing', 'Writing simple stories and descriptions'),
            ],
            3: [
                ('Vocabulary Building', 'Expanding word knowledge and usage'),
                ('Sentence Structure', 'Complex sentences and punctuation'),
                ('Reading Fluency', 'Reading with expression and understanding'),
                ('Poetry and Rhymes', 'Understanding rhythm and rhyme in poetry'),
            ],
            4: [
                ('Literature Study', 'Analyzing characters, plot, and setting'),
                ('Essay Writing', 'Writing structured paragraphs and essays'),
                ('Grammar Rules', 'Advanced grammar and sentence construction'),
                ('Public Speaking', 'Oral presentation and communication skills'),
            ],
            5: [
                ('Critical Reading', 'Analyzing texts for meaning and purpose'),
                ('Research Skills', 'Finding and using information from sources'),
                ('Narrative Writing', 'Writing detailed stories and narratives'),
                ('Language Arts', 'Comprehensive language skills integration'),
            ],
            6: [
                ('Literary Analysis', 'Understanding themes, symbolism, and literary devices'),
                ('Persuasive Writing', 'Writing arguments and persuasive essays'),
                ('Media Literacy', 'Understanding different types of media and texts'),
                ('Drama and Performance', 'Understanding and performing dramatic texts'),
            ]
        }
        
        # Create topics for each grade
        for grade, topics in english_topics.items():
            class_level = ClassLevel.objects.get(subject=subject, level_number=grade)
            
            for order, (title, description) in enumerate(topics, 1):
                topic, created = Topic.objects.get_or_create(
                    class_level=class_level,
                    title=title,
                    defaults={
                        'description': description,
                        'order': order,
                        'estimated_duration': 45,
                        'difficulty_level': 'beginner' if grade <= 3 else 'intermediate' if grade <= 6 else 'advanced',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'    ✅ Created topic: {topic.title}')

    def create_mathematics_content(self):
        """Create comprehensive Mathematics content"""
        self.stdout.write('🔢 Creating Mathematics content...')
        
        subject = Subject.objects.get(name='Mathematics')
        
        # Create class levels (Grades 1-12)
        self.create_class_levels_for_subject(subject, range(1, 13))
        
        # Mathematics topics by grade level
        math_topics = {
            1: [
                ('Numbers 1-20', 'Counting, recognizing, and writing numbers 1-20'),
                ('Addition Basics', 'Simple addition with numbers up to 10'),
                ('Subtraction Basics', 'Simple subtraction with numbers up to 10'),
                ('Shapes and Patterns', 'Identifying basic shapes and simple patterns'),
            ],
            2: [
                ('Numbers 1-100', 'Place value and number recognition to 100'),
                ('Addition and Subtraction', 'Two-digit addition and subtraction'),
                ('Measurement', 'Length, weight, and capacity using standard units'),
                ('Time and Money', 'Telling time and counting money'),
            ],
            3: [
                ('Multiplication Tables', 'Learning multiplication facts 1-12'),
                ('Division Basics', 'Understanding division as sharing and grouping'),
                ('Fractions Introduction', 'Understanding halves, quarters, and thirds'),
                ('Geometry', 'Properties of 2D and 3D shapes'),
            ],
            4: [
                ('Large Numbers', 'Working with thousands and ten thousands'),
                ('Multi-digit Operations', 'Complex addition, subtraction, multiplication'),
                ('Decimals', 'Understanding and working with decimal numbers'),
                ('Data and Graphs', 'Collecting data and creating simple graphs'),
            ],
            5: [
                ('Fractions and Decimals', 'Converting between fractions and decimals'),
                ('Percentages', 'Understanding percentages and their applications'),
                ('Area and Perimeter', 'Calculating area and perimeter of shapes'),
                ('Problem Solving', 'Multi-step word problems and logical reasoning'),
            ],
            6: [
                ('Ratios and Proportions', 'Understanding relationships between quantities'),
                ('Integers', 'Working with positive and negative numbers'),
                ('Algebraic Thinking', 'Introduction to variables and expressions'),
                ('Statistics', 'Mean, median, mode, and data interpretation'),
            ]
        }
        
        # Create topics for each grade
        for grade, topics in math_topics.items():
            class_level = ClassLevel.objects.get(subject=subject, level_number=grade)
            
            for order, (title, description) in enumerate(topics, 1):
                topic, created = Topic.objects.get_or_create(
                    class_level=class_level,
                    title=title,
                    defaults={
                        'description': description,
                        'order': order,
                        'estimated_duration': 50,
                        'difficulty_level': 'beginner' if grade <= 3 else 'intermediate' if grade <= 6 else 'advanced',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'    ✅ Created topic: {topic.title}')

    def create_science_content(self):
        """Create comprehensive Science content"""
        self.stdout.write('🔬 Creating Science content...')

        subject = Subject.objects.get(name='Science')

        # Create class levels (Grades 1-12)
        self.create_class_levels_for_subject(subject, range(1, 13))

        # Science topics by grade level
        science_topics = {
            1: [
                ('Living and Non-living Things', 'Identifying and classifying living and non-living things'),
                ('My Body', 'Basic body parts and their functions'),
                ('Weather and Seasons', 'Understanding different weather patterns and seasons'),
                ('Plants and Animals', 'Basic characteristics of plants and animals'),
            ],
            2: [
                ('Animal Habitats', 'Where different animals live and why'),
                ('Plant Life Cycle', 'How plants grow and reproduce'),
                ('Materials and Properties', 'Different materials and their properties'),
                ('Day and Night', 'Understanding the cycle of day and night'),
            ],
            3: [
                ('Food Chains', 'Understanding how energy flows in nature'),
                ('States of Matter', 'Solids, liquids, and gases'),
                ('Human Body Systems', 'Basic body systems and their functions'),
                ('Forces and Motion', 'Push, pull, and movement'),
            ],
            4: [
                ('Ecosystems', 'Understanding different ecosystems and biodiversity'),
                ('Water Cycle', 'How water moves through the environment'),
                ('Light and Sound', 'Properties and behavior of light and sound'),
                ('Electricity', 'Basic concepts of electricity and circuits'),
            ],
            5: [
                ('Classification of Living Things', 'Scientific classification systems'),
                ('Chemical and Physical Changes', 'Understanding different types of changes'),
                ('Earth and Space', 'Solar system, planets, and space exploration'),
                ('Health and Nutrition', 'Maintaining a healthy lifestyle'),
            ],
            6: [
                ('Cell Structure', 'Basic cell structure and functions'),
                ('Energy and Resources', 'Renewable and non-renewable energy sources'),
                ('Climate and Environment', 'Climate change and environmental protection'),
                ('Scientific Method', 'How to conduct scientific investigations'),
            ]
        }

        # Create topics for each grade
        for grade, topics in science_topics.items():
            class_level = ClassLevel.objects.get(subject=subject, level_number=grade)

            for order, (title, description) in enumerate(topics, 1):
                topic, created = Topic.objects.get_or_create(
                    class_level=class_level,
                    title=title,
                    defaults={
                        'description': description,
                        'order': order,
                        'estimated_duration': 55,
                        'difficulty_level': 'beginner' if grade <= 3 else 'intermediate' if grade <= 6 else 'advanced',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'    ✅ Created topic: {topic.title}')

    def create_social_studies_content(self):
        """Create comprehensive Social Studies content"""
        self.stdout.write('🌍 Creating Social Studies content...')

        subject = Subject.objects.get(name='Social Studies')

        # Create class levels (Grades 1-12)
        self.create_class_levels_for_subject(subject, range(1, 13))

        # Social Studies topics by grade level
        social_studies_topics = {
            1: [
                ('My Family and Community', 'Understanding family structures and community helpers'),
                ('School and Rules', 'Importance of rules and cooperation in school'),
                ('My Country Ghana', 'Basic facts about Ghana - flag, anthem, symbols'),
                ('Festivals and Celebrations', 'Traditional and modern celebrations in Ghana'),
            ],
            2: [
                ('Our Neighborhood', 'Understanding local community and services'),
                ('Transportation', 'Different modes of transportation and their uses'),
                ('Ghanaian Culture', 'Traditional customs, food, and clothing'),
                ('Maps and Directions', 'Basic map reading and giving directions'),
            ],
            3: [
                ('Regions of Ghana', 'The 16 regions of Ghana and their characteristics'),
                ('Traditional Leaders', 'Chiefs, queens, and traditional governance'),
                ('Natural Resources', 'Ghana\'s natural resources and their importance'),
                ('Historical Sites', 'Important historical places in Ghana'),
            ],
            4: [
                ('Pre-Colonial Ghana', 'Ancient kingdoms and empires in Ghana'),
                ('Colonial Period', 'European colonization and its effects'),
                ('Independence Struggle', 'Ghana\'s path to independence'),
                ('Government and Citizenship', 'How government works and civic responsibilities'),
            ],
            5: [
                ('West African History', 'History of West African civilizations'),
                ('Trade and Economy', 'Economic activities and trade in Ghana'),
                ('Geography of Africa', 'Physical features and climate of Africa'),
                ('Cultural Diversity', 'Ethnic groups and languages in Ghana'),
            ],
            6: [
                ('World Geography', 'Continents, countries, and major geographical features'),
                ('Global Citizenship', 'Understanding our role in the global community'),
                ('Environmental Issues', 'Climate change and environmental challenges'),
                ('International Organizations', 'UN, AU, ECOWAS and their roles'),
            ]
        }

        # Create topics for each grade
        for grade, topics in social_studies_topics.items():
            class_level = ClassLevel.objects.get(subject=subject, level_number=grade)

            for order, (title, description) in enumerate(topics, 1):
                topic, created = Topic.objects.get_or_create(
                    class_level=class_level,
                    title=title,
                    defaults={
                        'description': description,
                        'order': order,
                        'estimated_duration': 40,
                        'difficulty_level': 'beginner' if grade <= 3 else 'intermediate' if grade <= 6 else 'advanced',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'    ✅ Created topic: {topic.title}')

    def create_ict_content(self):
        """Create comprehensive ICT content"""
        self.stdout.write('💻 Creating ICT content...')

        subject = Subject.objects.get(name='Information Technology')

        # Create class levels (Grades 1-12)
        self.create_class_levels_for_subject(subject, range(1, 13))

        # ICT topics by grade level
        ict_topics = {
            1: [
                ('Introduction to Computers', 'What is a computer and its basic parts'),
                ('Computer Safety', 'Safe use of computers and basic rules'),
                ('Mouse and Keyboard', 'Learning to use mouse and keyboard'),
                ('Digital Citizenship', 'Being a good digital citizen'),
            ],
            2: [
                ('Computer Parts', 'Monitor, CPU, keyboard, mouse and their functions'),
                ('Basic Operations', 'Turning on/off computer and opening programs'),
                ('Drawing Programs', 'Using simple drawing and paint programs'),
                ('Internet Safety', 'Basic internet safety rules'),
            ],
            3: [
                ('File Management', 'Creating, saving, and organizing files'),
                ('Word Processing', 'Basic typing and formatting text'),
                ('Educational Games', 'Learning through educational computer games'),
                ('Digital Communication', 'Email basics and online communication'),
            ],
            4: [
                ('Presentation Software', 'Creating simple presentations'),
                ('Internet Research', 'Finding information online safely'),
                ('Spreadsheet Basics', 'Introduction to spreadsheets and data'),
                ('Digital Media', 'Working with images, audio, and video'),
            ],
            5: [
                ('Advanced Word Processing', 'Complex documents and formatting'),
                ('Database Concepts', 'Understanding databases and information storage'),
                ('Web Design Basics', 'Creating simple web pages'),
                ('Programming Introduction', 'Basic programming concepts and logic'),
            ],
            6: [
                ('Advanced Presentations', 'Multimedia presentations and design'),
                ('Data Analysis', 'Using spreadsheets for data analysis'),
                ('Digital Ethics', 'Understanding digital rights and responsibilities'),
                ('Technology Trends', 'Current and emerging technologies'),
            ]
        }

        # Create topics for each grade
        for grade, topics in ict_topics.items():
            class_level = ClassLevel.objects.get(subject=subject, level_number=grade)

            for order, (title, description) in enumerate(topics, 1):
                topic, created = Topic.objects.get_or_create(
                    class_level=class_level,
                    title=title,
                    defaults={
                        'description': description,
                        'order': order,
                        'estimated_duration': 45,
                        'difficulty_level': 'beginner' if grade <= 3 else 'intermediate' if grade <= 6 else 'advanced',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'    ✅ Created topic: {topic.title}')

    def create_french_content(self):
        """Create comprehensive French content"""
        self.stdout.write('🇫🇷 Creating French content...')

        subject = Subject.objects.get(name='French')

        # Create class levels (Grades 1-12)
        self.create_class_levels_for_subject(subject, range(1, 13))

        # French topics by grade level
        french_topics = {
            1: [
                ('French Alphabet', 'Learning French letters and pronunciation'),
                ('Basic Greetings', 'Hello, goodbye, please, thank you'),
                ('Numbers 1-20', 'Counting and number recognition in French'),
                ('Colors and Shapes', 'Basic colors and shapes in French'),
            ],
            2: [
                ('Family Members', 'Vocabulary for family relationships'),
                ('Days and Months', 'Days of the week and months of the year'),
                ('School Objects', 'Classroom items and school vocabulary'),
                ('Simple Sentences', 'Basic sentence structure in French'),
            ],
            3: [
                ('Food and Drinks', 'Vocabulary for meals and beverages'),
                ('Animals', 'Domestic and wild animals in French'),
                ('Present Tense Verbs', 'Basic verb conjugation in present tense'),
                ('Describing People', 'Adjectives for physical description'),
            ],
            4: [
                ('House and Home', 'Rooms, furniture, and household items'),
                ('Clothing', 'Types of clothing and accessories'),
                ('Weather', 'Weather conditions and seasons'),
                ('Past Tense Introduction', 'Basic past tense formation'),
            ],
            5: [
                ('Hobbies and Activities', 'Leisure activities and sports'),
                ('Transportation', 'Modes of transport and travel vocabulary'),
                ('Future Tense', 'Expressing future actions and plans'),
                ('French Culture', 'Introduction to French-speaking countries'),
            ],
            6: [
                ('Advanced Grammar', 'Complex sentence structures and grammar rules'),
                ('Reading Comprehension', 'Understanding French texts and stories'),
                ('Conversation Skills', 'Practical speaking and listening skills'),
                ('French Literature', 'Introduction to French poems and stories'),
            ]
        }

        # Create topics for each grade
        for grade, topics in french_topics.items():
            class_level = ClassLevel.objects.get(subject=subject, level_number=grade)

            for order, (title, description) in enumerate(topics, 1):
                topic, created = Topic.objects.get_or_create(
                    class_level=class_level,
                    title=title,
                    defaults={
                        'description': description,
                        'order': order,
                        'estimated_duration': 40,
                        'difficulty_level': 'beginner' if grade <= 3 else 'intermediate' if grade <= 6 else 'advanced',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(f'    ✅ Created topic: {topic.title}')
