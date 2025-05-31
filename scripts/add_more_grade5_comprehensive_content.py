#!/usr/bin/env python
"""
Additional Comprehensive Grade 5 Content - More Topics and Questions
Adds more detailed content to existing subjects with real-world examples
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

def add_more_mathematics_content():
    """Add more comprehensive mathematics content"""
    print("🔢 Adding more Grade 5 Mathematics content...")
    
    try:
        math_subject = Subject.objects.get(name="Mathematics")
        grade5_math = ClassLevel.objects.get(subject=math_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Mathematics subject or Grade 5 level not found!")
        return
    
    # Add more questions to existing topics
    additional_questions = {
        'Fractions': [
            {
                'question_text': 'Sarah ate 3/8 of a pizza and her brother ate 2/8 of the same pizza. How much pizza did they eat together?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '5/8', 'is_correct': True},
                    {'text': '5/16', 'is_correct': False},
                    {'text': '1/8', 'is_correct': False},
                    {'text': '6/8', 'is_correct': False}
                ],
                'explanation': 'When adding fractions with the same denominator, add the numerators: 3/8 + 2/8 = 5/8. They ate 5/8 of the pizza together.'
            },
            {
                'question_text': 'Which fraction is equivalent to 2/4?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '1/2', 'is_correct': True},
                    {'text': '4/8', 'is_correct': False},
                    {'text': '3/6', 'is_correct': False},
                    {'text': 'All of the above', 'is_correct': False}
                ],
                'explanation': '2/4 = 1/2 because both the numerator and denominator can be divided by 2. This is called simplifying fractions.'
            },
            {
                'question_text': 'A recipe calls for 3/4 cup of flour. If you want to make half the recipe, how much flour do you need?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '3/8 cup', 'is_correct': True},
                    {'text': '1/4 cup', 'is_correct': False},
                    {'text': '1/2 cup', 'is_correct': False},
                    {'text': '6/8 cup', 'is_correct': False}
                ],
                'explanation': 'Half of 3/4 means 3/4 ÷ 2 = 3/4 × 1/2 = 3/8 cup of flour.'
            },
            {
                'question_text': 'Look at this pizza divided into 8 equal slices. If 5 slices are eaten, what fraction represents the pizza that is left?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '3/8', 'is_correct': True},
                    {'text': '5/8', 'is_correct': False},
                    {'text': '3/5', 'is_correct': False},
                    {'text': '5/3', 'is_correct': False}
                ],
                'explanation': 'If 5 slices out of 8 are eaten, then 8 - 5 = 3 slices remain. So 3/8 of the pizza is left.'
            },
            {
                'question_text': 'Which fraction is larger: 2/3 or 3/4?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '2/3', 'is_correct': False},
                    {'text': '3/4', 'is_correct': True},
                    {'text': 'They are equal', 'is_correct': False},
                    {'text': 'Cannot determine', 'is_correct': False}
                ],
                'explanation': 'To compare fractions, find a common denominator. 2/3 = 8/12 and 3/4 = 9/12. Since 9/12 > 8/12, then 3/4 > 2/3.'
            }
        ],
        
        'Decimals': [
            {
                'question_text': 'The price of a book is $12.75. What does the digit 7 represent in this decimal?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '7 dollars', 'is_correct': False},
                    {'text': '7 cents', 'is_correct': False},
                    {'text': '70 cents', 'is_correct': True},
                    {'text': '7 tenths', 'is_correct': False}
                ],
                'explanation': 'In $12.75, the 7 is in the tenths place, which represents 7 tenths of a dollar, or 70 cents.'
            },
            {
                'question_text': 'Which decimal is equivalent to the fraction 3/10?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '0.3', 'is_correct': True},
                    {'text': '0.03', 'is_correct': False},
                    {'text': '3.0', 'is_correct': False},
                    {'text': '0.30', 'is_correct': False}
                ],
                'explanation': '3/10 means 3 tenths, which is written as 0.3 in decimal form. Note that 0.3 and 0.30 are equivalent.'
            },
            {
                'question_text': 'Order these decimals from smallest to largest: 0.45, 0.4, 0.54, 0.5',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '0.4, 0.45, 0.5, 0.54', 'is_correct': True},
                    {'text': '0.45, 0.4, 0.54, 0.5', 'is_correct': False},
                    {'text': '0.54, 0.5, 0.45, 0.4', 'is_correct': False},
                    {'text': '0.4, 0.5, 0.45, 0.54', 'is_correct': False}
                ],
                'explanation': 'Compare decimals by looking at each place value: 0.4 = 0.40, so 0.40 < 0.45 < 0.50 < 0.54.'
            },
            {
                'question_text': 'A runner completes a race in 12.8 seconds. Another runner finishes in 12.75 seconds. Who was faster?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'The first runner (12.8 seconds)', 'is_correct': False},
                    {'text': 'The second runner (12.75 seconds)', 'is_correct': True},
                    {'text': 'They tied', 'is_correct': False},
                    {'text': 'Cannot determine', 'is_correct': False}
                ],
                'explanation': 'The faster runner has the smaller time. 12.75 < 12.8 (or 12.75 < 12.80), so the second runner was faster.'
            }
        ],
        
        'Measurement': [
            {
                'question_text': 'How many centimeters are in 2.5 meters?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '25 cm', 'is_correct': False},
                    {'text': '250 cm', 'is_correct': True},
                    {'text': '2,500 cm', 'is_correct': False},
                    {'text': '0.25 cm', 'is_correct': False}
                ],
                'explanation': 'Since 1 meter = 100 centimeters, then 2.5 meters = 2.5 × 100 = 250 centimeters.'
            },
            {
                'question_text': 'A recipe calls for 2 liters of water. How many milliliters is this?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '200 mL', 'is_correct': False},
                    {'text': '2,000 mL', 'is_correct': True},
                    {'text': '20 mL', 'is_correct': False},
                    {'text': '20,000 mL', 'is_correct': False}
                ],
                'explanation': 'Since 1 liter = 1,000 milliliters, then 2 liters = 2 × 1,000 = 2,000 milliliters.'
            },
            {
                'question_text': 'Sarah is 1.4 meters tall. Her little brother is 95 centimeters tall. How much taller is Sarah?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '45 cm', 'is_correct': True},
                    {'text': '49 cm', 'is_correct': False},
                    {'text': '0.45 m', 'is_correct': False},
                    {'text': 'Both A and C', 'is_correct': False}
                ],
                'explanation': 'Convert Sarah\'s height to centimeters: 1.4 m = 140 cm. Difference: 140 cm - 95 cm = 45 cm taller.'
            },
            {
                'question_text': 'A school day starts at 8:30 AM and ends at 3:15 PM. How long is the school day?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '6 hours 45 minutes', 'is_correct': True},
                    {'text': '7 hours 15 minutes', 'is_correct': False},
                    {'text': '6 hours 15 minutes', 'is_correct': False},
                    {'text': '7 hours 45 minutes', 'is_correct': False}
                ],
                'explanation': 'From 8:30 AM to 3:15 PM: 8:30 to 12:00 is 3.5 hours, 12:00 to 3:15 is 3.25 hours. Total: 6 hours 45 minutes.'
            }
        ]
    }
    
    # Add questions to existing topics
    for topic_title, questions in additional_questions.items():
        try:
            topic = Topic.objects.get(title=topic_title, class_level=grade5_math)
            
            for i, q_data in enumerate(questions):
                question, created = Question.objects.get_or_create(
                    topic=topic,
                    question_text=q_data['question_text'],
                    defaults={
                        'question_type': q_data['question_type'],
                        'explanation': q_data.get('explanation', ''),
                        'order': 100 + i,  # Start from 100 to avoid conflicts
                        'is_active': True
                    }
                )
                
                if created:
                    print(f"  ❓ Added question to {topic_title}: {q_data['question_text'][:50]}...")
                    
                    # Create answer choices
                    for choice_data in q_data['choices']:
                        AnswerChoice.objects.create(
                            question=question,
                            text=choice_data['text'],
                            is_correct=choice_data['is_correct']
                        )
                        
        except Topic.DoesNotExist:
            print(f"⚠️  Topic '{topic_title}' not found, skipping...")

def add_more_science_content():
    """Add more comprehensive science content"""
    print("🔬 Adding more Grade 5 Science content...")
    
    try:
        science_subject = Subject.objects.get(name="Science")
        grade5_science = ClassLevel.objects.get(subject=science_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Science subject or Grade 5 level not found!")
        return
    
    additional_questions = {
        'Matter and Its Properties': [
            {
                'question_text': 'When you heat ice, it melts into water. This is an example of:',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'A chemical change', 'is_correct': False},
                    {'text': 'A physical change', 'is_correct': True},
                    {'text': 'No change at all', 'is_correct': False},
                    {'text': 'A dangerous reaction', 'is_correct': False}
                ],
                'explanation': 'Melting ice is a physical change because the water molecules stay the same - only the state of matter changes from solid to liquid.'
            },
            {
                'question_text': 'Which of these is a chemical change?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Cutting paper', 'is_correct': False},
                    {'text': 'Melting chocolate', 'is_correct': False},
                    {'text': 'Burning wood', 'is_correct': True},
                    {'text': 'Breaking glass', 'is_correct': False}
                ],
                'explanation': 'Burning wood is a chemical change because it creates new substances (ash, smoke, gases) and cannot be easily reversed.'
            },
            {
                'question_text': 'What happens to the particles in a gas when it is cooled down?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'They move faster', 'is_correct': False},
                    {'text': 'They move slower', 'is_correct': True},
                    {'text': 'They disappear', 'is_correct': False},
                    {'text': 'They stay the same', 'is_correct': False}
                ],
                'explanation': 'When gas is cooled, particles lose energy and move slower. If cooled enough, the gas can condense into a liquid.'
            }
        ],
        
        'Forces and Motion': [
            {
                'question_text': 'Why do you slide down a playground slide?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Because of gravity', 'is_correct': True},
                    {'text': 'Because of magnetism', 'is_correct': False},
                    {'text': 'Because of electricity', 'is_correct': False},
                    {'text': 'Because slides are magic', 'is_correct': False}
                ],
                'explanation': 'Gravity pulls you down the slide. The smooth surface reduces friction, allowing gravity to pull you downward.'
            },
            {
                'question_text': 'Which simple machine would make it easier to lift a heavy box to a high shelf?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'A wheel and axle', 'is_correct': False},
                    {'text': 'A pulley', 'is_correct': True},
                    {'text': 'A wedge', 'is_correct': False},
                    {'text': 'A screw', 'is_correct': False}
                ],
                'explanation': 'A pulley changes the direction of force and can provide mechanical advantage, making it easier to lift heavy objects.'
            }
        ]
    }
    
    # Add questions to existing topics
    for topic_title, questions in additional_questions.items():
        try:
            topic = Topic.objects.get(title=topic_title, class_level=grade5_science)
            
            for i, q_data in enumerate(questions):
                question, created = Question.objects.get_or_create(
                    topic=topic,
                    question_text=q_data['question_text'],
                    defaults={
                        'question_type': q_data['question_type'],
                        'explanation': q_data.get('explanation', ''),
                        'order': 100 + i,
                        'is_active': True
                    }
                )
                
                if created:
                    print(f"  ❓ Added question to {topic_title}: {q_data['question_text'][:50]}...")
                    
                    # Create answer choices
                    for choice_data in q_data['choices']:
                        AnswerChoice.objects.create(
                            question=question,
                            text=choice_data['text'],
                            is_correct=choice_data['is_correct']
                        )
                        
        except Topic.DoesNotExist:
            print(f"⚠️  Topic '{topic_title}' not found, skipping...")

if __name__ == '__main__':
    add_more_mathematics_content()
    add_more_science_content()
    print("✅ Additional Grade 5 content added successfully!")
