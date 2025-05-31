#!/usr/bin/env python
"""
Comprehensive Grade 5 Content Population
Adds real-life questions and detailed study notes to ALL Grade 5 topics
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

def add_comprehensive_english_content():
    """Add comprehensive content for all English Language Arts topics"""
    print("Adding comprehensive English Language Arts content...")
    
    try:
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
    except:
        print("  ERROR: English subject not found!")
        return False
    
    # Content for all English topics
    content_data = {
        'Reading Comprehension': {
            'notes': [
                {
                    'title': 'Reading Strategies for Better Understanding',
                    'content': """# Reading Comprehension Strategies

## Before Reading
1. **Preview the Text**
   - Look at the title, headings, and pictures
   - Think about what you already know about the topic
   - Make predictions about what you'll learn

2. **Set a Purpose**
   - Why are you reading this? (for fun, to learn, to find information)
   - What do you want to find out?

## During Reading
1. **Active Reading**
   - Stop and think about what you've read
   - Ask yourself questions: "What just happened?" "Why did this happen?"
   - Make connections to your own life or other books

2. **Visualize**
   - Create pictures in your mind as you read
   - Imagine the characters, settings, and events

3. **Monitor Understanding**
   - If something doesn't make sense, re-read it
   - Look up unfamiliar words
   - Use context clues to figure out meanings

## After Reading
1. **Summarize**
   - Tell the main ideas in your own words
   - What were the most important parts?

2. **Reflect**
   - What did you learn?
   - How did this make you feel?
   - What questions do you still have?

## Real-Life Example
When reading a news article about climate change:
- **Before:** Think about what you know about weather and environment
- **During:** Visualize the effects described, ask "How does this affect me?"
- **After:** Summarize the main points and think about what you can do to help"""
                }
            ],
            'questions': [
                {
                    'question_text': 'You are reading a story about a girl who moves to a new school. What is the BEST way to understand how she feels?',
                    'choices': [
                        {'text': 'Skip the parts about her feelings', 'is_correct': False},
                        {'text': 'Think about a time when you felt nervous or scared', 'is_correct': True},
                        {'text': 'Only focus on what happens in the story', 'is_correct': False},
                        {'text': 'Read as fast as possible', 'is_correct': False}
                    ],
                    'explanation': 'Making personal connections helps you understand characters better. When you relate to their experiences, you can better understand their emotions and motivations.'
                },
                {
                    'question_text': 'While reading an article about recycling, you come across the word "biodegradable." You don\'t know what it means. What should you do FIRST?',
                    'choices': [
                        {'text': 'Skip the word and keep reading', 'is_correct': False},
                        {'text': 'Look for clues in the sentences around it', 'is_correct': True},
                        {'text': 'Stop reading completely', 'is_correct': False},
                        {'text': 'Guess what it means without thinking', 'is_correct': False}
                    ],
                    'explanation': 'Using context clues is the first strategy to try. The sentences around an unknown word often give hints about its meaning.'
                },
                {
                    'question_text': 'After reading a story about friendship, what is the MOST important thing to do?',
                    'choices': [
                        {'text': 'Forget about it and read something else', 'is_correct': False},
                        {'text': 'Think about the main message and how it applies to your life', 'is_correct': True},
                        {'text': 'Memorize every detail', 'is_correct': False},
                        {'text': 'Only remember the characters\' names', 'is_correct': False}
                    ],
                    'explanation': 'Reflecting on the main message and connecting it to your own life helps you learn from what you read and apply those lessons.'
                }
            ]
        },
        'Vocabulary and Word Study': {
            'notes': [
                {
                    'title': 'Building Your Vocabulary',
                    'content': """# Vocabulary and Word Study

## Why Vocabulary Matters
- Helps you understand what you read
- Makes your writing more interesting
- Helps you express your thoughts clearly
- Improves your communication skills

## Strategies for Learning New Words

### 1. Context Clues
Use the words around an unknown word to figure out its meaning.

**Example:** "The enormous elephant was so huge that it couldn't fit through the gate."
- "Enormous" must mean very big because it says the elephant was "huge" and "couldn't fit"

