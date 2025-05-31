#!/usr/bin/env python
"""
Grammar Part 3: Comprehensive Adjectives and Adverbs
Self-explanatory content that teaches from scratch
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

def create_adjectives_adverbs_content():
    """Create comprehensive adjectives and adverbs content"""
    print("CREATING COMPREHENSIVE ADJECTIVES AND ADVERBS CONTENT")
    print("=" * 60)
    
    try:
        # Find the topic
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topic = Topic.objects.get(title="Grammar and Sentence Structure", class_level=class_level)
        
        print(f"Found topic: {topic.title}")
        
        # Create Part 3: Adjectives and Adverbs
        part3_content = """# Part 3: Understanding Adjectives and Adverbs

## What Exactly is an Adjective?

An adjective is a word that describes or gives more information about a noun or pronoun. Adjectives answer questions like: What kind? Which one? How many? What does it look like?

Think of adjectives as the "paint" for your sentences:
- Without adjectives: "The dog ran to the house." (basic, colorless)
- With adjectives: "The small, brown dog ran to the old, wooden house." (colorful, detailed)

**The Simple Test for Adjectives:**
Can you put the word between "the" and a noun, and does it make sense?
- "the **red** car" ✓ (red is an adjective)
- "the **beautiful** flower" ✓ (beautiful is an adjective)
- "the **run** car" ✗ (run is not an adjective in this context)

---

## Types of Adjectives Explained in Detail

### 1. Descriptive Adjectives

These adjectives describe the qualities or characteristics of nouns. They paint a picture in the reader's mind.

#### Size Adjectives

**What do size adjectives do?**
Size adjectives tell us how big or small something is. They help us understand the scale or dimensions of objects.

**Examples with detailed explanations:**
- **big** - "The **big** elephant walked slowly."
  - This tells us the elephant is large in size
  - It helps us picture a large elephant, not a baby elephant
- **small** - "She has a **small** dog."
  - This tells us the dog is little in size
  - We can imagine a tiny dog, maybe one that fits in your lap
- **tiny** - "I found a **tiny** ant."
  - This tells us the ant is extremely small
  - Even smaller than just "small" - so small you might barely see it
- **huge** - "They live in a **huge** house."
  - This tells us the house is very large
  - Much bigger than just "big" - maybe like a mansion
- **enormous** - "The **enormous** tree provided shade."
  - This tells us the tree is extremely large
  - So big that it can shade many people at once

#### Color Adjectives

**What do color adjectives do?**
Color adjectives tell us what color something is. They help us visualize exactly what something looks like.

**Examples with detailed explanations:**
- **red** - "She wore a **red** dress."
  - This tells us the exact color of the dress
  - We can picture a dress that's the color of fire or roses
- **blue** - "The **blue** sky was beautiful."
  - This tells us the color of the sky
  - We can imagine a clear day with a sky the color of the ocean
- **green** - "I like **green** apples."
  - This tells us which type of apples
  - Not red apples, but the green variety like Granny Smith
- **bright** - "The **bright** light hurt my eyes."
  - This tells us the intensity of the light's color
  - Not dim or dark, but very intense and strong
- **dark** - "He painted the room **dark** blue."
  - This tells us the shade of blue
  - Not light blue, but a deep, rich blue color

#### Shape Adjectives

**What do shape adjectives do?**
Shape adjectives tell us the form or outline of something. They help us understand the physical structure of objects.

**Examples with detailed explanations:**
- **round** - "The **round** ball rolled away."
  - This tells us the ball is circular, like a sphere
  - We can picture it rolling because round things roll easily
- **square** - "We sat at a **square** table."
  - This tells us the table has four equal sides
  - Not rectangular or round, but perfectly square
- **curved** - "The **curved** road was dangerous."
  - This tells us the road bends and turns
  - Not straight, but winding like an "S" shape
- **straight** - "Draw a **straight** line."
  - This tells us the line should not bend or curve
  - Like using a ruler to make a perfectly direct line

#### Texture Adjectives

**What do texture adjectives do?**
Texture adjectives tell us how something feels when you touch it. They describe the surface quality of objects.

**Examples with detailed explanations:**
- **smooth** - "The **smooth** stone felt nice."
  - This tells us the stone's surface is even and soft to touch
  - Like glass or silk - no bumps or rough spots
- **rough** - "The **rough** bark scratched my hand."
  - This tells us the bark's surface is uneven and coarse
  - Like sandpaper - bumpy and harsh to touch
