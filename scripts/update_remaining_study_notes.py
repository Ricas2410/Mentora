#!/usr/bin/env python3
"""
Script to update remaining Grade 5 English study notes with comprehensive content
Poetry Analysis, Grammar: Tenses, Grammar: Nouns, and Phonics
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

def update_poetry_analysis_notes(topic, admin_user):
    """Update Poetry Analysis study notes with comprehensive content"""
    content = """# Understanding and Analyzing Poetry

## What is Poetry?
Poetry is a form of literature that uses language in special ways to express emotions, ideas, and experiences. Poets choose words carefully for their:
- **Sound** - How words sound when spoken
- **Meaning** - What words represent or symbolize
- **Rhythm** - The musical quality of language
- **Imagery** - Pictures created with words

## Elements of Poetry

### 1. Rhyme
Rhyme occurs when words have similar ending sounds.

#### Types of Rhyme:
- **Perfect rhyme:** Words that sound exactly the same (cat/hat, moon/June)
- **Near rhyme:** Words that almost rhyme (love/move, eye/high)
- **Internal rhyme:** Rhyming within a single line

#### Rhyme Schemes:
Letters represent the rhyme pattern:
- **AABB:** Roses are red (A), Violets are blue (B), Sugar is sweet (A), And so are you (B)
- **ABAB:** Twinkle, twinkle little star (A), How I wonder what you are (B), Up above the world so high (A), Like a diamond in the sky (B)

### 2. Rhythm and Meter
Rhythm is the beat or pattern of stressed and unstressed syllables.

**Example:** "Hickory dickory dock" (HIC-ko-ry DIC-ko-ry DOCK)
- Capital letters = stressed syllables
- Lowercase = unstressed syllables

### 3. Figurative Language

#### Simile
Compares two things using "like" or "as"
- Her voice is like music
- He runs as fast as lightning
- The clouds look like cotton balls

#### Metaphor
Compares two things by saying one IS the other
- Life is a journey
- Time is money
- The classroom was a zoo

#### Personification
Gives human qualities to non-human things
- The wind whispered through the trees
- The sun smiled down on us
- The flowers danced in the breeze

#### Alliteration
Repetition of beginning consonant sounds
- Peter Piper picked pickled peppers
- Sally sells seashells by the seashore
- Big brown bears

#### Onomatopoeia
Words that imitate sounds
- Buzz, hiss, crash, bang
- Meow, woof, chirp
- Sizzle, pop, whoosh

### 4. Imagery
Descriptive language that appeals to the five senses:
- **Sight:** Golden sunset, sparkling snow
- **Sound:** Thundering waterfall, gentle whisper
- **Touch:** Rough bark, silky fabric
- **Taste:** Sweet honey, bitter medicine
- **Smell:** Fresh bread, blooming roses

### 5. Mood and Tone
- **Mood:** The feeling the poem creates in the reader (happy, sad, mysterious, excited)
- **Tone:** The poet's attitude toward the subject (serious, playful, angry, loving)

## Types of Poetry

### 1. Narrative Poetry
Tells a story with characters, setting, and plot
**Example:** "The Raven" by Edgar Allan Poe

### 2. Lyric Poetry
Expresses personal feelings and emotions
**Example:** "I Wandered Lonely as a Cloud" by William Wordsworth

### 3. Free Verse
Poetry without regular rhyme or rhythm patterns
**Example:** Many modern poems

### 4. Haiku
Traditional Japanese poetry with three lines (5-7-5 syllables)
**Example:**
Cherry blossoms fall (5)
Gentle breeze carries petals (7)
Spring's beauty fades fast (5)

### 5. Limerick
Humorous five-line poem with AABBA rhyme scheme
**Example:**
There once was a cat from Peru (A)
Who dreamed of sailing canoe (A)
He packed up his fish (B)
Made a nautical wish (B)
And set sail when the morning was new (A)

## How to Analyze Poetry

### Step 1: Read the Poem Multiple Times
1. **First reading:** Get the general idea
2. **Second reading:** Look for literary devices
3. **Third reading:** Think about meaning and message

### Step 2: Identify the Speaker
- Who is telling the poem?
- What is their perspective?
- How do they feel about the subject?

### Step 3: Determine the Theme
What is the main message or lesson?
Common themes:
- Love and friendship
- Nature and seasons
- Growing up and change
- Dreams and hopes
- Loss and sadness

### Step 4: Analyze Literary Devices
- Find examples of figurative language
- Identify rhyme scheme and rhythm
- Notice imagery and sensory details
- Look for repetition and patterns

### Step 5: Consider the Structure
- How many stanzas?
- How many lines per stanza?
- Does the structure support the meaning?

## Reading Poetry Aloud

### Tips for Performance:
1. **Read slowly** - Poetry needs time to be appreciated
2. **Pay attention to punctuation** - Pause at commas, stop at periods
3. **Emphasize important words** - Stress key ideas
4. **Use your voice** - Match tone to mood
5. **Practice** - Read several times before performing

## Writing Your Own Poetry

