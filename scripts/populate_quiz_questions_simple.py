#!/usr/bin/env python3
"""
Comprehensive script to populate Grade 5 and Grade 6 English quiz questions
Works with the actual Question and AnswerChoice model structure
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

def create_questions_and_choices():
    """Create questions and their multiple choice options"""

    try:
        # Get English subject
        english_subject = Subject.objects.get(name__icontains='English')
        print(f"Found English subject: {english_subject.name}")

        # Get Grade 5
        grade_5 = ClassLevel.objects.get(subject=english_subject, level_number=5)
        print(f"Found Grade 5: {grade_5.name}")

        # Get admin user for created_by field
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()

        # Create topics
        tenses_topic, created = Topic.objects.get_or_create(
            class_level=grade_5,
            title='Grammar: Tenses',
            defaults={
                'description': 'Understanding past, present, and future tenses in English grammar',
                'difficulty_level': 'intermediate',
                'estimated_duration': 30,
                'order': 5
            }
        )
        print(f"Tenses topic: {'created' if created else 'found'}")

        nouns_topic, created = Topic.objects.get_or_create(
            class_level=grade_5,
            title='Grammar: Nouns',
            defaults={
                'description': 'Types of nouns, singular/plural forms, and proper usage',
                'difficulty_level': 'beginner',
                'estimated_duration': 25,
                'order': 6
            }
        )
        print(f"Nouns topic: {'created' if created else 'found'}")

        phonics_topic, created = Topic.objects.get_or_create(
            class_level=grade_5,
            title='Phonics',
            defaults={
                'description': 'Sound patterns, pronunciation, and reading skills',
                'difficulty_level': 'intermediate',
                'estimated_duration': 20,
                'order': 7
            }
        )
        print(f"Phonics topic: {'created' if created else 'found'}")

        # Grade 5 Tenses Questions
        tenses_questions = [
            {
                'question_text': 'Which sentence uses the present tense correctly?',
                'correct_answer': 'She walks to school every day.',
                'explanation': 'Present tense describes actions happening now or regularly. "Walks" is the present tense form.',
                'choices': [
                    'She walks to school every day.',
                    'She walked to school every day.',
                    'She will walk to school every day.',
                    'She has walked to school every day.'
                ]
            },
            {
                'question_text': 'Complete the sentence: Yesterday, I _____ my homework.',
                'correct_answer': 'did',
                'explanation': '"Yesterday" indicates past time, so we use the past tense "did".',
                'choices': ['do', 'did', 'will do', 'doing']
            },
            {
                'question_text': 'What tense is used in this sentence: "Tomorrow we will visit the museum"?',
                'correct_answer': 'Future tense',
                'explanation': '"Will visit" indicates an action that will happen in the future.',
                'choices': ['Past tense', 'Present tense', 'Future tense', 'Present perfect tense']
            },
            {
                'question_text': 'Choose the correct past tense form: The children _____ in the playground.',
                'correct_answer': 'played',
                'explanation': 'For regular verbs, we add -ed to form the past tense.',
                'choices': ['play', 'played', 'will play', 'playing']
            },
            {
                'question_text': 'Which sentence shows future tense?',
                'correct_answer': 'I will read a book tonight.',
                'explanation': '"Will read" is the future tense form, indicating an action that will happen later.',
                'choices': [
                    'I am reading a book.',
                    'I read a book yesterday.',
                    'I will read a book tonight.',
                    'I have read many books.'
                ]
            }
        ]

        # Create questions for Tenses topic
        print(f"\nCreating questions for {tenses_topic.title}...")
        create_questions_for_topic(tenses_topic, tenses_questions, admin_user)

        # Grade 5 Nouns Questions
        nouns_questions = [
            {
                'question_text': 'Which word is a proper noun?',
                'correct_answer': 'London',
                'explanation': 'Proper nouns are specific names of people, places, or things and are always capitalized.',
                'choices': ['city', 'London', 'building', 'street']
            },
            {
                'question_text': 'What is the plural form of "child"?',
                'correct_answer': 'children',
                'explanation': '"Children" is the irregular plural form of "child".',
                'choices': ['childs', 'childes', 'children', 'child']
            },
            {
                'question_text': 'Identify the common noun in this sentence: "Sarah bought a beautiful dress."',
                'correct_answer': 'dress',
                'explanation': 'Common nouns are general names for people, places, or things. "Dress" is a common noun.',
                'choices': ['Sarah', 'bought', 'beautiful', 'dress']
            },
            {
                'question_text': 'Which noun is countable?',
                'correct_answer': 'books',
                'explanation': 'Countable nouns can be counted and have plural forms. "Books" can be counted.',
                'choices': ['water', 'happiness', 'books', 'music']
            },
            {
                'question_text': 'What type of noun is "team"?',
                'correct_answer': 'Collective noun',
                'explanation': 'Collective nouns refer to groups of people, animals, or things. "Team" is a group of people.',
                'choices': ['Proper noun', 'Abstract noun', 'Collective noun', 'Material noun']
            }
        ]

        # Create questions for Nouns topic
        print(f"\nCreating questions for {nouns_topic.title}...")
        create_questions_for_topic(nouns_topic, nouns_questions, admin_user)

        # Grade 5 Phonics Questions
        phonics_questions = [
            {
                'question_text': 'Which word has the same beginning sound as "cat"?',
                'correct_answer': 'car',
                'explanation': 'Both "cat" and "car" begin with the /k/ sound made by the letter "c".',
                'choices': ['dog', 'car', 'ball', 'fish']
            },
            {
                'question_text': 'How many syllables are in the word "elephant"?',
                'correct_answer': '3',
                'explanation': 'El-e-phant has three syllables. Clap while saying the word to count them.',
                'choices': ['2', '3', '4', '5']
            },
            {
                'question_text': 'Which word rhymes with "night"?',
                'correct_answer': 'light',
                'explanation': 'Words that rhyme have the same ending sound. "Night" and "light" both end with the -ight sound.',
                'choices': ['note', 'light', 'neat', 'net']
            },
            {
                'question_text': 'What sound does "ph" make in the word "phone"?',
                'correct_answer': '/f/',
                'explanation': 'The digraph "ph" makes the /f/ sound, as in "phone", "graph", and "elephant".',
                'choices': ['/p/', '/f/', '/ph/', '/h/']
            },
            {
                'question_text': 'Which word has a long "a" sound?',
                'correct_answer': 'cake',
                'explanation': 'The long "a" sound says its name. "Cake" has a long "a" sound, while the others have short "a".',
                'choices': ['cat', 'cake', 'cap', 'can']
            },
            {
                'question_text': 'Which word has a silent letter?',
                'correct_answer': 'lamb',
                'explanation': 'In "lamb", the letter "b" is silent. You only hear the sounds /l/ /a/ /m/.',
                'choices': ['dog', 'lamb', 'sun', 'red']
            },
            {
                'question_text': 'What is the first sound in the word "ship"?',
                'correct_answer': '/sh/',
                'explanation': 'The digraph "sh" makes one sound /sh/ at the beginning of "ship".',
                'choices': ['/s/', '/sh/', '/h/', '/ch/']
            },
            {
                'question_text': 'Which word has the short "e" sound?',
                'correct_answer': 'bed',
                'explanation': 'Short "e" sounds like /eh/. "Bed" has the short "e" sound.',
                'choices': ['bee', 'bed', 'beat', 'beach']
            },
            {
                'question_text': 'How many sounds are in the word "cat"?',
                'correct_answer': '3',
                'explanation': 'Cat has three sounds: /k/ /a/ /t/. Count the individual sounds, not the letters.',
                'choices': ['2', '3', '4', '5']
            },
            {
                'question_text': 'Which word ends with the same sound as "duck"?',
                'correct_answer': 'back',
                'explanation': 'Both "duck" and "back" end with the /k/ sound.',
                'choices': ['book', 'back', 'bike', 'ball']
            }
        ]

        # Create questions for Phonics topic
        print(f"\nCreating questions for {phonics_topic.title}...")
        create_questions_for_topic(phonics_topic, phonics_questions, admin_user)

        # Create Grade 6 topics and questions
        grade_6 = ClassLevel.objects.get(subject=english_subject, level_number=6)
        print(f"\nFound Grade 6: {grade_6.name}")

        # Create Grade 6 topics
        grade6_tenses_topic, created = Topic.objects.get_or_create(
            class_level=grade_6,
            title='Advanced Grammar: Tenses',
            defaults={
                'description': 'Perfect tenses, progressive forms, and complex sentence structures',
                'difficulty_level': 'advanced',
                'estimated_duration': 35,
                'order': 5
            }
        )
        print(f"Grade 6 Tenses topic: {'created' if created else 'found'}")

        grade6_writing_topic, created = Topic.objects.get_or_create(
            class_level=grade_6,
            title='Writing Skills',
            defaults={
                'description': 'Paragraph structure, essay writing, and creative composition',
                'difficulty_level': 'intermediate',
                'estimated_duration': 40,
                'order': 6
            }
        )
        print(f"Grade 6 Writing topic: {'created' if created else 'found'}")

        grade6_vocabulary_topic, created = Topic.objects.get_or_create(
            class_level=grade_6,
            title='Vocabulary Building',
            defaults={
                'description': 'Word roots, prefixes, suffixes, and context clues',
                'difficulty_level': 'intermediate',
                'estimated_duration': 30,
                'order': 7
            }
        )
        print(f"Grade 6 Vocabulary topic: {'created' if created else 'found'}")

        # Grade 6 Advanced Tenses Questions
        grade6_tenses_questions = [
            {
                'question_text': 'Which sentence correctly uses the present perfect tense?',
                'correct_answer': 'I have completed my project.',
                'explanation': 'Present perfect (have/has + past participle) shows completed actions with present relevance, without specific time.',
                'choices': ['I have completed my project yesterday.', 'I have completed my project.', 'I completed my project.', 'I will complete my project.']
            },
            {
                'question_text': 'Complete with the correct past perfect form: "She _____ the book before the movie started."',
                'correct_answer': 'had read',
                'explanation': 'Past perfect (had + past participle) shows an action completed before another past action.',
                'choices': ['read', 'reads', 'had read', 'has read']
            },
            {
                'question_text': 'Identify the tense: "By tomorrow evening, I will have finished all my homework."',
                'correct_answer': 'Future perfect',
                'explanation': 'Future perfect (will have + past participle) shows an action that will be completed by a specific future time.',
                'choices': ['Future simple', 'Future perfect', 'Present perfect', 'Past perfect']
            },
            {
                'question_text': 'Which sentence shows present perfect continuous tense?',
                'correct_answer': 'I have been studying for three hours.',
                'explanation': 'Present perfect continuous (have/has been + -ing) shows an action that started in the past and continues to the present.',
                'choices': ['I am studying for three hours.', 'I have been studying for three hours.', 'I studied for three hours.', 'I will study for three hours.']
            },
            {
                'question_text': 'Choose the correct form: "If I _____ harder, I would have passed the test."',
                'correct_answer': 'had studied',
                'explanation': 'This is a third conditional sentence requiring past perfect in the if-clause.',
                'choices': ['study', 'studied', 'had studied', 'have studied']
            }
        ]

        # Create questions for Grade 6 Advanced Tenses topic
        print(f"\nCreating questions for {grade6_tenses_topic.title}...")
        create_questions_for_topic(grade6_tenses_topic, grade6_tenses_questions, admin_user)

        # Grade 6 Writing Skills Questions
        grade6_writing_questions = [
            {
                'question_text': 'What is the main purpose of a topic sentence?',
                'correct_answer': 'To introduce the main idea of a paragraph',
                'explanation': 'A topic sentence states the main idea that will be developed in the paragraph.',
                'choices': ['To conclude the paragraph', 'To introduce the main idea of a paragraph', 'To provide supporting details', 'To connect to the next paragraph']
            },
            {
                'question_text': 'Which transition word shows contrast?',
                'correct_answer': 'However',
                'explanation': 'Transition words like "however" show contrast or opposition between ideas.',
                'choices': ['Furthermore', 'However', 'Therefore', 'Additionally']
            },
            {
                'question_text': 'In a five-paragraph essay, where should the thesis statement appear?',
                'correct_answer': 'At the end of the introduction',
                'explanation': 'The thesis statement typically appears at the end of the introductory paragraph.',
                'choices': ['At the beginning of the introduction', 'At the end of the introduction', 'In the first body paragraph', 'In the conclusion']
            },
            {
                'question_text': 'What makes a good supporting detail?',
                'correct_answer': 'It directly relates to and supports the main idea',
                'explanation': 'Good supporting details are specific, relevant, and directly support the main idea of the paragraph.',
                'choices': ['It is interesting to read', 'It directly relates to and supports the main idea', 'It is the longest sentence', 'It uses difficult vocabulary']
            },
            {
                'question_text': 'Which sentence shows active voice?',
                'correct_answer': 'The student wrote the essay.',
                'explanation': 'In active voice, the subject performs the action. "The student" is doing the writing.',
                'choices': ['The essay was written by the student.', 'The student wrote the essay.', 'The essay was completed.', 'Writing was done by the student.']
            }
        ]

        # Create questions for Grade 6 Writing Skills topic
        print(f"\nCreating questions for {grade6_writing_topic.title}...")
        create_questions_for_topic(grade6_writing_topic, grade6_writing_questions, admin_user)

        # Grade 6 Vocabulary Building Questions
        grade6_vocabulary_questions = [
            {
                'question_text': 'What does the prefix "pre-" mean?',
                'correct_answer': 'Before',
                'explanation': 'The prefix "pre-" means "before" as in "preview" (see before) or "prehistoric" (before history).',
                'choices': ['After', 'Before', 'Against', 'With']
            },
            {
                'question_text': 'What does the suffix "-ful" mean?',
                'correct_answer': 'Full of',
                'explanation': 'The suffix "-ful" means "full of" as in "helpful" (full of help) or "colorful" (full of color).',
                'choices': ['Without', 'Full of', 'Able to', 'Like']
            },
            {
                'question_text': 'Which word has the same root as "telephone"?',
                'correct_answer': 'Telegraph',
                'explanation': 'Both "telephone" and "telegraph" contain the Greek root "tele-" meaning "far" or "distant".',
                'choices': ['Microphone', 'Telegraph', 'Photograph', 'Paragraph']
            },
            {
                'question_text': 'Using context clues, what does "enormous" mean in: "The enormous elephant towered over the tiny mouse"?',
                'correct_answer': 'Very large',
                'explanation': 'Context clues like "towered over" and contrast with "tiny" suggest "enormous" means very large.',
                'choices': ['Very small', 'Very large', 'Very fast', 'Very slow']
            },
            {
                'question_text': 'What is a synonym for "difficult"?',
                'correct_answer': 'Challenging',
                'explanation': 'Synonyms are words with similar meanings. "Challenging" has a similar meaning to "difficult".',
                'choices': ['Easy', 'Simple', 'Challenging', 'Quick']
            }
        ]

        # Create questions for Grade 6 Vocabulary Building topic
        print(f"\nCreating questions for {grade6_vocabulary_topic.title}...")
        create_questions_for_topic(grade6_vocabulary_topic, grade6_vocabulary_questions, admin_user)

        print("\n✅ All quiz questions created successfully!")
        print(f"\nSummary:")
        print(f"Grade 5 Topics:")
        print(f"  - Grammar: Tenses: {Question.objects.filter(topic=tenses_topic).count()} questions")
        print(f"  - Grammar: Nouns: {Question.objects.filter(topic=nouns_topic).count()} questions")
        print(f"  - Phonics: {Question.objects.filter(topic=phonics_topic).count()} questions")
        print(f"Grade 6 Topics:")
        print(f"  - Advanced Grammar: Tenses: {Question.objects.filter(topic=grade6_tenses_topic).count()} questions")
        print(f"  - Writing Skills: {Question.objects.filter(topic=grade6_writing_topic).count()} questions")
        print(f"  - Vocabulary Building: {Question.objects.filter(topic=grade6_vocabulary_topic).count()} questions")

    except Exception as e:
        print(f"❌ Error creating quiz questions: {e}")
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
                    'difficulty': 'beginner',
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
    create_questions_and_choices()
    
