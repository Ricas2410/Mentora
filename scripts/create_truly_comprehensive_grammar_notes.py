#!/usr/bin/env python
"""
Create Truly Comprehensive, Self-Explanatory Grammar Notes
Detailed explanations that teach concepts from scratch with no prior knowledge assumed
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

def create_comprehensive_grammar_notes():
    """Create truly comprehensive, self-explanatory grammar notes"""
    print("CREATING TRULY COMPREHENSIVE GRAMMAR NOTES")
    print("=" * 60)
    
    try:
        # Find the topic
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topic = Topic.objects.get(title="Grammar and Sentence Structure", class_level=class_level)
        
        print(f"Found topic: {topic.title}")
        
        # Delete existing notes to replace with truly comprehensive version
        existing_notes = topic.study_notes.all()
        print(f"Removing {existing_notes.count()} existing notes...")
        existing_notes.delete()
        
        # Create truly comprehensive content that teaches from scratch
        comprehensive_content = """# Complete Self-Teaching Guide to Grammar and Sentence Structure

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

## Part 1: Understanding Nouns - The Naming Words

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

**Examples with explanations:**
- **dog** - This refers to any dog, not one specific dog. There are millions of dogs in the world.
- **school** - This refers to any school, not one particular school building.
- **book** - This could be any book among the millions of books that exist.
- **city** - This refers to any city, not one specific city.

**Proper Nouns** are specific names for particular people, places, or things. They're like giving someone's exact name instead of just saying "a person."

**What makes a noun "proper"?**
- It names one specific, unique person, place, or thing
- It always starts with a capital letter
- You usually can't put "a" or "an" in front of it
- There's only one of that exact thing in the world

**Examples with explanations:**
- **Sarah** - This is one specific person's name, not just any person
- **McDonald's** - This is the name of one specific restaurant company, not just any restaurant
- **iPhone** - This is the specific name of Apple's phone, not just any phone
- **Christmas** - This is the name of one specific holiday, not just any holiday

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
- **table** - You can see it (it has a shape and color), touch it (it feels hard or smooth), and even hear it (if you knock on it)
- **pizza** - You can see it (it looks round with toppings), smell it (it has a delicious aroma), taste it (it has flavors), and touch it (it feels warm and soft)
- **music** - You can hear it (it makes sounds), and sometimes you can even feel it (when the bass is strong)
- **flower** - You can see it (it has colors and shape), smell it (many flowers have scents), and touch it (it feels soft or rough)

**Abstract Nouns** are things you cannot experience with your five senses. They exist in your mind and heart.

**How to identify abstract nouns:**
- Can you think about it or feel it emotionally, but not touch it or see it?
- These are ideas, emotions, concepts, or qualities
- They exist, but not as physical objects

**Examples with detailed explanations:**
- **love** - You can feel love in your heart and think about it, but you can't touch love or see love itself (though you can see the effects of love)
- **courage** - This is the feeling of being brave. You can't hold courage in your hands, but you can feel it inside yourself
- **freedom** - This is an idea about being able to make your own choices. You can't touch freedom, but you can experience what it feels like
- **happiness** - This is an emotion you feel inside. You can't see happiness itself, but you can see someone's happy expression

