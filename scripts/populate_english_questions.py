#!/usr/bin/env python3
"""
Complete script to populate Grade 5 and Grade 6 English quiz questions
Topics: Grammar (Tenses and Nouns) and Phonics - 20 professional questions each
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question
from django.db import transaction

def get_all_questions_data():
    """Return all quiz questions organized by grade and topic"""

    return {
        'grade_5': {
            'Grammar: Tenses': [
                {
                    'question_text': 'Which sentence uses the present tense correctly?',
                    'question_type': 'multiple_choice',
                    'options': ['She walks to school every day.', 'She walked to school every day.', 'She will walk to school every day.', 'She has walked to school every day.'],
                    'correct_answer': 'She walks to school every day.',
                    'explanation': 'Present tense describes actions happening now or regularly. "Walks" is the present tense form.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Complete the sentence: Yesterday, I _____ my homework.',
                    'question_type': 'multiple_choice',
                    'options': ['do', 'did', 'will do', 'doing'],
                    'correct_answer': 'did',
                    'explanation': '"Yesterday" indicates past time, so we use the past tense "did".',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'What tense is used in this sentence: "Tomorrow we will visit the museum"?',
                    'question_type': 'multiple_choice',
                    'options': ['Past tense', 'Present tense', 'Future tense', 'Present perfect tense'],
                    'correct_answer': 'Future tense',
                    'explanation': '"Will visit" indicates an action that will happen in the future.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Choose the correct past tense form: The children _____ in the playground.',
                    'question_type': 'multiple_choice',
                    'options': ['play', 'played', 'will play', 'playing'],
                    'correct_answer': 'played',
                    'explanation': 'For regular verbs, we add -ed to form the past tense.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Which sentence shows future tense?',
                    'question_type': 'multiple_choice',
                    'options': ['I am reading a book.', 'I read a book yesterday.', 'I will read a book tonight.', 'I have read many books.'],
                    'correct_answer': 'I will read a book tonight.',
                    'explanation': '"Will read" is the future tense form, indicating an action that will happen later.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Fill in the blank with the correct present tense verb: My sister _____ beautiful pictures.',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'draws',
                    'alternative_answers': ['paints', 'creates', 'makes'],
                    'explanation': 'Present tense for third person singular (she/he/it) often ends in -s.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Which verb form correctly completes: "Last week, we _____ to the zoo"?',
                    'question_type': 'multiple_choice',
                    'options': ['go', 'went', 'will go', 'going'],
                    'correct_answer': 'went',
                    'explanation': '"Last week" indicates past time. "Went" is the irregular past tense of "go".',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Identify the tense: "The students are studying for their test."',
                    'question_type': 'multiple_choice',
                    'options': ['Simple present', 'Present continuous', 'Past continuous', 'Future continuous'],
                    'correct_answer': 'Present continuous',
                    'explanation': '"Are studying" shows an action happening right now (present continuous).',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Complete with future tense: Next summer, my family _____ to Europe.',
                    'question_type': 'multiple_choice',
                    'options': ['travel', 'traveled', 'will travel', 'traveling'],
                    'correct_answer': 'will travel',
                    'explanation': '"Next summer" indicates future time, requiring "will travel".',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Which sentence uses past tense correctly?',
                    'question_type': 'multiple_choice',
                    'options': ['She sings beautifully yesterday.', 'She sang beautifully yesterday.', 'She will sing beautifully yesterday.', 'She singing beautifully yesterday.'],
                    'correct_answer': 'She sang beautifully yesterday.',
                    'explanation': '"Yesterday" requires past tense. "Sang" is the correct past tense of "sing".',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'What is the present tense of "bought"?',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'buy',
                    'alternative_answers': ['buys'],
                    'explanation': '"Buy" is the present tense form of the irregular verb "bought".',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Choose the sentence with correct tense consistency:',
                    'question_type': 'multiple_choice',
                    'options': ['I wake up early and brush my teeth.', 'I woke up early and brush my teeth.', 'I will wake up early and brushed my teeth.', 'I am waking up early and will brush my teeth.'],
                    'correct_answer': 'I wake up early and brush my teeth.',
                    'explanation': 'Both actions should be in the same tense for consistency.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'Fill in with the correct form: "Every morning, the birds _____ sweetly."',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'sing',
                    'alternative_answers': ['chirp', 'tweet'],
                    'explanation': '"Every morning" indicates a regular action, requiring present tense.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Which shows an action that happened before another past action?',
                    'question_type': 'multiple_choice',
                    'options': ['I ate lunch.', 'I had eaten lunch before the meeting.', 'I will eat lunch.', 'I am eating lunch.'],
                    'correct_answer': 'I had eaten lunch before the meeting.',
                    'explanation': 'Past perfect tense (had + past participle) shows an action completed before another past action.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'Complete: "Right now, the teacher _____ the lesson."',
                    'question_type': 'multiple_choice',
                    'options': ['explains', 'explained', 'is explaining', 'will explain'],
                    'correct_answer': 'is explaining',
                    'explanation': '"Right now" indicates present continuous tense (is/are + -ing).',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'What tense is "I have finished my work"?',
                    'question_type': 'multiple_choice',
                    'options': ['Simple past', 'Present perfect', 'Past perfect', 'Future perfect'],
                    'correct_answer': 'Present perfect',
                    'explanation': 'Present perfect uses "have/has + past participle" to show completed actions with present relevance.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'Choose the correct future form: "The concert _____ at 8 PM tomorrow."',
                    'question_type': 'multiple_choice',
                    'options': ['start', 'started', 'starts', 'will start'],
                    'correct_answer': 'starts',
                    'explanation': 'For scheduled events, we often use simple present tense even for future time.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'Fill in the past continuous: "While I _____ TV, the phone rang."',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'was watching',
                    'alternative_answers': ['was viewing'],
                    'explanation': 'Past continuous (was/were + -ing) shows an ongoing action interrupted by another action.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'Which sentence uses the simple present for a general truth?',
                    'question_type': 'multiple_choice',
                    'options': ['Water boils at 100 degrees Celsius.', 'Water is boiling now.', 'Water boiled yesterday.', 'Water will boil tomorrow.'],
                    'correct_answer': 'Water boils at 100 degrees Celsius.',
                    'explanation': 'Simple present tense is used for scientific facts and general truths.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Complete with the correct tense: "By next year, I _____ how to drive."',
                    'question_type': 'multiple_choice',
                    'options': ['learn', 'learned', 'will learn', 'will have learned'],
                    'correct_answer': 'will have learned',
                    'explanation': 'Future perfect (will have + past participle) shows an action that will be completed by a specific future time.',
                    'difficulty_level': 'advanced'
                }
            ],
            'Grammar: Nouns': [
                {
                    'question_text': 'Which word is a proper noun?',
                    'question_type': 'multiple_choice',
                    'options': ['city', 'London', 'building', 'street'],
                    'correct_answer': 'London',
                    'explanation': 'Proper nouns are specific names of people, places, or things and are always capitalized.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'What is the plural form of "child"?',
                    'question_type': 'multiple_choice',
                    'options': ['childs', 'childes', 'children', 'child'],
                    'correct_answer': 'children',
                    'explanation': '"Children" is the irregular plural form of "child".',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Identify the common noun in this sentence: "Sarah bought a beautiful dress."',
                    'question_type': 'multiple_choice',
                    'options': ['Sarah', 'bought', 'beautiful', 'dress'],
                    'correct_answer': 'dress',
                    'explanation': 'Common nouns are general names for people, places, or things. "Dress" is a common noun.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Which noun is countable?',
                    'question_type': 'multiple_choice',
                    'options': ['water', 'happiness', 'books', 'music'],
                    'correct_answer': 'books',
                    'explanation': 'Countable nouns can be counted and have plural forms. "Books" can be counted.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'What type of noun is "team"?',
                    'question_type': 'multiple_choice',
                    'options': ['Proper noun', 'Abstract noun', 'Collective noun', 'Material noun'],
                    'correct_answer': 'Collective noun',
                    'explanation': 'Collective nouns refer to groups of people, animals, or things. "Team" is a group of people.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Choose the correct possessive form: "The _____ toys are scattered everywhere."',
                    'question_type': 'multiple_choice',
                    'options': ["childrens'", "children's", "childrens", "children"],
                    'correct_answer': "children's",
                    'explanation': 'For irregular plurals like "children", add apostrophe + s to show possession.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Which is an abstract noun?',
                    'question_type': 'multiple_choice',
                    'options': ['table', 'happiness', 'dog', 'school'],
                    'correct_answer': 'happiness',
                    'explanation': 'Abstract nouns name things you cannot see or touch, like feelings, ideas, or qualities.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Fill in the blank: "A group of lions is called a _____."',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'pride',
                    'alternative_answers': ['pack'],
                    'explanation': 'A "pride" is the collective noun for a group of lions.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'What is the plural of "mouse" (the animal)?',
                    'question_type': 'multiple_choice',
                    'options': ['mouses', 'mice', 'mouse', 'meese'],
                    'correct_answer': 'mice',
                    'explanation': '"Mice" is the irregular plural form of "mouse".',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Identify the concrete noun: "The teacher explained the concept clearly."',
                    'question_type': 'multiple_choice',
                    'options': ['teacher', 'explained', 'concept', 'clearly'],
                    'correct_answer': 'teacher',
                    'explanation': 'Concrete nouns name things you can see, touch, or experience with your senses.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Which sentence shows correct subject-verb agreement with a collective noun?',
                    'question_type': 'multiple_choice',
                    'options': ['The team are playing well.', 'The team is playing well.', 'The team were playing well.', 'The team have playing well.'],
                    'correct_answer': 'The team is playing well.',
                    'explanation': 'Collective nouns usually take singular verbs when acting as a unit.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'What is the possessive form of "James"?',
                    'question_type': 'multiple_choice',
                    'options': ["James'", "James's", "Jameses", "James"],
                    'correct_answer': "James's",
                    'explanation': 'For singular nouns ending in s, add apostrophe + s to show possession.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Choose the uncountable noun:',
                    'question_type': 'multiple_choice',
                    'options': ['chairs', 'information', 'students', 'pencils'],
                    'correct_answer': 'information',
                    'explanation': 'Uncountable nouns cannot be counted and do not have plural forms.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Fill in with a collective noun: "A _____ of bees buzzed around the flowers."',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'swarm',
                    'alternative_answers': ['hive'],
                    'explanation': 'A "swarm" is the collective noun for a group of bees.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'Which is the correct plural of "leaf"?',
                    'question_type': 'multiple_choice',
                    'options': ['leafs', 'leaves', 'leafes', 'leaf'],
                    'correct_answer': 'leaves',
                    'explanation': 'Words ending in "f" or "fe" usually change to "ves" in the plural.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Identify the material noun: "The ring is made of gold."',
                    'question_type': 'multiple_choice',
                    'options': ['ring', 'made', 'gold', 'of'],
                    'correct_answer': 'gold',
                    'explanation': 'Material nouns name substances or materials that things are made from.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'What type of noun is "freedom"?',
                    'question_type': 'multiple_choice',
                    'options': ['Concrete noun', 'Abstract noun', 'Collective noun', 'Proper noun'],
                    'correct_answer': 'Abstract noun',
                    'explanation': '"Freedom" is an abstract noun because it names an idea or concept you cannot touch.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Choose the sentence with correct capitalization of proper nouns:',
                    'question_type': 'multiple_choice',
                    'options': ['I live in new york city.', 'I live in New york City.', 'I live in New York City.', 'I live in new York city.'],
                    'correct_answer': 'I live in New York City.',
                    'explanation': 'All words in proper nouns should be capitalized.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Fill in the blank: "The _____ of students listened carefully to the lecture."',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'group',
                    'alternative_answers': ['class', 'crowd'],
                    'explanation': 'Collective nouns like "group" refer to collections of people or things.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Which shows the correct possessive form for multiple owners?',
                    'question_type': 'multiple_choice',
                    'options': ["The boys' bicycles", "The boy's bicycles", "The boys bicycles", "The boys's bicycles"],
                    'correct_answer': "The boys' bicycles",
                    'explanation': 'For plural nouns ending in s, add only an apostrophe to show possession.',
                    'difficulty_level': 'advanced'
                }
            ],
            'Phonics': [
                {
                    'question_text': 'Which word has the same beginning sound as "cat"?',
                    'question_type': 'multiple_choice',
                    'options': ['dog', 'car', 'ball', 'fish'],
                    'correct_answer': 'car',
                    'explanation': 'Both "cat" and "car" begin with the /k/ sound made by the letter "c".',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'How many syllables are in the word "elephant"?',
                    'question_type': 'multiple_choice',
                    'options': ['2', '3', '4', '5'],
                    'correct_answer': '3',
                    'explanation': 'El-e-phant has three syllables. Clap while saying the word to count them.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Which word rhymes with "night"?',
                    'question_type': 'multiple_choice',
                    'options': ['note', 'light', 'neat', 'net'],
                    'correct_answer': 'light',
                    'explanation': 'Words that rhyme have the same ending sound. "Night" and "light" both end with the -ight sound.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'What sound does "ph" make in the word "phone"?',
                    'question_type': 'multiple_choice',
                    'options': ['/p/', '/f/', '/ph/', '/h/'],
                    'correct_answer': '/f/',
                    'explanation': 'The digraph "ph" makes the /f/ sound, as in "phone", "graph", and "elephant".',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Which word has a long "a" sound?',
                    'question_type': 'multiple_choice',
                    'options': ['cat', 'cake', 'cap', 'can'],
                    'correct_answer': 'cake',
                    'explanation': 'The long "a" sound says its name. "Cake" has a long "a" sound, while the others have short "a".',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Fill in the missing letter: "The b_rd sang sweetly."',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'i',
                    'alternative_answers': [],
                    'explanation': 'The word is "bird". The letter "i" completes the word.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Which word has a silent letter?',
                    'question_type': 'multiple_choice',
                    'options': ['dog', 'lamb', 'sun', 'red'],
                    'correct_answer': 'lamb',
                    'explanation': 'In "lamb", the letter "b" is silent. You only hear the sounds /l/ /a/ /m/.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'What is the first sound in the word "ship"?',
                    'question_type': 'multiple_choice',
                    'options': ['/s/', '/sh/', '/h/', '/ch/'],
                    'correct_answer': '/sh/',
                    'explanation': 'The digraph "sh" makes one sound /sh/ at the beginning of "ship".',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Which word has the short "e" sound?',
                    'question_type': 'multiple_choice',
                    'options': ['bee', 'bed', 'beat', 'beach'],
                    'correct_answer': 'bed',
                    'explanation': 'Short "e" sounds like /eh/. "Bed" has the short "e" sound.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'How many sounds are in the word "cat"?',
                    'question_type': 'multiple_choice',
                    'options': ['2', '3', '4', '5'],
                    'correct_answer': '3',
                    'explanation': 'Cat has three sounds: /k/ /a/ /t/. Count the individual sounds, not the letters.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Which word ends with the same sound as "duck"?',
                    'question_type': 'multiple_choice',
                    'options': ['book', 'back', 'bike', 'ball'],
                    'correct_answer': 'back',
                    'explanation': 'Both "duck" and "back" end with the /k/ sound.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'What sound does "ck" make at the end of words?',
                    'question_type': 'multiple_choice',
                    'options': ['/c/', '/k/', '/ck/', '/ch/'],
                    'correct_answer': '/k/',
                    'explanation': 'The letters "ck" together make the /k/ sound at the end of words like "back" and "duck".',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Fill in the rhyming word: "The cat sat on the _____."',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'mat',
                    'alternative_answers': ['hat', 'bat', 'rat'],
                    'explanation': 'Words that rhyme with "cat" and "sat" include "mat", "hat", "bat", and "rat".',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Which word has a double consonant?',
                    'question_type': 'multiple_choice',
                    'options': ['cat', 'dog', 'bell', 'sun'],
                    'correct_answer': 'bell',
                    'explanation': '"Bell" has double "l" consonants. Double consonants often come after short vowels.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'What is the vowel sound in "book"?',
                    'question_type': 'multiple_choice',
                    'options': ['long oo', 'short oo', 'long o', 'short o'],
                    'correct_answer': 'short oo',
                    'explanation': '"Book" has the short "oo" sound, like in "look", "took", and "good".',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'Which word begins with a blend?',
                    'question_type': 'multiple_choice',
                    'options': ['cat', 'ship', 'stop', 'the'],
                    'correct_answer': 'stop',
                    'explanation': 'A blend is two consonants that keep their individual sounds. "St" in "stop" is a blend.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'Fill in the correct vowel: "The r_d car is fast."',
                    'question_type': 'fill_in_blank',
                    'correct_answer': 'e',
                    'alternative_answers': [],
                    'explanation': 'The word is "red". The letter "e" makes the short /e/ sound.',
                    'difficulty_level': 'beginner'
                },
                {
                    'question_text': 'Which word has the "th" sound?',
                    'question_type': 'multiple_choice',
                    'options': ['cat', 'dog', 'think', 'sun'],
                    'correct_answer': 'think',
                    'explanation': '"Think" begins with the digraph "th" which makes the /th/ sound.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'How many syllables are in "butterfly"?',
                    'question_type': 'multiple_choice',
                    'options': ['2', '3', '4', '5'],
                    'correct_answer': '3',
                    'explanation': 'But-ter-fly has three syllables. Each syllable has one vowel sound.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Which word has a magic "e" that makes the vowel say its name?',
                    'question_type': 'multiple_choice',
                    'options': ['cap', 'cape', 'cat', 'can'],
                    'correct_answer': 'cape',
                    'explanation': 'The silent "e" at the end of "cape" makes the "a" say its name (long "a" sound).',
                    'difficulty_level': 'advanced'
                }
            ]
        },
        'grade_6': {
            'Grammar: Tenses': [
                {
                    'question_text': 'Which sentence correctly uses the present perfect tense?',
                    'question_type': 'multiple_choice',
                    'options': ['I have completed my project yesterday.', 'I have completed my project.', 'I completed my project.', 'I will complete my project.'],
                    'correct_answer': 'I have completed my project.',
                    'explanation': 'Present perfect (have/has + past participle) shows completed actions with present relevance, without specific time.',
                    'difficulty_level': 'intermediate'
                },
                {
                    'question_text': 'Complete with the correct past perfect form: "She _____ the book before the movie started."',
                    'question_type': 'multiple_choice',
                    'options': ['read', 'reads', 'had read', 'has read'],
                    'correct_answer': 'had read',
                    'explanation': 'Past perfect (had + past participle) shows an action completed before another past action.',
                    'difficulty_level': 'advanced'
                },
                {
                    'question_text': 'Identify the tense: "By tomorrow evening, I will have finished all my homework."',
                    'question_type': 'multiple_choice',
                    'options': ['Future simple', 'Future perfect', 'Present perfect', 'Past perfect'],
                    'correct_answer': 'Future perfect',
                    'explanation': 'Future perfect (will have + past participle) shows an action that will be completed by a specific future time.',
                    'difficulty_level': 'advanced'
                }
            ]
        }
    }

def create_comprehensive_questions():
    """Create all quiz questions for Grade 5 and Grade 6 English"""

    try:
        # Get English subject
        english_subject = Subject.objects.get(name__icontains='English')
        print(f"Found English subject: {english_subject.name}")

        # Get all questions data
        all_questions = get_all_questions_data()

        # Process each grade
        for grade_key, grade_data in all_questions.items():
            grade_number = int(grade_key.split('_')[1])

            try:
                class_level = ClassLevel.objects.get(subject=english_subject, level_number=grade_number)
                print(f"\nProcessing {class_level.name}...")

                # Process each topic
                for topic_title, questions in grade_data.items():
                    print(f"  Creating topic: {topic_title}")

                    # Create or get topic
                    topic, created = Topic.objects.get_or_create(
                        class_level=class_level,
                        title=topic_title,
                        defaults={
                            'description': f'Professional {topic_title.lower()} questions for {class_level.name}',
                            'difficulty_level': 'intermediate',
                            'estimated_duration': 30,
                            'order': len(Topic.objects.filter(class_level=class_level)) + 1
                        }
                    )

                    if created:
                        print(f"    Created new topic: {topic.title}")
                    else:
                        print(f"    Found existing topic: {topic.title}")

                    # Create questions
                    create_questions_for_topic(topic, questions)

            except ClassLevel.DoesNotExist:
                print(f"Warning: Grade {grade_number} not found for English subject")
                continue

        print("\n✅ All quiz questions created successfully!")

    except Exception as e:
        print(f"❌ Error creating quiz questions: {e}")
        raise

def create_questions_for_topic(topic, questions_data):
    """Helper function to create questions for a specific topic"""
    with transaction.atomic():
        created_count = 0
        for i, q_data in enumerate(questions_data):
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': q_data['question_type'],
                    'options': q_data.get('options', []),
                    'correct_answer': q_data['correct_answer'],
                    'alternative_answers': q_data.get('alternative_answers', []),
                    'explanation': q_data['explanation'],
                    'difficulty_level': q_data['difficulty_level'],
                    'order': i + 1,
                    'points': 1,
                    'is_active': True
                }
            )
            if created:
                created_count += 1

        print(f"    Created {created_count} new questions for {topic.title}")

if __name__ == '__main__':
    create_comprehensive_questions()
