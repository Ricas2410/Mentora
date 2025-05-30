from django.core.management.base import BaseCommand
from django.db import transaction
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice
from users.models import User


class Command(BaseCommand):
    help = 'Populate the database with sample educational data'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate sample data...')
        
        with transaction.atomic():
            # Create subjects
            self.create_subjects()
            
            # Create English content
            self.create_english_content()
            
            # Create Mathematics content
            self.create_mathematics_content()
            
            # Create Science content
            self.create_science_content()
            
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data!')
        )

    def create_subjects(self):
        """Create sample subjects"""
        subjects_data = [
            {
                'name': 'English',
                'description': 'Master grammar, reading, writing, and listening skills. Build strong communication foundations.',
                'icon': '📚',
                'color': '#3B82F6',
                'order': 1
            },
            {
                'name': 'Mathematics',
                'description': 'From basic arithmetic to algebra. Build problem-solving skills step by step.',
                'icon': '🔢',
                'color': '#10B981',
                'order': 2
            },
            {
                'name': 'Science',
                'description': 'Explore basic concepts, environment, and health. Discover the world around you.',
                'icon': '🔬',
                'color': '#8B5CF6',
                'order': 3
            },
            {
                'name': 'Life Skills',
                'description': 'Learn hygiene, values, and communication skills for personal development.',
                'icon': '🌟',
                'color': '#F59E0B',
                'order': 4
            },
            {
                'name': 'Social Studies',
                'description': 'Understand culture, civics, and Ghanaian identity. Connect with your heritage.',
                'icon': '🌍',
                'color': '#EF4444',
                'order': 5
            }
        ]
        
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                name=subject_data['name'],
                defaults=subject_data
            )
            if created:
                self.stdout.write(f'Created subject: {subject.name}')

    def create_english_content(self):
        """Create English subject content"""
        english = Subject.objects.get(name='English')
        
        # Create class levels
        levels_data = [
            {
                'name': 'Class 1 - Basic English',
                'level_number': 1,
                'description': 'Learn the alphabet, basic words, and simple sentences. Perfect for beginners.',
                'pass_percentage': 60
            },
            {
                'name': 'Class 2 - Grammar Basics',
                'level_number': 2,
                'description': 'Understand nouns, verbs, adjectives, and basic sentence structure.',
                'pass_percentage': 60
            },
            {
                'name': 'Class 3 - Reading Comprehension',
                'level_number': 3,
                'description': 'Improve reading skills and understand different text types.',
                'pass_percentage': 65
            }
        ]
        
        previous_level = None
        for level_data in levels_data:
            level_data['subject'] = english
            level_data['prerequisite_level'] = previous_level
            
            level, created = ClassLevel.objects.get_or_create(
                subject=english,
                level_number=level_data['level_number'],
                defaults=level_data
            )
            if created:
                self.stdout.write(f'Created level: {level.name}')
            
            # Create topics for this level
            if level.level_number == 2:  # Grammar Basics
                self.create_grammar_topics(level)
            
            previous_level = level

    def create_grammar_topics(self, level):
        """Create topics for Grammar Basics level"""
        topics_data = [
            {
                'title': 'Introduction to Nouns',
                'description': 'Learn what nouns are and identify different types of nouns in sentences.',
                'order': 1,
                'estimated_duration': 15,
                'difficulty_level': 'beginner'
            },
            {
                'title': 'Understanding Verbs',
                'description': 'Discover action words and how they show what people and things do.',
                'order': 2,
                'estimated_duration': 20,
                'difficulty_level': 'beginner'
            },
            {
                'title': 'Describing with Adjectives',
                'description': 'Learn how adjectives describe nouns and make sentences more interesting.',
                'order': 3,
                'estimated_duration': 18,
                'difficulty_level': 'beginner'
            },
            {
                'title': 'Simple Sentences',
                'description': 'Build basic sentences using subjects, verbs, and objects.',
                'order': 4,
                'estimated_duration': 25,
                'difficulty_level': 'intermediate'
            }
        ]
        
        for topic_data in topics_data:
            topic_data['class_level'] = level
            
            topic, created = Topic.objects.get_or_create(
                class_level=level,
                order=topic_data['order'],
                defaults=topic_data
            )
            if created:
                self.stdout.write(f'Created topic: {topic.title}')
                
                # Create study notes and questions for this topic
                if topic.title == 'Describing with Adjectives':
                    self.create_adjectives_content(topic)

    def create_adjectives_content(self, topic):
        """Create content for the Adjectives topic"""
        # Create study note
        study_note = StudyNote.objects.create(
            topic=topic,
            title='What are Adjectives?',
            content='''
            Adjectives are words that describe or give more information about nouns. 
            They help us understand what something looks like, feels like, sounds like, or what kind of thing it is.
            
            Examples:
            - The big dog barked loudly.
            - She wore a beautiful dress to the party.
            - The cold water felt refreshing.
            ''',
            order=1
        )
        
        # Create questions
        questions_data = [
            {
                'question_text': 'Which word in this sentence is an adjective? "The beautiful flowers smell nice."',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': '"Beautiful" is an adjective because it describes the noun "flowers".',
                'choices': [
                    ('a', 'flowers'),
                    ('b', 'beautiful'),
                    ('c', 'smell'),
                    ('d', 'nice')
                ]
            },
            {
                'question_text': 'Complete the sentence with an appropriate adjective: "The _______ dog barked loudly."',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': '"Big" is an adjective that describes the size of the dog.',
                'choices': [
                    ('a', 'big'),
                    ('b', 'run'),
                    ('c', 'quickly'),
                    ('d', 'house')
                ]
            },
            {
                'question_text': 'True or False: Adjectives always come after the noun they describe.',
                'question_type': 'true_false',
                'correct_answer': 'b',
                'explanation': 'False. In English, adjectives usually come BEFORE the noun they describe.',
                'choices': [
                    ('a', 'True'),
                    ('b', 'False')
                ]
            }
        ]
        
        for q_data in questions_data:
            question = Question.objects.create(
                topic=topic,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation'],
                difficulty='medium',
                points=1
            )
            
            # Create answer choices
            for choice_value, choice_text in q_data['choices']:
                AnswerChoice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=(choice_value == q_data['correct_answer']),
                    order=ord(choice_value) - ord('a')
                )

    def create_mathematics_content(self):
        """Create Mathematics subject content"""
        math = Subject.objects.get(name='Mathematics')
        
        # Create basic math levels
        levels_data = [
            {
                'name': 'Class 1 - Basic Numbers',
                'level_number': 1,
                'description': 'Learn to count, recognize numbers, and understand basic number concepts.',
                'pass_percentage': 60
            },
            {
                'name': 'Class 2 - Addition & Subtraction',
                'level_number': 2,
                'description': 'Master basic addition and subtraction with single and double digits.',
                'pass_percentage': 60
            }
        ]
        
        previous_level = None
        for level_data in levels_data:
            level_data['subject'] = math
            level_data['prerequisite_level'] = previous_level
            
            level, created = ClassLevel.objects.get_or_create(
                subject=math,
                level_number=level_data['level_number'],
                defaults=level_data
            )
            if created:
                self.stdout.write(f'Created level: {level.name}')
            
            previous_level = level

    def create_science_content(self):
        """Create Science subject content"""
        science = Subject.objects.get(name='Science')
        
        # Create basic science levels
        levels_data = [
            {
                'name': 'Class 1 - Our Environment',
                'level_number': 1,
                'description': 'Explore the world around us - plants, animals, and nature.',
                'pass_percentage': 60
            },
            {
                'name': 'Class 2 - Our Bodies',
                'level_number': 2,
                'description': 'Learn about the human body, health, and hygiene.',
                'pass_percentage': 60
            }
        ]
        
        previous_level = None
        for level_data in levels_data:
            level_data['subject'] = science
            level_data['prerequisite_level'] = previous_level
            
            level, created = ClassLevel.objects.get_or_create(
                subject=science,
                level_number=level_data['level_number'],
                defaults=level_data
            )
            if created:
                self.stdout.write(f'Created level: {level.name}')
            
            previous_level = level
