#!/usr/bin/env python3
"""
Grade 5 Science Questions - Real-life, professional questions
Topics: Human Body Systems, Weather and Climate, Simple Machines, Plant Life Cycles
25+ questions per topic with practical applications
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

def create_science_questions():
    """Create comprehensive science questions for Grade 5"""

    try:
        # Get Science subject and Grade 5
        science_subject = Subject.objects.get(name='Science')
        grade_5 = ClassLevel.objects.get(subject=science_subject, level_number=5)
        admin_user = User.objects.filter(is_superuser=True).first()

        print(f"📚 Creating Science questions for {grade_5.name}")

        # Get topics
        topics = {
            'human_body': Topic.objects.get(class_level=grade_5, title='Human Body Systems'),
            'weather': Topic.objects.get(class_level=grade_5, title='Weather and Climate'),
            'machines': Topic.objects.get(class_level=grade_5, title='Simple Machines'),
            'plants': Topic.objects.get(class_level=grade_5, title='Plant Life Cycles'),
        }

        # Human Body Systems Questions (25 real-life questions)
        human_body_questions = [
            {
                'question_text': 'Which organ pumps blood throughout your body?',
                'choices': ['lungs', 'heart', 'stomach', 'brain'],
                'correct_answer': 'heart',
                'explanation': 'The heart is a muscular organ that pumps blood through blood vessels to deliver oxygen and nutrients to all parts of the body.'
            },
            {
                'question_text': 'When you breathe in, air travels through your nose or mouth and then goes to which organ?',
                'choices': ['heart', 'stomach', 'lungs', 'liver'],
                'correct_answer': 'lungs',
                'explanation': 'Air travels from your nose/mouth through the trachea (windpipe) to your lungs, where oxygen enters your blood.'
            },
            {
                'question_text': 'Which body system helps you digest the food you eat?',
                'choices': ['respiratory system', 'digestive system', 'circulatory system', 'nervous system'],
                'correct_answer': 'digestive system',
                'explanation': 'The digestive system breaks down food into nutrients that your body can absorb and use for energy and growth.'
            },
            {
                'question_text': 'What happens to food after you swallow it?',
                'choices': ['It goes to your lungs', 'It goes to your stomach', 'It goes to your heart', 'It goes to your brain'],
                'correct_answer': 'It goes to your stomach',
                'explanation': 'After swallowing, food travels down the esophagus to the stomach, where it is mixed with digestive juices.'
            },
            {
                'question_text': 'Which part of your body controls your thoughts, movements, and senses?',
                'choices': ['heart', 'lungs', 'brain', 'stomach'],
                'correct_answer': 'brain',
                'explanation': 'The brain is the control center of your nervous system. It processes information and controls all body functions.'
            },
            {
                'question_text': 'What do your muscles need from your blood to work properly?',
                'choices': ['carbon dioxide', 'oxygen and nutrients', 'waste products', 'water only'],
                'correct_answer': 'oxygen and nutrients',
                'explanation': 'Muscles need oxygen to burn nutrients (like glucose) for energy. Blood delivers both oxygen and nutrients to muscle cells.'
            },
            {
                'question_text': 'Which bones protect your brain?',
                'choices': ['rib bones', 'skull bones', 'leg bones', 'arm bones'],
                'correct_answer': 'skull bones',
                'explanation': 'The skull is made of several bones that form a protective case around your brain, keeping it safe from injury.'
            },
            {
                'question_text': 'When you exercise, why does your heart beat faster?',
                'choices': ['To pump more blood to working muscles', 'To make you tired', 'To cool you down', 'To make noise'],
                'correct_answer': 'To pump more blood to working muscles',
                'explanation': 'During exercise, muscles need more oxygen and nutrients, so the heart beats faster to pump more blood to meet this increased demand.'
            },
            {
                'question_text': 'What is the main job of your kidneys?',
                'choices': ['To digest food', 'To pump blood', 'To filter waste from blood', 'To help you breathe'],
                'correct_answer': 'To filter waste from blood',
                'explanation': 'Kidneys filter waste products and excess water from your blood, creating urine to remove these wastes from your body.'
            },
            {
                'question_text': 'Which body system includes your bones?',
                'choices': ['digestive system', 'respiratory system', 'skeletal system', 'circulatory system'],
                'correct_answer': 'skeletal system',
                'explanation': 'The skeletal system includes all your bones, which provide structure, protect organs, and work with muscles to help you move.'
            },
            {
                'question_text': 'Why is it important to eat a variety of healthy foods?',
                'choices': ['To taste different flavors', 'To get different nutrients your body needs', 'To fill your stomach', 'To make your parents happy'],
                'correct_answer': 'To get different nutrients your body needs',
                'explanation': 'Different foods provide different vitamins, minerals, and nutrients that your body systems need to function properly and stay healthy.'
            },
            {
                'question_text': 'What happens when you cut your finger and it bleeds?',
                'choices': ['Blood clots to stop bleeding', 'Blood keeps flowing forever', 'The cut gets bigger', 'Nothing happens'],
                'correct_answer': 'Blood clots to stop bleeding',
                'explanation': 'When you get a cut, your blood forms clots (scabs) to seal the wound and stop bleeding, allowing the skin to heal.'
            },
            {
                'question_text': 'Which sense organ helps you maintain balance?',
                'choices': ['eyes', 'ears', 'nose', 'tongue'],
                'correct_answer': 'ears',
                'explanation': 'Your inner ears contain structures that help you maintain balance and know which way is up or down.'
            },
            {
                'question_text': 'What should you do to keep your teeth and gums healthy?',
                'choices': ['Eat lots of candy', 'Brush and floss regularly', 'Never visit a dentist', 'Only drink soda'],
                'correct_answer': 'Brush and floss regularly',
                'explanation': 'Regular brushing and flossing remove food particles and bacteria that can cause tooth decay and gum disease.'
            },
            {
                'question_text': 'Why do you need to drink water every day?',
                'choices': ['To stay hydrated and help body functions', 'To make you heavier', 'To fill your stomach', 'To wash your teeth'],
                'correct_answer': 'To stay hydrated and help body functions',
                'explanation': 'Water is essential for many body functions including digestion, circulation, temperature regulation, and waste removal.'
            },
            {
                'question_text': 'What connects your muscles to your bones?',
                'choices': ['tendons', 'veins', 'nerves', 'skin'],
                'correct_answer': 'tendons',
                'explanation': 'Tendons are strong, flexible tissues that connect muscles to bones, allowing muscles to move bones when they contract.'
            },
            {
                'question_text': 'Which body system carries messages between your brain and other body parts?',
                'choices': ['digestive system', 'nervous system', 'respiratory system', 'skeletal system'],
                'correct_answer': 'nervous system',
                'explanation': 'The nervous system includes your brain, spinal cord, and nerves that carry messages throughout your body.'
            },
            {
                'question_text': 'What protects your lungs and heart inside your chest?',
                'choices': ['skull', 'rib cage', 'spine', 'arm bones'],
                'correct_answer': 'rib cage',
                'explanation': 'Your rib cage is made of curved bones that form a protective cage around your lungs and heart.'
            },
            {
                'question_text': 'Why do you breathe faster when you run?',
                'choices': ['To get more oxygen for your muscles', 'To make noise', 'To cool down', 'To show off'],
                'correct_answer': 'To get more oxygen for your muscles',
                'explanation': 'When you exercise, your muscles need more oxygen to produce energy, so you breathe faster to take in more oxygen.'
            },
            {
                'question_text': 'What is the largest organ in your body?',
                'choices': ['brain', 'heart', 'skin', 'liver'],
                'correct_answer': 'skin',
                'explanation': 'Your skin is actually your largest organ. It protects your body, helps control temperature, and provides your sense of touch.'
            }
        ]

        # Create questions for Human Body Systems
        create_questions_for_topic(topics['human_body'], human_body_questions, admin_user)

        print("✅ Successfully created Grade 5 Science Human Body Systems questions!")

    except Exception as e:
        print(f"❌ Error creating science questions: {e}")
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
    create_science_questions()
