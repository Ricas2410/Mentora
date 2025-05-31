#!/usr/bin/env python
"""
Add More Comprehensive Phonics Quizzes
Additional real-life phonics questions to reach 30+ total
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
from content.models import StudyNote, Question, AnswerChoice

def add_more_phonics_quizzes():
    """Add more comprehensive phonics quizzes"""
    print("ADDING MORE COMPREHENSIVE PHONICS QUIZZES")
    print("=" * 50)
    
    try:
        # Find the topic
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topic = Topic.objects.get(title="Spelling and Phonics", class_level=class_level)
        
        print(f"Found topic: {topic.title}")
        print(f"Current questions: {topic.questions.count()}")
        
        # Additional comprehensive phonics questions
        questions = [
            {
                'question_text': 'You\'re playing a word game and need to find words that rhyme with "light." Which word follows the same spelling pattern?',
                'choices': [
                    {'text': 'bite', 'is_correct': False},
                    {'text': 'sight', 'is_correct': True},
                    {'text': 'late', 'is_correct': False},
                    {'text': 'let', 'is_correct': False}
                ],
                'explanation': '"Sight" has the same -ight pattern as "light." Other words in this family include "night," "right," "bright," and "fight."'
            },
            {
                'question_text': 'You see a sign that says "CONSTRUCTION ZONE." The "tion" at the end of "construction" makes what sound?',
                'choices': [
                    {'text': '/shun/ like "shun"', 'is_correct': True},
                    {'text': '/tion/ like "tea-on"', 'is_correct': False},
                    {'text': '/ton/ like "ton"', 'is_correct': False},
                    {'text': '/shin/ like "shin"', 'is_correct': False}
                ],
                'explanation': 'The suffix "-tion" makes the /shun/ sound. You can hear this in "action," "nation," "vacation," and "celebration."'
            },
            {
                'question_text': 'Your friend is learning to spell "beautiful." Which strategy would help them remember the tricky part?',
                'choices': [
                    {'text': 'Remember "beau" means handsome in French', 'is_correct': True},
                    {'text': 'Sound it out exactly as it\'s pronounced', 'is_correct': False},
                    {'text': 'Spell it "beautifull" with double l', 'is_correct': False},
                    {'text': 'Break it as "be-a-u-ti-ful"', 'is_correct': False}
                ],
                'explanation': 'Remembering that "beau" means handsome helps with the unusual "eau" spelling. The word comes from French, which explains the spelling pattern.'
            },
            {
                'question_text': 'You\'re reading a recipe that mentions "kneading" the dough. Why is the "k" silent in "knead"?',
                'choices': [
                    {'text': 'It\'s a spelling mistake', 'is_correct': False},
                    {'text': 'Silent "k" before "n" is a common English pattern', 'is_correct': True},
                    {'text': 'The "k" should be pronounced', 'is_correct': False},
                    {'text': 'Only some people pronounce the "k"', 'is_correct': False}
                ],
                'explanation': 'Words starting with "kn" have silent "k" sounds. This includes "knee," "knife," "know," "knock," and "knight."'
            },
            {
                'question_text': 'In a text message, someone writes "definately." How should you help them spell it correctly?',
                'choices': [
                    {'text': 'It\'s spelled correctly', 'is_correct': False},
                    {'text': 'Change to "definitely" - think "finite" inside', 'is_correct': True},
                    {'text': 'Change to "definitly"', 'is_correct': False},
                    {'text': 'Change to "definatly"', 'is_correct': False}
                ],
                'explanation': 'The correct spelling is "definitely." Remember "finite" is inside the word: de-FINITE-ly. This helps avoid the common mistake of "definately."'
            },
            {
                'question_text': 'You\'re helping someone pronounce "psychology." Which letters are silent?',
                'choices': [
                    {'text': 'The "p" at the beginning', 'is_correct': True},
                    {'text': 'The "ch" in the middle', 'is_correct': False},
                    {'text': 'The "y" at the end', 'is_correct': False},
                    {'text': 'No letters are silent', 'is_correct': False}
                ],
                'explanation': 'The "p" is silent in "psychology." This happens in other Greek-origin words like "pneumonia," "psalm," and "pterodactyl."'
            },
            {
                'question_text': 'You\'re playing Scrabble and want to add "-ing" to "swim." What happens to the spelling?',
                'choices': [
                    {'text': 'swimming - double the "m"', 'is_correct': True},
                    {'text': 'swiming - just add "ing"', 'is_correct': False},
                    {'text': 'swimeing - add "e" then "ing"', 'is_correct': False},
                    {'text': 'swimning - change "m" to "mn"', 'is_correct': False}
                ],
                'explanation': 'The doubling rule applies: one syllable, one vowel, one consonant = double the final consonant. "Swim" becomes "swimming."'
            },
            {
                'question_text': 'You see the word "enough" and notice it doesn\'t follow typical phonics rules. What sound does "ough" make here?',
                'choices': [
                    {'text': '/uff/ like "stuff"', 'is_correct': True},
                    {'text': '/ow/ like "cow"', 'is_correct': False},
                    {'text': '/oh/ like "go"', 'is_correct': False},
                    {'text': '/ock/ like "rock"', 'is_correct': False}
                ],
                'explanation': 'In "enough," "ough" makes the /uff/ sound. English has many "ough" pronunciations: rough (/uff/), through (/oo/), though (/oh/).'
            },
            {
                'question_text': 'Your teacher asks you to identify the vowel digraph in "teacher." Which letters work together to make one vowel sound?',
                'choices': [
                    {'text': 'ea', 'is_correct': True},
                    {'text': 'te', 'is_correct': False},
                    {'text': 'er', 'is_correct': False},
                    {'text': 'ch', 'is_correct': False}
                ],
                'explanation': '"EA" is the vowel digraph making the long E sound (/ee/). Other "ea" words include "beach," "read," and "team."'
            },
            {
                'question_text': 'You\'re learning about compound words. Which of these is spelled as one word?',
                'choices': [
                    {'text': 'ice cream', 'is_correct': False},
                    {'text': 'basketball', 'is_correct': True},
                    {'text': 'high school', 'is_correct': False},
                    {'text': 'living room', 'is_correct': False}
                ],
                'explanation': '"Basketball" is written as one word. Some compounds are one word (basketball), some are two (ice cream), and some are hyphenated (twenty-one).'
            },
            {
                'question_text': 'In the word "island," which letter is silent and why might this confuse spellers?',
                'choices': [
                    {'text': 'The "s" is silent, making it sound like "iland"', 'is_correct': True},
                    {'text': 'The "l" is silent', 'is_correct': False},
                    {'text': 'The "d" is silent', 'is_correct': False},
                    {'text': 'No letters are silent', 'is_correct': False}
                ],
                'explanation': 'The "s" in "island" is silent, so it sounds like "iland." This makes it a tricky word to spell because you can\'t rely on pronunciation alone.'
            },
            {
                'question_text': 'You\'re writing about your "favorite" movie but aren\'t sure about the spelling. Which memory trick helps?',
                'choices': [
                    {'text': 'Remember "favor" + "ite"', 'is_correct': True},
                    {'text': 'Sound it out as "fav-or-ight"', 'is_correct': False},
                    {'text': 'Think of "favour" with British spelling', 'is_correct': False},
                    {'text': 'Remember it ends like "opposite"', 'is_correct': False}
                ],
                'explanation': 'Breaking "favorite" into "favor" + "ite" helps with spelling. The root word "favor" plus the suffix "-ite" makes "favorite."'
            },
            {
                'question_text': 'You\'re reading instructions that say "thoroughly mix the ingredients." What does the "ough" sound like in "thoroughly"?',
                'choices': [
                    {'text': '/oh/ like "go"', 'is_correct': True},
                    {'text': '/uff/ like "stuff"', 'is_correct': False},
                    {'text': '/ow/ like "cow"', 'is_correct': False},
                    {'text': '/ock/ like "rock"', 'is_correct': False}
                ],
                'explanation': 'In "thoroughly," "ough" makes the /oh/ sound, like in "though," "although," and "dough."'
            },
            {
                'question_text': 'You\'re helping a friend spell "separate." They keep writing "seperate." What\'s the memory trick?',
                'choices': [
                    {'text': 'Remember "there\'s A RAT in sepARAte"', 'is_correct': True},
                    {'text': 'Sound it out exactly as pronounced', 'is_correct': False},
                    {'text': 'Think of "desperate" with similar ending', 'is_correct': False},
                    {'text': 'Remember it\'s like "temperate"', 'is_correct': False}
                ],
                'explanation': 'The memory trick "there\'s A RAT in sepARAte" helps remember the "a" in the middle, not "e." Sep-A-rate, not sep-E-rate.'
            },
            {
                'question_text': 'You see the word "yacht" and notice it doesn\'t follow typical spelling patterns. What sound does "ach" make?',
                'choices': [
                    {'text': '/ot/ like "hot"', 'is_correct': True},
                    {'text': '/ach/ like "attach"', 'is_correct': False},
                    {'text': '/ash/ like "cash"', 'is_correct': False},
                    {'text': '/ack/ like "back"', 'is_correct': False}
                ],
                'explanation': 'In "yacht," the "ach" makes an /ot/ sound. This word comes from Dutch, which explains its unusual spelling pattern.'
            },
            {
                'question_text': 'You\'re learning about prefixes. In the word "impossible," what does "im-" mean?',
                'choices': [
                    {'text': 'Very or extremely', 'is_correct': False},
                    {'text': 'Not or opposite of', 'is_correct': True},
                    {'text': 'Again or repeat', 'is_correct': False},
                    {'text': 'Before or in advance', 'is_correct': False}
                ],
                'explanation': '"Im-" means "not" (like "un-"). "Impossible" means "not possible." "Im-" is used before words starting with "p," "b," or "m."'
            },
            {
                'question_text': 'In a word search puzzle, you find "rhythm." Why is this word challenging to spell?',
                'choices': [
                    {'text': 'It has no clear vowel sounds in the middle', 'is_correct': True},
                    {'text': 'It has too many vowels', 'is_correct': False},
                    {'text': 'It has silent letters at the beginning', 'is_correct': False},
                    {'text': 'It follows regular spelling patterns', 'is_correct': False}
                ],
                'explanation': '"Rhythm" is tricky because the "y" acts as a vowel, and there are no clear vowel letters in the middle. Remember: R-H-Y-T-H-M.'
            },
            {
                'question_text': 'You\'re reading a story about a "knight" and a "night." These words sound the same but are spelled differently. What are they called?',
                'choices': [
                    {'text': 'Synonyms', 'is_correct': False},
                    {'text': 'Homophones', 'is_correct': True},
                    {'text': 'Antonyms', 'is_correct': False},
                    {'text': 'Compound words', 'is_correct': False}
                ],
                'explanation': 'Homophones are words that sound the same but have different meanings and spellings, like "knight/night," "write/right," "there/their."'
            },
            {
                'question_text': 'You\'re writing about "Wednesday" and keep forgetting the "d." What\'s a good memory strategy?',
                'choices': [
                    {'text': 'Remember "Wed-nes-day" - break it into parts', 'is_correct': True},
                    {'text': 'Spell it like it sounds: "Wensday"', 'is_correct': False},
                    {'text': 'Think of it as "Wendsday"', 'is_correct': False},
                    {'text': 'Remember it\'s like "Tuesday"', 'is_correct': False}
                ],
                'explanation': 'Breaking "Wednesday" into syllables helps: "Wed-nes-day." The "d" is in "Wed" (like wedding), even though we don\'t pronounce it clearly.'
            },
            {
                'question_text': 'You\'re learning about syllables. How many syllables are in the word "computer"?',
                'choices': [
                    {'text': '2 syllables', 'is_correct': False},
                    {'text': '3 syllables', 'is_correct': True},
                    {'text': '4 syllables', 'is_correct': False},
                    {'text': '5 syllables', 'is_correct': False}
                ],
                'explanation': '"Computer" has 3 syllables: com-pu-ter. Each syllable has one vowel sound: "o," "u," and "e."'
            }
        ]
        
        # Add questions to database
        questions_added = 0
        current_order = topic.questions.count()
        
        for i, q_data in enumerate(questions):
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': 'multiple_choice',
                    'explanation': q_data['explanation'],
                    'order': current_order + i + 1,
                    'time_limit': 60,
                    'is_active': True
                }
            )
            
            if created:
                print(f"  ✅ Added: {q_data['question_text'][:60]}...")
                questions_added += 1
                
                # Add answer choices
                for j, choice_data in enumerate(q_data['choices']):
                    AnswerChoice.objects.create(
                        question=question,
                        choice_text=choice_data['text'],
                        is_correct=choice_data['is_correct'],
                        order=j + 1
                    )
            else:
                print(f"  ⏭️  Skipped: {q_data['question_text'][:60]}... (already exists)")
        
        print(f"\n📊 SUMMARY:")
        print(f"New questions added: {questions_added}")
        print(f"Total questions now: {topic.questions.count()}")
        print("🎯 Phonics topic now has extensive real-life quizzes!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Add more comprehensive phonics quizzes"""
    success = add_more_phonics_quizzes()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("Spelling and Phonics now has even more comprehensive quizzes!")
        print("Students can practice advanced phonics skills in real contexts.")
    else:
        print("\n❌ FAILED!")
        print("Could not add quizzes. Check the error above.")

if __name__ == '__main__':
    main()
