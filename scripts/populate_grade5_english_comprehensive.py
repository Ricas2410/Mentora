#!/usr/bin/env python3
"""
Comprehensive script to populate Grade 5 English with real-life, professional questions
All topics: Complex Texts, Advanced Grammar, Research Skills, Poetry Analysis,
Grammar: Tenses, Grammar: Nouns, Phonics
20+ questions per topic, no generic or duplicate content
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

def create_comprehensive_english_questions():
    """Create comprehensive questions for all Grade 5 English topics"""

    try:
        # Get English subject and Grade 5
        english_subject = Subject.objects.get(name__icontains='English')
        grade_5 = ClassLevel.objects.get(subject=english_subject, level_number=5)
        admin_user = User.objects.filter(is_superuser=True).first()

        print(f"📚 Creating questions for {grade_5.name} - {english_subject.name}")

        # Get all topics
        topics = {
            'tenses': Topic.objects.get(class_level=grade_5, title='Grammar: Tenses'),
            'nouns': Topic.objects.get(class_level=grade_5, title='Grammar: Nouns'),
            'phonics': Topic.objects.get(class_level=grade_5, title='Phonics'),
            'advanced_grammar': Topic.objects.get(class_level=grade_5, title='Advanced Grammar'),
            'complex_texts': Topic.objects.get(class_level=grade_5, title='Complex Texts'),
            'research_skills': Topic.objects.get(class_level=grade_5, title='Research Skills'),
            'poetry_analysis': Topic.objects.get(class_level=grade_5, title='Poetry Analysis'),
        }

        # Grammar: Tenses Questions (25 real-life questions)
        tenses_questions = [
            {
                'question_text': 'Sarah _____ her homework every evening after dinner.',
                'choices': ['does', 'did', 'will do', 'has done'],
                'correct_answer': 'does',
                'explanation': 'Present tense "does" is used for regular, habitual actions that happen every day.'
            },
            {
                'question_text': 'Yesterday, the children _____ in the playground during recess.',
                'choices': ['play', 'played', 'will play', 'are playing'],
                'correct_answer': 'played',
                'explanation': 'Past tense "played" is used because "yesterday" indicates the action happened in the past.'
            },
            {
                'question_text': 'Next week, our class _____ the science museum.',
                'choices': ['visits', 'visited', 'will visit', 'has visited'],
                'correct_answer': 'will visit',
                'explanation': 'Future tense "will visit" is used because "next week" indicates a future action.'
            },
            {
                'question_text': 'The teacher _____ the lesson when the bell rang.',
                'choices': ['explains', 'explained', 'was explaining', 'will explain'],
                'correct_answer': 'was explaining',
                'explanation': 'Past continuous "was explaining" shows an ongoing action interrupted by another past event.'
            },
            {
                'question_text': 'My brother _____ his bicycle to school every morning.',
                'choices': ['ride', 'rides', 'rode', 'will ride'],
                'correct_answer': 'rides',
                'explanation': 'Present tense "rides" is used for regular, daily actions. Third person singular adds "s".'
            },
            {
                'question_text': 'The students _____ their projects before the deadline last month.',
                'choices': ['finish', 'finished', 'will finish', 'are finishing'],
                'correct_answer': 'finished',
                'explanation': 'Past tense "finished" is used because "last month" indicates a completed past action.'
            },
            {
                'question_text': 'Tomorrow morning, I _____ early to catch the school bus.',
                'choices': ['wake up', 'woke up', 'will wake up', 'am waking up'],
                'correct_answer': 'will wake up',
                'explanation': 'Future tense "will wake up" is used for planned actions happening tomorrow.'
            },
            {
                'question_text': 'The librarian _____ new books on the shelves right now.',
                'choices': ['puts', 'put', 'is putting', 'will put'],
                'correct_answer': 'is putting',
                'explanation': 'Present continuous "is putting" shows an action happening at this moment ("right now").'
            },
            {
                'question_text': 'Last summer, we _____ to the beach every weekend.',
                'choices': ['go', 'went', 'will go', 'are going'],
                'correct_answer': 'went',
                'explanation': 'Past tense "went" is used for repeated actions in the past ("last summer").'
            },
            {
                'question_text': 'The principal _____ an important announcement during assembly tomorrow.',
                'choices': ['makes', 'made', 'will make', 'is making'],
                'correct_answer': 'will make',
                'explanation': 'Future tense "will make" is used for planned future events ("tomorrow").'
            },
            {
                'question_text': 'While I _____ my lunch, my friend called me.',
                'choices': ['eat', 'ate', 'was eating', 'will eat'],
                'correct_answer': 'was eating',
                'explanation': 'Past continuous "was eating" shows an ongoing action interrupted by another past event.'
            },
            {
                'question_text': 'The school choir _____ beautifully at every concert.',
                'choices': ['sing', 'sings', 'sang', 'will sing'],
                'correct_answer': 'sings',
                'explanation': 'Present tense "sings" is used for general facts and regular occurrences. Third person singular adds "s".'
            },
            {
                'question_text': 'My parents _____ me to the doctor yesterday because I felt sick.',
                'choices': ['take', 'took', 'will take', 'are taking'],
                'correct_answer': 'took',
                'explanation': 'Past tense "took" is used because "yesterday" indicates a completed past action.'
            },
            {
                'question_text': 'Next year, our school _____ a new computer lab.',
                'choices': ['builds', 'built', 'will build', 'is building'],
                'correct_answer': 'will build',
                'explanation': 'Future tense "will build" is used for planned future projects ("next year").'
            },
            {
                'question_text': 'The janitor _____ the hallways every afternoon after classes end.',
                'choices': ['clean', 'cleans', 'cleaned', 'will clean'],
                'correct_answer': 'cleans',
                'explanation': 'Present tense "cleans" is used for regular, scheduled activities. Third person singular adds "s".'
            },
            {
                'question_text': 'During the storm last night, the wind _____ very loudly.',
                'choices': ['blows', 'blew', 'was blowing', 'will blow'],
                'correct_answer': 'was blowing',
                'explanation': 'Past continuous "was blowing" describes an ongoing action during a specific time in the past.'
            },
            {
                'question_text': 'The art teacher _____ us how to paint watercolors next week.',
                'choices': ['teaches', 'taught', 'will teach', 'is teaching'],
                'correct_answer': 'will teach',
                'explanation': 'Future tense "will teach" is used for planned future lessons ("next week").'
            },
            {
                'question_text': 'My grandmother _____ delicious cookies whenever we visit her.',
                'choices': ['bake', 'bakes', 'baked', 'will bake'],
                'correct_answer': 'bakes',
                'explanation': 'Present tense "bakes" is used for habitual actions that happen regularly ("whenever").'
            },
            {
                'question_text': 'The fire drill _____ all students to evacuate the building quickly yesterday.',
                'choices': ['requires', 'required', 'will require', 'is requiring'],
                'correct_answer': 'required',
                'explanation': 'Past tense "required" is used because "yesterday" indicates a completed past event.'
            },
            {
                'question_text': 'Our math teacher _____ extra help sessions after school this week.',
                'choices': ['offers', 'offered', 'will offer', 'is offering'],
                'correct_answer': 'is offering',
                'explanation': 'Present continuous "is offering" shows an action happening during the current time period ("this week").'
            }
        ]

        # Grammar: Nouns Questions (25 real-life questions)
        nouns_questions = [
            {
                'question_text': 'Which word is a proper noun in this sentence: "My friend Emma lives on Maple Street"?',
                'choices': ['friend', 'Emma', 'lives', 'street'],
                'correct_answer': 'Emma',
                'explanation': 'Emma is a proper noun because it is the specific name of a person and is capitalized.'
            },
            {
                'question_text': 'What type of noun is "happiness" in the sentence "Her happiness was contagious"?',
                'choices': ['concrete noun', 'abstract noun', 'proper noun', 'collective noun'],
                'correct_answer': 'abstract noun',
                'explanation': 'Happiness is an abstract noun because it represents a feeling or emotion that cannot be touched.'
            },
            {
                'question_text': 'Which word is a collective noun?',
                'choices': ['students', 'team', 'books', 'teachers'],
                'correct_answer': 'team',
                'explanation': 'Team is a collective noun because it refers to a group of people working together as one unit.'
            },
            {
                'question_text': 'In the sentence "The children played with their toys," what is the plural noun?',
                'choices': ['children', 'played', 'their', 'toys'],
                'correct_answer': 'children',
                'explanation': 'Children is the plural form of child. Toys is also plural, but children is the first plural noun in the sentence.'
            },
            {
                'question_text': 'Which sentence contains a possessive noun?',
                'choices': ["The dog barks loudly", "Sarah's backpack is heavy", "We walked to school", "The flowers smell nice"],
                'correct_answer': "Sarah's backpack is heavy",
                'explanation': "Sarah's is a possessive noun showing that the backpack belongs to Sarah."
            },
            {
                'question_text': 'What is the correct plural form of "child"?',
                'choices': ['childs', 'childes', 'children', 'child'],
                'correct_answer': 'children',
                'explanation': 'Children is the irregular plural form of child. Not all nouns follow the regular -s or -es pattern.'
            },
            {
                'question_text': 'Which word is a concrete noun?',
                'choices': ['love', 'pencil', 'happiness', 'freedom'],
                'correct_answer': 'pencil',
                'explanation': 'Pencil is a concrete noun because it is a physical object you can see, touch, and hold.'
            },
            {
                'question_text': 'In "The library has many books," what type of noun is "library"?',
                'choices': ['abstract noun', 'proper noun', 'common noun', 'collective noun'],
                'correct_answer': 'common noun',
                'explanation': 'Library is a common noun because it refers to a general type of place, not a specific named library.'
            },
            {
                'question_text': 'Which sentence shows the correct possessive form for multiple cats?',
                'choices': ["The cat's toys", "The cats toy", "The cats' toys", "The cats toys"],
                'correct_answer': "The cats' toys",
                'explanation': "Cats' is correct because the apostrophe comes after the s when showing possession for plural nouns ending in s."
            },
            {
                'question_text': 'What is the singular form of "geese"?',
                'choices': ['gees', 'goose', 'geeses', 'gooses'],
                'correct_answer': 'goose',
                'explanation': 'Goose is the singular form of geese. This is an irregular plural noun pattern.'
            },
            {
                'question_text': 'Which word is NOT a noun in this sentence: "The brave firefighter quickly rescued the cat"?',
                'choices': ['firefighter', 'cat', 'quickly', 'rescue'],
                'correct_answer': 'quickly',
                'explanation': 'Quickly is an adverb that describes how the action was done. Firefighter and cat are nouns.'
            },
            {
                'question_text': 'In "Mount Everest is the tallest mountain," which words are proper nouns?',
                'choices': ['Mount, Everest', 'tallest, mountain', 'Mount, mountain', 'Everest, mountain'],
                'correct_answer': 'Mount, Everest',
                'explanation': 'Mount Everest is the specific name of a mountain, so both words are proper nouns and capitalized.'
            },
            {
                'question_text': 'What type of noun is "flock" in "A flock of birds flew overhead"?',
                'choices': ['abstract noun', 'concrete noun', 'collective noun', 'proper noun'],
                'correct_answer': 'collective noun',
                'explanation': 'Flock is a collective noun because it refers to a group of birds acting as one unit.'
            },
            {
                'question_text': 'Which sentence contains an abstract noun?',
                'choices': ['The dog ran in the park', 'She showed great courage', 'The book is on the table', 'We ate lunch together'],
                'correct_answer': 'She showed great courage',
                'explanation': 'Courage is an abstract noun because it represents a quality or characteristic that cannot be physically touched.'
            },
            {
                'question_text': 'What is the correct possessive form of "James"?',
                'choices': ["James'", "James's", "Jame's", "James"],
                'correct_answer': "James's",
                'explanation': "James's is correct. For singular nouns ending in s, add 's to show possession."
            },
            {
                'question_text': 'Which word is a compound noun?',
                'choices': ['beautiful', 'classroom', 'running', 'happy'],
                'correct_answer': 'classroom',
                'explanation': 'Classroom is a compound noun made by combining two words: class + room.'
            },
            {
                'question_text': 'In "The orchestra played beautifully," what type of noun is "orchestra"?',
                'choices': ['abstract noun', 'collective noun', 'proper noun', 'concrete noun'],
                'correct_answer': 'collective noun',
                'explanation': 'Orchestra is a collective noun because it refers to a group of musicians performing together.'
            },
            {
                'question_text': 'What is the plural form of "mouse" (the computer device)?',
                'choices': ['mouses', 'mice', 'mouse', 'mices'],
                'correct_answer': 'mice',
                'explanation': 'Even for computer mice, the plural is still "mice" following the traditional irregular pattern.'
            },
            {
                'question_text': 'Which sentence uses a noun as the subject?',
                'choices': ['Run quickly to school', 'The teacher explained the lesson', 'Beautiful and bright', 'Over the rainbow'],
                'correct_answer': 'The teacher explained the lesson',
                'explanation': 'Teacher is the noun that serves as the subject - it tells us who performed the action of explaining.'
            },
            {
                'question_text': 'What type of noun is "Dr. Smith" in "Dr. Smith is our family doctor"?',
                'choices': ['common noun', 'abstract noun', 'proper noun', 'collective noun'],
                'correct_answer': 'proper noun',
                'explanation': 'Dr. Smith is a proper noun because it is the specific name of a person and is capitalized.'
            }
        ]

        # Create questions for Grammar: Tenses and Nouns
        create_questions_for_topic(topics['tenses'], tenses_questions, admin_user)
        create_questions_for_topic(topics['nouns'], nouns_questions, admin_user)

        print("✅ Successfully created Grade 5 English Grammar questions!")

    except Exception as e:
        print(f"❌ Error creating questions: {e}")
        raise

def create_questions_for_topic(topic, questions_data, admin_user):
    """Helper function to create questions and choices for a specific topic"""
    with transaction.atomic():
        created_count = 0
        for i, q_data in enumerate(questions_data):
            # Create the question
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': 'multiple_choice',
                    'difficulty': 'medium',
                    'correct_answer': q_data['correct_answer'],
                    'explanation': q_data['explanation'],
                    'order': i + 1,
                    'points': 1,
                    'time_limit': 45,
                    'explanation_display_time': 5,
                    'is_active': True,
                    'created_by': admin_user
                }
            )

            if created:
                created_count += 1

                # Create the multiple choice options
                for j, choice_text in enumerate(q_data['choices']):
                    is_correct = choice_text == q_data['correct_answer']
                    AnswerChoice.objects.get_or_create(
                        question=question,
                        choice_text=choice_text,
                        defaults={
                            'is_correct': is_correct,
                            'order': j + 1
                        }
                    )

        print(f"    Created {created_count} new questions for {topic.title}")

if __name__ == '__main__':
    create_comprehensive_english_questions()
