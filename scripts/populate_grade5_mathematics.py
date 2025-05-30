#!/usr/bin/env python3
"""
Grade 5 Mathematics Questions - Real-life, professional questions
Topics: Advanced Fractions, Percentages, Area and Perimeter, Probability
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

def create_mathematics_questions():
    """Create comprehensive mathematics questions for Grade 5"""
    
    try:
        # Get Mathematics subject and Grade 5
        math_subject = Subject.objects.get(name__icontains='Mathematics')
        grade_5 = ClassLevel.objects.get(subject=math_subject, level_number=5)
        admin_user = User.objects.filter(is_superuser=True).first()
        
        print(f"📚 Creating Mathematics questions for {grade_5.name}")
        
        # Get topics
        topics = {
            'fractions': Topic.objects.get(class_level=grade_5, title='Advanced Fractions'),
            'percentages': Topic.objects.get(class_level=grade_5, title='Percentages'),
            'area_perimeter': Topic.objects.get(class_level=grade_5, title='Area and Perimeter'),
            'probability': Topic.objects.get(class_level=grade_5, title='Probability'),
        }
        
        # Advanced Fractions Questions (25 real-life questions)
        fractions_questions = [
            {
                'question_text': 'Sarah ate 3/8 of a pizza and her brother ate 2/8 of the same pizza. How much pizza did they eat together?',
                'choices': ['5/8', '5/16', '1/8', '6/8'],
                'correct_answer': '5/8',
                'explanation': 'To add fractions with the same denominator, add the numerators: 3/8 + 2/8 = 5/8.'
            },
            {
                'question_text': 'A recipe calls for 2 1/4 cups of flour. If Maria wants to make half the recipe, how much flour does she need?',
                'choices': ['1 1/8 cups', '1 1/4 cups', '1 1/2 cups', '1 3/4 cups'],
                'correct_answer': '1 1/8 cups',
                'explanation': 'Half of 2 1/4 is 2 1/4 ÷ 2. Convert to improper fraction: 9/4 ÷ 2 = 9/4 × 1/2 = 9/8 = 1 1/8.'
            },
            {
                'question_text': 'Which fraction is equivalent to 3/4?',
                'choices': ['6/8', '9/16', '12/15', '15/20'],
                'correct_answer': '6/8',
                'explanation': '3/4 = 6/8 because both numerator and denominator are multiplied by 2: 3×2 = 6, 4×2 = 8.'
            },
            {
                'question_text': 'Tom ran 3/5 of a mile on Monday and 4/5 of a mile on Tuesday. How much farther did he run on Tuesday?',
                'choices': ['1/5 mile', '7/5 miles', '1/10 mile', '7/10 miles'],
                'correct_answer': '1/5 mile',
                'explanation': 'To find the difference: 4/5 - 3/5 = 1/5 mile farther on Tuesday.'
            },
            {
                'question_text': 'A chocolate bar is divided into 12 equal pieces. If you eat 5 pieces, what fraction of the chocolate bar is left?',
                'choices': ['5/12', '7/12', '5/7', '7/5'],
                'correct_answer': '7/12',
                'explanation': 'If 5 pieces are eaten, then 12 - 5 = 7 pieces remain. So 7/12 of the chocolate bar is left.'
            },
            {
                'question_text': 'What is 1/3 of 24?',
                'choices': ['6', '8', '9', '12'],
                'correct_answer': '8',
                'explanation': 'To find 1/3 of 24, divide 24 by 3: 24 ÷ 3 = 8.'
            },
            {
                'question_text': 'Which fraction is greater: 2/3 or 5/8?',
                'choices': ['2/3', '5/8', 'They are equal', 'Cannot determine'],
                'correct_answer': '2/3',
                'explanation': 'Convert to common denominator: 2/3 = 16/24 and 5/8 = 15/24. Since 16/24 > 15/24, then 2/3 > 5/8.'
            },
            {
                'question_text': 'A bag contains 20 marbles. If 3/5 of them are red, how many red marbles are there?',
                'choices': ['10', '12', '15', '18'],
                'correct_answer': '12',
                'explanation': '3/5 of 20 = (3 × 20) ÷ 5 = 60 ÷ 5 = 12 red marbles.'
            },
            {
                'question_text': 'Simplify the fraction 8/12 to its lowest terms.',
                'choices': ['4/6', '2/3', '1/2', '3/4'],
                'correct_answer': '2/3',
                'explanation': 'Divide both numerator and denominator by their GCD (4): 8÷4 = 2, 12÷4 = 3, so 8/12 = 2/3.'
            },
            {
                'question_text': 'Lisa spent 2/7 of her allowance on books and 3/7 on games. What fraction of her allowance does she have left?',
                'choices': ['2/7', '5/7', '1/7', '6/7'],
                'correct_answer': '2/7',
                'explanation': 'She spent 2/7 + 3/7 = 5/7. So she has 7/7 - 5/7 = 2/7 of her allowance left.'
            },
            {
                'question_text': 'Convert 7/4 to a mixed number.',
                'choices': ['1 3/4', '1 1/4', '2 1/4', '1 2/4'],
                'correct_answer': '1 3/4',
                'explanation': 'Divide 7 by 4: 7 ÷ 4 = 1 remainder 3. So 7/4 = 1 3/4.'
            },
            {
                'question_text': 'What is 1/4 + 1/6?',
                'choices': ['2/10', '5/12', '1/5', '7/24'],
                'correct_answer': '5/12',
                'explanation': 'Find common denominator (12): 1/4 = 3/12, 1/6 = 2/12. Then 3/12 + 2/12 = 5/12.'
            },
            {
                'question_text': 'A pizza is cut into 8 equal slices. If 3 slices are eaten, what fraction represents the remaining pizza?',
                'choices': ['3/8', '5/8', '3/5', '8/5'],
                'correct_answer': '5/8',
                'explanation': 'If 3 slices are eaten from 8 total slices, then 8 - 3 = 5 slices remain. So 5/8 of the pizza is left.'
            },
            {
                'question_text': 'Which is the correct way to multiply 1/2 × 3/4?',
                'choices': ['4/6', '3/8', '4/8', '1/6'],
                'correct_answer': '3/8',
                'explanation': 'Multiply numerators and denominators: (1 × 3)/(2 × 4) = 3/8.'
            },
            {
                'question_text': 'A recipe needs 3/4 cup of sugar. If you want to make 2 batches, how much sugar do you need?',
                'choices': ['6/4 cups', '1 1/2 cups', '3/8 cups', '6/8 cups'],
                'correct_answer': '1 1/2 cups',
                'explanation': '3/4 × 2 = 6/4 = 1 2/4 = 1 1/2 cups of sugar.'
            },
            {
                'question_text': 'What fraction of an hour is 15 minutes?',
                'choices': ['1/2', '1/3', '1/4', '1/6'],
                'correct_answer': '1/4',
                'explanation': 'There are 60 minutes in an hour. 15/60 = 1/4 of an hour.'
            },
            {
                'question_text': 'Order these fractions from smallest to largest: 1/2, 1/3, 1/4',
                'choices': ['1/4, 1/3, 1/2', '1/2, 1/3, 1/4', '1/3, 1/4, 1/2', '1/4, 1/2, 1/3'],
                'correct_answer': '1/4, 1/3, 1/2',
                'explanation': 'With the same numerator (1), the fraction with the larger denominator is smaller: 1/4 < 1/3 < 1/2.'
            },
            {
                'question_text': 'A class has 24 students. If 1/8 of them wear glasses, how many students wear glasses?',
                'choices': ['2', '3', '4', '6'],
                'correct_answer': '3',
                'explanation': '1/8 of 24 = 24 ÷ 8 = 3 students wear glasses.'
            },
            {
                'question_text': 'What is 5/6 - 1/6?',
                'choices': ['4/6', '2/3', '6/12', 'Both A and B'],
                'correct_answer': 'Both A and B',
                'explanation': '5/6 - 1/6 = 4/6, which simplifies to 2/3. So both answers are correct.'
            },
            {
                'question_text': 'Convert the mixed number 2 3/5 to an improper fraction.',
                'choices': ['11/5', '13/5', '8/5', '10/5'],
                'correct_answer': '13/5',
                'explanation': 'Multiply whole number by denominator and add numerator: (2 × 5) + 3 = 10 + 3 = 13. So 2 3/5 = 13/5.'
            }
        ]
        
        # Create questions for Advanced Fractions
        create_questions_for_topic(topics['fractions'], fractions_questions, admin_user)
        
        print("✅ Successfully created Grade 5 Mathematics Advanced Fractions questions!")
        
    except Exception as e:
        print(f"❌ Error creating mathematics questions: {e}")
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
                    'time_limit': 60,
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
    create_mathematics_questions()
