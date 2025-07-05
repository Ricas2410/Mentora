#!/usr/bin/env python
"""
Create international sample content for the Pentora platform
- Grade 1-3 English Language Arts content
- Grade 1-3 Mathematics content
- International comprehension passages
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice, StudyNote, Passage
from users.models import User

def create_grade1_english_content():
    """Create Grade 1 English Language Arts content"""
    print("📚 Creating Grade 1 English content...")
    
    # Get Grade 1 English
    english_subject = Subject.objects.get(name='English Language Arts')
    grade1_level = ClassLevel.objects.get(subject=english_subject, level_number=1)
    admin_user = User.objects.get(username='admin')
    
    # Get topics
    alphabet_topic = Topic.objects.get(class_level=grade1_level, title='Alphabet and Phonics')
    simple_words_topic = Topic.objects.get(class_level=grade1_level, title='Simple Words')
    
    # Create study notes for Alphabet and Phonics
    StudyNote.objects.get_or_create(
        topic=alphabet_topic,
        title="Learning the Alphabet",
        defaults={
            'content': """The alphabet has 26 letters. Each letter has a sound.

**Vowels:** A, E, I, O, U
**Consonants:** All other letters

**Letter Sounds:**
- A says "ah" like in "apple"
- B says "buh" like in "ball"
- C says "kuh" like in "cat"
- D says "duh" like in "dog"

Practice saying each letter and its sound!""",
            'order': 1,
            'created_by': admin_user
        }
    )
    
    # Create questions for Alphabet and Phonics
    questions_data = [
        {
            'text': 'How many letters are in the alphabet?',
            'type': 'multiple_choice',
            'correct_answer': '26',
            'explanation': 'The English alphabet has 26 letters from A to Z.',
            'choices': [('26', True), ('24', False), ('25', False), ('27', False)]
        },
        {
            'text': 'Which letters are vowels?',
            'type': 'multiple_choice',
            'correct_answer': 'A, E, I, O, U',
            'explanation': 'The vowels are A, E, I, O, and U.',
            'choices': [('A, E, I, O, U', True), ('B, C, D, F', False), ('X, Y, Z', False), ('L, M, N', False)]
        },
        {
            'text': 'What sound does the letter "B" make?',
            'type': 'short_answer',
            'correct_answer': 'buh, b',
            'explanation': 'The letter B makes the "buh" sound.'
        },
        {
            'text': 'The letter A is a vowel.',
            'type': 'true_false',
            'correct_answer': 'true',
            'explanation': 'Yes! A is one of the five vowels.'
        }
    ]
    
    for i, q_data in enumerate(questions_data):
        question = Question.objects.create(
            topic=alphabet_topic,
            question_text=q_data['text'],
            question_type=q_data['type'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            difficulty='beginner',
            points=1,
            time_limit=30,
            explanation_display_time=5,
            order=i + 1,
            created_by=admin_user
        )
        
        if q_data['type'] == 'multiple_choice':
            for j, (choice_text, is_correct) in enumerate(q_data['choices']):
                AnswerChoice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=is_correct,
                    order=j + 1
                )
    
    print("✅ Grade 1 English content created")

def create_grade1_math_content():
    """Create Grade 1 Mathematics content"""
    print("🔢 Creating Grade 1 Math content...")
    
    # Get Grade 1 Math
    math_subject = Subject.objects.get(name='Mathematics')
    grade1_level = ClassLevel.objects.get(subject=math_subject, level_number=1)
    admin_user = User.objects.get(username='admin')
    
    # Get topics
    numbers_topic = Topic.objects.get(class_level=grade1_level, title='Numbers 1-20')
    addition_topic = Topic.objects.get(class_level=grade1_level, title='Basic Addition')
    
    # Create study notes for Numbers 1-20
    StudyNote.objects.get_or_create(
        topic=numbers_topic,
        title="Counting Numbers 1-20",
        defaults={
            'content': """Let's learn to count from 1 to 20!

**Numbers 1-10:**
1 - one
2 - two  
3 - three
4 - four
5 - five
6 - six
7 - seven
8 - eight
9 - nine
10 - ten

**Numbers 11-20:**
11 - eleven
12 - twelve
13 - thirteen
14 - fourteen
15 - fifteen
16 - sixteen
17 - seventeen
18 - eighteen
19 - nineteen
20 - twenty

