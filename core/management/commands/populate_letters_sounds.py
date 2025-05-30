from django.core.management.base import BaseCommand
from django.db import transaction
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Populate comprehensive Letters and Sounds content for Primary 1 English'

    def handle(self, *args, **options):
        self.populate_letters_and_sounds()
        self.stdout.write(
            self.style.SUCCESS('Successfully populated Letters and Sounds content!')
        )

    @transaction.atomic
    def populate_letters_and_sounds(self):
        """Populate comprehensive Letters and Sounds content"""
        self.stdout.write('Populating Letters and Sounds content...')
        
        # Get Primary 1 English
        try:
            english_subject = Subject.objects.get(name='English Language')
            primary_1_level = ClassLevel.objects.get(
                subject=english_subject, 
                level_number=1
            )
        except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
            self.stdout.write(
                self.style.ERROR('Primary 1 English not found. Run populate_ges_curriculum first.')
            )
            return

        # Get or create Letters and Sounds topic
        topic, created = Topic.objects.get_or_create(
            class_level=primary_1_level,
            title='Letters and Sounds',
            defaults={
                'description': 'Learn the English alphabet and basic letter sounds',
                'order': 1,
                'estimated_duration': 30,
                'difficulty_level': 'beginner'
            }
        )
        
        if created:
            self.stdout.write(f'Created topic: {topic.title}')
        else:
            self.stdout.write(f'Topic already exists: {topic.title}')
            # Clear existing content to repopulate
            StudyNote.objects.filter(topic=topic).delete()
            Question.objects.filter(topic=topic).delete()
            self.stdout.write('Cleared existing content')
        
        # Create comprehensive study notes
        self.create_comprehensive_study_notes(topic)
        
        # Create comprehensive quiz questions
        self.create_comprehensive_quiz_questions(topic)

    def create_comprehensive_study_notes(self, topic):
        """Create comprehensive study notes for Letters and Sounds"""
        
        # Main study guide
        main_content = """
# Letters and Sounds - Complete Learning Guide

Welcome to your first English lesson! Today we will learn about letters and the sounds they make.

## What are Letters?

Letters are the building blocks of words. Just like how we use blocks to build a house, we use letters to build words!

The English language has **26 letters**. These letters make up the **alphabet**.

## The English Alphabet

### Capital Letters (Big Letters)
**A B C D E F G H I J K L M N O P Q R S T U V W X Y Z**

### Small Letters (Little Letters)  
**a b c d e f g h i j k l m n o p q r s t u v w x y z**

## When Do We Use Capital Letters?

We use capital letters:
- At the beginning of our name: **Mary**, **John**, **Kwame**
- At the beginning of a sentence: **The cat is sleeping.**
- For important places: **Ghana**, **Accra**, **Africa**

## Letter Sounds

Each letter makes a special sound. Let's learn them!

### Vowels (Special Letters)
These 5 letters are called vowels: **A, E, I, O, U**

- **A** says "ah" like in **apple** 🍎
- **E** says "eh" like in **egg** 🥚  
- **I** says "ih" like in **igloo** 🏠
- **O** says "oh" like in **orange** 🍊
- **U** says "uh" like in **umbrella** ☂️

### Consonants (Other Letters)
All the other letters are consonants:

- **B** says "buh" like in **ball** ⚽
- **C** says "kuh" like in **cat** 🐱
- **D** says "duh" like in **dog** 🐕
- **F** says "fuh" like in **fish** 🐟
- **G** says "guh" like in **goat** 🐐
- **H** says "huh" like in **hat** 👒
- **J** says "juh" like in **jump** 
- **K** says "kuh" like in **kite** 🪁
- **L** says "luh" like in **lion** 🦁
- **M** says "muh" like in **moon** 🌙
- **N** says "nuh" like in **nose** 👃
- **P** says "puh" like in **pen** ✏️
- **Q** says "kwuh" like in **queen** 👑
- **R** says "ruh" like in **red** ❤️
- **S** says "suh" like in **sun** ☀️
- **T** says "tuh" like in **tree** 🌳
- **V** says "vuh" like in **van** 🚐
- **W** says "wuh" like in **water** 💧
- **X** says "ks" like in **box** 📦
- **Y** says "yuh" like in **yes** 
- **Z** says "zuh" like in **zebra** 🦓

## Practice Activities

### Activity 1: Letter Recognition
Look around your classroom or home. Can you find things that start with these letters?
- A: Apple, Ant
- B: Book, Ball  
- C: Chair, Cup

### Activity 2: Sound Practice
Say these sounds out loud:
- "Ah, Buh, Kuh, Duh, Eh"
- "Fuh, Guh, Huh, Ih, Juh"

### Activity 3: Writing Practice
Practice writing these letters:
- Start with straight lines: **I, L, T**
- Then curved letters: **O, C, S**
- Finally mixed letters: **A, B, D**

## Fun Facts About Letters

- The letter **E** is used most often in English words
- The letter **Q** is almost always followed by **U**
- Some letters look the same but sound different in different words
- Every word needs at least one vowel (A, E, I, O, U)

## Remember These Rules

1. **Practice every day** - Even 5 minutes helps!
2. **Say the sounds out loud** - This helps you remember
3. **Look for letters everywhere** - On signs, books, toys
4. **Ask for help** when you don't know a letter
5. **Have fun learning** - Learning should be enjoyable!

## What's Next?

After you learn all your letters and sounds, you'll be ready to:
- Read simple words like "cat", "dog", "sun"
- Write your own name
- Start reading short sentences
- Learn about rhyming words

Great job learning about letters and sounds! Keep practicing and you'll become a great reader and writer! 🌟
        """

        StudyNote.objects.create(
            topic=topic,
            title="Letters and Sounds - Complete Study Guide",
            content=main_content.strip(),
            order=1,
            is_active=True
        )

        # Additional practice note
        practice_content = """
# Extra Practice: Letter Games and Activities

## Game 1: Letter Hunt
Walk around and find 5 things that start with the letter **B**:
- Ball
- Book  
- Bag
- Banana
- Bird

## Game 2: Sound Matching
Match the letter to its sound:
- M → "muh"
- S → "suh"  
- T → "tuh"
- P → "puh"

## Game 3: Alphabet Song
Sing the alphabet song slowly and point to each letter:
🎵 A-B-C-D-E-F-G, H-I-J-K-L-M-N-O-P, Q-R-S-T-U-V, W-X-Y and Z! 🎵

## Writing Practice Sheet

Practice writing these letters 5 times each:

**A a** _____ _____ _____ _____ _____
**B b** _____ _____ _____ _____ _____  
**C c** _____ _____ _____ _____ _____

## Daily Challenge

Every day, try to:
1. Say the alphabet from A to Z
2. Find 3 new things that start with different letters
3. Practice writing 5 letters
4. Read the sounds of 10 letters

Keep practicing and you'll master all your letters! 🌟
        """

        StudyNote.objects.create(
            topic=topic,
            title="Letters and Sounds - Practice Activities",
            content=practice_content.strip(),
            order=2,
            is_active=True
        )

        self.stdout.write('Created comprehensive study notes')

    def create_comprehensive_quiz_questions(self, topic):
        """Create comprehensive quiz questions for Letters and Sounds"""
        
        questions_data = [
            {
                'question_text': 'How many letters are in the English alphabet?',
                'options': ['24 letters', '25 letters', '26 letters', '27 letters'],
                'correct_answer': 2,
                'explanation': 'The English alphabet has exactly 26 letters, from A to Z.'
            },
            {
                'question_text': 'Which letter comes right after B in the alphabet?',
                'options': ['A', 'C', 'D', 'E'],
                'correct_answer': 1,
                'explanation': 'The alphabet goes A, B, C, D... so C comes after B.'
            },
            {
                'question_text': 'What sound does the letter A make?',
                'options': ['buh', 'ah', 'kuh', 'duh'],
                'correct_answer': 1,
                'explanation': 'The letter A makes the "ah" sound, like in the word "apple".'
            },
            {
                'question_text': 'Which of these is a capital letter?',
                'options': ['a', 'b', 'C', 'd'],
                'correct_answer': 2,
                'explanation': 'Capital letters are big letters. C is a capital letter, while a, b, and d are small letters.'
            },
            {
                'question_text': 'What letter does the word "cat" start with?',
                'options': ['B', 'C', 'D', 'A'],
                'correct_answer': 1,
                'explanation': 'The word "cat" starts with the letter C, which makes the "kuh" sound.'
            },
            {
                'question_text': 'Which letters are vowels?',
                'options': ['A, B, C, D, E', 'A, E, I, O, U', 'B, C, D, F, G', 'X, Y, Z, A, B'],
                'correct_answer': 1,
                'explanation': 'The vowels are A, E, I, O, U. These are special letters that appear in every word.'
            },
            {
                'question_text': 'What sound does the letter M make?',
                'options': ['nuh', 'muh', 'puh', 'tuh'],
                'correct_answer': 1,
                'explanation': 'The letter M makes the "muh" sound, like in the word "moon".'
            },
            {
                'question_text': 'When do we use capital letters?',
                'options': ['Never', 'At the beginning of names', 'Only on Sundays', 'In the middle of words'],
                'correct_answer': 1,
                'explanation': 'We use capital letters at the beginning of names, sentences, and important places.'
            },
            {
                'question_text': 'Which letter makes the "suh" sound?',
                'options': ['T', 'S', 'P', 'R'],
                'correct_answer': 1,
                'explanation': 'The letter S makes the "suh" sound, like in the word "sun".'
            },
            {
                'question_text': 'What comes first in the alphabet?',
                'options': ['B', 'Z', 'A', 'C'],
                'correct_answer': 2,
                'explanation': 'A is the very first letter of the alphabet. The alphabet starts with A and ends with Z.'
            }
        ]

        # Create questions and answer choices
        for i, q_data in enumerate(questions_data, 1):
            question = Question.objects.create(
                topic=topic,
                question_text=q_data['question_text'],
                question_type='multiple_choice',
                explanation=q_data['explanation'],
                is_active=True
            )
            
            # Create answer choices
            for j, option_text in enumerate(q_data['options']):
                AnswerChoice.objects.create(
                    question=question,
                    choice_text=option_text,
                    is_correct=(j == q_data['correct_answer']),
                    order=j + 1
                )

        self.stdout.write(f'Created {len(questions_data)} comprehensive quiz questions')