### 2. Word Parts
Many words are made up of parts that have meanings:
- **Prefix:** Beginning part (un-, re-, pre-)
- **Root:** Main part (the core meaning)
- **Suffix:** Ending part (-ing, -ed, -tion)

**Example:** "Unhappy"
- "Un-" means "not"
- "Happy" means "feeling good"
- "Unhappy" means "not happy"

### 3. Word Families
Words that share the same root:
- Act, action, active, actor, activity
- Friend, friendly, friendship, unfriendly

### 4. Multiple Meanings
Many words have more than one meaning:
- **Bank:** Where you keep money OR the side of a river
- **Bark:** Sound a dog makes OR outer covering of a tree
- **Light:** Not heavy OR brightness

## Real-Life Vocabulary Practice
- Read signs, menus, and labels
- Listen to conversations and ask about new words
- Use new words in your own sentences
- Keep a vocabulary journal"""
                }
            ],
            'questions': [
                {
                    'question_text': 'In the sentence "The ancient castle was very old and crumbling," what does "ancient" most likely mean?',
                    'choices': [
                        {'text': 'New and modern', 'is_correct': False},
                        {'text': 'Very old', 'is_correct': True},
                        {'text': 'Small and tiny', 'is_correct': False},
                        {'text': 'Colorful and bright', 'is_correct': False}
                    ],
                    'explanation': 'The context clue "very old" helps us understand that "ancient" means very old. The word "crumbling" also suggests something old that is falling apart.'
                },
                {
                    'question_text': 'What does the prefix "re-" mean in words like "rewrite," "redo," and "replay"?',
                    'choices': [
                        {'text': 'Before', 'is_correct': False},
                        {'text': 'Against', 'is_correct': False},
                        {'text': 'Again', 'is_correct': True},
                        {'text': 'Not', 'is_correct': False}
                    ],
                    'explanation': 'The prefix "re-" means "again." Rewrite means to write again, redo means to do again, and replay means to play again.'
                },
                {
                    'question_text': 'Your friend says, "I need to deposit money at the bank." What does "bank" mean in this sentence?',
                    'choices': [
                        {'text': 'The side of a river', 'is_correct': False},
                        {'text': 'A place that keeps money safe', 'is_correct': True},
                        {'text': 'A type of chair', 'is_correct': False},
                        {'text': 'A kind of food', 'is_correct': False}
                    ],
                    'explanation': 'Context helps us know which meaning of "bank" is correct. Since they mention "deposit money," they mean the financial institution, not the side of a river.'
                }
            ]
        }
    }
    
    # Add content for each topic
    topics_added = 0
    for topic_title, data in content_data.items():
        try:
            topic = Topic.objects.get(title=topic_title, class_level=class_level)
            
            # Add study notes
            for note_data in data['notes']:
                note, created = StudyNote.objects.get_or_create(
                    topic=topic,
                    title=note_data['title'],
                    defaults={
                        'content': note_data['content'],
                        'order': 1
                    }
                )
                if created:
                    print(f"  Added note: {note_data['title']}")
            
            # Add questions
            for i, q_data in enumerate(data['questions']):
                question, created = Question.objects.get_or_create(
                    topic=topic,
                    question_text=q_data['question_text'],
                    defaults={
                        'question_type': 'multiple_choice',
                        'explanation': q_data.get('explanation', ''),
                        'order': i + 1,
                        'time_limit': 45,
                        'is_active': True
                    }
                )
                
                if created:
                    print(f"  Added question: {q_data['question_text'][:50]}...")
                    
                    # Add answer choices
                    for j, choice_data in enumerate(q_data['choices']):
                        AnswerChoice.objects.create(
                            question=question,
                            choice_text=choice_data['text'],
                            is_correct=choice_data['is_correct'],
                            order=j + 1
                        )
            
            topics_added += 1
            
        except Topic.DoesNotExist:
            print(f"  WARNING: Topic '{topic_title}' not found")
    
    print(f"  English Language Arts: {topics_added} topics updated")
    return topics_added > 0

def add_comprehensive_mathematics_content():
    """Add comprehensive content for all Mathematics topics"""
    print("Adding comprehensive Mathematics content...")

    try:
        subject = Subject.objects.get(name="Mathematics")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
    except:
        print("  ERROR: Mathematics subject not found!")
        return False

    # Content for Mathematics topics
    content_data = {
        'Place Value and Number Sense': {
            'notes': [
                {
                    'title': 'Understanding Place Value in Real Life',
                    'content': """# Place Value and Number Sense

