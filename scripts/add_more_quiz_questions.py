#!/usr/bin/env python3
"""
Script to add more comprehensive quiz questions to existing topics
Focuses on real-life, practical questions avoiding generic content
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
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

def create_questions_for_topic(topic, questions_data, admin_user):
    """Helper function to create questions and choices for a specific topic"""
    with transaction.atomic():
        created_count = 0
        existing_count = Question.objects.filter(topic=topic).count()

        for i, q_data in enumerate(questions_data):
            # Create the question with order starting after existing questions
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': 'multiple_choice',
                    'difficulty': q_data.get('difficulty', 'easy'),
                    'correct_answer': q_data['correct_answer'],
                    'explanation': q_data['explanation'],
                    'order': existing_count + i + 1,
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

def add_phonics_questions():
    """Add comprehensive phonics questions"""
    try:
        english_subject = Subject.objects.get(name__icontains='English')
        grade_5 = ClassLevel.objects.get(subject=english_subject, level_number=5)
        phonics_topic = Topic.objects.get(class_level=grade_5, title='Phonics')
        admin_user = User.objects.filter(is_superuser=True).first()

        phonics_questions = [
            {
                'question_text': 'Which word contains a digraph (two letters that make one sound)?',
                'correct_answer': 'chair',
                'explanation': 'A digraph is two letters that make one sound. "Ch" in "chair" makes the /ch/ sound.',
                'choices': ['cat', 'chair', 'dog', 'fish'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'What is the vowel sound in the word "rain"?',
                'correct_answer': 'long a',
                'explanation': 'The "ai" in "rain" makes the long "a" sound, which says the letter name.',
                'choices': ['short a', 'long a', 'short i', 'long i'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which word has a consonant blend at the beginning?',
                'correct_answer': 'train',
                'explanation': 'A consonant blend is two consonants that keep their individual sounds. "Tr" in "train" is a blend.',
                'choices': ['chair', 'train', 'phone', 'think'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'In the word "knight", which letters are silent?',
                'correct_answer': 'k and gh',
                'explanation': 'In "knight", the "k" at the beginning and "gh" in the middle are silent.',
                'choices': ['k only', 'gh only', 'k and gh', 'no silent letters'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'What sound does "oo" make in the word "book"?',
                'correct_answer': 'short oo',
                'explanation': 'The "oo" in "book" makes the short /oo/ sound, like in "look" and "took".',
                'choices': ['long oo', 'short oo', 'long o', 'short o'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which word has the same ending sound as "fox"?',
                'correct_answer': 'box',
                'explanation': 'Both "fox" and "box" end with the /ks/ sound made by the letter "x".',
                'choices': ['dog', 'box', 'cat', 'pig'],
                'difficulty': 'beginner'
            },
            {
                'question_text': 'What type of syllable is "cat" (consonant-vowel-consonant)?',
                'correct_answer': 'closed syllable',
                'explanation': 'A closed syllable ends with a consonant and usually has a short vowel sound.',
                'choices': ['open syllable', 'closed syllable', 'silent e syllable', 'vowel team syllable'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'Which word contains a long vowel sound?',
                'correct_answer': 'bike',
                'explanation': 'The "i" in "bike" makes a long vowel sound because of the silent "e" at the end.',
                'choices': ['cat', 'dog', 'bike', 'cup'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'What sound does "ch" make in the word "school"?',
                'correct_answer': '/k/',
                'explanation': 'In "school", the "ch" makes the /k/ sound, which is less common than the /ch/ sound.',
                'choices': ['/ch/', '/k/', '/sh/', '/s/'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'Which word has a diphthong (two vowel sounds blended together)?',
                'correct_answer': 'coin',
                'explanation': 'A diphthong is two vowel sounds blended together. "Oi" in "coin" is a diphthong.',
                'choices': ['cat', 'coin', 'tree', 'book'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'How many phonemes (individual sounds) are in the word "ship"?',
                'correct_answer': '3',
                'explanation': 'Ship has three phonemes: /sh/ /i/ /p/. The "sh" is one sound.',
                'choices': ['2', '3', '4', '5'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which word follows the "magic e" rule?',
                'correct_answer': 'hope',
                'explanation': 'The silent "e" at the end of "hope" makes the "o" say its name (long vowel sound).',
                'choices': ['cat', 'hope', 'dog', 'fish'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'What is the schwa sound in the word "about"?',
                'correct_answer': 'the "a" sound',
                'explanation': 'The schwa is the unstressed vowel sound. In "about", the "a" makes the schwa sound /uh/.',
                'choices': ['the "a" sound', 'the "ou" sound', 'the "b" sound', 'the "t" sound'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'Which word has a soft "c" sound?',
                'correct_answer': 'city',
                'explanation': 'Soft "c" sounds like /s/. In "city", the "c" is soft because it comes before "i".',
                'choices': ['cat', 'city', 'car', 'cup'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'What sound does "y" make at the end of the word "happy"?',
                'correct_answer': 'long e',
                'explanation': 'When "y" is at the end of a word with more than one syllable, it usually makes the long "e" sound.',
                'choices': ['long i', 'long e', 'short i', 'short e'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which word contains a trigraph (three letters that make one sound)?',
                'correct_answer': 'night',
                'explanation': 'A trigraph is three letters that make one sound. "Igh" in "night" makes the long "i" sound.',
                'choices': ['cat', 'ship', 'night', 'tree'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'What happens to the "e" in "hope" when we add "-ing"?',
                'correct_answer': 'it is dropped',
                'explanation': 'When adding "-ing" to words ending in silent "e", we drop the "e": hope → hoping.',
                'choices': ['it stays', 'it is dropped', 'it becomes "i"', 'it becomes "a"'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'Which word has the same vowel sound as "cow"?',
                'correct_answer': 'house',
                'explanation': 'Both "cow" and "house" have the /ow/ diphthong sound.',
                'choices': ['cat', 'house', 'tree', 'bike'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'What type of word is "can\'t" (cannot)?',
                'correct_answer': 'contraction',
                'explanation': 'A contraction combines two words with an apostrophe replacing missing letters.',
                'choices': ['compound word', 'contraction', 'prefix word', 'suffix word'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which word has a hard "g" sound?',
                'correct_answer': 'goat',
                'explanation': 'Hard "g" sounds like /g/. In "goat", the "g" is hard because it comes before "o".',
                'choices': ['giant', 'goat', 'giraffe', 'gym'],
                'difficulty': 'intermediate'
            }
        ]

        print(f"\nAdding {len(phonics_questions)} questions to Phonics topic...")
        create_questions_for_topic(phonics_topic, phonics_questions, admin_user)

    except Exception as e:
        print(f"Error adding phonics questions: {e}")
        raise

def add_grammar_questions():
    """Add comprehensive grammar questions for nouns and tenses"""
    try:
        english_subject = Subject.objects.get(name__icontains='English')
        grade_5 = ClassLevel.objects.get(subject=english_subject, level_number=5)
        nouns_topic = Topic.objects.get(class_level=grade_5, title='Grammar: Nouns')
        tenses_topic = Topic.objects.get(class_level=grade_5, title='Grammar: Tenses')
        admin_user = User.objects.filter(is_superuser=True).first()

        # Additional Nouns Questions
        nouns_questions = [
            {
                'question_text': 'Which sentence correctly shows possession for a singular noun ending in "s"?',
                'correct_answer': "Chris's backpack is heavy.",
                'explanation': 'For singular nouns ending in "s", add apostrophe + s to show possession.',
                'choices': ["Chris' backpack is heavy.", "Chris's backpack is heavy.", "Chrises backpack is heavy.", "Chris backpack is heavy."],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'What is the collective noun for a group of fish?',
                'correct_answer': 'school',
                'explanation': 'A "school" is the collective noun for a group of fish swimming together.',
                'choices': ['herd', 'flock', 'school', 'pack'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which word is a compound noun?',
                'correct_answer': 'basketball',
                'explanation': 'A compound noun is made of two or more words joined together. "Basketball" = basket + ball.',
                'choices': ['running', 'basketball', 'quickly', 'beautiful'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Identify the gerund (noun form of a verb) in: "Swimming is my favorite activity."',
                'correct_answer': 'Swimming',
                'explanation': 'A gerund is a verb form ending in -ing that acts as a noun. "Swimming" is the subject of the sentence.',
                'choices': ['Swimming', 'favorite', 'activity', 'is'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'What type of noun is "honesty"?',
                'correct_answer': 'Abstract noun',
                'explanation': 'Abstract nouns name ideas, qualities, or feelings that cannot be touched or seen.',
                'choices': ['Concrete noun', 'Abstract noun', 'Proper noun', 'Collective noun'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which is the correct plural of "knife"?',
                'correct_answer': 'knives',
                'explanation': 'Words ending in "f" or "fe" usually change to "ves" in the plural form.',
                'choices': ['knifes', 'knives', 'knifees', 'knife'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'In "The teacher gave homework to the students," what is the indirect object?',
                'correct_answer': 'students',
                'explanation': 'The indirect object receives the direct object. The students receive the homework.',
                'choices': ['teacher', 'homework', 'students', 'gave'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'Which sentence uses an appositive correctly?',
                'correct_answer': 'My friend Sarah, a talented artist, painted this picture.',
                'explanation': 'An appositive renames or explains a noun. "A talented artist" explains who Sarah is.',
                'choices': ['My friend Sarah painted this picture.', 'My friend Sarah, a talented artist, painted this picture.', 'Sarah painted this picture, my friend.', 'My friend, Sarah painted this picture.'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'What is the possessive form of "women"?',
                'correct_answer': "women's",
                'explanation': 'For irregular plurals that don\'t end in "s", add apostrophe + s to show possession.',
                'choices': ["womens'", "women's", "womens", "women"],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which word functions as a noun in this sentence: "The blue car drives fast"?',
                'correct_answer': 'car',
                'explanation': 'A noun names a person, place, thing, or idea. "Car" is the thing being described.',
                'choices': ['blue', 'car', 'drives', 'fast'],
                'difficulty': 'beginner'
            }
        ]

        print(f"\nAdding {len(nouns_questions)} questions to Grammar: Nouns topic...")
        create_questions_for_topic(nouns_topic, nouns_questions, admin_user)

        # Additional Tenses Questions
        tenses_questions = [
            {
                'question_text': 'Which sentence uses the present continuous tense correctly?',
                'correct_answer': 'She is reading a book right now.',
                'explanation': 'Present continuous uses "am/is/are + verb-ing" to show actions happening now.',
                'choices': ['She reads a book right now.', 'She is reading a book right now.', 'She read a book right now.', 'She will read a book right now.'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Complete the sentence with the correct past tense: "Yesterday, the children _____ soccer in the park."',
                'correct_answer': 'played',
                'explanation': 'For regular verbs, add -ed to form the past tense. Play becomes played.',
                'choices': ['play', 'played', 'playing', 'will play'],
                'difficulty': 'beginner'
            },
            {
                'question_text': 'Which sentence shows a future plan or intention?',
                'correct_answer': 'I am going to visit my grandmother tomorrow.',
                'explanation': '"Going to" is used to express future plans or intentions that have been decided.',
                'choices': ['I visit my grandmother tomorrow.', 'I am going to visit my grandmother tomorrow.', 'I visited my grandmother tomorrow.', 'I have visited my grandmother tomorrow.'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'What is the past tense of the irregular verb "bring"?',
                'correct_answer': 'brought',
                'explanation': 'Irregular verbs don\'t follow the regular -ed pattern. "Bring" becomes "brought" in the past.',
                'choices': ['bringed', 'brought', 'brung', 'brang'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which sentence uses the simple present tense for a habit?',
                'correct_answer': 'I brush my teeth every morning.',
                'explanation': 'Simple present tense is used for habits, routines, and repeated actions.',
                'choices': ['I am brushing my teeth every morning.', 'I brush my teeth every morning.', 'I brushed my teeth every morning.', 'I will brush my teeth every morning.'],
                'difficulty': 'beginner'
            },
            {
                'question_text': 'Complete with the correct form: "If it _____ tomorrow, we will stay inside."',
                'correct_answer': 'rains',
                'explanation': 'In first conditional sentences, use simple present in the if-clause and future in the main clause.',
                'choices': ['rain', 'rains', 'will rain', 'rained'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'Which sentence shows an action that started in the past and continues now?',
                'correct_answer': 'I have lived here for five years.',
                'explanation': 'Present perfect tense (have/has + past participle) shows actions that started in the past and continue to the present.',
                'choices': ['I live here for five years.', 'I have lived here for five years.', 'I lived here for five years.', 'I am living here for five years.'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'What is the past participle of "eat"?',
                'correct_answer': 'eaten',
                'explanation': 'The past participle of "eat" is "eaten", used with helping verbs like have, has, had.',
                'choices': ['ate', 'eaten', 'eating', 'eated'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which sentence uses the past continuous tense?',
                'correct_answer': 'I was watching TV when you called.',
                'explanation': 'Past continuous uses "was/were + verb-ing" to show ongoing actions in the past.',
                'choices': ['I watched TV when you called.', 'I was watching TV when you called.', 'I have watched TV when you called.', 'I watch TV when you called.'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Complete the sentence: "By next year, I _____ my degree."',
                'correct_answer': 'will have completed',
                'explanation': 'Future perfect tense (will have + past participle) shows actions that will be completed by a specific future time.',
                'choices': ['complete', 'will complete', 'will have completed', 'have completed'],
                'difficulty': 'advanced'
            }
        ]

        print(f"\nAdding {len(tenses_questions)} questions to Grammar: Tenses topic...")
        create_questions_for_topic(tenses_topic, tenses_questions, admin_user)

    except Exception as e:
        print(f"Error adding grammar questions: {e}")
        raise

def add_vocabulary_questions():
    """Add comprehensive vocabulary questions for Grade 6"""
    try:
        english_subject = Subject.objects.get(name__icontains='English')
        grade_6 = ClassLevel.objects.get(subject=english_subject, level_number=6)
        vocabulary_topic = Topic.objects.get(class_level=grade_6, title='Vocabulary Building')
        admin_user = User.objects.filter(is_superuser=True).first()

        vocabulary_questions = [
            {
                'question_text': 'What does the root word "bio" mean in words like "biology" and "biography"?',
                'correct_answer': 'life',
                'explanation': 'The Greek root "bio" means life. Biology is the study of life, biography is a life story.',
                'choices': ['water', 'life', 'earth', 'time'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which prefix means "not" or "opposite of"?',
                'correct_answer': 'un-',
                'explanation': 'The prefix "un-" means not or opposite, as in "unhappy" (not happy) or "unlock" (opposite of lock).',
                'choices': ['re-', 'un-', 'pre-', 'sub-'],
                'difficulty': 'beginner'
            },
            {
                'question_text': 'What does the suffix "-ology" mean?',
                'correct_answer': 'study of',
                'explanation': 'The suffix "-ology" means "study of", as in psychology (study of mind) or geology (study of earth).',
                'choices': ['fear of', 'study of', 'love of', 'made of'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Using context clues, what does "famished" mean in: "After hiking all day without food, we were famished"?',
                'correct_answer': 'very hungry',
                'explanation': 'Context clues "hiking all day without food" suggest famished means very hungry.',
                'choices': ['tired', 'very hungry', 'excited', 'lost'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'What is an antonym for "generous"?',
                'correct_answer': 'selfish',
                'explanation': 'Antonyms are words with opposite meanings. "Selfish" is the opposite of "generous".',
                'choices': ['kind', 'selfish', 'helpful', 'caring'],
                'difficulty': 'beginner'
            },
            {
                'question_text': 'Which word is a synonym for "enormous"?',
                'correct_answer': 'gigantic',
                'explanation': 'Synonyms are words with similar meanings. "Gigantic" means very large, like "enormous".',
                'choices': ['tiny', 'gigantic', 'medium', 'normal'],
                'difficulty': 'beginner'
            },
            {
                'question_text': 'What does the prefix "multi-" mean in "multicultural"?',
                'correct_answer': 'many',
                'explanation': 'The prefix "multi-" means many or multiple, so multicultural means having many cultures.',
                'choices': ['one', 'two', 'many', 'few'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which word shows the correct use of "affect" vs "effect"?',
                'correct_answer': 'The rain will affect our picnic plans.',
                'explanation': '"Affect" is a verb meaning to influence. "Effect" is a noun meaning result.',
                'choices': ['The rain will affect our picnic plans.', 'The rain will effect our picnic plans.', 'The affect of rain on our plans.', 'Rain has an affect on plans.'],
                'difficulty': 'advanced'
            },
            {
                'question_text': 'What does "chronological" mean?',
                'correct_answer': 'arranged in time order',
                'explanation': 'Chronological means arranged in the order that events happened in time.',
                'choices': ['arranged alphabetically', 'arranged in time order', 'arranged by size', 'arranged randomly'],
                'difficulty': 'intermediate'
            },
            {
                'question_text': 'Which word has a positive connotation?',
                'correct_answer': 'determined',
                'explanation': 'Connotation is the feeling a word gives. "Determined" has a positive feeling, while "stubborn" is negative.',
                'choices': ['stubborn', 'determined', 'pushy', 'demanding'],
                'difficulty': 'advanced'
            }
        ]

        print(f"\nAdding {len(vocabulary_questions)} questions to Vocabulary Building topic...")
        create_questions_for_topic(vocabulary_topic, vocabulary_questions, admin_user)

    except Exception as e:
        print(f"Error adding vocabulary questions: {e}")
        raise

if __name__ == '__main__':
    add_phonics_questions()
    add_grammar_questions()
    add_vocabulary_questions()
    print("\n✅ All additional quiz questions added successfully!")
