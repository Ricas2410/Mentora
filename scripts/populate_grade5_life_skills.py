#!/usr/bin/env python3
"""
Grade 5 Life Skills Questions - Real-life, professional questions
Topics: Health and Nutrition, Safety and First Aid, Communication Skills, Problem Solving
20+ questions per topic with practical applications
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

def create_life_skills_questions():
    """Create comprehensive life skills questions for Grade 5"""
    
    try:
        # Get Life Skills subject and Grade 5
        life_skills_subject = Subject.objects.get(name='Life Skills')
        grade_5 = ClassLevel.objects.get(subject=life_skills_subject, level_number=5)
        admin_user = User.objects.filter(is_superuser=True).first()
        
        print(f"📚 Creating Life Skills questions for {grade_5.name}")
        
        # Get topics
        topics = {
            'health': Topic.objects.get(class_level=grade_5, title='Health and Nutrition'),
            'safety': Topic.objects.get(class_level=grade_5, title='Safety and First Aid'),
            'communication': Topic.objects.get(class_level=grade_5, title='Communication Skills'),
            'problem_solving': Topic.objects.get(class_level=grade_5, title='Problem Solving'),
        }
        
        # Health and Nutrition Questions (20 real-life questions)
        health_questions = [
            {
                'question_text': 'Which food group should make up the largest part of your daily meals?',
                'choices': ['Fruits and vegetables', 'Meat and fish', 'Sweets and snacks', 'Dairy products'],
                'correct_answer': 'Fruits and vegetables',
                'explanation': 'Fruits and vegetables provide essential vitamins, minerals, and fiber that your body needs to stay healthy and grow properly.'
            },
            {
                'question_text': 'How many glasses of water should you drink each day?',
                'choices': ['2-3 glasses', '4-5 glasses', '6-8 glasses', '10-12 glasses'],
                'correct_answer': '6-8 glasses',
                'explanation': 'Drinking 6-8 glasses of water daily helps keep your body hydrated and supports all your body functions.'
            },
            {
                'question_text': 'What is the best way to keep your teeth healthy?',
                'choices': ['Brush once a week', 'Brush twice daily and floss', 'Only use mouthwash', 'Eat lots of candy'],
                'correct_answer': 'Brush twice daily and floss',
                'explanation': 'Brushing twice daily and flossing removes food particles and bacteria that can cause tooth decay and gum disease.'
            },
            {
                'question_text': 'Which activity is best for keeping your heart healthy?',
                'choices': ['Watching TV all day', 'Playing video games', 'Running and playing sports', 'Sleeping 12 hours'],
                'correct_answer': 'Running and playing sports',
                'explanation': 'Physical activities like running and sports make your heart stronger and improve your overall health.'
            },
            {
                'question_text': 'What should you do before eating any meal?',
                'choices': ['Watch TV', 'Wash your hands', 'Take a nap', 'Play games'],
                'correct_answer': 'Wash your hands',
                'explanation': 'Washing your hands before eating removes germs and bacteria that could make you sick.'
            },
            {
                'question_text': 'Which breakfast choice is the healthiest?',
                'choices': ['Candy and soda', 'Oatmeal with fruit', 'Just coffee', 'Chips and cookies'],
                'correct_answer': 'Oatmeal with fruit',
                'explanation': 'Oatmeal with fruit provides fiber, vitamins, and energy to start your day in a healthy way.'
            },
            {
                'question_text': 'How many hours of sleep do 10-year-olds need each night?',
                'choices': ['4-5 hours', '6-7 hours', '9-11 hours', '12-14 hours'],
                'correct_answer': '9-11 hours',
                'explanation': 'Children need 9-11 hours of sleep each night for proper growth, learning, and health.'
            },
            {
                'question_text': 'What should you do if you feel stressed or worried?',
                'choices': ['Keep it to yourself', 'Talk to a trusted adult', 'Eat lots of junk food', 'Stay awake all night'],
                'correct_answer': 'Talk to a trusted adult',
                'explanation': 'Talking to trusted adults like parents, teachers, or counselors helps you deal with stress in healthy ways.'
            },
            {
                'question_text': 'Which snack is the healthiest choice?',
                'choices': ['Potato chips', 'Apple slices with peanut butter', 'Candy bars', 'Sugary cookies'],
                'correct_answer': 'Apple slices with peanut butter',
                'explanation': 'Apple slices with peanut butter provide vitamins, fiber, and protein for sustained energy.'
            },
            {
                'question_text': 'What is the most important reason to exercise regularly?',
                'choices': ['To look good', 'To keep your body and mind healthy', 'To win competitions', 'To impress friends'],
                'correct_answer': 'To keep your body and mind healthy',
                'explanation': 'Regular exercise keeps your body strong, your mind sharp, and helps prevent many health problems.'
            },
            {
                'question_text': 'How often should you wash your hair?',
                'choices': ['Once a month', 'Every day', '2-3 times per week', 'Never'],
                'correct_answer': '2-3 times per week',
                'explanation': 'Washing your hair 2-3 times per week keeps it clean without removing natural oils that protect your scalp.'
            },
            {
                'question_text': 'What should you do if you have a cut or scrape?',
                'choices': ['Ignore it', 'Clean it and cover with a bandage', 'Put dirt on it', 'Lick it'],
                'correct_answer': 'Clean it and cover with a bandage',
                'explanation': 'Cleaning cuts and covering them with bandages prevents infection and helps them heal properly.'
            },
            {
                'question_text': 'Which habit is most important for preventing illness?',
                'choices': ['Staying indoors always', 'Washing hands frequently', 'Avoiding all people', 'Eating only one type of food'],
                'correct_answer': 'Washing hands frequently',
                'explanation': 'Frequent hand washing is one of the best ways to prevent the spread of germs and illness.'
            },
            {
                'question_text': 'What should you do if you feel sick at school?',
                'choices': ['Hide it from everyone', 'Tell your teacher immediately', 'Keep playing', 'Go home without telling anyone'],
                'correct_answer': 'Tell your teacher immediately',
                'explanation': 'Telling your teacher when you feel sick ensures you get proper care and prevents spreading illness to others.'
            },
            {
                'question_text': 'Which food should you limit in your diet?',
                'choices': ['Fresh fruits', 'Vegetables', 'Whole grains', 'Sugary snacks and drinks'],
                'correct_answer': 'Sugary snacks and drinks',
                'explanation': 'Too much sugar can cause tooth decay, weight gain, and other health problems, so it should be limited.'
            },
            {
                'question_text': 'What is the best way to handle anger?',
                'choices': ['Hit something', 'Yell at people', 'Take deep breaths and count to ten', 'Break things'],
                'correct_answer': 'Take deep breaths and count to ten',
                'explanation': 'Taking deep breaths and counting helps you calm down and think clearly before reacting to anger.'
            },
            {
                'question_text': 'Why is it important to eat breakfast?',
                'choices': ['It tastes good', 'It gives you energy for the day', 'Your parents say so', 'It makes you taller'],
                'correct_answer': 'It gives you energy for the day',
                'explanation': 'Breakfast provides the energy and nutrients your body and brain need to function well throughout the morning.'
            },
            {
                'question_text': 'What should you do to protect your skin from the sun?',
                'choices': ['Stay in the sun all day', 'Use sunscreen and wear protective clothing', 'Never go outside', 'Only go out at night'],
                'correct_answer': 'Use sunscreen and wear protective clothing',
                'explanation': 'Sunscreen and protective clothing help prevent sunburn and skin damage from harmful UV rays.'
            },
            {
                'question_text': 'How can you keep your eyes healthy?',
                'choices': ['Stare at screens all day', 'Read in very dim light', 'Take breaks from screens and read in good light', 'Never read books'],
                'correct_answer': 'Take breaks from screens and read in good light',
                'explanation': 'Taking breaks from screens and reading in good light helps prevent eye strain and keeps your vision healthy.'
            },
            {
                'question_text': 'What is the best way to build strong friendships?',
                'choices': ['Always get your way', 'Be kind, honest, and respectful', 'Only talk about yourself', 'Ignore your friends'],
                'correct_answer': 'Be kind, honest, and respectful',
                'explanation': 'Being kind, honest, and respectful helps build trust and strong, lasting friendships.'
            }
        ]
        
        # Create questions for Health and Nutrition
        create_questions_for_topic(topics['health'], health_questions, admin_user)
        
        print("✅ Successfully created Grade 5 Life Skills Health and Nutrition questions!")
        
    except Exception as e:
        print(f"❌ Error creating life skills questions: {e}")
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
    create_life_skills_questions()