## What is Place Value?
Place value tells us what each digit in a number represents based on where it sits.

## Place Value Chart
```
Millions | Hundred Thousands | Ten Thousands | Thousands | Hundreds | Tens | Ones
    2    |        5          |       4       |     3     |    6     |  7   |  8
```

The number 2,543,678 means:
- 2 millions = 2,000,000
- 5 hundred thousands = 500,000
- 4 ten thousands = 40,000
- 3 thousands = 3,000
- 6 hundreds = 600
- 7 tens = 70
- 8 ones = 8

## Real-Life Examples

### Population Numbers
- New York City: 8,336,817 people
- The 8 is in the millions place = 8,000,000 people
- The 3 is in the hundred thousands place = 300,000 people

### Money and Place Value
- $1,234.56
- 1 is in the thousands place = $1,000
- 2 is in the hundreds place = $200
- 3 is in the tens place = $30
- 4 is in the ones place = $4
- 5 is in the tenths place = 50 cents
- 6 is in the hundredths place = 6 cents

### Sports Statistics
- A baseball player's salary: $2,500,000
- The 2 represents $2,000,000
- The 5 represents $500,000

## Comparing Numbers
To compare large numbers:
1. Start from the left (highest place value)
2. Compare digit by digit
3. The first different digit determines which is larger

Example: 45,678 vs 45,876
- Same in ten thousands (4) and thousands (5)
- Different in hundreds: 6 vs 8
- Since 8 > 6, then 45,876 > 45,678"""
                }
            ],
            'questions': [
                {
                    'question_text': 'The attendance at a football game was 67,842 people. What is the value of the digit 7 in this number?',
                    'choices': [
                        {'text': '7', 'is_correct': False},
                        {'text': '70', 'is_correct': False},
                        {'text': '7,000', 'is_correct': True},
                        {'text': '70,000', 'is_correct': False}
                    ],
                    'explanation': 'The digit 7 is in the thousands place, so its value is 7 × 1,000 = 7,000.'
                },
                {
                    'question_text': 'A new video game costs $1,234. Your friend says the 2 represents $200. Is your friend correct?',
                    'choices': [
                        {'text': 'Yes, the 2 is worth $200', 'is_correct': True},
                        {'text': 'No, the 2 is worth $20', 'is_correct': False},
                        {'text': 'No, the 2 is worth $2,000', 'is_correct': False},
                        {'text': 'No, the 2 is worth $2', 'is_correct': False}
                    ],
                    'explanation': 'In $1,234, the digit 2 is in the hundreds place, so it represents $200.'
                }
            ]
        },
        'Multiplication and Division': {
            'notes': [
                {
                    'title': 'Multiplication and Division in Everyday Life',
                    'content': """# Multiplication and Division

## Understanding Multiplication
Multiplication is repeated addition or finding the total when you have equal groups.

### Real-Life Multiplication Examples

#### Shopping
- You buy 4 packs of gum, each pack has 5 pieces
- 4 × 5 = 20 pieces of gum total

#### Cooking
- A recipe calls for 3 cups of flour, but you want to make 4 batches
- 3 × 4 = 12 cups of flour needed

#### Time
- You practice piano 30 minutes each day for 7 days
- 30 × 7 = 210 minutes total practice time

## Understanding Division
Division is splitting things into equal groups or finding how many times one number goes into another.

### Real-Life Division Examples

#### Sharing
- 24 cookies shared equally among 6 friends
- 24 ÷ 6 = 4 cookies per friend

#### Organizing
- 48 students need to form teams of 8
- 48 ÷ 8 = 6 teams

#### Money
- You have $36 and want to buy books that cost $9 each
- $36 ÷ $9 = 4 books you can buy

## Multiplication Strategies

