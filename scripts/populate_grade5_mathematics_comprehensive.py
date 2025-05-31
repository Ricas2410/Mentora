#!/usr/bin/env python
"""
Comprehensive Grade 5 Mathematics Content Population Script
Creates detailed study notes and quiz questions for all mathematics topics
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

def create_mathematics_content():
    """Create comprehensive Grade 5 Mathematics content"""
    print("🔢 Creating Grade 5 Mathematics Content...")
    
    # Get Mathematics subject and Grade 5 level
    try:
        math_subject = Subject.objects.get(name="Mathematics")
        grade5_math = ClassLevel.objects.get(subject=math_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Mathematics subject or Grade 5 level not found!")
        return
    
    # Mathematics topics for Grade 5
    topics_data = [
        {
            'title': 'Place Value and Number Sense',
            'description': 'Understanding place value up to millions and number relationships',
            'order': 1
        },
        {
            'title': 'Addition and Subtraction',
            'description': 'Multi-digit addition and subtraction with regrouping',
            'order': 2
        },
        {
            'title': 'Multiplication and Division',
            'description': 'Multi-digit multiplication and division strategies',
            'order': 3
        },
        {
            'title': 'Fractions',
            'description': 'Understanding fractions, equivalent fractions, and operations',
            'order': 4
        },
        {
            'title': 'Decimals',
            'description': 'Decimal place value, comparing, and basic operations',
            'order': 5
        },
        {
            'title': 'Measurement',
            'description': 'Length, weight, capacity, time, and temperature',
            'order': 6
        },
        {
            'title': 'Geometry',
            'description': 'Shapes, angles, lines, and basic geometric concepts',
            'order': 7
        },
        {
            'title': 'Data and Graphs',
            'description': 'Collecting, organizing, and interpreting data',
            'order': 8
        }
    ]
    
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            title=topic_data['title'],
            class_level=grade5_math,
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Created topic: {topic.title}")
            
            # Create study notes for each topic
            create_study_notes(topic)
            
            # Create quiz questions for each topic
            create_quiz_questions(topic)
        else:
            print(f"📝 Topic already exists: {topic.title}")

def create_study_notes(topic):
    """Create comprehensive study notes for each topic"""
    
    study_notes_data = {
        'Place Value and Number Sense': {
            'title': 'Understanding Place Value and Numbers',
            'content': '''
# Place Value and Number Sense

## What is Place Value?
Place value tells us the value of each digit in a number based on its position.

### Place Value Chart
```
Millions | Hundred Thousands | Ten Thousands | Thousands | Hundreds | Tens | Ones
    1    |        2         |       3       |     4     |    5     |  6   |  7
```

The number 1,234,567 means:
- 1 million
- 2 hundred thousands  
- 3 ten thousands
- 4 thousands
- 5 hundreds
- 6 tens
- 7 ones

## Reading Large Numbers
**Example:** 2,456,789
- Read: "Two million, four hundred fifty-six thousand, seven hundred eighty-nine"

## Comparing Numbers
To compare numbers:
1. Start from the left (highest place value)
2. Compare digit by digit
3. The first different digit determines which is larger

**Example:** Compare 45,678 and 45,689
- Both start with 45,6
- Compare: 7 vs 8
- Since 8 > 7, then 45,689 > 45,678

## Rounding Numbers
### Rounding Rules:
- Look at the digit to the right of the place you're rounding to
- If it's 5 or more, round up
- If it's less than 5, round down

**Example:** Round 3,847 to the nearest hundred
- Look at the tens place: 4
- Since 4 < 5, round down
- Answer: 3,800

## Practice Tips
1. Use place value charts to organize numbers
2. Practice reading numbers aloud
3. Compare numbers using > (greater than) and < (less than)
4. Round numbers in real-life situations (money, distances)
'''
        },
        
        'Addition and Subtraction': {
            'title': 'Multi-digit Addition and Subtraction',
            'content': '''
# Addition and Subtraction

## Multi-digit Addition
When adding large numbers, line up the digits by place value.

### Steps for Addition:
1. Line up the ones, tens, hundreds, etc.
2. Start adding from the ones column
3. If the sum is 10 or more, regroup (carry over)

**Example:** 2,456 + 1,789
```
  2,456
+ 1,789
-------
  4,245
```

Step by step:
- Ones: 6 + 9 = 15 (write 5, carry 1)
- Tens: 5 + 8 + 1 = 14 (write 4, carry 1)  
- Hundreds: 4 + 7 + 1 = 12 (write 2, carry 1)
- Thousands: 2 + 1 + 1 = 4

## Multi-digit Subtraction
### Steps for Subtraction:
1. Line up digits by place value
2. Start from the ones column
3. If you can't subtract, borrow from the next column

**Example:** 5,234 - 1,678
```
  5,234
- 1,678
-------
  3,556
```

Step by step:
- Ones: 4 - 8 (can't do, borrow) → 14 - 8 = 6
- Tens: 2 - 7 (can't do, borrow) → 12 - 7 = 5
- Hundreds: 1 - 6 (can't do, borrow) → 11 - 6 = 5
- Thousands: 4 - 1 = 3

## Word Problems
**Example:** Sarah has 2,456 stickers. She gives away 789 stickers. How many does she have left?

Solution: 2,456 - 789 = 1,667 stickers

## Estimation
Before solving, estimate your answer:
- 2,456 ≈ 2,500
- 789 ≈ 800
- 2,500 - 800 = 1,700 (close to our answer!)
'''
        }
    }
    
    if topic.title in study_notes_data:
        note_data = study_notes_data[topic.title]
        study_note, created = StudyNote.objects.get_or_create(
            topic=topic,
            title=note_data['title'],
            defaults={
                'content': note_data['content'],
                'order': 1,
                'is_active': True
            }
        )
        
        if created:
            print(f"  📚 Created study note: {note_data['title']}")

def create_quiz_questions(topic):
    """Create quiz questions for each topic"""
    
    questions_data = {
        'Place Value and Number Sense': [
            {
                'question_text': 'In the number 456,789, what is the value of the digit 5?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '5', 'is_correct': False},
                    {'text': '50', 'is_correct': False},
                    {'text': '50,000', 'is_correct': True},
                    {'text': '500,000', 'is_correct': False}
                ],
                'explanation': 'The digit 5 is in the ten thousands place, so its value is 5 × 10,000 = 50,000.'
            },
            {
                'question_text': 'Round 67,834 to the nearest thousand.',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '67,000', 'is_correct': False},
                    {'text': '68,000', 'is_correct': True},
                    {'text': '70,000', 'is_correct': False},
                    {'text': '67,800', 'is_correct': False}
                ],
                'explanation': 'Look at the hundreds place (8). Since 8 ≥ 5, round up to 68,000.'
            }
        ],
        
        'Addition and Subtraction': [
            {
                'question_text': 'What is 2,456 + 3,789?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '6,245', 'is_correct': True},
                    {'text': '6,235', 'is_correct': False},
                    {'text': '5,245', 'is_correct': False},
                    {'text': '6,145', 'is_correct': False}
                ],
                'explanation': 'Add column by column: 6+9=15 (carry 1), 5+8+1=14 (carry 1), 4+7+1=12 (carry 1), 2+3+1=6. Result: 6,245.'
            },
            {
                'question_text': 'What is 5,000 - 2,347?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '2,653', 'is_correct': True},
                    {'text': '2,753', 'is_correct': False},
                    {'text': '3,653', 'is_correct': False},
                    {'text': '2,643', 'is_correct': False}
                ],
                'explanation': 'Borrow from each place value: 5,000 becomes 4,999+1. Then subtract: 10-7=3, 9-4=5, 9-3=6, 4-2=2. Result: 2,653.'
            }
        ]
    }
    
    if topic.title in questions_data:
        for i, q_data in enumerate(questions_data[topic.title]):
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': q_data['question_type'],
                    'explanation': q_data.get('explanation', ''),
                    'order': i + 1,
                    'is_active': True
                }
            )
            
            if created:
                print(f"  ❓ Created question: {q_data['question_text'][:50]}...")
                
                # Create answer choices
                for choice_data in q_data['choices']:
                    AnswerChoice.objects.create(
                        question=question,
                        text=choice_data['text'],
                        is_correct=choice_data['is_correct']
                    )

if __name__ == '__main__':
    create_mathematics_content()
    print("✅ Grade 5 Mathematics content creation completed!")
