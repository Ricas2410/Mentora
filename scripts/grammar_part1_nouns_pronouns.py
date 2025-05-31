#!/usr/bin/env python
"""
Grammar Part 1: Comprehensive Nouns and Pronouns
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

def create_nouns_pronouns_content():
    """Create comprehensive nouns and pronouns content"""
    print("CREATING COMPREHENSIVE NOUNS AND PRONOUNS CONTENT")
    print("=" * 60)
    
    try:
        # Find the topic
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topic = Topic.objects.get(title="Grammar and Sentence Structure", class_level=class_level)
        
        print(f"Found topic: {topic.title}")
        
        # Delete existing notes to start fresh
        existing_notes = topic.study_notes.all()
        print(f"Removing {existing_notes.count()} existing notes...")
        existing_notes.delete()
        
        # Create Part 1: Nouns and Pronouns
        part1_content = """# Part 1: Understanding Nouns and Pronouns

## Introduction: What is Grammar and Why Does It Matter?

Grammar is like the instruction manual for language. Just like you need rules to play a game fairly, you need grammar rules to communicate clearly with others. When you follow grammar rules, people understand exactly what you mean. When you don't follow them, people might get confused or misunderstand you.

Think of grammar as the traffic rules for language:
- **Traffic rules** help cars move safely and efficiently on roads
- **Grammar rules** help words move safely and efficiently in sentences

Without traffic rules, there would be chaos on the roads. Without grammar rules, there would be chaos in communication!

