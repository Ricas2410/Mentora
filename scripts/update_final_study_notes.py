#!/usr/bin/env python3
"""
Script to update final Grade 5 English study notes with comprehensive content
Grammar: Nouns and Phonics
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
from users.models import User
from django.db import transaction

def update_grammar_nouns_notes(topic, admin_user):
    """Update Grammar: Nouns study notes with comprehensive content"""
    content = """# Understanding Nouns

## What Are Nouns?
Nouns are words that name people, places, things, or ideas. They are the "naming words" in our language.

**Examples:**
- **People:** teacher, doctor, Sarah, mother
- **Places:** school, park, London, kitchen
- **Things:** book, car, apple, computer
- **Ideas:** happiness, freedom, love, courage

## Types of Nouns

### 1. Common Nouns
Name general people, places, or things (not capitalized unless at the beginning of a sentence).

**Examples:**
- dog, city, book, teacher, car, house

**In sentences:**
- The dog barked loudly.
- We visited a beautiful city.
- She read an interesting book.

### 2. Proper Nouns
Name specific people, places, or things (always capitalized).

**Examples:**
- **People:** Sarah, Dr. Smith, President Lincoln
- **Places:** New York, Africa, Main Street
- **Things:** Coca-Cola, iPhone, Monday

**In sentences:**
- Sarah lives in New York.
- We visited the Statue of Liberty.
- My birthday is on Monday.

### 3. Concrete Nouns
Name things you can see, touch, hear, smell, or taste.

**Examples:**
- apple (taste, see, touch)
- music (hear)
- flower (see, smell)
- ice (touch, see)

### 4. Abstract Nouns
Name ideas, feelings, or qualities you cannot touch.

**Examples:**
- happiness, sadness, anger
- love, friendship, kindness
- courage, honesty, wisdom
- freedom, justice, peace

**In sentences:**
- Her happiness was contagious.
- Courage helped him face his fears.
- Friendship is very important.

### 5. Collective Nouns
Name groups of people, animals, or things.

**Examples:**
- **People:** team, family, class, crowd
- **Animals:** flock (birds), herd (cattle), pack (wolves)
- **Things:** bunch (grapes), stack (books)

**In sentences:**
- The team won the championship.
- A flock of birds flew overhead.
- Our family went on vacation.

### 6. Compound Nouns
Made by combining two or more words.

**Written as one word:**
- classroom, basketball, toothbrush, sunlight

**Written as separate words:**
- ice cream, high school, post office

**Written with hyphens:**
- mother-in-law, merry-go-round, six-year-old

## Singular and Plural Nouns

### Regular Plurals
Most nouns add -s or -es to form plurals.

#### Add -s:
- cat → cats
- book → books
- car → cars

#### Add -es (words ending in s, x, z, ch, sh):
- box → boxes
- church → churches
- dish → dishes
- bus → buses

#### Words ending in consonant + y:
Change y to i and add -es
- baby → babies
- city → cities
- story → stories

#### Words ending in vowel + y:
Just add -s
- boy → boys
- day → days
- key → keys

#### Words ending in f or fe:
Change f/fe to v and add -es
- leaf → leaves
- knife → knives
- wolf → wolves

### Irregular Plurals
Some nouns change completely or stay the same.

**Complete changes:**
- child → children
- man → men
- woman → women
- foot → feet
- tooth → teeth
- mouse → mice
- goose → geese

**Same form for singular and plural:**
- sheep → sheep
- deer → deer
- fish → fish
- moose → moose

## Possessive Nouns
Show ownership or belonging.