**Practice Understanding:**
- "The **book** gave me **joy**" (book = concrete, you can touch it; joy = abstract, you feel it)
- "Her **smile** showed her **confidence**" (smile = concrete, you can see it; confidence = abstract, it's a feeling)

### Why Understanding Noun Types Matters

When you understand different types of nouns, you can:
1. **Write more clearly** - You know when to capitalize proper nouns
2. **Choose better words** - You can pick specific nouns instead of general ones
3. **Understand reading better** - You recognize what authors are talking about
4. **Follow grammar rules** - You know how to use nouns correctly in sentences

---

## Part 2: Understanding Pronouns - The Replacement Words

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

**Second Person** (the person being spoken to):
- **you** - Use when talking directly to someone
  - "**You** are my best friend." (The person you're talking to is your friend)
  - "**You** did a great job!" (The person you're talking to did the job)

**Third Person** (the person or thing being spoken about):
- **he** - Use for one male person
  - "**He** is my brother." (Some male person is your brother)
- **she** - Use for one female person
  - "**She** is my teacher." (Some female person is your teacher)
- **it** - Use for one thing, animal, or idea
  - "**It** is raining." (The weather is raining)
  - "**It** is a beautiful day." (The day is beautiful)
- **we** - Use for yourself plus other people
  - "**We** are going to the movies." (You and other people are going)
- **they** - Use for multiple people or things
  - "**They** are my friends." (Multiple people are your friends)

**Object Pronouns** (these receive the action in a sentence)

- **me** - Use when someone is doing something to you
  - "She gave **me** a present." (You received the present)
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

## Part 3: Understanding Verbs - The Action and Being Words

### What Exactly is a Verb?

A verb is a word that shows action or state of being. Verbs are the "engine" of every sentence - they make things happen or describe how things are.

**Every complete sentence must have a verb.** Without a verb, you don't have a complete thought.

### Types of Verbs Explained in Detail

#### 1. Action Verbs

Action verbs show what someone or something does. These are the "doing" words.

**Physical Action Verbs** (actions you can see):
- **run** - "She **runs** every morning." (You can see someone running)
- **jump** - "The cat **jumped** over the fence." (You can see the jumping motion)
- **write** - "I **write** in my journal." (You can see the writing action)
- **cook** - "Mom **cooks** dinner." (You can see the cooking process)
- **dance** - "They **dance** at the party." (You can see the dancing movements)

**Mental Action Verbs** (actions that happen in your mind):
- **think** - "I **think** about my future." (This happens in your mind)
- **believe** - "She **believes** in herself." (This is a mental state)
- **remember** - "He **remembers** his childhood." (This is a mental process)
- **understand** - "We **understand** the lesson." (This happens in your mind)
- **imagine** - "They **imagine** flying." (This is mental activity)

#### 2. Linking Verbs

Linking verbs don't show action. Instead, they connect the subject to more information about the subject. They're like an equals sign (=) in math.

**The Most Common Linking Verb: Forms of "BE"**
- **am** - "I **am** happy." (I = happy)
- **is** - "She **is** a teacher." (She = a teacher)
- **are** - "They **are** friends." (They = friends)
- **was** - "He **was** tired." (He = tired, in the past)
- **were** - "We **were** excited." (We = excited, in the past)
- **being** - "You are **being** helpful." (You = helpful, right now)
- **been** - "I have **been** sick." (I = sick, recently)

**Other Linking Verbs:**
- **seem** - "You **seem** worried." (You = worried, apparently)
- **appear** - "She **appears** confident." (She = confident, from what we can see)
- **become** - "He **became** a doctor." (He = a doctor, after change)
- **feel** - "I **feel** excited." (I = excited, emotionally)
- **look** - "You **look** tired." (You = tired, from appearance)
- **sound** - "That **sounds** interesting." (That = interesting, from what we hear)

**How to Test if a Verb is Linking:**
Replace the verb with "=" (equals). If the sentence still makes sense, it's a linking verb.
- "She **is** happy." → "She = happy." ✓ (Makes sense, so "is" is linking)
- "She **runs** fast." → "She = fast." ✗ (Doesn't make sense, so "runs" is action)

#### 3. Helping Verbs

Helping verbs work together with main verbs to show different meanings like time, possibility, or necessity.

**Common Helping Verbs:**
- **am, is, are** + main verb ending in -ing
  - "I **am studying**." (happening right now)
  - "She **is reading**." (happening right now)
  - "They **are playing**." (happening right now)

- **has, have** + past participle
  - "I **have finished** my homework." (completed recently)
  - "She **has eaten** lunch." (completed recently)

- **will** + main verb
  - "I **will go** tomorrow." (future action)
  - "She **will help** you." (future action)

- **can, could** + main verb
  - "I **can swim**." (ability)
  - "She **could help** if needed." (possibility)

- **should, would** + main verb
  - "You **should study**." (advice)
  - "I **would like** some water." (polite request)

**Understanding Helping + Main Verb Combinations:**
The helping verb changes the meaning, while the main verb shows the action.
- "I **study**." (simple present - happens regularly)
- "I **am studying**." (present continuous - happening right now)
- "I **have studied**." (present perfect - completed recently)
- "I **will study**." (future - will happen later)

---

## Part 4: Understanding Adjectives - The Describing Words

### What Exactly is an Adjective?

An adjective is a word that describes or gives more information about a noun or pronoun. Adjectives answer questions like: What kind? Which one? How many? What does it look like?

**The Simple Test for Adjectives:**
Can you put the word between "the" and a noun, and does it make sense?
- "the **red** car" ✓ (red is an adjective)
- "the **beautiful** flower" ✓ (beautiful is an adjective)
- "the **run** car" ✗ (run is not an adjective in this context)

### Types of Adjectives Explained in Detail

#### 1. Descriptive Adjectives

These adjectives describe the qualities or characteristics of nouns.

**Size Adjectives:**
- **big** - "The **big** elephant walked slowly." (tells us the elephant's size)
- **small** - "She has a **small** dog." (tells us the dog's size)
- **tiny** - "I found a **tiny** ant." (tells us the ant's size)
- **huge** - "They live in a **huge** house." (tells us the house's size)
- **enormous** - "The **enormous** tree provided shade." (tells us the tree's size)

**Color Adjectives:**
- **red** - "She wore a **red** dress." (tells us the dress's color)
- **blue** - "The **blue** sky was beautiful." (tells us the sky's color)
- **green** - "I like **green** apples." (tells us the apples' color)
- **bright** - "The **bright** light hurt my eyes." (tells us the light's intensity)
- **dark** - "He painted the room **dark** blue." (tells us the shade)

**Shape Adjectives:**
- **round** - "The **round** ball rolled away." (tells us the ball's shape)
- **square** - "We sat at a **square** table." (tells us the table's shape)
- **curved** - "The **curved** road was dangerous." (tells us the road's shape)
- **straight** - "Draw a **straight** line." (tells us the line's shape)

**Texture Adjectives:**
- **smooth** - "The **smooth** stone felt nice." (tells us how the stone feels)
- **rough** - "The **rough** bark scratched my hand." (tells us how the bark feels)
- **soft** - "The **soft** pillow was comfortable." (tells us how the pillow feels)
- **hard** - "The **hard** floor hurt my feet." (tells us how the floor feels)

#### 2. Opinion Adjectives

These adjectives express what someone thinks or feels about something.

**Positive Opinion Adjectives:**
- **beautiful** - "What a **beautiful** sunset!" (expresses admiration)
- **wonderful** - "We had a **wonderful** time." (expresses enjoyment)
- **amazing** - "That was an **amazing** performance." (expresses awe)
- **fantastic** - "The movie was **fantastic**." (expresses enthusiasm)
- **perfect** - "This is the **perfect** day." (expresses satisfaction)

**Negative Opinion Adjectives:**
- **terrible** - "The weather was **terrible**." (expresses dislike)
- **awful** - "That was an **awful** movie." (expresses strong dislike)
- **boring** - "The lecture was **boring**." (expresses lack of interest)
- **ugly** - "He thinks the building is **ugly**." (expresses aesthetic dislike)

**Important Note:** Opinion adjectives are subjective - different people might have different opinions about the same thing.

#### 3. Number Adjectives

These adjectives tell us "how many" or "which number."

**Exact Numbers:**
- **one** - "I have **one** brother." (exact quantity)
- **two** - "She bought **two** books." (exact quantity)
- **fifteen** - "There are **fifteen** students." (exact quantity)

**Approximate Numbers:**
- **many** - "**Many** people came to the party." (a large but unspecified number)
- **few** - "Only a **few** cookies are left." (a small number)
- **several** - "I've read **several** books this month." (more than two but not many)
- **some** - "**Some** students stayed after school." (an unspecified number)

**Order Numbers:**
- **first** - "She was the **first** person to arrive." (position in order)
- **second** - "He came in **second** place." (position in order)
- **last** - "This is my **last** chance." (final position)

### How Adjectives Make Writing Better

**Without adjectives (boring):**
"The dog ran to the house."

**With adjectives (interesting):**
"The **small, brown** dog ran to the **old, wooden** house."

See how adjectives paint a picture in your mind? They help readers visualize exactly what you're describing.

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

---

## Part 5: Understanding Adverbs - The Words That Describe Actions

### What Exactly is an Adverb?

An adverb is a word that describes or gives more information about verbs, adjectives, or other adverbs. Adverbs answer questions like: How? When? Where? How much? How often?

**The Simple Test for Adverbs:**
Many adverbs end in "-ly," but not all. Ask yourself: Does this word tell me HOW, WHEN, WHERE, or HOW MUCH about an action or description?

### Types of Adverbs Explained in Detail

#### 1. Adverbs of Manner (How?)

These adverbs tell us HOW an action is performed.

**Common -ly Adverbs:**
- **quickly** - "She **quickly** finished her homework." (tells us HOW she finished)
- **slowly** - "The turtle moved **slowly**." (tells us HOW the turtle moved)
- **carefully** - "He **carefully** carried the glass." (tells us HOW he carried it)
- **loudly** - "The baby cried **loudly**." (tells us HOW the baby cried)
- **quietly** - "We **quietly** entered the room." (tells us HOW we entered)

**Adverbs Without -ly:**
- **well** - "She sings **well**." (tells us HOW she sings)
- **fast** - "He runs **fast**." (tells us HOW he runs)
- **hard** - "They worked **hard**." (tells us HOW they worked)

#### 2. Adverbs of Time (When?)

These adverbs tell us WHEN an action happens.

**Specific Time:**
- **yesterday** - "I saw him **yesterday**." (tells us WHEN you saw him)
- **today** - "We have a test **today**." (tells us WHEN the test is)
- **tomorrow** - "She will call **tomorrow**." (tells us WHEN she will call)
- **now** - "Please come here **now**." (tells us WHEN to come)

**Frequency (How Often):**
- **always** - "I **always** brush my teeth." (tells us HOW OFTEN you brush)
- **never** - "He **never** eats vegetables." (tells us HOW OFTEN he eats them)
- **sometimes** - "We **sometimes** go to the park." (tells us HOW OFTEN you go)
- **often** - "She **often** helps her mother." (tells us HOW OFTEN she helps)
- **rarely** - "They **rarely** watch TV." (tells us HOW OFTEN they watch)

#### 3. Adverbs of Place (Where?)

These adverbs tell us WHERE an action happens.

- **here** - "Please sit **here**." (tells us WHERE to sit)
- **there** - "The book is **there**." (tells us WHERE the book is)
- **everywhere** - "I looked **everywhere** for my keys." (tells us WHERE you looked)
- **outside** - "The children are playing **outside**." (tells us WHERE they're playing)
- **inside** - "Come **inside** the house." (tells us WHERE to come)
- **upstairs** - "My room is **upstairs**." (tells us WHERE the room is)
- **downstairs** - "The kitchen is **downstairs**." (tells us WHERE the kitchen is)

#### 4. Adverbs of Degree (How Much?)

These adverbs tell us HOW MUCH or TO WHAT EXTENT something happens.

- **very** - "She is **very** smart." (tells us HOW MUCH smart she is)
- **quite** - "The movie was **quite** good." (tells us HOW MUCH good it was)
- **extremely** - "The weather is **extremely** hot." (tells us HOW MUCH hot it is)
- **barely** - "I can **barely** hear you." (tells us HOW MUCH you can hear)
- **almost** - "We're **almost** finished." (tells us HOW MUCH finished you are)
- **completely** - "I **completely** forgot." (tells us HOW MUCH you forgot)

### How Adverbs Make Sentences More Interesting

**Without adverbs (basic):**
"The dog ran."

**With adverbs (detailed):**
"The dog **quickly** ran **outside** **yesterday**."

Now we know HOW the dog ran (quickly), WHERE it ran (outside), and WHEN it ran (yesterday).

### Common Mistakes with Adverbs

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

## Conclusion: Putting It All Together

Understanding these parts of speech is like learning the ingredients for cooking. Once you know what each ingredient does, you can combine them to create delicious sentences that communicate exactly what you mean.

**Remember:**
- **Nouns** name things (people, places, objects, ideas)
- **Pronouns** replace nouns to avoid repetition
- **Verbs** show action or state of being
- **Adjectives** describe nouns and pronouns
- **Adverbs** describe verbs, adjectives, and other adverbs

**Practice Daily:**
- Read sentences and identify each part of speech
- Write your own sentences using different types of words
- Pay attention to how professional writers use these parts of speech
- Don't be afraid to make mistakes - that's how you learn!

The more you practice, the more natural these concepts will become. Soon, you'll be using proper grammar without even thinking about it!"""

        # Create the new comprehensive study note
        study_note = StudyNote.objects.create(
            topic=topic,
            title="Complete Self-Teaching Guide to Grammar and Sentence Structure",
            content=comprehensive_content,
            order=1,
            is_active=True
        )
        
        print(f"✅ Created truly comprehensive study note: {study_note.title}")
        print(f"📝 Content length: {len(comprehensive_content):,} characters")
        print(f"📖 Word count: ~{len(comprehensive_content.split()):,} words")
        print("🎯 Content is now truly self-explanatory and teaches from scratch!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Create truly comprehensive grammar notes"""
    success = create_comprehensive_grammar_notes()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("Grammar notes are now truly comprehensive and self-explanatory!")
        print("Students can learn from scratch without any prior knowledge.")
    else:
        print("\n❌ FAILED!")
        print("Could not create the content. Check the error above.")

if __name__ == '__main__':
    main()
