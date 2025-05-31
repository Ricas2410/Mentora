#!/usr/bin/env python
"""
Add Comprehensive Phonics Questions
Real-life, practical questions that test phonics understanding
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

def add_comprehensive_phonics_questions():
    """Add comprehensive phonics questions"""
    print("ADDING COMPREHENSIVE PHONICS QUESTIONS")
    print("=" * 50)
    
    try:
        # Find the topic
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topic = Topic.objects.get(title="Spelling and Phonics", class_level=class_level)
        
        print(f"Found topic: {topic.title}")
        print(f"Current questions: {topic.questions.count()}")
        
        # Comprehensive phonics questions
        questions = [
            {
                'question_text': 'You see the word "knight" in a story. The "kn" at the beginning is silent. Which other word follows the same pattern?',
                'choices': [
                    {'text': 'night', 'is_correct': False},
                    {'text': 'knee', 'is_correct': True},
                    {'text': 'kind', 'is_correct': False},
                    {'text': 'king', 'is_correct': False}
                ],
                'explanation': 'In "knee," the "k" is silent just like in "knight." Other silent "kn" words include "know," "knife," and "knock."'
            },
            {
                'question_text': 'Your friend writes "recieve" in a text message. How should you help them spell it correctly?',
                'choices': [
                    {'text': 'It\'s spelled correctly', 'is_correct': False},
                    {'text': 'Change it to "receive" - I before E except after C', 'is_correct': True},
                    {'text': 'Change it to "receve"', 'is_correct': False},
                    {'text': 'Change it to "reciave"', 'is_correct': False}
                ],
                'explanation': 'The rule "I before E except after C" applies here. After the letter C, we use "ei" not "ie," so it\'s "receive."'
            },
            {
                'question_text': 'You\'re reading a recipe that says to "whisk" the eggs. What sound does "wh" make in this word?',
                'choices': [
                    {'text': '/w/ like in "win"', 'is_correct': True},
                    {'text': '/h/ like in "hat"', 'is_correct': False},
                    {'text': '/sh/ like in "ship"', 'is_correct': False},
                    {'text': '/ch/ like in "chair"', 'is_correct': False}
                ],
                'explanation': 'The "wh" digraph usually makes the /w/ sound, like in "whisk," "when," "where," and "white."'
            },
            {
                'question_text': 'You want to add "-ing" to the word "run" to make "running." Why do you double the "n"?',
                'choices': [
                    {'text': 'It looks better with two n\'s', 'is_correct': False},
                    {'text': 'The doubling rule: one syllable, one vowel, one consonant', 'is_correct': True},
                    {'text': 'All words ending in "n" get doubled', 'is_correct': False},
                    {'text': 'It\'s a mistake - it should be "runing"', 'is_correct': False}
                ],
                'explanation': 'The doubling rule applies to one-syllable words with one vowel and one final consonant. We double the consonant before adding "-ing."'
            },
            {
                'question_text': 'In a text message, someone writes "your going to love this movie." What\'s the spelling error?',
                'choices': [
                    {'text': 'Should be "you\'re" (you are) going to love this', 'is_correct': True},
                    {'text': 'Should be "yore" going to love this', 'is_correct': False},
                    {'text': 'The spelling is correct', 'is_correct': False},
                    {'text': 'Should be "youre" going to love this', 'is_correct': False}
                ],
                'explanation': '"Your" shows ownership (your book), but "you\'re" means "you are." The sentence needs "you\'re" (you are) going to love this.'
            },
            {
                'question_text': 'You\'re playing a word game and need to break "basketball" into syllables. How would you divide it?',
                'choices': [
                    {'text': 'bas-ket-ball', 'is_correct': True},
                    {'text': 'ba-sket-ball', 'is_correct': False},
                    {'text': 'basket-ball', 'is_correct': False},
                    {'text': 'bas-ketball', 'is_correct': False}
                ],
                'explanation': 'Divide between consonants: "bas-ket-ball." Each syllable has one vowel sound: bas (a), ket (e), ball (a).'
            },
            {
                'question_text': 'You see the word "phone" and notice it sounds like it should start with "f." Why is it spelled with "ph"?',
                'choices': [
                    {'text': 'It\'s a spelling mistake', 'is_correct': False},
                    {'text': 'The "ph" digraph makes the /f/ sound in words from Greek', 'is_correct': True},
                    {'text': 'The "p" is silent', 'is_correct': False},
                    {'text': 'It should be spelled "fone"', 'is_correct': False}
                ],
                'explanation': 'Many English words from Greek use "ph" to make the /f/ sound, like "phone," "graph," "elephant," and "alphabet."'
            },
            {
                'question_text': 'Your teacher asks you to find the long vowel sound in "cake." Which vowel is long and why?',
                'choices': [
                    {'text': 'The "a" is long because of the magic E at the end', 'is_correct': True},
                    {'text': 'The "e" is long because it\'s at the end', 'is_correct': False},
                    {'text': 'Both vowels are long', 'is_correct': False},
                    {'text': 'There are no long vowels in "cake"', 'is_correct': False}
                ],
                'explanation': 'The silent E at the end makes the "a" say its name (long A sound). This is the "magic E" rule: consonant-vowel-consonant-E.'
            },
            {
                'question_text': 'You\'re writing about your "happyness" but it looks wrong. What\'s the correct spelling?',
                'choices': [
                    {'text': 'happyness', 'is_correct': False},
                    {'text': 'happiness', 'is_correct': True},
                    {'text': 'hapiness', 'is_correct': False},
                    {'text': 'happines', 'is_correct': False}
                ],
                'explanation': 'When adding "-ness" to words ending in "y" after a consonant, change the "y" to "i": happy + ness = happiness.'
            },
            {
                'question_text': 'In the word "train," what type of vowel combination is "ai"?',
                'choices': [
                    {'text': 'A vowel blend where you hear both sounds', 'is_correct': False},
                    {'text': 'A vowel digraph that makes the long A sound', 'is_correct': True},
                    {'text': 'Two separate vowel sounds', 'is_correct': False},
                    {'text': 'A silent vowel combination', 'is_correct': False}
                ],
                'explanation': '"AI" is a vowel digraph - two vowels that make one sound. It makes the long A sound, like in "rain," "pain," and "main."'
            },
            {
                'question_text': 'You\'re reading instructions that say "catch the ball." What spelling pattern does "catch" follow?',
                'choices': [
                    {'text': 'The -ch pattern after long vowels', 'is_correct': False},
                    {'text': 'The -tch pattern after short vowels', 'is_correct': True},
                    {'text': 'The silent letter pattern', 'is_correct': False},
                    {'text': 'The double consonant pattern', 'is_correct': False}
                ],
                'explanation': 'Use "-tch" after short vowels: catch, fetch, pitch, watch, hutch. Use "-ch" after long vowels or consonants: beach, lunch.'
            },
            {
                'question_text': 'Your friend says "I can\'t weight for the party!" What homophone error did they make?',
                'choices': [
                    {'text': 'Should be "wait" - weight is how heavy something is', 'is_correct': True},
                    {'text': 'Should be "wate" - a shorter spelling', 'is_correct': False},
                    {'text': 'The spelling is correct', 'is_correct': False},
                    {'text': 'Should be "wayt" - phonetic spelling', 'is_correct': False}
                ],
                'explanation': '"Weight" refers to how heavy something is. "Wait" means to stay or pause. They sound the same but have different meanings and spellings.'
            },
            {
                'question_text': 'You need to spell a word that rhymes with "night" and means "correct." Which spelling is right?',
                'choices': [
                    {'text': 'rite', 'is_correct': False},
                    {'text': 'write', 'is_correct': False},
                    {'text': 'right', 'is_correct': True},
                    {'text': 'wright', 'is_correct': False}
                ],
                'explanation': '"Right" means correct. "Write" means to put words on paper. "Rite" is a ceremony. "Wright" is a worker (like playwright).'
            },
            {
                'question_text': 'You see the word "thumb" and notice the "b" is silent. Which other word has a similar silent letter?',
                'choices': [
                    {'text': 'crab', 'is_correct': False},
                    {'text': 'lamb', 'is_correct': True},
                    {'text': 'grab', 'is_correct': False},
                    {'text': 'club', 'is_correct': False}
                ],
                'explanation': 'In "lamb," the "b" is silent, just like in "thumb." Other examples include "comb," "climb," and "crumb."'
            },
            {
                'question_text': 'You\'re learning about the word "unhappy." What does the prefix "un-" tell you about the word\'s meaning?',
                'choices': [
                    {'text': 'It makes the word mean "very happy"', 'is_correct': False},
                    {'text': 'It makes the word mean "not happy"', 'is_correct': True},
                    {'text': 'It makes the word mean "happy again"', 'is_correct': False},
                    {'text': 'It doesn\'t change the meaning', 'is_correct': False}
                ],
                'explanation': 'The prefix "un-" means "not" or "opposite of." So "unhappy" means "not happy." Other examples: unfair, unlock, undo.'
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
                    'time_limit': 60,  # Phonics questions might need more time
                    'is_active': True
                }
            )
            
            if created:
                print(f"  ✅ Added: {q_data['question_text'][:50]}...")
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
                print(f"  ⏭️  Skipped: {q_data['question_text'][:50]}... (already exists)")
        
        print(f"\n📊 SUMMARY:")
        print(f"Questions added: {questions_added}")
        print(f"Total questions now: {topic.questions.count()}")
        print("🎯 Phonics topic now has comprehensive, real-life questions!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Add comprehensive phonics questions"""
    success = add_comprehensive_phonics_questions()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("Spelling and Phonics now has comprehensive questions!")
        print("Students can practice real-life phonics skills.")
    else:
        print("\n❌ FAILED!")
        print("Could not add questions. Check the error above.")

if __name__ == '__main__':
    main()
