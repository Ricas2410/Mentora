#!/usr/bin/env python3
"""
Script to add study notes to topics so the "Start Learning" buttons work
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

def add_study_notes():
    """Add study notes to topics"""
    try:
        english_subject = Subject.objects.get(name__icontains='English')
        grade_5 = ClassLevel.objects.get(subject=english_subject, level_number=5)
        admin_user = User.objects.filter(is_superuser=True).first()
        
        # Get topics
        tenses_topic = Topic.objects.get(class_level=grade_5, title='Grammar: Tenses')
        nouns_topic = Topic.objects.get(class_level=grade_5, title='Grammar: Nouns')
        phonics_topic = Topic.objects.get(class_level=grade_5, title='Phonics')
        
        # Tenses Study Note
        tenses_content = """
# Grammar: Tenses

## What are Tenses?

Tenses tell us **when** something happens. They help us understand if an action happened in the past, is happening now, or will happen in the future.

## The Three Main Tenses

### 1. Past Tense
- **When to use**: For actions that already happened
- **Examples**: 
  - I **walked** to school yesterday.
  - She **played** soccer last week.
  - They **visited** the museum.

### 2. Present Tense
- **When to use**: For actions happening now or regularly
- **Examples**:
  - I **walk** to school every day.
  - She **plays** soccer on weekends.
  - They **visit** museums often.

### 3. Future Tense
- **When to use**: For actions that will happen later
- **Examples**:
  - I **will walk** to school tomorrow.
  - She **will play** soccer next week.
  - They **will visit** the museum soon.

## Regular vs Irregular Verbs

### Regular Verbs
- Add **-ed** to make past tense
- Examples: walk → walked, play → played, visit → visited

### Irregular Verbs
- Change completely in past tense
- Examples: go → went, eat → ate, see → saw

## Practice Tips
1. Pay attention to time words (yesterday, now, tomorrow)
2. Remember regular verbs add -ed for past tense
3. Memorize common irregular verbs
4. Practice with real-life examples
"""

        tenses_note, created = StudyNote.objects.get_or_create(
            topic=tenses_topic,
            title="Understanding Tenses",
            defaults={
                'content': tenses_content,
                'order': 1,
                'is_active': True,
                'created_by': admin_user
            }
        )
        print(f"Tenses study note: {'created' if created else 'found'}")

        # Nouns Study Note
        nouns_content = """
# Grammar: Nouns

## What are Nouns?

Nouns are **naming words**. They name people, places, things, and ideas.

## Types of Nouns

### 1. Common Nouns
- General names for things
- **Examples**: dog, school, book, car
- **Not capitalized** (unless at start of sentence)

### 2. Proper Nouns
- Specific names of people, places, or things
- **Examples**: Sarah, London, McDonald's, Monday
- **Always capitalized**

### 3. Concrete Nouns
- Things you can see, touch, or experience with your senses
- **Examples**: apple, music, flower, rain

### 4. Abstract Nouns
- Ideas, feelings, or qualities you cannot touch
- **Examples**: happiness, love, courage, freedom

### 5. Collective Nouns
- Names for groups of people, animals, or things
- **Examples**: team, family, flock, herd

## Singular and Plural

### Regular Plurals
- Add **-s** to most nouns: cat → cats, book → books
- Add **-es** to nouns ending in s, x, z, ch, sh: box → boxes

### Irregular Plurals
- Some nouns change completely: child → children, mouse → mice
- Some stay the same: sheep → sheep, fish → fish

## Possessive Nouns
- Show ownership or belonging
- Add **'s** to singular nouns: Sarah's book
- Add **'** to plural nouns ending in s: students' desks
- Add **'s** to irregular plurals: children's toys

## Practice Tips
1. Look for naming words in sentences
2. Check if nouns are specific (proper) or general (common)
3. Practice making plurals
4. Remember to capitalize proper nouns
"""

        nouns_note, created = StudyNote.objects.get_or_create(
            topic=nouns_topic,
            title="Understanding Nouns",
            defaults={
                'content': nouns_content,
                'order': 1,
                'is_active': True,
                'created_by': admin_user
            }
        )
        print(f"Nouns study note: {'created' if created else 'found'}")

        # Phonics Study Note
        phonics_content = """
# Phonics: Sounds and Letters

## What is Phonics?

Phonics helps us understand the **relationship between letters and sounds**. It's the key to reading and spelling!

## Letter Sounds

### Consonants
- Most consonants make one sound: b, d, f, g, h, j, k, l, m, n, p, r, s, t, v, w, x, z
- Some have different sounds in different words: c (cat/city), g (go/gym)

### Vowels
- **Short vowel sounds**: a (cat), e (bed), i (sit), o (hot), u (cup)
- **Long vowel sounds**: a (cake), e (tree), i (bike), o (boat), u (cute)
- Long vowels "say their name"

## Special Letter Combinations

### Digraphs (Two letters, one sound)
- **ch**: chair, much
- **sh**: ship, fish
- **th**: think, that
- **ph**: phone, graph
- **wh**: when, what

### Blends (Two letters, two sounds)
- **Beginning blends**: bl (blue), cr (crab), st (stop)
- **Ending blends**: nd (hand), st (fast), mp (jump)

### Silent Letters
- **Silent e**: makes vowels long (cake, bike, hope)
- **Silent letters**: lamb (b), knee (k), write (w)

## Syllables

### What are syllables?
- Parts of words with one vowel sound
- Clap while saying words to count syllables

### Examples:
- **1 syllable**: cat, dog, tree
- **2 syllables**: ta-ble, hap-py, pen-cil
- **3 syllables**: el-e-phant, com-pu-ter

## Rhyming Words
- Words that end with the same sound
- **Examples**: cat/hat, night/light, play/day

## Practice Tips
1. Sound out words letter by letter
2. Look for patterns in word families
3. Practice with rhyming games
4. Read aloud to hear the sounds
5. Break long words into syllables
"""

        phonics_note, created = StudyNote.objects.get_or_create(
            topic=phonics_topic,
            title="Phonics Fundamentals",
            defaults={
                'content': phonics_content,
                'order': 1,
                'is_active': True,
                'created_by': admin_user
            }
        )
        print(f"Phonics study note: {'created' if created else 'found'}")

        print("\n✅ Study notes added successfully!")
        
    except Exception as e:
        print(f"❌ Error adding study notes: {e}")
        raise

if __name__ == '__main__':
    add_study_notes()
