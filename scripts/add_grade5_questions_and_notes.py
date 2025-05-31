#!/usr/bin/env python
"""
Add Questions and Study Notes to Grade 5 Topics
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

def add_english_content():
    """Add questions and notes for English Language Arts"""
    print("Adding English Language Arts content...")
    
    try:
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
    except:
        print("  ERROR: English subject or class level not found!")
        return False
    
    # Reading Comprehension
    topic = Topic.objects.get(title="Reading Comprehension", class_level=class_level)
    
    # Add study note
    StudyNote.objects.get_or_create(
        topic=topic,
        title="Understanding What You Read",
        defaults={
            'content': """Reading comprehension means understanding what you read. Here are key strategies:

1. **Before Reading:**
   - Look at the title and pictures
   - Think about what you already know about the topic
   - Predict what the text might be about

2. **While Reading:**
   - Read slowly and carefully
   - Stop and think about what you've read
   - Ask yourself questions about the text
   - Look for main ideas and details

3. **After Reading:**
   - Summarize what you read in your own words
   - Think about the main message
   - Connect it to your own experiences

**Example:** If you're reading about animals, think about animals you know before reading, look for new facts while reading, and summarize what you learned afterward.""",
            'order': 1
        }
    )
    
    # Add questions
    question1 = Question.objects.get_or_create(
        topic=topic,
        question_text="What should you do BEFORE reading a new text?",
        question_type="multiple_choice",
        defaults={'order': 1, 'time_limit': 45}
    )[0]
    
    AnswerChoice.objects.get_or_create(question=question1, choice_text="Start reading immediately", defaults={'is_correct': False, 'order': 1})
    AnswerChoice.objects.get_or_create(question=question1, choice_text="Look at the title and pictures", defaults={'is_correct': True, 'order': 2})
    AnswerChoice.objects.get_or_create(question=question1, choice_text="Read the last page first", defaults={'is_correct': False, 'order': 3})
    AnswerChoice.objects.get_or_create(question=question1, choice_text="Skip the difficult words", defaults={'is_correct': False, 'order': 4})
    
    question2 = Question.objects.get_or_create(
        topic=topic,
        question_text="Reading comprehension means:",
        question_type="multiple_choice",
        defaults={'order': 2, 'time_limit': 45}
    )[0]
    
    AnswerChoice.objects.get_or_create(question=question2, choice_text="Reading very fast", defaults={'is_correct': False, 'order': 1})
    AnswerChoice.objects.get_or_create(question=question2, choice_text="Understanding what you read", defaults={'is_correct': True, 'order': 2})
    AnswerChoice.objects.get_or_create(question=question2, choice_text="Reading out loud", defaults={'is_correct': False, 'order': 3})
    AnswerChoice.objects.get_or_create(question=question2, choice_text="Memorizing every word", defaults={'is_correct': False, 'order': 4})
    
    print("  English Language Arts content added successfully!")
    return True

def add_mathematics_content():
    """Add questions and notes for Mathematics"""
    print("Adding Mathematics content...")
    
    try:
        subject = Subject.objects.get(name="Mathematics")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
    except:
        print("  ERROR: Mathematics subject or class level not found!")
        return False
    
    # Place Value and Number Sense
    topic = Topic.objects.get(title="Place Value and Number Sense", class_level=class_level)
    
    # Add study note
    StudyNote.objects.get_or_create(
        topic=topic,
        title="Understanding Place Value",
        defaults={
            'content': """Place value tells us what each digit in a number represents based on its position.

**Place Value Chart:**
```
Millions | Hundred Thousands | Ten Thousands | Thousands | Hundreds | Tens | Ones
    1    |        2          |       3       |     4     |    5     |  6   |  7
```

In the number 1,234,567:
- 1 is in the millions place = 1,000,000
- 2 is in the hundred thousands place = 200,000
- 3 is in the ten thousands place = 30,000
- 4 is in the thousands place = 4,000
- 5 is in the hundreds place = 500
- 6 is in the tens place = 60
- 7 is in the ones place = 7

**Example:** The number 45,678 means:
- 4 ten thousands (40,000)
- 5 thousands (5,000)
- 6 hundreds (600)
- 7 tens (70)
- 8 ones (8)

Total: 40,000 + 5,000 + 600 + 70 + 8 = 45,678""",
            'order': 1
        }
    )
    
    # Add questions
    question1 = Question.objects.get_or_create(
        topic=topic,
        question_text="In the number 52,847, what is the value of the digit 5?",
        question_type="multiple_choice",
        defaults={'order': 1, 'time_limit': 45}
    )[0]
    
    AnswerChoice.objects.get_or_create(question=question1, choice_text="5", defaults={'is_correct': False, 'order': 1})
    AnswerChoice.objects.get_or_create(question=question1, choice_text="50", defaults={'is_correct': False, 'order': 2})
    AnswerChoice.objects.get_or_create(question=question1, choice_text="5,000", defaults={'is_correct': False, 'order': 3})
    AnswerChoice.objects.get_or_create(question=question1, choice_text="50,000", defaults={'is_correct': True, 'order': 4})
    
    question2 = Question.objects.get_or_create(
        topic=topic,
        question_text="Which number has 3 in the hundreds place?",
        question_type="multiple_choice",
        defaults={'order': 2, 'time_limit': 45}
    )[0]
    
    AnswerChoice.objects.get_or_create(question=question2, choice_text="1,234", defaults={'is_correct': False, 'order': 1})
    AnswerChoice.objects.get_or_create(question=question2, choice_text="5,367", defaults={'is_correct': True, 'order': 2})
    AnswerChoice.objects.get_or_create(question=question2, choice_text="3,456", defaults={'is_correct': False, 'order': 3})
    AnswerChoice.objects.get_or_create(question=question2, choice_text="7,893", defaults={'is_correct': False, 'order': 4})
    
    print("  Mathematics content added successfully!")
    return True

