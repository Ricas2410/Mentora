from django.core.management.base import BaseCommand
from django.db import transaction
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Populate sample content for Primary 1 English'

    def handle(self, *args, **options):
        self.populate_primary_1_english()
        self.stdout.write(
            self.style.SUCCESS('Successfully populated Primary 1 English content!')
        )

    @transaction.atomic
    def populate_primary_1_english(self):
        """Populate Primary 1 English with study notes and quizzes"""
        self.stdout.write('Populating Primary 1 English content...')

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

        # Get or create topics
        topics_data = [
            {
                'title': 'Letters and Sounds',
                'description': 'Learn the English alphabet and basic letter sounds',
                'order': 1,
                'estimated_duration': 30,
                'difficulty_level': 'beginner'
            },
            {
                'title': 'Reading and Comprehension',
                'description': 'Basic reading skills and understanding simple texts',
                'order': 2,
                'estimated_duration': 45,
                'difficulty_level': 'beginner'
            },
            {
                'title': 'Writing Skills',
                'description': 'Learn to write letters, words, and simple sentences',
                'order': 3,
                'estimated_duration': 40,
                'difficulty_level': 'beginner'
            }
        ]

        for topic_data in topics_data:
            topic, created = Topic.objects.get_or_create(
                class_level=primary_1_level,
                title=topic_data['title'],
                defaults=topic_data
            )

            if created:
                self.stdout.write(f'Created topic: {topic.title}')

                # Add study notes for each topic
                self.create_study_notes(topic)

                # Add quiz questions for each topic
                self.create_quiz_questions(topic)

    def create_study_notes(self, topic):
        """Create study notes for a topic"""
        if topic.title == 'Letters and Sounds':
            content = """
# Letters and Sounds

## The English Alphabet

The English alphabet has 26 letters. Let's learn them!

### Capital Letters (Big Letters)
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

### Small Letters (Little Letters)
a b c d e f g h i j k l m n o p q r s t u v w x y z

## Letter Sounds

Each letter makes a sound. Let's practice:

- **A** says "ah" like in "apple"
- **B** says "buh" like in "ball"
- **C** says "kuh" like in "cat"
- **D** says "duh" like in "dog"
- **E** says "eh" like in "egg"

## Practice Activity

Try to say each letter and its sound. Ask your teacher or parent to help you!

### Remember:
- Capital letters are used at the beginning of names and sentences
- Small letters are used most of the time
- Practice makes perfect!
            """

        elif topic.title == 'Reading and Comprehension':
            content = """
# Reading and Comprehension

## What is Reading?

Reading means looking at words and understanding what they mean.

## Simple Words to Practice

### Three-Letter Words
- **cat** - a small animal that says "meow"
- **dog** - an animal that says "woof"
- **sun** - the bright light in the sky
- **run** - to move very fast
- **fun** - something that makes you happy

### Simple Sentences
- The cat is big.
- I can run fast.
- The sun is hot.
- Dogs are fun pets.

## Reading Tips

1. **Look at each word carefully**
2. **Sound out letters you don't know**
3. **Think about what the sentence means**
4. **Ask for help when you need it**

## Practice

Read these sentences slowly:
- I like to play.
- The dog can run.
- My cat is small.
            """

        elif topic.title == 'Writing Skills':
            content = """
# Writing Skills

## How to Hold a Pencil

1. Hold the pencil between your thumb and first finger
2. Rest it on your middle finger
3. Keep your hand relaxed

## Writing Letters

### Start with Straight Lines
Practice drawing:
- | (up and down lines)
- — (left and right lines)

### Curved Lines
Practice drawing:
- O (circles)
- C (half circles)

## Writing Words

Start with simple words:
- **cat**
- **dog**
- **sun**
- **fun**

## Writing Sentences

Remember:
- Start with a capital letter
- End with a period (.)
- Leave spaces between words

### Example:
I like cats.

## Practice Every Day

The more you practice, the better you will write!
            """

        StudyNote.objects.create(
            topic=topic,
            title=f"{topic.title} - Study Guide",
            content=content.strip(),
            order=1,
            is_active=True
        )

    def create_quiz_questions(self, topic):
        """Create quiz questions for a topic"""

        if topic.title == 'Letters and Sounds':
            questions_data = [
                {
                    'question_text': 'How many letters are in the English alphabet?',
                    'options': ['24', '25', '26', '27'],
                    'correct_answer': 2  # Index of correct answer (26)
                },
                {
                    'question_text': 'Which letter comes after B?',
                    'options': ['A', 'C', 'D', 'E'],
                    'correct_answer': 1  # C
                },
                {
                    'question_text': 'What sound does the letter A make?',
                    'options': ['buh', 'ah', 'kuh', 'duh'],
                    'correct_answer': 1  # ah
                },
                {
                    'question_text': 'Which is a capital letter?',
                    'options': ['a', 'b', 'C', 'd'],
                    'correct_answer': 2  # C
                },
                {
                    'question_text': 'What letter does "cat" start with?',
                    'options': ['B', 'C', 'D', 'A'],
                    'correct_answer': 1  # C
                }
            ]

        elif topic.title == 'Reading and Comprehension':
            questions_data = [
                {
                    'question_text': 'What does reading mean?',
                    'options': ['Drawing pictures', 'Looking at words and understanding them', 'Singing songs', 'Playing games'],
                    'correct_answer': 1
                },
                {
                    'question_text': 'Which animal says "meow"?',
                    'options': ['Dog', 'Cat', 'Bird', 'Fish'],
                    'correct_answer': 1
                },
                {
                    'question_text': 'Complete the sentence: "The sun is ___"',
                    'options': ['cold', 'hot', 'small', 'quiet'],
                    'correct_answer': 1
                },
                {
                    'question_text': 'How many words are in "I can run"?',
                    'options': ['2', '3', '4', '5'],
                    'correct_answer': 1
                },
                {
                    'question_text': 'What should you do when you don\'t know a word?',
                    'options': ['Give up', 'Ask for help', 'Skip it', 'Guess randomly'],
                    'correct_answer': 1
                }
            ]

        elif topic.title == 'Writing Skills':
            questions_data = [
                {
                    'question_text': 'How should you hold a pencil?',
                    'options': ['With your whole hand', 'Between thumb and first finger', 'With your toes', 'In your mouth'],
                    'correct_answer': 1
                },
                {
                    'question_text': 'What should you put at the end of a sentence?',
                    'options': ['Nothing', 'A period (.)', 'A comma (,)', 'A question mark (?)'],
                    'correct_answer': 1
                },
                {
                    'question_text': 'How should sentences start?',
                    'options': ['With a small letter', 'With a capital letter', 'With a number', 'With a picture'],
                    'correct_answer': 1
                },
                {
                    'question_text': 'What should you put between words?',
                    'options': ['Nothing', 'Spaces', 'Lines', 'Dots'],
                    'correct_answer': 1
                },
                {
                    'question_text': 'Which is a simple word to practice writing?',
                    'options': ['elephant', 'cat', 'butterfly', 'computer'],
                    'correct_answer': 1
                }
            ]

        # Create questions and answer choices
        for i, q_data in enumerate(questions_data, 1):
            question = Question.objects.create(
                topic=topic,
                question_text=q_data['question_text'],
                question_type='multiple_choice',
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

        self.stdout.write(f'Created quiz with {len(questions_data)} questions for {topic.title}')