**Real-Life Example:**
Imagine you're texting a friend about meeting up. Without grammar rules:
- "meet you park 3 tomorrow" (confusing - which park? 3 what? 3 o'clock?)
With grammar rules:
- "I'll meet you at Central Park at 3 PM tomorrow." (clear and understandable!)

Grammar helps you communicate your thoughts clearly so others understand exactly what you mean.

---

## Understanding Nouns - The Naming Words

### What Exactly is a Noun?

A noun is any word that names something. If you can point to it, think about it, or experience it, there's probably a noun for it. Nouns are the "naming words" in our language.

**The Simple Test for Nouns:**
Can you put the word "the" or "a" in front of it? If yes, it's probably a noun!
- "the dog" ✓ (dog is a noun)
- "the happiness" ✓ (happiness is a noun)
- "the run" ✗ (run is usually a verb, not a noun in this form)

### Types of Nouns Explained in Detail

#### 1. Common Nouns vs. Proper Nouns

**Common Nouns** are general names for things. They're like saying "a person" instead of giving someone's specific name.

**What makes a noun "common"?**
- It names a general type or category of thing
- It doesn't refer to one specific, unique item
- It starts with a lowercase letter (unless it's the first word in a sentence)
- You can usually put "a" or "an" in front of it

**Examples with detailed explanations:**
- **dog** - This refers to any dog, not one specific dog. There are millions of dogs in the world. When you say "I saw a dog," people know you mean some dog, but they don't know which specific dog.
- **school** - This refers to any school, not one particular school building. Every town has schools, and this word could mean any of them.
- **book** - This could be any book among the millions of books that exist. It could be a novel, textbook, cookbook, or any other type of book.
- **city** - This refers to any city, not one specific city. There are thousands of cities worldwide.

**Proper Nouns** are specific names for particular people, places, or things. They're like giving someone's exact name instead of just saying "a person."

**What makes a noun "proper"?**
- It names one specific, unique person, place, or thing
- It always starts with a capital letter
- You usually can't put "a" or "an" in front of it
- There's only one of that exact thing in the world

**Examples with detailed explanations:**
- **Sarah** - This is one specific person's name, not just any person. When you say "Sarah," everyone knows you mean that particular girl named Sarah.
- **McDonald's** - This is the name of one specific restaurant company, not just any restaurant. Even though there are many McDonald's locations, they all belong to the same company.
- **iPhone** - This is the specific name of Apple's phone, not just any phone. It's different from other phones like Samsung or Google phones.
- **Christmas** - This is the name of one specific holiday, not just any holiday. It happens on December 25th every year.

**Practice Understanding:**
- "I go to school" (common noun - any school)
- "I go to Lincoln Elementary School" (proper noun - one specific school)
- "My dog is friendly" (common noun - any dog)
- "My dog Buddy is friendly" (proper noun - one specific dog named Buddy)

#### 2. Concrete Nouns vs. Abstract Nouns

**Concrete Nouns** are things you can experience with your five senses (see, hear, touch, taste, smell).

**How to identify concrete nouns:**
- Can you see it? Can you touch it? Can you hear it? Can you smell it? Can you taste it?
- If you answered "yes" to any of these questions, it's concrete
- These are physical things that exist in the real world

**Examples with detailed explanations:**
- **table** - You can see it (it has a shape and color), touch it (it feels hard or smooth), and even hear it (if you knock on it). You could even smell it if it's made of wood.
- **pizza** - You can see it (it looks round with toppings), smell it (it has a delicious aroma), taste it (it has flavors like cheese and sauce), and touch it (it feels warm and soft).
- **music** - You can hear it (it makes sounds and melodies), and sometimes you can even feel it (when the bass is strong, you feel vibrations).
- **flower** - You can see it (it has colors and petals), smell it (many flowers have sweet scents), and touch it (petals feel soft, stems feel firm).

**Abstract Nouns** are things you cannot experience with your five senses. They exist in your mind and heart.

**How to identify abstract nouns:**
- Can you think about it or feel it emotionally, but not touch it or see it?
- These are ideas, emotions, concepts, or qualities
- They exist, but not as physical objects you can hold

**Examples with detailed explanations:**
- **love** - You can feel love in your heart and think about it, but you can't touch love or see love itself. You can see the effects of love (like people hugging), but not love itself.
- **courage** - This is the feeling of being brave. You can't hold courage in your hands, but you can feel it inside yourself when you do something scary but right.
- **freedom** - This is an idea about being able to make your own choices. You can't touch freedom, but you can experience what it feels like to be free.
- **happiness** - This is an emotion you feel inside. You can't see happiness itself, but you can see someone's happy expression or smile.

**Practice Understanding:**
- "The **book** gave me **joy**" (book = concrete, you can touch it; joy = abstract, you feel it)
- "Her **smile** showed her **confidence**" (smile = concrete, you can see it; confidence = abstract, it's a feeling)

---

## Understanding Pronouns - The Replacement Words

### What Exactly is a Pronoun?

A pronoun is a word that takes the place of a noun. Think of pronouns as "stand-ins" or "substitutes" for nouns.

**Why do we need pronouns?**
Without pronouns, our language would be very repetitive and awkward. Look at this example:

**Without pronouns (awkward):**
"Sarah went to Sarah's room. Sarah picked up Sarah's book. Sarah read Sarah's book until Sarah fell asleep."

**With pronouns (smooth):**
"Sarah went to her room. She picked up her book. She read it until she fell asleep."

See how much better that sounds? Pronouns make our language flow naturally.

### Types of Pronouns Explained in Detail

#### 1. Personal Pronouns

Personal pronouns refer to specific people or things. They change depending on who is speaking, who is being spoken to, and who is being spoken about.

**Subject Pronouns** (these do the action in a sentence)

**First Person** (the person speaking):
- **I** - Use when you're talking about yourself doing something
  - "**I** am going to the store." (You are doing the action of going)
  - "**I** like ice cream." (You are doing the action of liking)
  - Think of it this way: When YOU are the one doing something, use "I"

**Second Person** (the person being spoken to):
- **you** - Use when talking directly to someone
  - "**You** are my best friend." (The person you're talking to is your friend)
  - "**You** did a great job!" (The person you're talking to did the job)
  - Think of it this way: When the person you're talking TO is doing something, use "you"

**Third Person** (the person or thing being spoken about):
- **he** - Use for one male person
  - "**He** is my brother." (Some male person is your brother)
  - "**He** plays basketball." (Some male person plays)
- **she** - Use for one female person
  - "**She** is my teacher." (Some female person is your teacher)
  - "**She** loves reading." (Some female person loves reading)
- **it** - Use for one thing, animal, or idea
  - "**It** is raining." (The weather is raining)
  - "**It** is a beautiful day." (The day is beautiful)
- **we** - Use for yourself plus other people
  - "**We** are going to the movies." (You and other people are going)
  - "**We** won the game." (You and your team won)
- **they** - Use for multiple people or things
  - "**They** are my friends." (Multiple people are your friends)
  - "**They** live next door." (Multiple people live there)

**Object Pronouns** (these receive the action in a sentence)

- **me** - Use when someone is doing something to you
  - "She gave **me** a present." (You received the present)
  - "The teacher called **me**." (You were called)
- **you** - Use when someone is doing something to the person you're talking to
  - "I will help **you** with homework." (The person you're talking to will receive help)
- **him** - Use when someone is doing something to a male person
  - "We saw **him** at the store." (The male person was seen)
- **her** - Use when someone is doing something to a female person
  - "They invited **her** to the party." (The female person was invited)
- **it** - Use when someone is doing something to a thing
  - "I found **it** under the bed." (The thing was found)
- **us** - Use when someone is doing something to you and other people
  - "The teacher gave **us** homework." (You and others received homework)
- **them** - Use when someone is doing something to multiple people or things
  - "I saw **them** yesterday." (Multiple people were seen)

**Possessive Pronouns** (these show ownership)

**Possessive Adjectives** (used before nouns):
- **my** - "**My** book is on the table." (The book belongs to you)
- **your** - "**Your** car is blue." (The car belongs to the person you're talking to)
- **his** - "**His** dog is friendly." (The dog belongs to a male person)
- **her** - "**Her** house is big." (The house belongs to a female person)
- **its** - "**Its** color is red." (The color belongs to a thing)
- **our** - "**Our** team won the game." (The team belongs to you and others)
- **their** - "**Their** books are heavy." (The books belong to multiple people)

**Possessive Pronouns** (used alone, without nouns):
- **mine** - "That book is **mine**." (The book belongs to you)
- **yours** - "This pen is **yours**." (The pen belongs to the person you're talking to)
- **his** - "The red car is **his**." (The car belongs to a male person)
- **hers** - "The blue bag is **hers**." (The bag belongs to a female person)
- **ours** - "The victory is **ours**." (The victory belongs to you and others)
- **theirs** - "Those seats are **theirs**." (The seats belong to multiple people)

### How to Choose the Right Pronoun

**Step 1: Identify what the pronoun is replacing**
- Is it a person? (he, she, they)
- Is it a thing? (it)
- Is it yourself? (I, me, my, mine)

**Step 2: Determine the pronoun's job in the sentence**
- Is it doing the action? (Use subject pronouns: I, you, he, she, it, we, they)
- Is it receiving the action? (Use object pronouns: me, you, him, her, it, us, them)
- Is it showing ownership? (Use possessive pronouns: my, your, his, her, its, our, their)

**Step 3: Check if it sounds right**
- Read the sentence out loud
- Does it sound natural?
- Would other people understand what you mean?

**Practice Examples:**

**Example 1:** "Sarah and ___ went to the store."
- Step 1: The pronoun replaces your name (yourself)
- Step 2: The pronoun is doing the action (going)
- Step 3: Use "I" → "Sarah and **I** went to the store."

**Example 2:** "The teacher gave ___ the assignment."
- Step 1: The pronoun replaces your name (yourself)
- Step 2: The pronoun is receiving the action (being given something)
- Step 3: Use "me" → "The teacher gave **me** the assignment."

---

## Why Understanding Nouns and Pronouns Matters

When you understand nouns and pronouns, you can:
1. **Write more clearly** - You know when to capitalize proper nouns
2. **Choose better words** - You can pick specific nouns instead of general ones
3. **Avoid repetition** - You can use pronouns instead of repeating the same nouns
4. **Follow grammar rules** - You know how to use nouns and pronouns correctly
5. **Understand reading better** - You recognize what authors are talking about

**Practice Daily:**
- Read sentences and identify nouns and pronouns
- Write your own sentences using different types of nouns
- Practice replacing nouns with appropriate pronouns
- Pay attention to how professional writers use these words

The more you practice, the more natural these concepts will become!"""

        # Create the study note
        study_note = StudyNote.objects.create(
            topic=topic,
            title="Part 1: Understanding Nouns and Pronouns",
            content=part1_content,
            order=1,
            is_active=True
        )
        
        print(f"✅ Created Part 1: {study_note.title}")
        print(f"📝 Content length: {len(part1_content):,} characters")
        print(f"📖 Word count: ~{len(part1_content.split()):,} words")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Create Part 1 of comprehensive grammar content"""
    success = create_nouns_pronouns_content()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("Part 1 (Nouns and Pronouns) created successfully!")
        print("Content is comprehensive and teaches from scratch.")
    else:
        print("\n❌ FAILED!")
        print("Could not create the content. Check the error above.")

if __name__ == '__main__':
    main()
