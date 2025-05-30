#!/usr/bin/env python3
"""
Grade 5 Phonics Questions - Real-life, professional questions
25+ questions covering advanced phonics concepts for Grade 5
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

def create_phonics_questions():
    """Create comprehensive phonics questions for Grade 5"""
    
    try:
        # Get English subject and Grade 5
        english_subject = Subject.objects.get(name__icontains='English')
        grade_5 = ClassLevel.objects.get(subject=english_subject, level_number=5)
        admin_user = User.objects.filter(is_superuser=True).first()
        
        # Get Phonics topic
        phonics_topic = Topic.objects.get(class_level=grade_5, title='Phonics')
        
        print(f"📚 Creating Phonics questions for {grade_5.name}")
        
        # Phonics Questions (25 real-life questions)
        phonics_questions = [
            {
                'question_text': 'Which word has the same vowel sound as "cake"?',
                'choices': ['cat', 'make', 'cap', 'can'],
                'correct_answer': 'make',
                'explanation': 'Both "cake" and "make" have the long A sound (/eɪ/). The silent E makes the A say its name.'
            },
            {
                'question_text': 'What sound does "ph" make in the word "phone"?',
                'choices': ['p sound', 'f sound', 'h sound', 'ph sound'],
                'correct_answer': 'f sound',
                'explanation': 'The digraph "ph" makes the /f/ sound, just like in phone, graph, and elephant.'
            },
            {
                'question_text': 'Which word contains a silent letter?',
                'choices': ['jump', 'knife', 'stop', 'help'],
                'correct_answer': 'knife',
                'explanation': 'In "knife," the K is silent. You only hear the /n/ sound at the beginning.'
            },
            {
                'question_text': 'What is the vowel sound in "book"?',
                'choices': ['long oo', 'short oo', 'long o', 'short o'],
                'correct_answer': 'short oo',
                'explanation': 'Book has the short OO sound (/ʊ/), like in look, took, and good.'
            },
            {
                'question_text': 'Which word has the same ending sound as "nation"?',
                'choices': ['vacation', 'national', 'native', 'natural'],
                'correct_answer': 'vacation',
                'explanation': 'Both "nation" and "vacation" end with the /ʃən/ sound spelled "-tion".'
            },
            {
                'question_text': 'What sound does "igh" make in "night"?',
                'choices': ['short i', 'long i', 'short a', 'long a'],
                'correct_answer': 'long i',
                'explanation': 'The trigraph "igh" makes the long I sound (/aɪ/), like in night, light, and bright.'
            },
            {
                'question_text': 'Which word has a soft C sound?',
                'choices': ['cat', 'city', 'cup', 'car'],
                'correct_answer': 'city',
                'explanation': 'In "city," C makes the soft /s/ sound because it comes before I. Hard C sounds like /k/.'
            },
            {
                'question_text': 'What is the correct way to divide "butterfly" into syllables?',
                'choices': ['but-ter-fly', 'butt-er-fly', 'butter-fly', 'but-terfly'],
                'correct_answer': 'but-ter-fly',
                'explanation': 'Butterfly has three syllables: but-ter-fly. Each syllable has one vowel sound.'
            },
            {
                'question_text': 'Which word contains a diphthong (two vowel sounds together)?',
                'choices': ['coat', 'rain', 'tree', 'boat'],
                'correct_answer': 'rain',
                'explanation': 'Rain contains the diphthong "ai" which makes the long A sound (/eɪ/).'
            },
            {
                'question_text': 'What sound does "ch" make in "school"?',
                'choices': ['ch sound', 'sh sound', 'k sound', 's sound'],
                'correct_answer': 'k sound',
                'explanation': 'In "school," CH makes the /k/ sound. This is common in words from Greek origin.'
            },
            {
                'question_text': 'Which word has the same vowel pattern as "meat"?',
                'choices': ['head', 'seat', 'great', 'bread'],
                'correct_answer': 'seat',
                'explanation': 'Both "meat" and "seat" have the EA pattern making the long E sound (/iː/).'
            },
            {
                'question_text': 'What is the schwa sound in "about"?',
                'choices': ['the a sound', 'the o sound', 'both a and o', 'the u sound'],
                'correct_answer': 'the a sound',
                'explanation': 'In "about," the first A makes the schwa sound (/ə/), which sounds like "uh".'
            },
            {
                'question_text': 'Which word has a hard G sound?',
                'choices': ['giant', 'giraffe', 'goat', 'gentle'],
                'correct_answer': 'goat',
                'explanation': 'In "goat," G makes the hard /g/ sound. Soft G (like J) appears before E, I, or Y.'
            },
            {
                'question_text': 'What sound does "ough" make in "cough"?',
                'choices': ['off sound', 'oo sound', 'ow sound', 'uff sound'],
                'correct_answer': 'off sound',
                'explanation': 'In "cough," OUGH makes the /ɔf/ sound. This spelling pattern has many different sounds.'
            },
            {
                'question_text': 'Which word contains a prefix?',
                'choices': ['happy', 'unhappy', 'happiness', 'happily'],
                'correct_answer': 'unhappy',
                'explanation': 'Unhappy has the prefix "un-" which means "not." It changes the meaning of happy.'
            },
            {
                'question_text': 'What is the root word in "replay"?',
                'choices': ['re', 'play', 'rep', 'lay'],
                'correct_answer': 'play',
                'explanation': 'The root word is "play." The prefix "re-" means "again," so replay means "play again."'
            },
            {
                'question_text': 'Which word has the same sound as "ew" in "new"?',
                'choices': ['sew', 'few', 'pew', 'all of these'],
                'correct_answer': 'all of these',
                'explanation': 'All these words have the /uː/ sound: new, sew, few, and pew all sound the same.'
            },
            {
                'question_text': 'What sound does "y" make at the end of "happy"?',
                'choices': ['long i', 'short i', 'long e', 'short e'],
                'correct_answer': 'long e',
                'explanation': 'When Y is at the end of a word with more than one syllable, it usually makes the long E sound.'
            },
            {
                'question_text': 'Which word has a silent W?',
                'choices': ['write', 'water', 'window', 'winter'],
                'correct_answer': 'write',
                'explanation': 'In "write," the W is silent. You only hear the /r/ sound at the beginning.'
            },
            {
                'question_text': 'What is the vowel sound in "bird"?',
                'choices': ['short i', 'long i', 'r-controlled i', 'short u'],
                'correct_answer': 'r-controlled i',
                'explanation': 'In "bird," the IR makes an r-controlled vowel sound (/ɜr/). The R changes the vowel sound.'
            },
            {
                'question_text': 'Which word contains a compound word?',
                'choices': ['basketball', 'beautiful', 'important', 'elephant'],
                'correct_answer': 'basketball',
                'explanation': 'Basketball is made of two words: basket + ball. This makes it a compound word.'
            },
            {
                'question_text': 'What sound does "qu" make in "queen"?',
                'choices': ['k sound', 'kw sound', 'q sound', 'w sound'],
                'correct_answer': 'kw sound',
                'explanation': 'QU makes the /kw/ sound, like in queen, quick, and question. Q is almost always followed by U.'
            },
            {
                'question_text': 'Which word has the same vowel sound as "coin"?',
                'choices': ['join', 'cone', 'corn', 'come'],
                'correct_answer': 'join',
                'explanation': 'Both "coin" and "join" have the OI diphthong making the /ɔɪ/ sound.'
            },
            {
                'question_text': 'What is the suffix in "teacher"?',
                'choices': ['tea', 'teach', 'er', 'cher'],
                'correct_answer': 'er',
                'explanation': 'The suffix "-er" means "one who does." A teacher is "one who teaches."'
            },
            {
                'question_text': 'Which word has a long vowel sound?',
                'choices': ['cat', 'cut', 'cute', 'cot'],
                'correct_answer': 'cute',
                'explanation': 'Cute has the long U sound (/juː/). The silent E at the end makes the U say its name.'
            }
        ]
        
        # Create questions for Phonics
        create_questions_for_topic(phonics_topic, phonics_questions, admin_user)
        
        print("✅ Successfully created Grade 5 Phonics questions!")
        
    except Exception as e:
        print(f"❌ Error creating phonics questions: {e}")
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
    create_phonics_questions()