- **soft** - "The **soft** pillow was comfortable."
  - This tells us the pillow feels gentle and cushiony
  - Like a cloud or cotton - pleasant to touch
- **hard** - "The **hard** floor hurt my feet."
  - This tells us the floor is solid and firm
  - Like concrete or wood - not cushioned or soft

### 2. Opinion Adjectives

These adjectives express what someone thinks or feels about something. They show personal judgment or evaluation.

**Important Note:** Opinion adjectives are subjective - different people might have different opinions about the same thing.

#### Positive Opinion Adjectives

**What do positive opinion adjectives do?**
These show that someone likes or approves of something. They express good feelings or positive judgments.

**Examples with detailed explanations:**
- **beautiful** - "What a **beautiful** sunset!"
  - This expresses that someone finds the sunset very pleasing to look at
  - It shows admiration and appreciation for the sunset's appearance
- **wonderful** - "We had a **wonderful** time."
  - This expresses that someone really enjoyed their experience
  - It shows the time was much better than just "good"
- **amazing** - "That was an **amazing** performance."
  - This expresses that someone was impressed and surprised by how good it was
  - It shows the performance exceeded expectations
- **fantastic** - "The movie was **fantastic**."
  - This expresses strong enthusiasm and approval
  - It shows the person really loved the movie
- **perfect** - "This is the **perfect** day."
  - This expresses that everything about the day is exactly right
  - It shows complete satisfaction with how things are

#### Negative Opinion Adjectives

**What do negative opinion adjectives do?**
These show that someone dislikes or disapproves of something. They express bad feelings or negative judgments.

**Examples with detailed explanations:**
- **terrible** - "The weather was **terrible**."
  - This expresses that someone strongly disliked the weather
  - It shows the weather was much worse than just "bad"
- **awful** - "That was an **awful** movie."
  - This expresses very strong dislike or disgust
  - It shows the person really hated the movie
- **boring** - "The lecture was **boring**."
  - This expresses that someone found it uninteresting
  - It shows lack of engagement or excitement
- **ugly** - "He thinks the building is **ugly**."
  - This expresses that someone finds it unpleasant to look at
  - It shows aesthetic displeasure with the building's appearance

### 3. Number Adjectives

These adjectives tell us "how many" or "which number." They give us quantity information.

#### Exact Numbers

**What do exact number adjectives do?**
These tell us the precise quantity of something. They give specific amounts.

**Examples with detailed explanations:**
- **one** - "I have **one** brother."
  - This tells us the exact number of brothers (not zero, not two, but exactly one)
- **two** - "She bought **two** books."
  - This tells us the precise quantity of books purchased
- **fifteen** - "There are **fifteen** students."
  - This gives us the exact count of students in the group

#### Approximate Numbers

**What do approximate number adjectives do?**
These give us a general idea of quantity without being exact. They're useful when we don't know or don't need to know the precise number.

**Examples with detailed explanations:**
- **many** - "**Many** people came to the party."
  - This tells us a large number of people came, but we don't know exactly how many
  - It could be 50, 100, or 200 people - the point is it was a lot
- **few** - "Only a **few** cookies are left."
  - This tells us a small number of cookies remain
  - Maybe 2, 3, or 4 cookies - not many, but some
- **several** - "I've read **several** books this month."
  - This tells us more than two but not a huge number
  - Maybe 3, 4, or 5 books - a moderate amount
- **some** - "**Some** students stayed after school."
  - This tells us an unspecified number stayed
  - Could be 5, 10, or 15 students - we just know it wasn't all or none

#### Order Numbers

**What do order number adjectives do?**
These tell us the position of something in a sequence. They show rank or order.

**Examples with detailed explanations:**
- **first** - "She was the **first** person to arrive."
  - This tells us her position in the order of arrival (before everyone else)
- **second** - "He came in **second** place."
  - This tells us his position in a competition (after first, before third)
- **last** - "This is my **last** chance."
  - This tells us the position in a series (final opportunity, no more after this)

---

## What Exactly is an Adverb?

An adverb is a word that describes or gives more information about verbs, adjectives, or other adverbs. Adverbs answer questions like: How? When? Where? How much? How often?

Think of adverbs as the "details" that make actions and descriptions more specific:
- Without adverbs: "She ran." (basic information)
- With adverbs: "She quickly ran outside yesterday." (detailed information)

**The Simple Test for Adverbs:**
Many adverbs end in "-ly," but not all. Ask yourself: Does this word tell me HOW, WHEN, WHERE, or HOW MUCH about an action or description?