### Getting Started:
1. **Choose a topic** you care about
2. **Brainstorm words** related to your topic
3. **Think about emotions** you want to express
4. **Decide on a form** (free verse, rhyming, haiku)

### Writing Tips:
1. **Show, don't tell** - Use imagery instead of stating facts
2. **Use specific details** - "Red rose" instead of "flower"
3. **Appeal to the senses** - Help readers see, hear, feel
4. **Read your work aloud** - Listen to how it sounds
5. **Revise and edit** - Poetry improves with revision

## Famous Poets to Explore

### Classic Poets:
- **Robert Frost** - Nature poetry ("The Road Not Taken")
- **Emily Dickinson** - Short, powerful poems about life and death
- **Langston Hughes** - Poems about dreams and equality
- **Maya Angelou** - Inspiring poems about overcoming challenges

### Children's Poets:
- **Shel Silverstein** - Funny, imaginative poems
- **Jack Prelutsky** - Playful poems for young readers
- **Judith Viorst** - Poems about everyday life
- **Douglas Florian** - Nature and animal poems

## Real-Life Applications

### Academic Benefits:
- **Improved vocabulary** through exposure to rich language
- **Better reading comprehension** by analyzing meaning
- **Enhanced writing skills** through studying techniques
- **Cultural understanding** through diverse voices

### Personal Growth:
- **Emotional expression** - Poetry helps process feelings
- **Creativity development** - Encourages imaginative thinking
- **Confidence building** - Sharing poetry builds self-esteem
- **Stress relief** - Writing and reading poetry can be therapeutic

### Communication Skills:
- **Public speaking** - Reading poetry aloud builds confidence
- **Listening skills** - Appreciating poetry requires careful attention
- **Empathy** - Understanding different perspectives in poems
- **Critical thinking** - Analyzing poetry develops reasoning skills

## Practice Activities

### For Reading Poetry:
1. **Poetry journals** - Keep favorite poems and reflections
2. **Poetry circles** - Discuss poems with friends
3. **Memorization** - Learn favorite poems by heart
4. **Illustration** - Draw pictures inspired by poems

### For Writing Poetry:
1. **Daily observations** - Write about what you notice
2. **Emotion poems** - Express how you feel
3. **Nature walks** - Find inspiration outdoors
4. **Word play** - Experiment with sounds and rhythms

### For Analysis:
1. **Compare poems** - Look at different treatments of same theme
2. **Timeline study** - See how poetry has changed over time
3. **Cultural exploration** - Read poetry from different countries
4. **Performance practice** - Act out dramatic poems

## Tips for Success

1. **Be patient** - Poetry appreciation develops over time
2. **Keep an open mind** - Try different types of poetry
3. **Ask questions** - Wonder about the poet's choices
4. **Make connections** - Relate poems to your own experiences
5. **Have fun** - Poetry should be enjoyable!

