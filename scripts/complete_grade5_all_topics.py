#!/usr/bin/env python
"""
Complete Grade 5 Content for ALL Topics
Adds comprehensive real-life questions and study notes to every topic
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

def add_content_to_topic(topic, note_title, note_content, questions_data):
    """Helper function to add content to any topic"""
    # Add study note
    note, created = StudyNote.objects.get_or_create(
        topic=topic,
        title=note_title,
        defaults={
            'content': note_content,
            'order': 1
        }
    )
    if created:
        print(f"    Added note: {note_title}")
    
    # Add questions
    for i, q_data in enumerate(questions_data):
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
            print(f"    Added question: {q_data['question_text'][:50]}...")
            
            # Add answer choices
            for j, choice_data in enumerate(q_data['choices']):
                AnswerChoice.objects.create(
                    question=question,
                    choice_text=choice_data['text'],
                    is_correct=choice_data['is_correct'],
                    order=j + 1
                )

def add_all_english_content():
    """Add content to ALL English Language Arts topics"""
    print("Adding content to ALL English Language Arts topics...")
    
    try:
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topics = Topic.objects.filter(class_level=class_level).order_by('order')
    except:
        print("  ERROR: English subject not found!")
        return 0
    
    content_map = {
        'Grammar and Sentence Structure': {
            'note_title': 'Grammar Rules for Better Writing',
            'note_content': """# Grammar and Sentence Structure

## Parts of Speech

### Nouns
Words that name people, places, things, or ideas.
- **Person:** teacher, doctor, Maria
- **Place:** school, park, library  
- **Thing:** book, computer, bicycle
- **Idea:** happiness, freedom, love

### Verbs
Action words or words that show being.
- **Action verbs:** run, jump, write, think
- **Being verbs:** is, are, was, were, am

### Adjectives
Words that describe nouns.
- **Size:** big, small, tiny, huge
- **Color:** red, blue, green, purple
- **Feeling:** happy, sad, excited, angry

### Adverbs
Words that describe verbs, adjectives, or other adverbs.
- **How:** quickly, slowly, carefully, loudly
- **When:** yesterday, today, soon, never
- **Where:** here, there, everywhere, outside

## Sentence Types

### Complete Sentences
Every sentence needs:
1. **Subject:** Who or what the sentence is about
2. **Predicate:** What the subject does or is

**Examples:**
- The dog (subject) barked loudly (predicate).
- My sister (subject) loves reading (predicate).

### Types by Purpose
1. **Statement:** The sky is blue.
2. **Question:** What time is it?
3. **Command:** Please close the door.
4. **Exclamation:** What a beautiful day!

## Real-Life Grammar Tips
- Read your writing out loud to catch mistakes
- Use spell check, but also learn the rules
- Practice writing different types of sentences
- Ask someone to read your work and give feedback""",
            'questions': [
                {
                    'question_text': 'In the sentence "The excited students quickly finished their homework," what part of speech is "quickly"?',
                    'choices': [
                        {'text': 'Noun', 'is_correct': False},
                        {'text': 'Verb', 'is_correct': False},
                        {'text': 'Adjective', 'is_correct': False},
                        {'text': 'Adverb', 'is_correct': True}
                    ],
                    'explanation': '"Quickly" is an adverb because it describes HOW the students finished their homework. Adverbs often end in -ly and describe verbs.'
                },
                {
                    'question_text': 'Which sentence is a complete sentence?',
                    'choices': [
                        {'text': 'Running in the park.', 'is_correct': False},
                        {'text': 'The beautiful flowers.', 'is_correct': False},
                        {'text': 'My dog loves to play fetch.', 'is_correct': True},
                        {'text': 'After the game ended.', 'is_correct': False}
                    ],
                    'explanation': '"My dog loves to play fetch" has both a subject (my dog) and a predicate (loves to play fetch). The other options are sentence fragments.'
                }
            ]
        },
        'Writing Skills': {
            'note_title': 'Becoming a Better Writer',
            'note_content': """# Writing Skills

## Types of Writing

### Narrative Writing (Telling Stories)
- Has characters, setting, and plot
- Uses descriptive words to paint pictures
- Has a beginning, middle, and end
- **Example:** Writing about your summer vacation

### Informative Writing (Teaching Others)
- Explains facts or teaches something
- Uses clear, simple language
- Organized with main ideas and details
- **Example:** How to make a peanut butter sandwich

### Opinion Writing (Persuading Others)
- States your opinion clearly
- Gives reasons to support your opinion
- Uses facts and examples
- **Example:** Why students should have longer recess

## The Writing Process

### 1. Planning (Prewriting)
- Think about your topic
- Make a list of ideas
- Organize your thoughts

### 2. Drafting
- Write your first version
- Don't worry about perfect spelling yet
- Focus on getting your ideas down

### 3. Revising
- Read your writing out loud
- Add more details
- Move sentences around if needed
- Make sure it makes sense

### 4. Editing
- Check spelling and grammar
- Fix punctuation
- Make sure sentences are complete

### 5. Publishing
- Write or type your final copy
- Share it with others

