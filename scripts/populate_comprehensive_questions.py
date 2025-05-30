#!/usr/bin/env python3
"""
Comprehensive script to populate English quiz questions for Grades 5 and 6
This script creates topics and questions with proper answer choices
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
        for i, q_data in enumerate(questions_data):
            # Create the question
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': 'multiple_choice',
                    'difficulty': 'easy',
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

def create_grade_6_content():
    """Create Grade 6 topics and questions"""
    try:
        # Get English subject and Grade 6
        english_subject = Subject.objects.get(name__icontains='English')
        grade_6 = ClassLevel.objects.get(subject=english_subject, level_number=6)
        admin_user = User.objects.filter(is_superuser=True).first()
        
        print(f"Creating Grade 6 content for {english_subject.name}")
        
        # Create Grade 6 topics
        advanced_tenses_topic, created = Topic.objects.get_or_create(
            class_level=grade_6,
            title='Advanced Grammar: Tenses',
            defaults={
                'description': 'Perfect tenses, progressive forms, and complex sentence structures',
                'difficulty_level': 'advanced',
                'estimated_duration': 35,
                'order': 5
            }
        )
        print(f"Advanced Tenses topic: {'created' if created else 'found'}")
        
        writing_topic, created = Topic.objects.get_or_create(
            class_level=grade_6,
            title='Writing Skills',
            defaults={
                'description': 'Paragraph structure, essay writing, and creative composition',
                'difficulty_level': 'intermediate',
                'estimated_duration': 40,
                'order': 6
            }
        )
        print(f"Writing Skills topic: {'created' if created else 'found'}")
        
        vocabulary_topic, created = Topic.objects.get_or_create(
            class_level=grade_6,
            title='Vocabulary Building',
            defaults={
                'description': 'Word roots, prefixes, suffixes, and context clues',
                'difficulty_level': 'intermediate',
                'estimated_duration': 30,
                'order': 7
            }
        )
        print(f"Vocabulary Building topic: {'created' if created else 'found'}")
        
        # Grade 6 Advanced Tenses Questions
        advanced_tenses_questions = [
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
        
        # Create questions for Advanced Tenses topic
        print(f"\nCreating questions for {advanced_tenses_topic.title}...")
        create_questions_for_topic(advanced_tenses_topic, advanced_tenses_questions, admin_user)
        
        # Grade 6 Writing Skills Questions
        writing_questions = [
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
        
        # Create questions for Writing Skills topic
        print(f"\nCreating questions for {writing_topic.title}...")
        create_questions_for_topic(writing_topic, writing_questions, admin_user)
        
        # Grade 6 Vocabulary Building Questions
        vocabulary_questions = [
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
        
        # Create questions for Vocabulary Building topic
        print(f"\nCreating questions for {vocabulary_topic.title}...")
        create_questions_for_topic(vocabulary_topic, vocabulary_questions, admin_user)
        
        print("\nGrade 6 content created successfully!")
        print(f"Summary:")
        print(f"  - Advanced Grammar: Tenses: {Question.objects.filter(topic=advanced_tenses_topic).count()} questions")
        print(f"  - Writing Skills: {Question.objects.filter(topic=writing_topic).count()} questions")
        print(f"  - Vocabulary Building: {Question.objects.filter(topic=vocabulary_topic).count()} questions")
        
    except Exception as e:
        print(f"Error creating Grade 6 content: {e}")
        raise

if __name__ == '__main__':
    create_grade_6_content()