### Arrays
Arrange objects in rows and columns:
```
* * * * *
* * * * *
* * * * *
```
3 rows × 5 columns = 15 total

### Skip Counting
- 5 × 4: Count by 5s four times: 5, 10, 15, 20
- 3 × 6: Count by 3s six times: 3, 6, 9, 12, 15, 18

### Breaking Apart (Distributive Property)
- 7 × 8 = 7 × (5 + 3) = (7 × 5) + (7 × 3) = 35 + 21 = 56

## Division Strategies

### Equal Groups
- 20 ÷ 4: Make 4 equal groups from 20 items
- Each group has 5 items

### Repeated Subtraction
- 15 ÷ 3: How many times can you subtract 3 from 15?
- 15 - 3 = 12, 12 - 3 = 9, 9 - 3 = 6, 6 - 3 = 3, 3 - 3 = 0
- You subtracted 5 times, so 15 ÷ 3 = 5"""
                }
            ],
            'questions': [
                {
                    'question_text': 'A school cafeteria orders 8 boxes of apples. Each box contains 24 apples. How many apples did they order in total?',
                    'choices': [
                        {'text': '32 apples', 'is_correct': False},
                        {'text': '192 apples', 'is_correct': True},
                        {'text': '16 apples', 'is_correct': False},
                        {'text': '240 apples', 'is_correct': False}
                    ],
                    'explanation': '8 boxes × 24 apples per box = 192 apples total. This is a real-life example of multiplication to find the total amount.'
                },
                {
                    'question_text': 'A teacher has 72 stickers to give equally to 9 students. How many stickers will each student receive?',
                    'choices': [
                        {'text': '6 stickers', 'is_correct': False},
                        {'text': '7 stickers', 'is_correct': False},
                        {'text': '8 stickers', 'is_correct': True},
                        {'text': '9 stickers', 'is_correct': False}
                    ],
                    'explanation': '72 ÷ 9 = 8 stickers per student. Division helps us share things equally among groups.'
                }
            ]
        }
    }

    # Add content for each topic
    topics_added = 0
    for topic_title, data in content_data.items():
        try:
            topic = Topic.objects.get(title=topic_title, class_level=class_level)

            # Add study notes
            for note_data in data['notes']:
                note, created = StudyNote.objects.get_or_create(
                    topic=topic,
                    title=note_data['title'],
                    defaults={
                        'content': note_data['content'],
                        'order': 1
                    }
                )
                if created:
                    print(f"  Added note: {note_data['title']}")

            # Add questions
            for i, q_data in enumerate(data['questions']):
                question, created = Question.objects.get_or_create(
                    topic=topic,
                    question_text=q_data['question_text'],
                    defaults={
                        'question_type': 'multiple_choice',
                        'explanation': q_data.get('explanation', ''),
                        'order': i + 1,
                        'time_limit': 45,
                        'is_active': True
                    }
                )

                if created:
                    print(f"  Added question: {q_data['question_text'][:50]}...")

                    # Add answer choices
                    for j, choice_data in enumerate(q_data['choices']):
                        AnswerChoice.objects.create(
                            question=question,
                            choice_text=choice_data['text'],
                            is_correct=choice_data['is_correct'],
                            order=j + 1
                        )

            topics_added += 1

        except Topic.DoesNotExist:
            print(f"  WARNING: Topic '{topic_title}' not found")

    print(f"  Mathematics: {topics_added} topics updated")
    return topics_added > 0

def main():
    """Add comprehensive content to all Grade 5 subjects"""
    print("COMPREHENSIVE GRADE 5 CONTENT POPULATION")
    print("=" * 60)
    print("Adding real-life questions and detailed study notes to ALL topics")
    print("=" * 60)

    subjects_completed = 0

    # English Language Arts
    if add_comprehensive_english_content():
        subjects_completed += 1

    # Mathematics
    if add_comprehensive_mathematics_content():
        subjects_completed += 1

    print(f"\nSUMMARY:")
    print(f"Subjects completed: {subjects_completed}")
    print("Comprehensive content added with real-life examples!")

if __name__ == '__main__':
    main()

