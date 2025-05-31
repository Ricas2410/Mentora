#!/usr/bin/env python
"""
Comprehensive Grade 5 English Language Arts Content Population Script
Creates detailed study notes and quiz questions for all English topics
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

def create_english_content():
    """Create comprehensive Grade 5 English Language Arts content"""
    print("📚 Creating Grade 5 English Language Arts Content...")
    
    # Get English Language Arts subject and Grade 5 level
    try:
        english_subject = Subject.objects.get(name="English Language Arts")
        grade5_english = ClassLevel.objects.get(subject=english_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ English Language Arts subject or Grade 5 level not found!")
        return
    
    # English Language Arts topics for Grade 5
    topics_data = [
        {
            'title': 'Reading Comprehension',
            'description': 'Understanding and analyzing what you read',
            'order': 1
        },
        {
            'title': 'Vocabulary and Word Study',
            'description': 'Learning new words and their meanings',
            'order': 2
        },
        {
            'title': 'Grammar and Sentence Structure',
            'description': 'Parts of speech, sentence types, and proper grammar',
            'order': 3
        },
        {
            'title': 'Writing Skills',
            'description': 'Different types of writing and composition techniques',
            'order': 4
        },
        {
            'title': 'Spelling and Phonics',
            'description': 'Spelling patterns, rules, and sound-letter relationships',
            'order': 5
        },
        {
            'title': 'Literature and Poetry',
            'description': 'Understanding stories, poems, and literary elements',
            'order': 6
        },
        {
            'title': 'Speaking and Listening',
            'description': 'Communication skills and presentation techniques',
            'order': 7
        },
        {
            'title': 'Research and Information',
            'description': 'Finding, evaluating, and using information sources',
            'order': 8
        }
    ]
    
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            title=topic_data['title'],
            class_level=grade5_english,
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Created topic: {topic.title}")
            create_study_notes(topic)
            create_quiz_questions(topic)
        else:
            print(f"📝 Topic already exists: {topic.title}")

def create_study_notes(topic):
    """Create comprehensive study notes for each topic"""
    
    study_notes_data = {
        'Reading Comprehension': {
            'title': 'Understanding What You Read',
            'content': '''
# Reading Comprehension

## What is Reading Comprehension?
Reading comprehension is the ability to understand, remember, and think about what you read. It's not just reading the words, but understanding the meaning and message.

## Reading Strategies

### Before Reading
**Preview the Text:**
- Look at the title, headings, and pictures
- Think about what you already know about the topic
- Predict what the text might be about
- Set a purpose for reading

### During Reading
**Active Reading Strategies:**
- Ask questions as you read
- Make connections to your own life
- Visualize (create pictures in your mind)
- Make predictions about what will happen next
- Stop and summarize what you've read

### After Reading
**Reflect and Review:**
- Summarize the main ideas
- Think about what you learned
- Ask questions about confusing parts
- Connect the reading to other texts or experiences

## Types of Questions

### Literal Questions (Right There)
- Answers are directly stated in the text
- Example: "What color was the dog?"

### Inferential Questions (Think and Search)
- Answers require you to put clues together
- Example: "How do you think the character felt?"

### Critical Thinking Questions (On Your Own)
- Answers come from your own knowledge and opinions
- Example: "Do you agree with the character's decision? Why?"

## Text Features
Understanding different parts of texts helps comprehension:

### Fiction Text Features:
- **Characters:** People or animals in the story
- **Setting:** When and where the story takes place
- **Plot:** What happens in the story (beginning, middle, end)
- **Theme:** The main message or lesson

### Non-fiction Text Features:
- **Headings:** Tell you what each section is about
- **Captions:** Explain pictures and diagrams
- **Bold words:** Important vocabulary
- **Charts and graphs:** Show information visually
- **Index:** Helps you find specific topics

## Main Idea and Supporting Details

### Finding the Main Idea:
- What is the text mostly about?
- What is the most important point?
- Often found in the first or last sentence of a paragraph

### Supporting Details:
- Facts, examples, or reasons that support the main idea
- Answer questions like who, what, when, where, why, how

**Example:**
**Main Idea:** Dogs make great pets.
**Supporting Details:** 
- They are loyal and friendly
- They can be trained to follow commands
- They provide companionship and protection

## Making Connections

### Text-to-Self:
- How does this remind you of your own life?
- "This reminds me of when I..."

### Text-to-Text:
- How does this connect to other books you've read?
- "This is similar to another story because..."

### Text-to-World:
- How does this connect to the real world?
- "This reminds me of something I saw on the news..."

## Reading Different Genres

### Fiction:
- Stories that are made up
- Includes novels, short stories, fairy tales

### Non-fiction:
- True information about real people, places, events
- Includes biographies, science books, history books

### Poetry:
- Uses rhythm, rhyme, and imagery
- Expresses feelings and ideas in creative ways

### Drama:
- Stories written to be performed
- Includes plays and scripts

## Improving Reading Comprehension

### Tips for Better Understanding:
1. Read regularly (at least 20 minutes per day)
2. Choose books at your reading level
3. Discuss what you read with others
4. Keep a reading journal
5. Re-read difficult parts
6. Look up unfamiliar words
7. Take breaks when you get tired
'''
        },
        
        'Grammar and Sentence Structure': {
            'title': 'Building Strong Sentences',
            'content': '''
# Grammar and Sentence Structure

## Parts of Speech

### Nouns
**Definition:** Words that name people, places, things, or ideas

**Types of Nouns:**
- **Common nouns:** general names (dog, city, book)
- **Proper nouns:** specific names (Rover, New York, Harry Potter)
- **Singular nouns:** one thing (cat)
- **Plural nouns:** more than one (cats)

**Examples:**
- Person: teacher, student, doctor
- Place: school, park, library
- Thing: pencil, computer, car
- Idea: happiness, freedom, love

### Verbs
**Definition:** Words that show action or state of being

**Types of Verbs:**
- **Action verbs:** show what someone does (run, jump, think)
- **Linking verbs:** connect the subject to more information (is, are, was, were)
- **Helping verbs:** work with main verbs (will, have, can, should)

**Verb Tenses:**
- **Present:** I walk to school every day
- **Past:** I walked to school yesterday
- **Future:** I will walk to school tomorrow

### Adjectives
**Definition:** Words that describe nouns

**Examples:**
- Size: big, small, tiny, huge
- Color: red, blue, green, yellow
- Shape: round, square, long, short
- Feeling: happy, sad, excited, tired

**Example Sentences:**
- The **big** dog ran quickly.
- She wore a **beautiful** dress.
- The **old** book had **yellow** pages.

### Adverbs
**Definition:** Words that describe verbs, adjectives, or other adverbs

**Many adverbs end in -ly:**
- quickly, slowly, carefully, loudly

**Examples:**
- She ran **quickly** to catch the bus.
- The music played **loudly**.
- He **carefully** painted the picture.

## Sentence Structure

### Complete Sentences
Every complete sentence needs:
1. **Subject:** Who or what the sentence is about
2. **Predicate:** What the subject does or is

**Examples:**
- **The dog** (subject) **barked loudly** (predicate).
- **My sister** (subject) **loves to read** (predicate).

### Types of Sentences

#### By Purpose:
1. **Declarative:** Makes a statement (ends with .)
   - "The sky is blue."

2. **Interrogative:** Asks a question (ends with ?)
   - "What time is it?"

3. **Imperative:** Gives a command (ends with . or !)
   - "Please close the door."

4. **Exclamatory:** Shows strong emotion (ends with !)
   - "What a beautiful day!"

#### By Structure:
1. **Simple:** One independent clause
   - "I like pizza."

2. **Compound:** Two independent clauses joined by a conjunction
   - "I like pizza, but my sister prefers pasta."

3. **Complex:** One independent clause and one dependent clause
   - "Because it was raining, we stayed inside."

## Punctuation Rules

### Period (.)
- End of declarative sentences
- After abbreviations (Dr., Mrs., etc.)

### Question Mark (?)
- End of interrogative sentences
- "Where are you going?"

### Exclamation Point (!)
- End of exclamatory sentences
- Shows strong emotion
- "Watch out!"

### Comma (,)
- Separate items in a list
- Before conjunctions in compound sentences
- After introductory words
- Around extra information

### Apostrophe (')
- Show possession (Sarah's book)
- Contractions (don't, can't, won't)

## Common Grammar Mistakes

### Subject-Verb Agreement
- Singular subjects need singular verbs
- Plural subjects need plural verbs

**Correct:** The dog runs fast.
**Incorrect:** The dog run fast.

### Pronoun Usage
- Use the correct pronoun case

**Correct:** She and I went to the store.
**Incorrect:** Her and me went to the store.

### Double Negatives
- Don't use two negative words together

**Correct:** I don't have any money.
**Incorrect:** I don't have no money.
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
        'Reading Comprehension': [
            {
                'question_text': 'What should you do BEFORE you start reading a new text?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Read as fast as possible', 'is_correct': False},
                    {'text': 'Preview the title and headings', 'is_correct': True},
                    {'text': 'Skip to the end', 'is_correct': False},
                    {'text': 'Read every word carefully', 'is_correct': False}
                ],
                'explanation': 'Previewing the text by looking at titles, headings, and pictures helps you prepare for reading and understand the content better.'
            },
            {
                'question_text': 'What is the main idea of a paragraph?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'The first sentence', 'is_correct': False},
                    {'text': 'The most important point', 'is_correct': True},
                    {'text': 'The longest sentence', 'is_correct': False},
                    {'text': 'The last sentence', 'is_correct': False}
                ],
                'explanation': 'The main idea is the most important point or what the paragraph is mostly about. It can be found anywhere in the paragraph.'
            }
        ],
        
        'Grammar and Sentence Structure': [
            {
                'question_text': 'Which word is a proper noun?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'dog', 'is_correct': False},
                    {'text': 'city', 'is_correct': False},
                    {'text': 'London', 'is_correct': True},
                    {'text': 'book', 'is_correct': False}
                ],
                'explanation': 'London is a proper noun because it names a specific place. Proper nouns are always capitalized.'
            },
            {
                'question_text': 'What type of sentence is this: "Please pass the salt."',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Declarative', 'is_correct': False},
                    {'text': 'Interrogative', 'is_correct': False},
                    {'text': 'Imperative', 'is_correct': True},
                    {'text': 'Exclamatory', 'is_correct': False}
                ],
                'explanation': 'This is an imperative sentence because it gives a command or makes a request.'
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
    create_english_content()
    print("✅ Grade 5 English Language Arts content creation completed!")
