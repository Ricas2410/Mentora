#!/usr/bin/env python3
"""
Script to add 15-20 additional real-life questions to remaining Grade 5 English topics:
Grammar: Tenses, Grammar: Nouns, and Phonics
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice
from users.models import User
from django.db import transaction

def create_question_with_choices(topic, question_data, admin_user):
    """Helper function to create a question with multiple choice answers"""
    with transaction.atomic():
        # Check if question already exists
        if Question.objects.filter(topic=topic, question_text=question_data['question_text']).exists():
            return False

        question = Question.objects.create(
            topic=topic,
            question_text=question_data['question_text'],
            question_type='multiple_choice',
            difficulty=question_data.get('difficulty', 'medium'),
            correct_answer=question_data['correct_answer'],
            explanation=question_data['explanation'],
            order=Question.objects.filter(topic=topic).count() + 1,
            points=question_data.get('points', 1),
            time_limit=45,
            explanation_display_time=5,
            is_active=True,
            created_by=admin_user
        )

        # Create answer choices
        for i, (choice_text, is_correct) in enumerate(question_data['choices']):
            AnswerChoice.objects.create(
                question=question,
                choice_text=choice_text,
                is_correct=is_correct,
                order=i + 1
            )

        return True

def populate_grammar_tenses_questions(topic, admin_user):
    """Add 15 additional Grammar: Tenses questions"""
    questions = [
        {
            'question_text': 'Choose the sentence that correctly uses the future tense:',
            'choices': [
                ('I go to the store tomorrow.', False),
                ('I will go to the store tomorrow.', True),
                ('I went to the store tomorrow.', False),
                ('I am going to the store yesterday.', False)
            ],
            'correct_answer': 'I will go to the store tomorrow.',
            'explanation': 'Future tense uses "will" + base verb to show actions that will happen later.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence shows an action that happened in the past and is still continuing?',
            'choices': [
                ('She walked to school.', False),
                ('She has been walking to school.', True),
                ('She walks to school.', False),
                ('She will walk to school.', False)
            ],
            'correct_answer': 'She has been walking to school.',
            'explanation': 'Present perfect continuous tense shows actions that started in the past and continue to the present.',
            'difficulty': 'hard',
            'points': 3
        },
        {
            'question_text': 'What tense is used in: "The children were playing outside when it started raining"?',
            'choices': [
                ('Simple past', False),
                ('Past continuous', True),
                ('Present perfect', False),
                ('Future tense', False)
            ],
            'correct_answer': 'Past continuous',
            'explanation': 'Past continuous (were + -ing) shows an ongoing action in the past that was interrupted.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Choose the correct present perfect sentence:',
            'choices': [
                ('I have ate my lunch.', False),
                ('I have eaten my lunch.', True),
                ('I have eat my lunch.', False),
                ('I has eaten my lunch.', False)
            ],
            'correct_answer': 'I have eaten my lunch.',
            'explanation': 'Present perfect uses "have/has" + past participle. "Eaten" is the past participle of "eat."',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence correctly uses the simple past tense?',
            'choices': [
                ('Yesterday, I am going to the park.', False),
                ('Yesterday, I go to the park.', False),
                ('Yesterday, I went to the park.', True),
                ('Yesterday, I will go to the park.', False)
            ],
            'correct_answer': 'Yesterday, I went to the park.',
            'explanation': 'Simple past tense shows completed actions. "Went" is the past tense of "go."',
            'difficulty': 'easy',
            'points': 1
        },
        {
            'question_text': 'What is the correct past tense of "run"?',
            'choices': [
                ('runned', False),
                ('ran', True),
                ('runed', False),
                ('running', False)
            ],
            'correct_answer': 'ran',
            'explanation': '"Ran" is the irregular past tense form of "run." Not all verbs add -ed for past tense.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Choose the sentence that uses present continuous tense:',
            'choices': [
                ('She reads a book every night.', False),
                ('She is reading a book right now.', True),
                ('She read a book yesterday.', False),
                ('She will read a book tomorrow.', False)
            ],
            'correct_answer': 'She is reading a book right now.',
            'explanation': 'Present continuous uses "am/is/are" + -ing to show actions happening now.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence shows a habit or routine?',
            'choices': [
                ('I am eating breakfast now.', False),
                ('I eat breakfast every morning.', True),
                ('I ate breakfast yesterday.', False),
                ('I will eat breakfast tomorrow.', False)
            ],
            'correct_answer': 'I eat breakfast every morning.',
            'explanation': 'Simple present tense is used for habits, routines, and general truths.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the future tense of "They study hard"?',
            'choices': [
                ('They will study hard.', True),
                ('They studied hard.', False),
                ('They are studying hard.', False),
                ('They have studied hard.', False)
            ],
            'correct_answer': 'They will study hard.',
            'explanation': 'Future tense is formed by adding "will" before the base form of the verb.',
            'difficulty': 'easy',
            'points': 1
        },
        {
            'question_text': 'Choose the sentence with correct subject-verb agreement in present tense:',
            'choices': [
                ('She walk to school.', False),
                ('She walks to school.', True),
                ('She walking to school.', False),
                ('She walked to school.', False)
            ],
            'correct_answer': 'She walks to school.',
            'explanation': 'In present tense, third person singular subjects (he, she, it) need an -s on the verb.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence uses past perfect tense?',
            'choices': [
                ('I finished my homework.', False),
                ('I had finished my homework before dinner.', True),
                ('I am finishing my homework.', False),
                ('I will finish my homework.', False)
            ],
            'correct_answer': 'I had finished my homework before dinner.',
            'explanation': 'Past perfect uses "had" + past participle to show an action completed before another past action.',
            'difficulty': 'hard',
            'points': 3
        },
        {
            'question_text': 'What tense is "going to" used for?',
            'choices': [
                ('Past actions', False),
                ('Present actions', False),
                ('Future plans or intentions', True),
                ('Completed actions', False)
            ],
            'correct_answer': 'Future plans or intentions',
            'explanation': '"Going to" + base verb expresses future plans or intentions that are already decided.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Choose the correct negative form of "She has a cat":',
            'choices': [
                ('She doesn\'t has a cat.', False),
                ('She doesn\'t have a cat.', True),
                ('She don\'t have a cat.', False),
                ('She hasn\'t a cat.', False)
            ],
            'correct_answer': 'She doesn\'t have a cat.',
            'explanation': 'In present tense negatives, use "doesn\'t" with third person singular and the base form of the verb.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence correctly uses the present perfect tense?',
            'choices': [
                ('I have saw that movie.', False),
                ('I have seen that movie.', True),
                ('I have see that movie.', False),
                ('I has seen that movie.', False)
            ],
            'correct_answer': 'I have seen that movie.',
            'explanation': 'Present perfect uses "have/has" + past participle. "Seen" is the past participle of "see."',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the past tense of "bring"?',
            'choices': [
                ('bringed', False),
                ('brought', True),
                ('brung', False),
                ('bringing', False)
            ],
            'correct_answer': 'brought',
            'explanation': '"Brought" is the irregular past tense form of "bring."',
            'difficulty': 'medium',
            'points': 2
        }
    ]

    created_count = 0
    for q_data in questions:
        if create_question_with_choices(topic, q_data, admin_user):
            created_count += 1

    print(f"    Created {created_count} new Grammar: Tenses questions")

def populate_grammar_nouns_questions(topic, admin_user):
    """Add 15 additional Grammar: Nouns questions"""
    questions = [
        {
            'question_text': 'Which word is a collective noun?',
            'choices': [
                ('dog', False),
                ('team', True),
                ('running', False),
                ('quickly', False)
            ],
            'correct_answer': 'team',
            'explanation': 'A collective noun refers to a group of people, animals, or things. "Team" refers to a group of players.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the possessive form of "children"?',
            'choices': [
                ('childrens', False),
                ('children\'s', True),
                ('childrens\'', False),
                ('children', False)
            ],
            'correct_answer': 'children\'s',
            'explanation': 'For plural nouns not ending in -s, add apostrophe + s to show possession.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence contains a concrete noun?',
            'choices': [
                ('Her happiness was obvious.', False),
                ('The red apple fell from the tree.', True),
                ('His courage impressed everyone.', False),
                ('Freedom is important.', False)
            ],
            'correct_answer': 'The red apple fell from the tree.',
            'explanation': 'Concrete nouns name things you can see, touch, hear, smell, or taste. "Apple" and "tree" are concrete.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the plural form of "mouse"?',
            'choices': [
                ('mouses', False),
                ('mice', True),
                ('mouse', False),
                ('mousies', False)
            ],
            'correct_answer': 'mice',
            'explanation': '"Mice" is the irregular plural form of "mouse."',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which word is an abstract noun?',
            'choices': [
                ('book', False),
                ('kindness', True),
                ('chair', False),
                ('pencil', False)
            ],
            'correct_answer': 'kindness',
            'explanation': 'Abstract nouns name ideas, feelings, or qualities that cannot be touched. "Kindness" is a quality.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the correct possessive form of "dogs" (plural)?',
            'choices': [
                ('dog\'s', False),
                ('dogs\'', True),
                ('dogs\'s', False),
                ('dogses', False)
            ],
            'correct_answer': 'dogs\'',
            'explanation': 'For plural nouns ending in -s, add only an apostrophe to show possession.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which noun is capitalized correctly?',
            'choices': [
                ('monday', False),
                ('Monday', True),
                ('MONDAY', False),
                ('MoNdAy', False)
            ],
            'correct_answer': 'Monday',
            'explanation': 'Days of the week are proper nouns and should be capitalized.',
            'difficulty': 'easy',
            'points': 1
        },
        {
            'question_text': 'What type of noun is "flock" in "a flock of sheep"?',
            'choices': [
                ('Common noun', False),
                ('Proper noun', False),
                ('Collective noun', True),
                ('Abstract noun', False)
            ],
            'correct_answer': 'Collective noun',
            'explanation': '"Flock" is a collective noun because it refers to a group of animals.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence uses a noun as the subject?',
            'choices': [
                ('The cat sleeps peacefully.', True),
                ('She runs quickly.', False),
                ('They are happy.', False),
                ('It is raining.', False)
            ],
            'correct_answer': 'The cat sleeps peacefully.',
            'explanation': '"Cat" is a noun serving as the subject of the sentence.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the plural of "leaf"?',
            'choices': [
                ('leafs', False),
                ('leaves', True),
                ('leafes', False),
                ('leaf', False)
            ],
            'correct_answer': 'leaves',
            'explanation': 'Words ending in -f or -fe usually change to -ves in the plural.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which word is a proper noun?',
            'choices': [
                ('city', False),
                ('New York', True),
                ('building', False),
                ('street', False)
            ],
            'correct_answer': 'New York',
            'explanation': 'Proper nouns are specific names of people, places, or things and are always capitalized.',
            'difficulty': 'easy',
            'points': 1
        },
        {
            'question_text': 'In "The teacher\'s desk is clean," what does "teacher\'s" show?',
            'choices': [
                ('Plural', False),
                ('Possession', True),
                ('Past tense', False),
                ('Future tense', False)
            ],
            'correct_answer': 'Possession',
            'explanation': 'The apostrophe + s shows that the desk belongs to the teacher.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which noun can be counted?',
            'choices': [
                ('water', False),
                ('books', True),
                ('happiness', False),
                ('music', False)
            ],
            'correct_answer': 'books',
            'explanation': 'Countable nouns can be counted and have plural forms. "Books" can be counted (one book, two books).',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the singular form of "geese"?',
            'choices': [
                ('gees', False),
                ('goose', True),
                ('geeses', False),
                ('gooses', False)
            ],
            'correct_answer': 'goose',
            'explanation': '"Goose" is the singular form of the irregular plural "geese."',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence contains a compound noun?',
            'choices': [
                ('The dog barked loudly.', False),
                ('She opened the mailbox.', True),
                ('They ran quickly.', False),
                ('The book is interesting.', False)
            ],
            'correct_answer': 'She opened the mailbox.',
            'explanation': 'A compound noun is made of two or more words. "Mailbox" combines "mail" and "box."',
            'difficulty': 'medium',
            'points': 2
        }
    ]

    created_count = 0
    for q_data in questions:
        if create_question_with_choices(topic, q_data, admin_user):
            created_count += 1

    print(f"    Created {created_count} new Grammar: Nouns questions")

def populate_phonics_questions(topic, admin_user):
    """Add 15 additional Phonics questions"""
    questions = [
        {
            'question_text': 'Which word has the same vowel sound as "cake"?',
            'choices': [
                ('cat', False),
                ('make', True),
                ('cap', False),
                ('can', False)
            ],
            'correct_answer': 'make',
            'explanation': 'Both "cake" and "make" have the long A sound (/eɪ/).',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'How many syllables are in the word "elephant"?',
            'choices': [
                ('2', False),
                ('3', True),
                ('4', False),
                ('5', False)
            ],
            'correct_answer': '3',
            'explanation': '"Elephant" has three syllables: el-e-phant.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which word contains a silent letter?',
            'choices': [
                ('cat', False),
                ('knee', True),
                ('dog', False),
                ('sun', False)
            ],
            'correct_answer': 'knee',
            'explanation': 'In "knee," the letter K is silent. You only hear the "nee" sound.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What sound does "ph" make in "phone"?',
            'choices': [
                ('/p/', False),
                ('/f/', True),
                ('/h/', False),
                ('/ph/', False)
            ],
            'correct_answer': '/f/',
            'explanation': 'The digraph "ph" makes the /f/ sound, as in "phone" and "elephant."',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which word has a short vowel sound?',
            'choices': [
                ('bike', False),
                ('cat', True),
                ('cake', False),
                ('kite', False)
            ],
            'correct_answer': 'cat',
            'explanation': '"Cat" has a short A sound (/æ/), while the others have long vowel sounds.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the beginning sound in "chair"?',
            'choices': [
                ('/c/', False),
                ('/ch/', True),
                ('/h/', False),
                ('/sh/', False)
            ],
            'correct_answer': '/ch/',
            'explanation': '"Chair" begins with the digraph "ch" which makes the /ch/ sound.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which word rhymes with "light"?',
            'choices': [
                ('let', False),
                ('night', True),
                ('lot', False),
                ('late', False)
            ],
            'correct_answer': 'night',
            'explanation': '"Light" and "night" both end with the same sound pattern (-ight).',
            'difficulty': 'easy',
            'points': 1
        },
        {
            'question_text': 'How many sounds are in the word "ship"?',
            'choices': [
                ('2', False),
                ('3', True),
                ('4', False),
                ('5', False)
            ],
            'correct_answer': '3',
            'explanation': '"Ship" has three sounds: /sh/ - /i/ - /p/.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which word contains the "oo" sound as in "book"?',
            'choices': [
                ('moon', False),
                ('look', True),
                ('boot', False),
                ('food', False)
            ],
            'correct_answer': 'look',
            'explanation': '"Look" and "book" both have the short "oo" sound, while others have the long "oo" sound.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the ending sound in "dogs"?',
            'choices': [
                ('/s/', False),
                ('/z/', True),
                ('/g/', False),
                ('/gs/', False)
            ],
            'correct_answer': '/z/',
            'explanation': 'When "s" follows a voiced sound like /g/, it makes the /z/ sound.',
            'difficulty': 'hard',
            'points': 3
        },
        {
            'question_text': 'Which word has a long vowel sound?',
            'choices': [
                ('bed', False),
                ('bee', True),
                ('bet', False),
                ('bell', False)
            ],
            'correct_answer': 'bee',
            'explanation': '"Bee" has a long E sound (/iː/), while the others have short E sounds.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What sound does "ck" make in "duck"?',
            'choices': [
                ('/c/', False),
                ('/k/', True),
                ('/ck/', False),
                ('/ch/', False)
            ],
            'correct_answer': '/k/',
            'explanation': 'The "ck" combination makes the /k/ sound at the end of words.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which word contains a blend at the beginning?',
            'choices': [
                ('cat', False),
                ('stop', True),
                ('hat', False),
                ('dog', False)
            ],
            'correct_answer': 'stop',
            'explanation': '"Stop" begins with the blend "st" where both sounds /s/ and /t/ are heard.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'How many syllables are in "butterfly"?',
            'choices': [
                ('2', False),
                ('3', True),
                ('4', False),
                ('5', False)
            ],
            'correct_answer': '3',
            'explanation': '"Butterfly" has three syllables: but-ter-fly.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which word has the same ending sound as "cats"?',
            'choices': [
                ('dogs', False),
                ('hats', True),
                ('cars', False),
                ('toys', False)
            ],
            'correct_answer': 'hats',
            'explanation': 'Both "cats" and "hats" end with the /s/ sound after voiceless consonants.',
            'difficulty': 'medium',
            'points': 2
        }
    ]

    created_count = 0
    for q_data in questions:
        if create_question_with_choices(topic, q_data, admin_user):
            created_count += 1

    print(f"    Created {created_count} new Phonics questions")

def main():
    """Main function to populate additional questions"""
    try:
        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No admin user found. Please create a superuser first.")
            return

        # Get Grade 5 English
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)

        print(f"📚 Adding additional questions to remaining Grade 5 English topics...")

        # Get topics
        topics = {
            'tenses': Topic.objects.get(class_level=grade5, title='Grammar: Tenses'),
            'nouns': Topic.objects.get(class_level=grade5, title='Grammar: Nouns'),
            'phonics': Topic.objects.get(class_level=grade5, title='Phonics'),
        }

        # Populate questions for each topic
        populate_grammar_tenses_questions(topics['tenses'], admin_user)
        populate_grammar_nouns_questions(topics['nouns'], admin_user)
        populate_phonics_questions(topics['phonics'], admin_user)

        print("✅ Successfully added additional questions to remaining Grade 5 English topics!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
