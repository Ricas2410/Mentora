#!/usr/bin/env python3
"""
Add real-life Grade 5 English questions for Phonics, Grammar: Nouns, Grammar: Tenses, and Advanced Grammar
Professional questions avoiding duplications and generic content
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice
from users.models import User

def create_questions_for_topic(topic, questions_data, admin_user):
    """Create questions for a specific topic"""
    created_count = 0

    for q_data in questions_data:
        # Check if question already exists to avoid duplicates
        existing_question = Question.objects.filter(
            topic=topic,
            question_text=q_data['question_text']
        ).first()

        if existing_question:
            print(f"    Question already exists: {q_data['question_text'][:50]}...")
            continue

        # Create the question
        # Map difficulty levels to match the model choices
        difficulty_mapping = {
            'beginner': 'easy',
            'intermediate': 'medium',
            'advanced': 'hard'
        }
        difficulty = difficulty_mapping.get(q_data.get('difficulty', 'intermediate'), 'medium')

        question = Question.objects.create(
            topic=topic,
            question_text=q_data['question_text'],
            question_type='multiple_choice',
            correct_answer=q_data['correct_answer'],
            explanation=q_data['explanation'],
            difficulty=difficulty,
            time_limit=45,
            explanation_display_time=5,
            created_by=admin_user
        )

        # Create answer choices
        for i, choice in enumerate(q_data['choices']):
            AnswerChoice.objects.create(
                question=question,
                choice_text=choice,
                is_correct=(choice == q_data['correct_answer']),
                order=i + 1
            )

        created_count += 1

    print(f"    Created {created_count} new questions for {topic.title}")

def get_phonics_questions():
    """Real-life phonics questions for Grade 5"""
    return [
        {
            'question_text': 'When you see the word "phone" in a text message, what sound does "ph" make?',
            'correct_answer': '/f/ sound',
            'explanation': 'The digraph "ph" makes the /f/ sound, like in phone, photo, and elephant.',
            'choices': ['/p/ sound', '/f/ sound', '/h/ sound', '/ph/ sound'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your friend writes "I ate eight cookies." Which words are homophones?',
            'correct_answer': 'ate and eight',
            'explanation': 'Homophones are words that sound the same but have different meanings and spellings.',
            'choices': ['I and ate', 'ate and eight', 'eight and cookies', 'I and cookies'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'In the word "knight" on a medieval story book, which letters are silent?',
            'correct_answer': 'k and gh',
            'explanation': 'In "knight," the "k" at the beginning and "gh" in the middle are silent.',
            'choices': ['k only', 'gh only', 'k and gh', 'n and t'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'When reading a recipe that says "knead the dough," what sound does "kn" make?',
            'correct_answer': '/n/ sound',
            'explanation': 'In words starting with "kn," the "k" is silent, so we only hear the /n/ sound.',
            'choices': ['/k/ sound', '/n/ sound', '/kn/ sound', 'no sound'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your teacher writes "The rough cough made him laugh." How many different sounds does "gh" make?',
            'correct_answer': '3 different sounds',
            'explanation': '"Gh" makes /f/ in rough and cough, is silent in laugh, showing 3 different patterns.',
            'choices': ['1 sound', '2 different sounds', '3 different sounds', '4 different sounds'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'In your science book, you read "The scientist studied the specimen." What makes the /s/ sound in "scientist"?',
            'correct_answer': 'sc',
            'explanation': 'The letter combination "sc" makes the /s/ sound in words like scientist and science.',
            'choices': ['s only', 'c only', 'sc', 'ci'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'When texting your mom "I\'ll be there soon," what type of word is "I\'ll"?',
            'correct_answer': 'contraction',
            'explanation': 'A contraction combines two words with an apostrophe. "I\'ll" = "I will".',
            'choices': ['compound word', 'contraction', 'abbreviation', 'acronym'],
            'difficulty': 'beginner'
        },
        {
            'question_text': 'Reading a story about a "giant giraffe," why does "g" sound different in these words?',
            'correct_answer': 'g before i makes soft sound, g before i makes hard sound',
            'explanation': 'G is usually soft (/j/) before i, e, y (giant, giraffe) and hard (/g/) before a, o, u.',
            'choices': ['They sound the same', 'g before i makes soft sound, g before a makes hard sound', 'g before vowels is always soft', 'g before consonants is always hard'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your friend asks "How do you spell the /sh/ sound in \'nation\'?"',
            'correct_answer': 'ti',
            'explanation': 'The /sh/ sound can be spelled different ways: sh (ship), ti (nation), ci (special).',
            'choices': ['sh', 'ti', 'ch', 'th'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'In the word "psychology" from your health class, which letter is silent?',
            'correct_answer': 'p',
            'explanation': 'In words starting with "ps," the "p" is silent, like in psychology and psalm.',
            'choices': ['p', 's', 'y', 'h'],
            'difficulty': 'advanced'
        }
    ]

def get_nouns_questions():
    """Real-life grammar questions about nouns for Grade 5"""
    return [
        {
            'question_text': 'Your class is planning a field trip to "Disney World." What type of noun is "Disney World"?',
            'correct_answer': 'proper noun',
            'explanation': 'Proper nouns name specific people, places, or things and are always capitalized.',
            'choices': ['common noun', 'proper noun', 'collective noun', 'abstract noun'],
            'difficulty': 'beginner'
        },
        {
            'question_text': 'The cafeteria menu says "The children\'s lunches are ready." What does the apostrophe show?',
            'correct_answer': 'possession by plural noun',
            'explanation': 'For plural nouns ending in s, add only an apostrophe to show possession.',
            'choices': ['plural form', 'possession by singular noun', 'possession by plural noun', 'contraction'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your mom says "Please put the dishes in the dishwasher." What is "dishwasher"?',
            'correct_answer': 'compound noun',
            'explanation': 'A compound noun combines two words to make a new word with a new meaning.',
            'choices': ['simple noun', 'compound noun', 'proper noun', 'collective noun'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The news reports "The team celebrated their victory." What type of noun is "team"?',
            'correct_answer': 'collective noun',
            'explanation': 'Collective nouns name groups of people, animals, or things acting as one unit.',
            'choices': ['common noun', 'proper noun', 'collective noun', 'abstract noun'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your teacher says "Show kindness to others." What type of noun is "kindness"?',
            'correct_answer': 'abstract noun',
            'explanation': 'Abstract nouns name ideas, feelings, or qualities that cannot be touched.',
            'choices': ['concrete noun', 'abstract noun', 'proper noun', 'collective noun'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The recipe calls for "three cups of flour." What type of noun is "flour"?',
            'correct_answer': 'uncountable noun',
            'explanation': 'Uncountable nouns cannot be counted individually and don\'t have plural forms.',
            'choices': ['countable noun', 'uncountable noun', 'proper noun', 'collective noun'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your friend writes "My sister-in-law is visiting." How should this be made plural?',
            'correct_answer': 'sisters-in-law',
            'explanation': 'In compound nouns with hyphens, usually the main noun becomes plural.',
            'choices': ['sister-in-laws', 'sisters-in-law', 'sisters-in-laws', 'sister-in-law'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The sign reads "James\'s Bakery." Why is there an apostrophe and s after James?',
            'correct_answer': 'to show possession by a singular noun ending in s',
            'explanation': 'For singular nouns ending in s, add apostrophe + s to show possession.',
            'choices': ['to make it plural', 'to show possession by a singular noun ending in s', 'to show possession by a plural noun', 'it\'s a mistake'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your science teacher mentions "a school of fish." What is "school" in this context?',
            'correct_answer': 'collective noun',
            'explanation': 'A "school" of fish is a collective noun describing a group of fish.',
            'choices': ['building noun', 'education noun', 'collective noun', 'proper noun'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The weather report says "The geese are flying south." What is the singular form of "geese"?',
            'correct_answer': 'goose',
            'explanation': '"Goose" becomes "geese" in the plural form - this is an irregular plural.',
            'choices': ['goos', 'goose', 'geeses', 'gooses'],
            'difficulty': 'intermediate'
        }
    ]

def get_tenses_questions():
    """Real-life grammar questions about tenses for Grade 5"""
    return [
        {
            'question_text': 'Your friend texts "I am eating lunch right now." What tense is this?',
            'correct_answer': 'present continuous',
            'explanation': 'Present continuous uses "am/is/are + verb-ing" for actions happening now.',
            'choices': ['simple present', 'present continuous', 'present perfect', 'future tense'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The weather forecast says "It will rain tomorrow." What tense is "will rain"?',
            'correct_answer': 'future simple',
            'explanation': 'Future simple uses "will + base verb" to talk about future events.',
            'choices': ['present tense', 'past tense', 'future simple', 'future continuous'],
            'difficulty': 'beginner'
        },
        {
            'question_text': 'Your mom says "I have already finished cooking dinner." What tense is this?',
            'correct_answer': 'present perfect',
            'explanation': 'Present perfect uses "have/has + past participle" for completed actions affecting now.',
            'choices': ['simple past', 'present perfect', 'past perfect', 'present continuous'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'In your diary you write "Yesterday I walked to school." What tense is "walked"?',
            'correct_answer': 'simple past',
            'explanation': 'Simple past describes completed actions in the past, often with time words like "yesterday".',
            'choices': ['simple present', 'simple past', 'past continuous', 'present perfect'],
            'difficulty': 'beginner'
        },
        {
            'question_text': 'Your teacher announces "We are going to visit the museum next week." What future form is this?',
            'correct_answer': 'going to future',
            'explanation': '"Going to" future is used for planned future actions or predictions based on evidence.',
            'choices': ['will future', 'going to future', 'present continuous', 'future perfect'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'You tell your friend "I was playing video games when you called." What tense is "was playing"?',
            'correct_answer': 'past continuous',
            'explanation': 'Past continuous uses "was/were + verb-ing" for ongoing past actions.',
            'choices': ['simple past', 'past continuous', 'past perfect', 'present continuous'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The coach says "By the time the game starts, we will have practiced for two hours." What tense is this?',
            'correct_answer': 'future perfect',
            'explanation': 'Future perfect uses "will have + past participle" for actions completed before a future time.',
            'choices': ['future simple', 'future continuous', 'future perfect', 'present perfect'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your sister says "I had finished my homework before dinner started." What tense is "had finished"?',
            'correct_answer': 'past perfect',
            'explanation': 'Past perfect uses "had + past participle" for actions completed before another past action.',
            'choices': ['simple past', 'past continuous', 'past perfect', 'present perfect'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The news reporter says "The president is visiting our city tomorrow." Why use present continuous for future?',
            'correct_answer': 'for definite planned future events',
            'explanation': 'Present continuous can express future when the action is planned and definite.',
            'choices': ['it\'s a mistake', 'for definite planned future events', 'for predictions', 'for habits'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your dad says "I have been working here for ten years." What tense is this?',
            'correct_answer': 'present perfect continuous',
            'explanation': 'Present perfect continuous uses "have/has been + verb-ing" for ongoing actions that started in the past.',
            'choices': ['present continuous', 'present perfect', 'present perfect continuous', 'past continuous'],
            'difficulty': 'advanced'
        }
    ]

def get_advanced_grammar_questions():
    """Real-life advanced grammar questions for Grade 5"""
    return [
        {
            'question_text': 'Your teacher says "Either Sarah or Tom is responsible for this project." Why use "is" not "are"?',
            'correct_answer': 'the verb agrees with the nearest subject',
            'explanation': 'With "either...or," the verb agrees with the subject closest to it.',
            'choices': ['always use singular with either/or', 'always use plural with either/or', 'the verb agrees with the nearest subject', 'it doesn\'t matter'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The librarian says "Each of the students has a library card." Why "has" not "have"?',
            'correct_answer': '"each" is always singular',
            'explanation': 'Words like "each," "every," and "either" are always singular and take singular verbs.',
            'choices': ['"students" is plural', '"each" is always singular', '"of" makes it plural', 'both are correct'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your friend writes "Me and John went to the store." How should this be corrected?',
            'correct_answer': '"John and I went to the store."',
            'explanation': 'Use "I" as a subject, and put the other person\'s name first out of politeness.',
            'choices': ['"Me and John went to the store."', '"John and I went to the store."', '"John and me went to the store."', '"I and John went to the store."'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The coach announces "The team, along with their coach, are ready." What\'s wrong with this sentence?',
            'correct_answer': 'should be "is ready" because team is singular',
            'explanation': 'The main subject "team" is singular, so use "is." Phrases like "along with" don\'t change the verb.',
            'choices': ['nothing is wrong', 'should be "is ready" because team is singular', 'should be "were ready"', 'should be "have been ready"'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your mom asks "Who did you give the book to?" What\'s the formal way to say this?',
            'correct_answer': '"To whom did you give the book?"',
            'explanation': 'In formal English, don\'t end sentences with prepositions. Use "whom" as the object.',
            'choices': ['"Who did you give the book to?"', '"To whom did you give the book?"', '"Whom did you give the book to?"', '"Who gave you the book?"'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The sign reads "Less than 10 items." What should it say for correct grammar?',
            'correct_answer': '"Fewer than 10 items"',
            'explanation': 'Use "fewer" with countable nouns (items you can count) and "less" with uncountable nouns.',
            'choices': ['"Less than 10 items"', '"Fewer than 10 items"', '"Lesser than 10 items"', '"Under 10 items"'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your friend says "I could care less about that movie." What do they really mean?',
            'correct_answer': 'they should say "couldn\'t care less"',
            'explanation': '"I couldn\'t care less" means you care so little that you couldn\'t care any less.',
            'choices': ['they care a lot', 'they should say "couldn\'t care less"', 'they care a little', 'the phrase is correct'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The teacher writes "Between you and I, this test is hard." What\'s the error?',
            'correct_answer': 'should be "between you and me"',
            'explanation': 'After prepositions like "between," use object pronouns (me, him, her, us, them).',
            'choices': ['should be "between you and me"', 'should be "among you and I"', 'nothing is wrong', 'should be "between I and you"'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your dad says "If I was you, I would study more." How should this be corrected?',
            'correct_answer': '"If I were you" (subjunctive mood)',
            'explanation': 'Use "were" in hypothetical situations with "if" - this is called the subjunctive mood.',
            'choices': ['"If I was you"', '"If I were you" (subjunctive mood)', '"If I am you"', '"If I will be you"'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The news says "The data shows interesting results." Is this correct?',
            'correct_answer': 'should be "data show" because data is plural',
            'explanation': '"Data" is the plural form of "datum," so it takes plural verbs in formal writing.',
            'choices': ['yes, it\'s correct', 'should be "data show" because data is plural', 'should be "the datas show"', 'should be "datum shows"'],
            'difficulty': 'advanced'
        }
    ]

def main():
    """Main function to add all Grade 5 real-life questions"""
    try:
        # Get English subject and Grade 5
        english_subject = Subject.objects.get(name__icontains='English')
        grade_5 = ClassLevel.objects.get(subject=english_subject, level_number=5)
        admin_user = User.objects.filter(is_superuser=True).first()

        if not admin_user:
            admin_user = User.objects.first()

        print(f"Found English subject: {english_subject.name}")
        print(f"Found Grade 5: {grade_5.name}")
        print(f"Using admin user: {admin_user.username}")

        # Get or create topics
        topics_data = [
            ('Phonics', 'Sound patterns, pronunciation, and reading skills'),
            ('Grammar: Nouns', 'Types of nouns, singular/plural forms, and proper usage'),
            ('Grammar: Tenses', 'Understanding past, present, and future tenses'),
            ('Advanced Grammar', 'Complex grammar rules and advanced language usage')
        ]

        topics = {}
        for title, description in topics_data:
            topic, created = Topic.objects.get_or_create(
                class_level=grade_5,
                title=title,
                defaults={
                    'description': description,
                    'difficulty_level': 'intermediate',
                    'estimated_duration': 30,
                    'order': len(Topic.objects.filter(class_level=grade_5)) + 1
                }
            )
            topics[title] = topic
            if created:
                print(f"Created new topic: {title}")
            else:
                print(f"Found existing topic: {title}")

        # Add questions for each topic
        print("\nAdding Phonics questions...")
        create_questions_for_topic(topics['Phonics'], get_phonics_questions(), admin_user)

        print("\nAdding Grammar: Nouns questions...")
        create_questions_for_topic(topics['Grammar: Nouns'], get_nouns_questions(), admin_user)

        print("\nAdding Grammar: Tenses questions...")
        create_questions_for_topic(topics['Grammar: Tenses'], get_tenses_questions(), admin_user)

        print("\nAdding Advanced Grammar questions...")
        create_questions_for_topic(topics['Advanced Grammar'], get_advanced_grammar_questions(), admin_user)

        print("\n✅ Successfully added all Grade 5 real-life English questions!")
        print("📚 Topics covered:")
        print("   - Phonics (10 questions)")
        print("   - Grammar: Nouns (10 questions)")
        print("   - Grammar: Tenses (10 questions)")
        print("   - Advanced Grammar (10 questions)")
        print("📝 Total: 40 new real-life questions added!")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == '__main__':
    main()