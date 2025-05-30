#!/usr/bin/env python
"""
Simple script to populate Primary 1 English content
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice, StudyNote
from django.contrib.auth import get_user_model

User = get_user_model()

def create_simple_content():
    """Create simple Primary 1 English content"""
    
    print("🎓 Creating Primary 1 English content...")
    
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@mentora.edu.gh',
            'first_name': 'System',
            'last_name': 'Administrator',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
    
    # Get or create English subject
    english_subject, created = Subject.objects.get_or_create(
        name='English Language',
        defaults={
            'description': 'English Language learning for Ghanaian primary school students',
            'icon': '📚',
            'color': '#10B981',
            'order': 1,
            'is_active': True
        }
    )
    
    # Get or create Primary 1 level
    primary1_level, created = ClassLevel.objects.get_or_create(
        subject=english_subject,
        level_number=1,
        defaults={
            'name': 'Primary 1',
            'description': 'Foundation English language skills for 6-7 year olds',
            'pass_percentage': 60,
            'is_active': True
        }
    )
    
    # Get the next available order number
    existing_topics = Topic.objects.filter(class_level=primary1_level)
    max_order = max([t.order for t in existing_topics] + [0])
    
    # Create Letters and Sounds topic
    letters_topic, created = Topic.objects.get_or_create(
        class_level=primary1_level,
        title='Letters and Sounds',
        defaults={
            'description': 'Learning alphabet letters and their sounds (phonics foundation)',
            'order': max_order + 1,
            'estimated_duration': 45,
            'difficulty_level': 'beginner',
            'is_active': True
        }
    )
    
    if created:
        print("✅ Created Letters and Sounds topic")
        
        # Add study note
        StudyNote.objects.create(
            topic=letters_topic,
            title="Learning the Alphabet",
            content="""The alphabet has 26 letters. Each letter has a sound.

Capital Letters: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Small Letters: a b c d e f g h i j k l m n o p q r s t u v w x y z

We use letters to make words. Every word starts with a letter sound.""",
            order=1,
            created_by=admin_user
        )
        
        # Add questions
        questions = [
            {
                'question_text': 'What sound does the letter "A" make?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'The letter A makes the /a/ sound like in "apple"',
                'choices': ['/a/ like in apple', '/b/ like in ball', '/c/ like in cat', '/d/ like in dog']
            },
            {
                'question_text': 'Which letter comes after "B" in the alphabet?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'C comes after B in the alphabet: A, B, C, D...',
                'choices': ['A', 'B', 'C', 'D']
            },
            {
                'question_text': 'The letter "M" makes the sound /m/ like in "mango".',
                'question_type': 'true_false',
                'correct_answer': 'true',
                'explanation': 'Yes! The letter M makes the /m/ sound like in "mango"',
                'choices': []
            },
            {
                'question_text': 'What is the first letter of the alphabet?',
                'question_type': 'short_answer',
                'correct_answer': 'A',
                'explanation': 'A is the first letter of the alphabet',
                'choices': []
            },
            {
                'question_text': 'Fill in the missing letter: A, B, __, D',
                'question_type': 'fill_blank',
                'correct_answer': 'C',
                'explanation': 'C comes between B and D in the alphabet',
                'choices': []
            }
        ]
        
        for q_data in questions:
            question = Question.objects.create(
                topic=letters_topic,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation'],
                difficulty='easy',
                points=1,
                time_limit=30,
                created_by=admin_user,
                is_active=True
            )
            
            if q_data['question_type'] == 'multiple_choice' and q_data['choices']:
                choice_letters = ['a', 'b', 'c', 'd']
                for i, choice_text in enumerate(q_data['choices']):
                    if choice_text and i < len(choice_letters):
                        AnswerChoice.objects.create(
                            question=question,
                            choice_text=choice_text,
                            is_correct=(choice_letters[i] == q_data['correct_answer']),
                            order=i
                        )
        
        print(f"✅ Created {len(questions)} questions for Letters and Sounds")
    else:
        print("📖 Letters and Sounds topic already exists")
    
    # Create Simple Words topic
    words_topic, created = Topic.objects.get_or_create(
        class_level=primary1_level,
        title='Simple Words',
        defaults={
            'description': 'Reading and writing simple 3-letter words (CVC patterns)',
            'order': max_order + 2,
            'estimated_duration': 40,
            'difficulty_level': 'beginner',
            'is_active': True
        }
    )
    
    if created:
        print("✅ Created Simple Words topic")
        
        # Add study note
        StudyNote.objects.create(
            topic=words_topic,
            title="Making Simple Words",
            content="""We can put letters together to make words.

Simple words have 3 letters:
• First letter: consonant (like b, c, d)
• Middle letter: vowel (a, e, i, o, u)
• Last letter: consonant

Examples: cat, dog, bag, pen, sun""",
            order=1,
            created_by=admin_user
        )
        
        # Add questions
        questions = [
            {
                'question_text': 'What word do these letters make: C-A-T?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'C-A-T spells "cat" - a small animal that says meow',
                'choices': ['bat', 'cat', 'hat', 'rat']
            },
            {
                'question_text': 'Which word rhymes with "bag"?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'Tag rhymes with bag - they both end with "ag"',
                'choices': ['tag', 'big', 'dog', 'pen']
            },
            {
                'question_text': 'The word "sun" has 3 letters.',
                'question_type': 'true_false',
                'correct_answer': 'true',
                'explanation': 'Yes! S-U-N has 3 letters',
                'choices': []
            },
            {
                'question_text': 'Complete the word: d_g (animal)',
                'question_type': 'fill_blank',
                'correct_answer': 'o',
                'explanation': 'The word is "dog" - d-o-g',
                'choices': []
            }
        ]
        
        for q_data in questions:
            question = Question.objects.create(
                topic=words_topic,
                question_text=q_data['question_text'],
                question_type=q_data['question_type'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation'],
                difficulty='easy',
                points=1,
                time_limit=35,
                created_by=admin_user,
                is_active=True
            )
            
            if q_data['question_type'] == 'multiple_choice' and q_data['choices']:
                choice_letters = ['a', 'b', 'c', 'd']
                for i, choice_text in enumerate(q_data['choices']):
                    if choice_text and i < len(choice_letters):
                        AnswerChoice.objects.create(
                            question=question,
                            choice_text=choice_text,
                            is_correct=(choice_letters[i] == q_data['correct_answer']),
                            order=i
                        )
        
        print(f"✅ Created {len(questions)} questions for Simple Words")
    else:
        print("📖 Simple Words topic already exists")
    
    print("\n🎉 Successfully created Primary 1 English content!")
    print("📊 Content Summary:")
    print(f"   📚 Subject: {english_subject.name}")
    print(f"   🎓 Class Level: {primary1_level.name}")
    print(f"   📖 Topics: {Topic.objects.filter(class_level=primary1_level).count()}")
    print(f"   ❓ Questions: {Question.objects.filter(topic__class_level=primary1_level).count()}")
    print(f"   📝 Study Notes: {StudyNote.objects.filter(topic__class_level=primary1_level).count()}")


if __name__ == '__main__':
    create_simple_content()
