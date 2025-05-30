#!/usr/bin/env python3
"""
Add even more real-life Grade 5 English questions
This script adds 20 additional questions each for existing topics
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

def get_additional_phonics_questions():
    """Additional real-life phonics questions for Grade 5"""
    return [
        {
            'question_text': 'Your friend sends you a text saying "I\'m writing with a pencil." What sound does "wr" make?',
            'correct_answer': '/r/ sound',
            'explanation': 'In words starting with "wr," the "w" is silent, so we only hear the /r/ sound.',
            'choices': ['/w/ sound', '/r/ sound', '/wr/ sound', 'both sounds'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Reading a story about a "lamb in the field," which letter is silent in "lamb"?',
            'correct_answer': 'b',
            'explanation': 'The "b" at the end of "lamb" is silent, like in thumb, comb, and climb.',
            'choices': ['l', 'a', 'm', 'b'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your teacher writes "The chef made delicious food." What sound does "ch" make in "chef"?',
            'correct_answer': '/sh/ sound',
            'explanation': 'In words from French like "chef," "ch" makes the /sh/ sound instead of /ch/.',
            'choices': ['/ch/ sound', '/sh/ sound', '/k/ sound', '/s/ sound'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'In your science book, you read "The island was beautiful." Which letter is silent?',
            'correct_answer': 's',
            'explanation': 'The "s" in "island" is silent. It\'s pronounced like "eye-land."',
            'choices': ['i', 's', 'l', 'd'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your mom asks you to "listen carefully." Which letters are silent in "listen"?',
            'correct_answer': 't',
            'explanation': 'The "t" in "listen" is silent, like in castle, whistle, and Christmas.',
            'choices': ['l', 'i', 't', 'n'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Reading about "autumn leaves," what sound does "au" make?',
            'correct_answer': '/aw/ sound',
            'explanation': 'The vowel team "au" makes the /aw/ sound, like in sauce, because, and author.',
            'choices': ['/a/ sound', '/u/ sound', '/aw/ sound', '/ou/ sound'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your friend writes "I caught a fish." What sound does "aught" make?',
            'correct_answer': '/awt/ sound',
            'explanation': 'The pattern "aught" makes the /awt/ sound, like in taught, daughter, and naughty.',
            'choices': ['/ag/ sound', '/awt/ sound', '/aut/ sound', '/ough/ sound'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'In the word "through" from your reading book, what sound does "ough" make?',
            'correct_answer': '/oo/ sound',
            'explanation': '"Ough" can make different sounds. In "through," it makes the /oo/ sound.',
            'choices': ['/ow/ sound', '/oo/ sound', '/uff/ sound', '/off/ sound'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your teacher mentions "the rhythm of music." What makes the /th/ sound?',
            'correct_answer': 'th',
            'explanation': 'The digraph "th" makes the /th/ sound in rhythm, even though it\'s spelled unusually.',
            'choices': ['rh', 'th', 'yt', 'hm'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Reading "The knight fought bravely," how many silent letters are in "knight"?',
            'correct_answer': '2',
            'explanation': 'In "knight," both the "k" and "gh" are silent, making it sound like "night."',
            'choices': ['1', '2', '3', '0'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your friend says "I have enough money." What sound does "ough" make in "enough"?',
            'correct_answer': '/uff/ sound',
            'explanation': 'In "enough," "ough" makes the /uff/ sound, like in rough, tough, and cough.',
            'choices': ['/ow/ sound', '/oo/ sound', '/uff/ sound', '/off/ sound'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'In your art class, you use "scissors." Which letter is silent?',
            'correct_answer': 'c',
            'explanation': 'The first "c" in "scissors" is silent. It\'s pronounced like "sizzors."',
            'choices': ['s', 'c', 'i', 'r'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Reading "The sign said stop," which letter is silent in "sign"?',
            'correct_answer': 'g',
            'explanation': 'The "g" in "sign" is silent, like in design, resign, and assign.',
            'choices': ['s', 'i', 'g', 'n'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your teacher writes "Wednesday is tomorrow." Which letters are silent?',
            'correct_answer': 'd',
            'explanation': 'The "d" in "Wednesday" is silent. It\'s pronounced like "Wens-day."',
            'choices': ['w', 'e', 'd', 'n'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'In the word "honest" from your reading, which letter is silent?',
            'correct_answer': 'h',
            'explanation': 'The "h" in "honest" is silent, like in hour, honor, and heir.',
            'choices': ['h', 'o', 'n', 't'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your friend texts "I bought new shoes." What sound does "ought" make?',
            'correct_answer': '/awt/ sound',
            'explanation': 'In "bought," "ought" makes the /awt/ sound, like in thought, brought, and fought.',
            'choices': ['/ow/ sound', '/awt/ sound', '/oot/ sound', '/out/ sound'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Reading about "a beautiful bouquet," what sound does "eau" make?',
            'correct_answer': '/oo/ sound',
            'explanation': 'In words from French like "beautiful" and "bouquet," "eau" makes the /oo/ sound.',
            'choices': ['/e/ sound', '/a/ sound', '/oo/ sound', '/ow/ sound'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your mom says "Don\'t doubt yourself." What sound does "ou" make in "doubt"?',
            'correct_answer': '/ow/ sound',
            'explanation': 'In "doubt," "ou" makes the /ow/ sound, like in shout, about, and cloud.',
            'choices': ['/oo/ sound', '/ow/ sound', '/u/ sound', '/o/ sound'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'In your geography book, you read "colonel." How is this word pronounced?',
            'correct_answer': 'like "kernel"',
            'explanation': '"Colonel" is pronounced like "kernel" - it\'s an unusual spelling from its French origin.',
            'choices': ['like "colonial"', 'like "kernel"', 'like "color-nel"', 'like "cone-el"'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your teacher mentions "yacht racing." What sound does "ach" make in "yacht"?',
            'correct_answer': '/ot/ sound',
            'explanation': '"Yacht" is pronounced like "yot" - the "ach" makes an /ot/ sound in this word.',
            'choices': ['/ach/ sound', '/ot/ sound', '/atch/ sound', '/ak/ sound'],
            'difficulty': 'advanced'
        }
    ]

def get_additional_nouns_questions():
    """Additional real-life grammar questions about nouns for Grade 5"""
    return [
        {
            'question_text': 'The news reports "A flock of birds flew overhead." What type of noun is "flock"?',
            'correct_answer': 'collective noun',
            'explanation': 'A collective noun names a group of people, animals, or things as one unit.',
            'choices': ['common noun', 'proper noun', 'collective noun', 'abstract noun'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your friend says "My happiness depends on friendship." What type of nouns are "happiness" and "friendship"?',
            'correct_answer': 'abstract nouns',
            'explanation': 'Abstract nouns name feelings, ideas, or qualities that cannot be touched.',
            'choices': ['concrete nouns', 'abstract nouns', 'proper nouns', 'collective nouns'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The store sign reads "Children\'s toys are upstairs." What does the apostrophe show?',
            'correct_answer': 'possession by plural noun',
            'explanation': 'For irregular plurals like "children," add apostrophe + s to show possession.',
            'choices': ['plural form', 'possession by singular noun', 'possession by plural noun', 'contraction'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your teacher says "The mice ate the cheese." What is the singular form of "mice"?',
            'correct_answer': 'mouse',
            'explanation': '"Mouse" becomes "mice" in the plural form - this is an irregular plural.',
            'choices': ['mous', 'mouse', 'mices', 'mice'],
            'difficulty': 'beginner'
        },
        {
            'question_text': 'The recipe says "Add two tablespoons of sugar." What type of noun is "sugar"?',
            'correct_answer': 'uncountable noun',
            'explanation': 'Uncountable nouns like "sugar" cannot be counted individually and don\'t have plural forms.',
            'choices': ['countable noun', 'uncountable noun', 'proper noun', 'collective noun'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your mom writes "The women\'s meeting is today." Why is there an apostrophe before the s?',
            'correct_answer': 'to show possession by irregular plural',
            'explanation': 'For irregular plurals like "women," add apostrophe + s to show possession.',
            'choices': ['to make it plural', 'to show possession by irregular plural', 'to show possession by singular', 'it\'s a mistake'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The newspaper headline reads "Firefighter saves family." What type of noun is "firefighter"?',
            'correct_answer': 'compound noun',
            'explanation': 'A compound noun combines two words to make a new word with a new meaning.',
            'choices': ['simple noun', 'compound noun', 'proper noun', 'collective noun'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your friend says "I have three brothers-in-law." What is the correct plural?',
            'correct_answer': 'brothers-in-law',
            'explanation': 'In hyphenated compound nouns, usually the main noun (brothers) becomes plural.',
            'choices': ['brother-in-laws', 'brothers-in-law', 'brothers-in-laws', 'brother-in-law'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The zoo guide says "A pride of lions is resting." What is "pride" in this context?',
            'correct_answer': 'collective noun',
            'explanation': 'A "pride" of lions is a collective noun describing a group of lions.',
            'choices': ['emotion noun', 'feeling noun', 'collective noun', 'proper noun'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your teacher mentions "The deer are grazing." What is unusual about "deer"?',
            'correct_answer': 'same form for singular and plural',
            'explanation': '"Deer" is the same in both singular and plural forms, like sheep, fish, and moose.',
            'choices': ['it\'s always plural', 'same form for singular and plural', 'it\'s always singular', 'it has no plural'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The invitation says "The Johnsons\' house party." How do you show possession for a family name ending in s?',
            'correct_answer': 'add apostrophe only',
            'explanation': 'For plural family names ending in s, add only an apostrophe to show possession.',
            'choices': ['add apostrophe + s', 'add apostrophe only', 'add s only', 'no change needed'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your friend writes "I saw a herd of cattle." What type of noun is "cattle"?',
            'correct_answer': 'plural-only noun',
            'explanation': '"Cattle" is always plural and doesn\'t have a singular form. We say "one cow" or "one bull."',
            'choices': ['singular noun', 'plural-only noun', 'collective noun', 'uncountable noun'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The weather report says "The phenomena are unusual." What is the singular of "phenomena"?',
            'correct_answer': 'phenomenon',
            'explanation': '"Phenomenon" becomes "phenomena" in plural - it\'s from Greek and follows Greek rules.',
            'choices': ['phenomena', 'phenomenon', 'phenomenas', 'phenomenons'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your science teacher says "The fungi are growing." What is the singular form?',
            'correct_answer': 'fungus',
            'explanation': '"Fungus" becomes "fungi" in plural - it\'s from Latin and follows Latin rules.',
            'choices': ['fungi', 'fungus', 'funguses', 'fungas'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The librarian says "These criteria are important." What is the singular?',
            'correct_answer': 'criterion',
            'explanation': '"Criterion" becomes "criteria" in plural - it\'s from Greek.',
            'choices': ['criteria', 'criterion', 'criterias', 'criterions'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your friend says "The staff are meeting today." What type of noun is "staff"?',
            'correct_answer': 'collective noun that can be plural',
            'explanation': 'Collective nouns like "staff" can take plural verbs when referring to individuals in the group.',
            'choices': ['always singular', 'collective noun that can be plural', 'always plural', 'uncountable noun'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The coach announces "The team\'s uniforms are ready." What shows possession here?',
            'correct_answer': 'apostrophe + s',
            'explanation': 'For singular nouns, add apostrophe + s to show possession, even for collective nouns.',
            'choices': ['apostrophe only', 'apostrophe + s', 's only', 'no apostrophe needed'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your mom says "Please put the dishes away." What type of noun is "dishes"?',
            'correct_answer': 'countable plural noun',
            'explanation': '"Dishes" is a countable noun in its plural form - you can count individual dishes.',
            'choices': ['uncountable noun', 'countable plural noun', 'collective noun', 'abstract noun'],
            'difficulty': 'beginner'
        },
        {
            'question_text': 'The news says "The police are investigating." What is unusual about "police"?',
            'correct_answer': 'always takes plural verbs',
            'explanation': '"Police" is always treated as plural and takes plural verbs, even though it doesn\'t end in s.',
            'choices': ['always singular', 'always takes plural verbs', 'can be singular or plural', 'is uncountable'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your teacher says "Mathematics is my favorite subject." Why use "is" not "are"?',
            'correct_answer': 'subject names ending in -s are singular',
            'explanation': 'Subject names like mathematics, physics, and economics are singular despite ending in s.',
            'choices': ['it\'s a mistake', 'subject names ending in -s are singular', 'mathematics is plural', 'both are correct'],
            'difficulty': 'advanced'
        }
    ]

def get_additional_tenses_questions():
    """Additional real-life grammar questions about tenses for Grade 5"""
    return [
        {
            'question_text': 'Your friend calls and says "I am studying for the test right now." What tense is this?',
            'correct_answer': 'present continuous',
            'explanation': 'Present continuous uses "am/is/are + verb-ing" for actions happening at the moment of speaking.',
            'choices': ['simple present', 'present continuous', 'present perfect', 'future tense'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your mom says "I will be cooking dinner when you get home." What tense is "will be cooking"?',
            'correct_answer': 'future continuous',
            'explanation': 'Future continuous uses "will be + verb-ing" for ongoing actions in the future.',
            'choices': ['future simple', 'future continuous', 'future perfect', 'present continuous'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The teacher announces "We have been learning about space for two weeks." What tense is this?',
            'correct_answer': 'present perfect continuous',
            'explanation': 'Present perfect continuous uses "have/has been + verb-ing" for ongoing actions that started in the past.',
            'choices': ['present continuous', 'present perfect', 'present perfect continuous', 'past continuous'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your diary entry says "Yesterday I was playing soccer when it started raining." What tense is "was playing"?',
            'correct_answer': 'past continuous',
            'explanation': 'Past continuous uses "was/were + verb-ing" for ongoing past actions, often interrupted by another action.',
            'choices': ['simple past', 'past continuous', 'past perfect', 'present continuous'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The news reporter says "The president has arrived at the airport." What tense is this?',
            'correct_answer': 'present perfect',
            'explanation': 'Present perfect uses "have/has + past participle" for recently completed actions with present relevance.',
            'choices': ['simple past', 'present perfect', 'past perfect', 'simple present'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your friend texts "I had finished my homework before the movie started." What tense is "had finished"?',
            'correct_answer': 'past perfect',
            'explanation': 'Past perfect uses "had + past participle" for actions completed before another past action.',
            'choices': ['simple past', 'past continuous', 'past perfect', 'present perfect'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The coach says "By next month, we will have practiced for 100 hours." What tense is this?',
            'correct_answer': 'future perfect',
            'explanation': 'Future perfect uses "will have + past participle" for actions that will be completed by a specific future time.',
            'choices': ['future simple', 'future continuous', 'future perfect', 'present perfect'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your teacher says "The bus leaves at 3 PM tomorrow." Why use present tense for future?',
            'correct_answer': 'for scheduled events',
            'explanation': 'Simple present can express future for scheduled events like timetables, schedules, and programs.',
            'choices': ['it\'s a mistake', 'for scheduled events', 'for predictions', 'for habits'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your mom asks "How long have you been waiting?" What type of question is this asking about?',
            'correct_answer': 'duration of ongoing action',
            'explanation': 'Present perfect continuous with "how long" asks about the duration of an action that started in the past and continues now.',
            'choices': ['completed action', 'duration of ongoing action', 'future plans', 'past habits'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The weather forecast says "It is going to rain this afternoon." What future form is this?',
            'correct_answer': 'going to future',
            'explanation': '"Going to" future is used for predictions based on present evidence or planned future actions.',
            'choices': ['will future', 'going to future', 'present continuous', 'future perfect'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your friend says "I wish I were taller." What type of grammar is "were" here?',
            'correct_answer': 'subjunctive mood',
            'explanation': 'The subjunctive mood uses "were" for all persons in hypothetical or wish situations.',
            'choices': ['past tense', 'subjunctive mood', 'conditional', 'future tense'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The story begins "Once upon a time, there lived a princess." What tense is "lived"?',
            'correct_answer': 'simple past',
            'explanation': 'Simple past is used in stories to describe completed actions in the past.',
            'choices': ['simple present', 'simple past', 'past continuous', 'present perfect'],
            'difficulty': 'beginner'
        },
        {
            'question_text': 'Your dad says "I used to play basketball in high school." What does "used to" express?',
            'correct_answer': 'past habits that no longer happen',
            'explanation': '"Used to" expresses past habits, states, or repeated actions that are no longer true.',
            'choices': ['present habits', 'past habits that no longer happen', 'future plans', 'ongoing actions'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'The recipe says "First, you mix the ingredients." What tense is used for instructions?',
            'correct_answer': 'simple present',
            'explanation': 'Instructions and directions typically use simple present tense.',
            'choices': ['simple present', 'imperative', 'future tense', 'present continuous'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your friend says "If I had studied harder, I would have passed." What type of conditional is this?',
            'correct_answer': 'third conditional',
            'explanation': 'Third conditional uses "if + past perfect, would have + past participle" for impossible past situations.',
            'choices': ['first conditional', 'second conditional', 'third conditional', 'zero conditional'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The announcement says "The train is arriving at platform 3." Why use present continuous for future?',
            'correct_answer': 'for definite near future events',
            'explanation': 'Present continuous can express near future for definite, planned events.',
            'choices': ['it\'s a mistake', 'for definite near future events', 'for habits', 'for general truths'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your teacher says "Water boils at 100 degrees Celsius." What tense expresses scientific facts?',
            'correct_answer': 'simple present',
            'explanation': 'Simple present is used for scientific facts, general truths, and universal statements.',
            'choices': ['simple present', 'present continuous', 'present perfect', 'future tense'],
            'difficulty': 'intermediate'
        },
        {
            'question_text': 'Your friend texts "I would help you if I could." What mood is this expressing?',
            'correct_answer': 'conditional mood',
            'explanation': 'The conditional mood uses "would" to express hypothetical situations or polite requests.',
            'choices': ['indicative mood', 'conditional mood', 'subjunctive mood', 'imperative mood'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'The news says "The accident happened while people were crossing the street." What shows the relationship between these actions?',
            'correct_answer': 'past simple interrupted past continuous',
            'explanation': 'Past simple (happened) interrupts past continuous (were crossing) to show one action interrupting another.',
            'choices': ['both actions finished', 'past simple interrupted past continuous', 'both actions ongoing', 'future actions'],
            'difficulty': 'advanced'
        },
        {
            'question_text': 'Your mom says "You had better finish your homework." What does "had better" express?',
            'correct_answer': 'strong advice or warning',
            'explanation': '"Had better" expresses strong advice, recommendations, or warnings about consequences.',
            'choices': ['past obligation', 'strong advice or warning', 'future possibility', 'present ability'],
            'difficulty': 'advanced'
        }
    ]

def main():
    """Main function to add additional Grade 5 real-life questions"""
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

        # Get existing topics
        topics = {
            'Phonics': Topic.objects.get(class_level=grade_5, title='Phonics'),
            'Grammar: Nouns': Topic.objects.get(class_level=grade_5, title='Grammar: Nouns'),
            'Grammar: Tenses': Topic.objects.get(class_level=grade_5, title='Grammar: Tenses'),
        }

        # Add additional questions for each topic
        print("\nAdding additional Phonics questions...")
        create_questions_for_topic(topics['Phonics'], get_additional_phonics_questions(), admin_user)

        print("\nAdding additional Grammar: Nouns questions...")
        create_questions_for_topic(topics['Grammar: Nouns'], get_additional_nouns_questions(), admin_user)

        print("\nAdding additional Grammar: Tenses questions...")
        create_questions_for_topic(topics['Grammar: Tenses'], get_additional_tenses_questions(), admin_user)

        print("\n✅ Successfully added additional Grade 5 real-life English questions!")
        print("📚 Additional questions added:")
        print("   - Phonics (20 more questions)")
        print("   - Grammar: Nouns (20 more questions)")
        print("   - Grammar: Tenses (20 more questions)")
        print("📝 Total: 60 additional real-life questions added!")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == '__main__':
    main()