---

## Types of Adverbs Explained in Detail

### 1. Adverbs of Manner (How?)

These adverbs tell us HOW an action is performed. They describe the way something is done.

#### Common -ly Adverbs

**What do manner adverbs do?**
They give us details about the style, method, or way an action happens.

**Examples with detailed explanations:**
- **quickly** - "She **quickly** finished her homework."
  - This tells us HOW she finished (in a fast manner)
  - We can picture her working at a rapid pace, not slowly
- **slowly** - "The turtle moved **slowly**."
  - This tells us HOW the turtle moved (at a slow pace)
  - We can imagine the turtle taking its time, moving gradually
- **carefully** - "He **carefully** carried the glass."
  - This tells us HOW he carried it (with caution and attention)
  - We can picture him being gentle and paying close attention
- **loudly** - "The baby cried **loudly**."
  - This tells us HOW the baby cried (with high volume)
  - We can imagine the crying being very noisy and intense
- **quietly** - "We **quietly** entered the room."
  - This tells us HOW they entered (without making noise)
  - We can picture them being careful not to disturb anyone

#### Adverbs Without -ly

**Important Note:** Not all adverbs end in -ly. Some common adverbs have their own forms.

**Examples with detailed explanations:**
- **well** - "She sings **well**."
  - This tells us HOW she sings (in a good manner, with skill)
  - Note: "good" is an adjective, "well" is the adverb
- **fast** - "He runs **fast**."
  - This tells us HOW he runs (at high speed)
  - Note: "fast" can be both an adjective and an adverb
- **hard** - "They worked **hard**."
  - This tells us HOW they worked (with great effort and intensity)
  - Note: "hard" can be both an adjective and an adverb

### 2. Adverbs of Time (When?)

These adverbs tell us WHEN an action happens. They give us time information.

#### Specific Time

**What do specific time adverbs do?**
They tell us the exact time or day when something happens.

**Examples with detailed explanations:**
- **yesterday** - "I saw him **yesterday**."
  - This tells us WHEN you saw him (the day before today)
  - It gives us a specific time reference
- **today** - "We have a test **today**."
  - This tells us WHEN the test is (this current day)
  - It specifies the exact day
- **tomorrow** - "She will call **tomorrow**."
  - This tells us WHEN she will call (the day after today)
  - It gives us a future time reference
- **now** - "Please come here **now**."
  - This tells us WHEN to come (at this exact moment)
  - It emphasizes immediate timing

#### Frequency (How Often)

**What do frequency adverbs do?**
They tell us how often something happens - whether it's regular, occasional, or rare.

**Examples with detailed explanations:**
- **always** - "I **always** brush my teeth."
  - This tells us HOW OFTEN you brush (every single time, without exception)
  - It shows this is a consistent habit
- **never** - "He **never** eats vegetables."
  - This tells us HOW OFTEN he eats them (not even once, zero times)
  - It shows this never happens
- **sometimes** - "We **sometimes** go to the park."
  - This tells us HOW OFTEN you go (occasionally, not always but not never)
  - It shows this happens irregularly
- **often** - "She **often** helps her mother."
  - This tells us HOW OFTEN she helps (frequently, many times)
  - It shows this is a regular occurrence
- **rarely** - "They **rarely** watch TV."
  - This tells us HOW OFTEN they watch (very seldom, almost never)
  - It shows this happens very infrequently

### 3. Adverbs of Place (Where?)

These adverbs tell us WHERE an action happens. They give us location information.

**What do place adverbs do?**
They specify the location or direction of an action.

**Examples with detailed explanations:**
- **here** - "Please sit **here**."
  - This tells us WHERE to sit (in this location, close to the speaker)
  - It points to a specific nearby place
- **there** - "The book is **there**."
  - This tells us WHERE the book is (in that location, away from the speaker)
  - It points to a specific distant place
- **everywhere** - "I looked **everywhere** for my keys."
  - This tells us WHERE you looked (in all possible places)
  - It emphasizes the thoroughness of the search
- **outside** - "The children are playing **outside**."
  - This tells us WHERE they're playing (not inside, but outdoors)
  - It specifies the outdoor location
- **inside** - "Come **inside** the house."
  - This tells us WHERE to come (into the interior of the house)
  - It specifies moving from outside to inside
- **upstairs** - "My room is **upstairs**."
  - This tells us WHERE the room is (on a higher floor)
  - It gives vertical location information
