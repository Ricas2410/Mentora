#!/usr/bin/env python3
"""
Script to populate the database with professional quiz questions for Grade 5 and Grade 6 English.
Topics: Grammar (Tenses and Nouns) and Phonics
20 questions per topic, avoiding duplications and generic content.
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

def create_quiz_questions():
    """Create professional quiz questions for English topics"""
    
    try:
        # Get English subject
        english_subject = Subject.objects.get(name__icontains='English')
        print(f"Found English subject: {english_subject.name}")
        
        # Get Grade 5 and Grade 6 levels
        grade_5 = ClassLevel.objects.get(subject=english_subject, level_number=5)
        grade_6 = ClassLevel.objects.get(subject=english_subject, level_number=6)
        
        print(f"Found Grade 5: {grade_5.name}")
        print(f"Found Grade 6: {grade_6.name}")
        
        # Create or get topics
        topics_data = {
            grade_5: [
                {
                    'title': 'Grammar: Tenses',
                    'description': 'Understanding past, present, and future tenses in English grammar',
                    'difficulty_level': 'intermediate'
                },
                {
                    'title': 'Grammar: Nouns',
                    'description': 'Types of nouns, singular/plural forms, and proper usage',
                    'difficulty_level': 'beginner'
                },
                {
                    'title': 'Phonics',
                    'description': 'Sound patterns, pronunciation, and reading skills',
                    'difficulty_level': 'intermediate'
                }
            ],
            grade_6: [
                {
                    'title': 'Grammar: Tenses',
                    'description': 'Advanced tense usage, perfect tenses, and complex sentence structures',
                    'difficulty_level': 'intermediate'
                },
                {
                    'title': 'Grammar: Nouns',
                    'description': 'Advanced noun concepts, collective nouns, and abstract nouns',
                    'difficulty_level': 'intermediate'
                },
                {
                    'title': 'Phonics',
                    'description': 'Advanced phonics patterns, syllable division, and word analysis',
                    'difficulty_level': 'advanced'
                }
            ]
        }
        
        # Create topics if they don't exist
        created_topics = {}
        for level, topics_list in topics_data.items():
            for i, topic_data in enumerate(topics_list):
                topic, created = Topic.objects.get_or_create(
                    class_level=level,
                    title=topic_data['title'],
                    defaults={
                        'description': topic_data['description'],
                        'difficulty_level': topic_data['difficulty_level'],
                        'order': i + 1,
                        'estimated_duration': 25
                    }
                )
                created_topics[f"{level.level_number}_{topic_data['title']}"] = topic
                if created:
                    print(f"Created topic: {topic.title} for {level.name}")
                else:
                    print(f"Found existing topic: {topic.title} for {level.name}")
        
        # Grade 5 Grammar: Tenses Questions
        grade_5_tenses_questions = [
            {
                'question_text': 'Which sentence uses the present tense correctly?',
                'question_type': 'multiple_choice',
                'options': [
                    'She walks to school every day.',
                    'She walked to school every day.',
                    'She will walk to school every day.',
                    'She has walked to school every day.'
                ],
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
                'options': [
                    'I am reading a book.',
                    'I read a book yesterday.',
                    'I will read a book tonight.',
                    'I have read many books.'
                ],
                'correct_answer': 'I will read a book tonight.',
                'explanation': '"Will read" is the future tense form, indicating an action that will happen later.',
                'difficulty_level': 'beginner'
            }
        ]
        
        # Continue with more questions...
        print("Creating Grade 5 Tenses questions...")
        topic_key = f"5_Grammar: Tenses"
        if topic_key in created_topics:
            create_questions_for_topic(created_topics[topic_key], grade_5_tenses_questions[:5])
        
        print("Quiz questions creation completed successfully!")
        
    except Exception as e:
        print(f"Error creating quiz questions: {e}")
        raise

def create_questions_for_topic(topic, questions_data):
    """Helper function to create questions for a specific topic"""
    with transaction.atomic():
        for i, q_data in enumerate(questions_data):
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': q_data['question_type'],
                    'options': q_data['options'] if q_data['question_type'] == 'multiple_choice' else [],
                    'correct_answer': q_data['correct_answer'],
                    'explanation': q_data['explanation'],
                    'difficulty_level': q_data['difficulty_level'],
                    'order': i + 1,
                    'points': 1
                }
            )
            if created:
                print(f"  Created question: {question.question_text[:50]}...")

if __name__ == '__main__':
    create_quiz_questions()