def add_science_content():
    """Add questions and notes for Science"""
    print("Adding Science content...")
    
    try:
        subject = Subject.objects.get(name="Science")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
    except:
        print("  ERROR: Science subject or class level not found!")
        return False
    
    # Living Things and Their Environment
    topic = Topic.objects.get(title="Living Things and Their Environment", class_level=class_level)
    
    # Add study note
    StudyNote.objects.get_or_create(
        topic=topic,
        title="Ecosystems and Habitats",
        defaults={
            'content': """An ecosystem is a community of living things and their environment working together.

**Parts of an Ecosystem:**

1. **Living Things (Biotic):**
   - Plants (producers) - make their own food using sunlight
   - Animals (consumers) - eat plants or other animals
   - Decomposers - break down dead things (bacteria, fungi)

2. **Non-living Things (Abiotic):**
   - Water, air, soil, sunlight, temperature

**Types of Ecosystems:**
- **Forest:** Trees, animals, rich soil
- **Ocean:** Fish, seaweed, salt water
- **Desert:** Cacti, lizards, very little water
- **Grassland:** Grass, grazing animals

**Food Chain Example:**
Grass → Rabbit → Fox → Decomposers

**Example:** In a pond ecosystem:
- Plants: Water lilies, algae
- Animals: Fish, frogs, ducks
- Non-living: Water, sunlight, rocks""",
            'order': 1
        }
    )
    
    # Add questions
    question1 = Question.objects.get_or_create(
        topic=topic,
        question_text="What do we call the non-living parts of an ecosystem?",
        question_type="multiple_choice",
        defaults={'order': 1, 'time_limit': 45}
    )[0]
    
    AnswerChoice.objects.get_or_create(question=question1, choice_text="Biotic", defaults={'is_correct': False, 'order': 1})
    AnswerChoice.objects.get_or_create(question=question1, choice_text="Abiotic", defaults={'is_correct': True, 'order': 2})
    AnswerChoice.objects.get_or_create(question=question1, choice_text="Producers", defaults={'is_correct': False, 'order': 3})
    AnswerChoice.objects.get_or_create(question=question1, choice_text="Consumers", defaults={'is_correct': False, 'order': 4})
    
    print("  Science content added successfully!")
    return True

def main():
    """Add content to all Grade 5 subjects"""
    print("ADDING GRADE 5 QUESTIONS AND STUDY NOTES")
    print("=" * 50)
    
    subjects = [
        ("English Language Arts", add_english_content),
        ("Mathematics", add_mathematics_content),
        ("Science", add_science_content),
    ]
    
    success_count = 0
    
    for subject_name, add_func in subjects:
        try:
            if add_func():
                success_count += 1
            else:
                print(f"  FAILED: {subject_name}")
        except Exception as e:
            print(f"  ERROR in {subject_name}: {str(e)}")
    
    print(f"\nSUMMARY:")
    print(f"Subjects with content added: {success_count}/{len(subjects)}")
    
    if success_count == len(subjects):
        print("SUCCESS: All content added successfully!")
    else:
        print("Some subjects failed. Check errors above.")

if __name__ == '__main__':
    main()