- **downstairs** - "The kitchen is **downstairs**."
  - This tells us WHERE the kitchen is (on a lower floor)
  - It gives vertical location information

### 4. Adverbs of Degree (How Much?)

These adverbs tell us HOW MUCH or TO WHAT EXTENT something happens. They show intensity or degree.

**What do degree adverbs do?**
They modify the intensity of adjectives, other adverbs, or sometimes verbs.

**Examples with detailed explanations:**
- **very** - "She is **very** smart."
  - This tells us HOW MUCH smart she is (to a high degree)
  - It intensifies the adjective "smart"
- **quite** - "The movie was **quite** good."
  - This tells us HOW MUCH good it was (to a considerable degree)
  - It shows the movie was more than just "good"
- **extremely** - "The weather is **extremely** hot."
  - This tells us HOW MUCH hot it is (to the highest degree)
  - It shows the heat is at a very intense level
- **barely** - "I can **barely** hear you."
  - This tells us HOW MUCH you can hear (to a very small degree)
  - It shows the hearing is at the minimum level
- **almost** - "We're **almost** finished."
  - This tells us HOW MUCH finished you are (nearly completely)
  - It shows you're very close to being done
- **completely** - "I **completely** forgot."
  - This tells us HOW MUCH you forgot (totally, 100%)
  - It shows the forgetting was absolute

---

## How Adjectives and Adverbs Make Communication Better

### Adjectives Paint Pictures

**Without adjectives (basic):**
"The dog ran to the house."

**With adjectives (detailed):**
"The small, brown dog ran to the old, wooden house."

Now we can picture exactly what kind of dog and house we're talking about!

### Adverbs Add Action Details

**Without adverbs (basic):**
"The dog ran."

**With adverbs (detailed):**
"The dog quickly ran outside yesterday."

Now we know HOW the dog ran (quickly), WHERE it ran (outside), and WHEN it ran (yesterday).

### Order of Adjectives

When you use multiple adjectives, they follow a specific order:
1. **Opinion** (beautiful, nice, ugly)
2. **Size** (big, small, tiny)
3. **Age** (old, new, young)
4. **Shape** (round, square, long)
5. **Color** (red, blue, green)
6. **Origin** (American, Chinese, local)
7. **Material** (wooden, plastic, metal)
8. **Purpose** (sleeping bag, running shoes)

**Example:** "She bought a **beautiful** (opinion) **small** (size) **old** (age) **wooden** (material) table."

### Common Mistakes to Avoid

**Mistake 1: Using adjectives instead of adverbs**
- Wrong: "She sings **good**." (good is an adjective)
- Right: "She sings **well**." (well is an adverb)

**Mistake 2: Double negatives**
- Wrong: "I don't have **no** money." (don't + no = double negative)
- Right: "I don't have **any** money." or "I have **no** money."

**Mistake 3: Placing adverbs in the wrong position**
- Awkward: "I **quickly** am running."
- Better: "I am running **quickly**." or "I **quickly** run."

---

## Why Understanding Adjectives and Adverbs Matters

When you understand adjectives and adverbs, you can:
1. **Paint vivid pictures** - Your writing becomes more interesting
2. **Give precise information** - People understand exactly what you mean
3. **Express emotions better** - You can show how you feel about things
4. **Sound more sophisticated** - Your language becomes more mature
5. **Avoid confusion** - You can be specific instead of vague

**Practice Daily:**
- Add adjectives to describe nouns in your writing
- Use adverbs to show how actions are performed
- Read books and notice how authors use descriptive words
- Practice putting adjectives in the correct order

The more you practice with adjectives and adverbs, the more colorful and precise your communication will become!"""

        # Create the study note
        study_note = StudyNote.objects.create(
            topic=topic,
            title="Part 3: Understanding Adjectives and Adverbs",
            content=part3_content,
            order=3,
            is_active=True
        )
        
        print(f"✅ Created Part 3: {study_note.title}")
        print(f"📝 Content length: {len(part3_content):,} characters")
        print(f"📖 Word count: ~{len(part3_content.split()):,} words")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Create Part 3 of comprehensive grammar content"""
    success = create_adjectives_adverbs_content()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("Part 3 (Adjectives and Adverbs) created successfully!")
        print("Content is comprehensive and teaches from scratch.")
    else:
        print("\n❌ FAILED!")
        print("Could not create the content. Check the error above.")

if __name__ == '__main__':
    main()