### Singular Possessive
Add apostrophe + s ('s)
- The cat's toy (the toy belongs to the cat)
- Sarah's book (the book belongs to Sarah)
- The teacher's desk (the desk belongs to the teacher)

### Plural Possessive

#### If plural ends in -s:
Add only an apostrophe (')
- The cats' toys (toys belong to multiple cats)
- The teachers' meeting (meeting for multiple teachers)
- The students' projects (projects by multiple students)

#### If plural doesn't end in -s:
Add apostrophe + s ('s)
- The children's playground
- The men's room
- The women's club

## Nouns as Different Parts of Speech

### Subject
The noun that does the action
- **The dog** barked.
- **Sarah** runs fast.
- **Books** are educational.

### Direct Object
The noun that receives the action
- I read **a book**.
- She ate **an apple**.
- We saw **the movie**.

### Indirect Object
The noun that tells to whom or for whom
- I gave **Sarah** a gift. (Sarah is the indirect object)
- Mom made **us** dinner. (us is the indirect object)

### Object of Preposition
The noun that follows a preposition
- The cat is under **the table**.
- We walked through **the park**.
- She put the book on **the shelf**.

## Countable vs. Uncountable Nouns

### Countable Nouns
Can be counted and have plural forms
- one book, two books, three books
- one apple, five apples
- one student, twenty students

**Use with:** a/an, many, few, several, numbers

### Uncountable Nouns
Cannot be counted individually
- water, milk, sugar, rice
- happiness, music, information
- furniture, homework, advice

**Use with:** much, little, some, any
**Don't use with:** a/an, numbers, many

## Gender in Nouns
Some nouns show gender differences:

**Male/Female pairs:**
- actor/actress
- king/queen
- brother/sister
- uncle/aunt
- grandfather/grandmother

**Neutral nouns (same for male/female):**
- teacher, doctor, student, friend, cousin

## Real-Life Applications

### Academic Writing
- **Proper capitalization** of proper nouns
- **Correct plurals** in research and reports
- **Clear subjects and objects** in sentences

### Daily Communication
- **Describing people and places** accurately
- **Showing ownership** with possessives
- **Counting and measuring** with appropriate nouns

### Creative Writing
- **Specific nouns** make writing more interesting
- **Collective nouns** add variety
- **Abstract nouns** express emotions and ideas

## Common Mistakes to Avoid

### 1. Capitalization Errors
**Wrong:** I live in new york city.
**Right:** I live in New York City.

### 2. Incorrect Plurals
**Wrong:** I have two childs.
**Right:** I have two children.

### 3. Possessive Confusion
**Wrong:** The dogs toy is red.
**Right:** The dog's toy is red.

### 4. Its vs. It's
**Wrong:** The dog wagged it's tail.
**Right:** The dog wagged its tail. (possessive)
**Right:** It's raining outside. (it is)

## Practice Activities

### 1. Noun Hunts
Find different types of nouns in books, magazines, or around your environment.

### 2. Sorting Games
Sort nouns into categories: people, places, things, ideas.

### 3. Plural Practice
Practice making singular nouns plural, especially irregular ones.

### 4. Possessive Practice
Write sentences showing ownership using possessive nouns.

### 5. Writing Exercises
Write descriptive paragraphs using various types of nouns.

## Memory Tips

### For Irregular Plurals:
Create silly sentences:
- "The children's feet hurt from chasing geese and mice."

### For Possessives:
Remember: If it belongs to someone, use an apostrophe.

### For Proper Nouns:
Think "special names get capital letters."

## Fun Facts About Nouns

1. **Most common noun in English:** "time"
2. **Longest noun:** "pneumonoultramicroscopicsilicovolcanoconiosiss" (a lung disease)
3. **Collective noun variety:** English has many creative collective nouns like "a murder of crows" or "a pride of lions"

Remember: Nouns are the building blocks of sentences - they tell us who or what the sentence is about!"""

    # Update or create the study note
    study_note, created = StudyNote.objects.update_or_create(
        topic=topic,
        title="Understanding Nouns - Complete Guide",
        defaults={
            'content': content,
            'order': 1,
            'is_active': True,
            'created_by': admin_user
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"    {action} comprehensive study note for Grammar: Nouns")

def update_phonics_notes(topic, admin_user):
    """Update Phonics study notes with comprehensive content"""
    content = """# Phonics Fundamentals

## What is Phonics?
Phonics is the relationship between letters (graphemes) and sounds (phonemes). It helps us:
- **Decode** unfamiliar words when reading
- **Spell** words correctly when writing
- **Pronounce** new words properly
- **Build vocabulary** through word patterns

Think of phonics as the "code" that connects written letters to spoken sounds!

## The Building Blocks of Phonics

### Phonemes
The smallest units of sound in language
- English has about 44 phonemes
- Examples: /b/, /a/, /t/ in "bat"
- Some phonemes are made by one letter, others by letter combinations

### Graphemes
The written symbols (letters) that represent phonemes
- Single letters: b, a, t
- Letter combinations: ch, sh, th, ck

### Syllables
Units of sound that contain one vowel sound
- cat (1 syllable)
- happy (2 syllables: hap-py)
- elephant (3 syllables: el-e-phant)

## Vowel Sounds

### Short Vowels
**a** as in cat, hat, map
**e** as in bed, red, pen
**i** as in sit, big, win
**o** as in hot, dog, box
**u** as in cup, run, bus

**Memory tip:** "The cat sat on the red bed with a big dog in a hot cup."

### Long Vowels
Sound like the letter name:
**a** as in cake, rain, play
**e** as in bee, feet, eat
**i** as in bike, light, fly
**o** as in boat, snow, go
**u** as in cute, blue, few

### Vowel Teams
Two vowels that work together to make one sound:
- **ai/ay:** rain, play
- **ea/ee:** eat, bee
- **oa/ow:** boat, snow
- **oo:** book (short), moon (long)
- **ou/ow:** house, cow

### R-Controlled Vowels
When 'r' follows a vowel, it changes the sound:
- **ar:** car, star, park
- **er:** her, fern, bird
- **ir:** girl, first, shirt
- **or:** for, corn, short
- **ur:** turn, hurt, nurse

## Consonant Sounds

### Single Consonants
Most consonants make one sound:
- b, c, d, f, g, h, j, k, l, m, n, p, q, r, s, t, v, w, x, y, z

### Consonant Digraphs
Two consonants that make one new sound:
- **ch:** chair, much, lunch
- **sh:** ship, fish, wish
- **th:** think, bath (voiceless) / this, with (voiced)
- **wh:** when, where, what
- **ph:** phone, graph (sounds like /f/)
- **ck:** back, duck, rock (sounds like /k/)

### Consonant Blends
Two or more consonants where you hear each sound:
- **Beginning blends:** bl (blue), cr (crab), st (stop), tr (tree)
- **Ending blends:** nd (hand), st (fast), mp (jump)

## Silent Letters
Letters that are written but not pronounced:
- **Silent b:** lamb, thumb, climb
- **Silent k:** knee, knife, know
- **Silent l:** half, walk, talk
- **Silent w:** write, wrong, wrist
- **Silent t:** castle, listen, Christmas

## Word Patterns

### CVC Pattern (Consonant-Vowel-Consonant)
Usually has short vowel sounds:
- cat, dog, run, sit, pen

### CVCe Pattern (Magic E)
The 'e' at the end makes the vowel say its name:
- cake (a says "ay")
- bike (i says "eye")
- cute (u says "you")

### CVVC Pattern
Two vowels in the middle:
- rain, boat, feet, coat

## Syllable Types

### 1. Closed Syllables
End with a consonant, vowel is usually short:
- cat, run, basket (bas-ket)

### 2. Open Syllables
End with a vowel, vowel is usually long:
- go, me, baby (ba-by)

### 3. Magic E Syllables
End with consonant + e, first vowel is long:
- cake, bike, home

### 4. Vowel Team Syllables
Contain vowel teams:
- rain, boat, play

### 5. R-Controlled Syllables
Contain r-controlled vowels:
- car, bird, turn

### 6. Consonant + LE Syllables
End with consonant + le:
- table (ta-ble), purple (pur-ple)

## Decoding Strategies

### 1. Sound It Out
Break the word into individual sounds:
- c-a-t = cat
- s-t-o-p = stop

### 2. Look for Patterns
Recognize common letter patterns:
- Words ending in -ing: running, jumping
- Words with -tion: action, nation

### 3. Chunk the Word
Break longer words into smaller parts:
- un-happy
- re-read
- basket-ball

### 4. Use Context Clues
Use the sentence to help figure out the word:
- "The cat climbed the tall ___." (tree)

## Spelling Rules

### 1. The "i before e" Rule
"i before e except after c, or when sounding like 'a' as in neighbor and weigh"
- believe, receive, eight, freight

### 2. Drop the E Rule
When adding a suffix that starts with a vowel, drop the silent e:
- make + ing = making
- hope + ed = hoped

### 3. Double the Consonant Rule
For one-syllable words ending in consonant-vowel-consonant, double the final consonant before adding a vowel suffix:
- run + ing = running
- big + er = bigger

### 4. Change Y to I Rule
When a word ends in consonant + y, change y to i before adding a suffix:
- happy + ness = happiness
- carry + ed = carried

## Common Phonics Patterns

### Word Families (Rimes)
Groups of words that end the same way:
- -at family: cat, bat, hat, rat
- -ight family: light, night, right, sight
- -ake family: cake, make, take, wake

### Prefixes
Word parts added to the beginning:
- un- (not): unhappy, undo
- re- (again): reread, replay
- pre- (before): preview, preschool

### Suffixes
Word parts added to the end:
- -ing (action): running, playing
- -ed (past): walked, jumped
- -er (person who): teacher, runner
- -ly (how): quickly, slowly

## Reading Fluency Tips

### 1. Practice Sight Words
Learn common words that don't follow phonics rules:
- the, was, said, come, some, one

### 2. Read Regularly
Practice makes perfect:
- Start with simple books
- Gradually increase difficulty
- Reread favorite books

### 3. Use Expression
Make reading sound like talking:
- Pay attention to punctuation
- Use different voices for characters
- Match tone to meaning

## Real-Life Applications

### Academic Success
- **Reading comprehension** improves with strong phonics
- **Spelling tests** become easier
- **Vocabulary growth** accelerates
- **Writing skills** develop naturally

### Communication Skills
- **Pronunciation** of new words
- **Confidence** in reading aloud
- **Understanding** of word relationships
- **Learning** other languages becomes easier

## Practice Activities

### 1. Word Sorts
Sort words by patterns:
- Short a vs. long a
- Words with 'ch' vs. 'sh'
- One syllable vs. two syllables

### 2. Rhyming Games
Find words that rhyme:
- What rhymes with "cat"?
- Make up silly rhyming sentences

### 3. Sound Hunts
Find objects that start with specific sounds:
- Things that start with /b/
- Things with the long 'e' sound

### 4. Word Building
Use letter tiles or cards to build words:
- Change one letter at a time: cat → bat → bit → sit

### 5. Reading Practice
Read books at your level:
- Decodable books for practice
- Favorite stories for enjoyment

## Technology Tools

### Apps and Websites
- Phonics games and activities
- Interactive word building
- Reading practice programs
- Pronunciation guides

### Traditional Tools
- Phonics workbooks
- Letter manipulatives
- Word cards
- Reading charts

Remember: Phonics is like learning to ride a bike - it takes practice, but once you get it, reading becomes much easier and more enjoyable!"""

    # Update or create the study note
    study_note, created = StudyNote.objects.update_or_create(
        topic=topic,
        title="Phonics Fundamentals - Complete Guide",
        defaults={
            'content': content,
            'order': 1,
            'is_active': True,
            'created_by': admin_user
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"    {action} comprehensive study note for Phonics")

def main():
    """Main function to update final study notes"""
    try:
        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No admin user found. Please create a superuser first.")
            return
        
        # Get Grade 5 English
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)
        
        print(f"📚 Updating final comprehensive study notes for Grade 5 English...")
        
        # Get topics
        topics = {
            'nouns': Topic.objects.get(class_level=grade5, title='Grammar: Nouns'),
            'phonics': Topic.objects.get(class_level=grade5, title='Phonics'),
        }
        
        # Update study notes for each topic
        update_grammar_nouns_notes(topics['nouns'], admin_user)
        update_phonics_notes(topics['phonics'], admin_user)
        
        print("✅ Successfully updated final comprehensive study notes!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