## Writing Tips for Real Life
- **Keep a journal:** Write about your day
- **Write letters:** To family members or friends
- **Make lists:** Shopping lists, to-do lists
- **Write instructions:** Teach someone how to do something
- **Write reviews:** About books, movies, or games you like""",
            'questions': [
                {
                    'question_text': 'You want to convince your parents to let you have a pet. What type of writing should you use?',
                    'choices': [
                        {'text': 'Narrative writing', 'is_correct': False},
                        {'text': 'Informative writing', 'is_correct': False},
                        {'text': 'Opinion writing', 'is_correct': True},
                        {'text': 'Poetry writing', 'is_correct': False}
                    ],
                    'explanation': 'Opinion writing is used to persuade others. You would state your opinion (I should have a pet) and give reasons to support it.'
                },
                {
                    'question_text': 'During which step of the writing process should you focus on fixing spelling and grammar mistakes?',
                    'choices': [
                        {'text': 'Planning', 'is_correct': False},
                        {'text': 'Drafting', 'is_correct': False},
                        {'text': 'Revising', 'is_correct': False},
                        {'text': 'Editing', 'is_correct': True}
                    ],
                    'explanation': 'Editing is when you fix spelling, grammar, and punctuation. During drafting and revising, you focus on ideas and organization first.'
                }
            ]
        }
    }
    
    topics_updated = 0
    for topic in topics:
        if topic.title in content_map:
            data = content_map[topic.title]
            add_content_to_topic(topic, data['note_title'], data['note_content'], data['questions'])
            topics_updated += 1
        else:
            print(f"  Skipping {topic.title} (content already exists or not in map)")
    
    print(f"  English Language Arts: {topics_updated} additional topics updated")
    return topics_updated

def add_all_mathematics_content():
    """Add content to ALL Mathematics topics"""
    print("Adding content to ALL Mathematics topics...")
    
    try:
        subject = Subject.objects.get(name="Mathematics")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topics = Topic.objects.filter(class_level=class_level).order_by('order')
    except:
        print("  ERROR: Mathematics subject not found!")
        return 0
    
    content_map = {
        'Fractions': {
            'note_title': 'Understanding Fractions in Real Life',
            'note_content': """# Fractions

## What are Fractions?
Fractions represent parts of a whole. They show how many equal parts you have out of the total.

## Parts of a Fraction
- **Numerator:** Top number (how many parts you have)
- **Denominator:** Bottom number (total number of equal parts)

Example: 3/4
- 3 is the numerator (you have 3 parts)
- 4 is the denominator (there are 4 total parts)

## Real-Life Fraction Examples

### Pizza Fractions
- You order a pizza cut into 8 slices
- You eat 3 slices
- You ate 3/8 of the pizza
- 5/8 of the pizza is left

### Time Fractions
- 1/2 hour = 30 minutes
- 1/4 hour = 15 minutes  
- 3/4 hour = 45 minutes

### Money Fractions
- 1/4 of a dollar = 25 cents (quarter)
- 1/2 of a dollar = 50 cents
- 3/4 of a dollar = 75 cents

### Sports Fractions
- A basketball player makes 7 out of 10 free throws
- That's 7/10 or 70% success rate

## Equivalent Fractions
Different fractions that represent the same amount:
- 1/2 = 2/4 = 4/8 = 8/16
- 1/3 = 2/6 = 3/9 = 4/12

## Comparing Fractions
- Same denominator: Compare numerators (3/8 < 5/8)
- Different denominators: Find common denominators first

## Adding and Subtracting Fractions
- Same denominator: Add/subtract numerators, keep denominator
- 2/5 + 1/5 = 3/5
- 4/7 - 2/7 = 2/7""",
            'questions': [
                {
                    'question_text': 'You and your friends order a pizza cut into 12 slices. If you eat 4 slices, what fraction of the pizza did you eat?',
                    'choices': [
                        {'text': '4/8', 'is_correct': False},
                        {'text': '4/12', 'is_correct': True},
                        {'text': '8/12', 'is_correct': False},
                        {'text': '12/4', 'is_correct': False}
                    ],
                    'explanation': 'You ate 4 slices out of 12 total slices, so you ate 4/12 of the pizza. This can also be simplified to 1/3.'
                },
                {
                    'question_text': 'Your soccer practice lasts 3/4 of an hour. How many minutes is that?',
                    'choices': [
                        {'text': '30 minutes', 'is_correct': False},
                        {'text': '45 minutes', 'is_correct': True},
                        {'text': '60 minutes', 'is_correct': False},
                        {'text': '75 minutes', 'is_correct': False}
                    ],
                    'explanation': '3/4 of an hour means 3/4 × 60 minutes = 45 minutes. This is a common real-life use of fractions with time.'
                }
            ]
        }
    }
    
    topics_updated = 0
    for topic in topics:
        if topic.title in content_map:
            data = content_map[topic.title]
            add_content_to_topic(topic, data['note_title'], data['note_content'], data['questions'])
            topics_updated += 1
        else:
            print(f"  Skipping {topic.title} (content already exists or not in map)")
    
    print(f"  Mathematics: {topics_updated} additional topics updated")
    return topics_updated

def main():
    """Add comprehensive content to ALL Grade 5 topics"""
    print("COMPLETE GRADE 5 CONTENT FOR ALL TOPICS")
    print("=" * 50)
    print("Adding real-life content to remaining topics...")
    print("=" * 50)
    
    total_topics_updated = 0
    
    # Add content to remaining English topics
    total_topics_updated += add_all_english_content()
    
    # Add content to remaining Mathematics topics  
    total_topics_updated += add_all_mathematics_content()
    
    print(f"\nSUMMARY:")
    print(f"Additional topics updated: {total_topics_updated}")
    print("Run this after the main comprehensive scripts!")

if __name__ == '__main__':
    main()