Remember: Poetry is like music made with words - it's meant to be felt as much as understood!"""

    # Update or create the study note
    study_note, created = StudyNote.objects.update_or_create(
        topic=topic,
        title="Understanding and Analyzing Poetry - Complete Guide",
        defaults={
            'content': content,
            'order': 1,
            'is_active': True,
            'created_by': admin_user
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"    {action} comprehensive study note for Poetry Analysis")

def update_grammar_tenses_notes(topic, admin_user):
    """Update Grammar: Tenses study notes with comprehensive content"""
    content = """# Understanding Tenses

## What Are Tenses?
Tenses tell us WHEN an action happens. They help us understand if something:
- **Already happened** (past)
- **Is happening now** (present)
- **Will happen later** (future)

Think of tenses as time machines for verbs!

## The Three Main Tenses

### 1. Past Tense
Shows actions that already happened.

#### Simple Past
**Formation:** Add -ed to regular verbs
- walk → walked
- play → played
- jump → jumped

**Irregular verbs** change completely:
- go → went
- eat → ate
- see → saw
- run → ran

**Examples:**
- Yesterday, I walked to school.
- She played soccer last weekend.
- We saw a movie on Friday.

#### Past Continuous (was/were + -ing)
Shows ongoing actions in the past
- I was reading when you called.
- They were playing outside all afternoon.
- She was cooking dinner at 6 PM.

#### Past Perfect (had + past participle)
Shows actions completed before another past action
- I had finished my homework before dinner.
- She had left before the rain started.
- We had seen that movie before.

### 2. Present Tense
Shows actions happening now or regularly.

#### Simple Present
**Formation:** Use base form (add -s for he/she/it)
- I walk to school every day.
- She walks to school every day.
- They walk to school every day.

**Uses:**
- **Habits:** I brush my teeth twice a day.
- **Facts:** The sun rises in the east.
- **Schedules:** The bus arrives at 8:00 AM.

#### Present Continuous (am/is/are + -ing)
Shows actions happening right now
- I am writing a letter.
- She is reading a book.
- They are playing outside.

**Signal words:** now, right now, at the moment, currently

#### Present Perfect (have/has + past participle)
Shows actions that started in the past and continue to now
- I have lived here for five years.
- She has finished her homework.
- We have seen that movie three times.

### 3. Future Tense
Shows actions that will happen later.

#### Simple Future (will + base verb)
- I will go to the store tomorrow.
- She will call you later.
- We will have a test next week.

#### Future with "going to"
Shows planned actions or predictions
- I am going to visit my grandmother.
- It is going to rain today.
- We are going to have pizza for dinner.

#### Future Continuous (will be + -ing)
Shows ongoing actions in the future
- I will be sleeping at midnight.
- She will be studying all evening.
- They will be traveling next month.

## Subject-Verb Agreement

### Basic Rules
The verb must match the subject in number.

#### Singular Subjects (one person/thing)
- **I** walk (except: I am, I have)
- **You** walk
- **He/She/It** walks (add -s)
- **The dog** walks
- **Sarah** walks

#### Plural Subjects (more than one)
- **We** walk
- **You** walk (same for one or many)
- **They** walk
- **The dogs** walk
- **Sarah and Tom** walk

### Tricky Situations

#### Subjects joined by "and"
Usually plural:
- Tom and Jerry are friends.
- The cat and dog play together.

#### Subjects joined by "or" or "nor"
Verb agrees with the closest subject:
- Neither Tom nor his friends are coming.
- Either the teacher or the students have the key.

#### Collective nouns
Can be singular or plural:
- The team is winning. (acting as one group)
- The team are arguing. (acting as individuals)

## Common Irregular Verbs

### Present → Past → Past Participle
- be → was/were → been
- have → had → had
- do → did → done
- go → went → gone
- come → came → come
- see → saw → seen
- get → got → gotten
- take → took → taken
- give → gave → given
- make → made → made
- know → knew → known
- think → thought → thought
- say → said → said
- find → found → found
- bring → brought → brought

## Time Signal Words

### Past Tense Signals
- yesterday
- last (week/month/year)
- ago (two days ago)
- in 2020
- when I was young

### Present Tense Signals
- now
- today
- every day/week
- usually
- always
- never
- sometimes

### Future Tense Signals
- tomorrow
- next (week/month/year)
- in the future
- later
- soon
- in two hours

## Common Mistakes to Avoid

### 1. Mixing Tenses
**Wrong:** Yesterday I go to the store and buy milk.
**Right:** Yesterday I went to the store and bought milk.

### 2. Forgetting -s for Third Person
**Wrong:** She walk to school.
**Right:** She walks to school.

### 3. Using Wrong Past Forms
**Wrong:** I seen that movie.
**Right:** I saw that movie. OR I have seen that movie.

### 4. Double Past
**Wrong:** I didn't went there.
**Right:** I didn't go there.

## Practice Strategies

### 1. Timeline Activities
Draw a timeline and place actions in past, present, or future.

### 2. Story Telling
Tell stories using different tenses:
- Past: What happened yesterday
- Present: What you do every day
- Future: What you plan to do

### 3. Verb Charts
Make charts of irregular verbs and practice them daily.

### 4. Reading Practice
Notice tenses in books and articles you read.

### 5. Writing Exercises
Write paragraphs focusing on one tense at a time.

## Real-Life Applications

### Academic Writing
- **Reports:** Use past tense for completed research
- **Essays:** Use present tense for general truths
- **Stories:** Use past tense for narratives

### Daily Communication
- **Planning:** Use future tense for schedules
- **Describing:** Use present tense for current situations
- **Sharing experiences:** Use past tense for stories

### Professional Skills
- **Job interviews:** Describe past experience and future goals
- **Presentations:** Use appropriate tenses for different information
- **Email writing:** Match tense to time of action

## Fun Activities

### 1. Tense Detective
Read a paragraph and identify all the tenses used.

### 2. Time Travel Stories
Write stories where characters travel through time, using different tenses.

### 3. Verb Races
Compete to change verbs to different tenses quickly.

### 4. Daily Journals
Write about your day using past tense, then plan tomorrow using future tense.

Remember: Tenses are like road signs for time - they help readers know exactly when things happen in your writing!"""

    # Update or create the study note
    study_note, created = StudyNote.objects.update_or_create(
        topic=topic,
        title="Understanding Tenses - Complete Guide",
        defaults={
            'content': content,
            'order': 1,
            'is_active': True,
            'created_by': admin_user
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"    {action} comprehensive study note for Grammar: Tenses")

def main():
    """Main function to update remaining study notes"""
    try:
        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No admin user found. Please create a superuser first.")
            return
        
        # Get Grade 5 English
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)
        
        print(f"📚 Updating remaining comprehensive study notes for Grade 5 English...")
        
        # Get topics
        topics = {
            'poetry_analysis': Topic.objects.get(class_level=grade5, title='Poetry Analysis'),
            'tenses': Topic.objects.get(class_level=grade5, title='Grammar: Tenses'),
        }
        
        # Update study notes for each topic
        update_poetry_analysis_notes(topics['poetry_analysis'], admin_user)
        update_grammar_tenses_notes(topics['tenses'], admin_user)
        
        print("✅ Successfully updated remaining comprehensive study notes!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