Practice counting objects around you!""",
            'order': 1,
            'created_by': admin_user
        }
    )
    
    # Create questions for Numbers 1-20
    questions_data = [
        {
            'text': 'What number comes after 5?',
            'type': 'multiple_choice',
            'correct_answer': '6',
            'explanation': 'The number 6 comes after 5 when counting.',
            'choices': [('6', True), ('4', False), ('7', False), ('5', False)]
        },
        {
            'text': 'Count: 1, 2, 3, __, 5',
            'type': 'fill_blank',
            'correct_answer': '4, four',
            'explanation': 'The missing number is 4.'
        },
        {
            'text': 'How do you write the number "seven"?',
            'type': 'short_answer',
            'correct_answer': '7, seven',
            'explanation': 'Seven is written as the number 7.'
        },
        {
            'text': 'The number 10 comes before 11.',
            'type': 'true_false',
            'correct_answer': 'true',
            'explanation': 'Yes! When counting, 10 comes before 11.'
        }
    ]
    
    for i, q_data in enumerate(questions_data):
        question = Question.objects.create(
            topic=numbers_topic,
            question_text=q_data['text'],
            question_type=q_data['type'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            difficulty='beginner',
            points=1,
            time_limit=30,
            explanation_display_time=5,
            order=i + 1,
            created_by=admin_user
        )
        
        if q_data['type'] == 'multiple_choice':
            for j, (choice_text, is_correct) in enumerate(q_data['choices']):
                AnswerChoice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=is_correct,
                    order=j + 1
                )
    
    print("✅ Grade 1 Math content created")

def create_international_passages():
    """Create international reading comprehension passages"""
    print("📖 Creating international comprehension passages...")
    
    # Get Grade 3 English for passages
    english_subject = Subject.objects.get(name='English Language Arts')
    grade3_level = ClassLevel.objects.get(subject=english_subject, level_number=3)
    reading_topic = Topic.objects.get(class_level=grade3_level, title='Reading Comprehension')
    admin_user = User.objects.get(username='admin')
    
    # Create international passage
    passage = Passage.objects.create(
        topic=reading_topic,
        title="The Little Seed",
        content="""Once upon a time, there was a tiny seed buried deep in the dark soil. The seed was scared because it was all alone and couldn't see anything around it.

"I wish I could see the world," said the little seed. "It's so dark down here."

One day, warm rain began to fall. The water soaked into the soil and reached the little seed. The seed felt the cool water and began to grow.

Slowly, a small green shoot pushed up through the soil. Day by day, it grew taller and stronger. The sun shone down and gave the plant energy to grow even more.

Soon, the little seed had become a beautiful sunflower, tall and bright yellow. It could see the whole world around it - other flowers, trees, birds, and children playing.

"I'm so happy I grew up," said the sunflower. "Now I can see everything and make the world more beautiful."

The sunflower learned that sometimes we need to be patient and trust that good things will happen, even when we can't see them yet.""",
        passage_type='story',
        author='International Education Team',
        reading_level='Grade 3',
        estimated_reading_time=3,
        created_by=admin_user
    )
    
    # Create questions for the passage
    questions_data = [
        {
            'text': 'Where was the little seed at the beginning of the story?',
            'type': 'multiple_choice',
            'correct_answer': 'Buried in the soil',
            'explanation': 'The story says the seed was buried deep in the dark soil.',
            'choices': [('Buried in the soil', True), ('On a tree', False), ('In a pot', False), ('In the water', False)]
        },
        {
            'text': 'What helped the seed start to grow?',
            'type': 'short_answer',
            'correct_answer': 'rain, water, warm rain',
            'explanation': 'The warm rain that fell helped the seed begin to grow.'
        },
        {
            'text': 'What kind of flower did the seed become?',
            'type': 'fill_blank',
            'correct_answer': 'sunflower, a sunflower',
            'explanation': 'The little seed grew into a beautiful sunflower.'
        },
        {
            'text': 'The seed was happy at the beginning of the story.',
            'type': 'true_false',
            'correct_answer': 'false',
            'explanation': 'No, the seed was scared because it was alone and in the dark.'
        },
        {
            'text': 'What lesson did the sunflower learn?',
            'type': 'short_answer',
            'correct_answer': 'to be patient, patience, trust that good things will happen',
            'explanation': 'The sunflower learned to be patient and trust that good things will happen.'
        }
    ]
    
    for i, q_data in enumerate(questions_data):
        question = Question.objects.create(
            topic=reading_topic,
            passage=passage,
            question_text=q_data['text'],
            question_type=q_data['type'],
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            difficulty='intermediate',
            points=1,
            time_limit=45,
            explanation_display_time=5,
            order=i + 1,
            created_by=admin_user
        )
        
        if q_data['type'] == 'multiple_choice':
            for j, (choice_text, is_correct) in enumerate(q_data['choices']):
                AnswerChoice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=is_correct,
                    order=j + 1
                )
    
    print("✅ International comprehension passages created")

def main():
    """Create international sample content"""
    print("🌍 Creating international sample content...")
    print("=" * 50)
    
    create_grade1_english_content()
    create_grade1_math_content()
    create_international_passages()
    
    print("\n" + "=" * 50)
    print("🎉 International sample content created successfully!")
    print(f"   • {StudyNote.objects.count()} study notes created")
    print(f"   • {Question.objects.count()} questions created")
    print(f"   • {Passage.objects.count()} reading passages created")

if __name__ == '__main__':
    main()
