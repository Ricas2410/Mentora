#!/usr/bin/env python
"""
Grammar Part 2: Comprehensive Verbs and Tenses
Self-explanatory content that teaches from scratch
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice

def create_verbs_tenses_content():
    """Create comprehensive verbs and tenses content"""
    print("CREATING COMPREHENSIVE VERBS AND TENSES CONTENT")
    print("=" * 60)
    
    try:
        # Find the topic
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topic = Topic.objects.get(title="Grammar and Sentence Structure", class_level=class_level)
        
        print(f"Found topic: {topic.title}")
        
        # Create Part 2: Verbs and Tenses
        part2_content = """# Part 2: Understanding Verbs and Tenses

## What Exactly is a Verb?

A verb is a word that shows action or state of being. Verbs are the "engine" of every sentence - they make things happen or describe how things are.

**Every complete sentence must have a verb.** Without a verb, you don't have a complete thought.

Think of verbs as the "movie" part of a sentence:
- Nouns are like the "actors" (who or what)
- Verbs are like the "action" (what happens)

---

## Types of Verbs Explained in Detail

### 1. Action Verbs

Action verbs show what someone or something does. These are the "doing" words.

#### Physical Action Verbs (actions you can see)

**What are physical action verbs?**
These are actions that you can actually watch someone do. If you can see the movement or activity happening, it's a physical action verb.

**Examples with detailed explanations:**
- **run** - "She **runs** every morning." 
  - You can see someone running - their legs moving, their body moving forward
  - This is something that happens in the physical world
- **jump** - "The cat **jumped** over the fence." 
  - You can see the jumping motion - the cat leaving the ground and going over something
- **write** - "I **write** in my journal." 
  - You can see the writing action - the hand moving, the pen making marks on paper
- **cook** - "Mom **cooks** dinner." 
  - You can see the cooking process - stirring, chopping, using the stove
- **dance** - "They **dance** at the party." 
  - You can see the dancing movements - bodies moving to music

#### Mental Action Verbs (actions that happen in your mind)

**What are mental action verbs?**
These are actions that happen inside your head. You can't see them happening, but they're still actions because your mind is "doing" something.

**Examples with detailed explanations:**
- **think** - "I **think** about my future." 
  - This happens in your mind - you're actively using your brain to consider something
  - Even though you can't see thinking, your mind is working
- **believe** - "She **believes** in herself." 
  - This is a mental state where someone accepts something as true
  - It's an action of the mind, not the body
- **remember** - "He **remembers** his childhood." 
  - This is your mind actively bringing back past experiences
  - Your brain is "doing" the work of recalling information
- **understand** - "We **understand** the lesson." 
  - This is your mind grasping or comprehending information
  - Your brain is actively processing and making sense of something
- **imagine** - "They **imagine** flying." 
  - This is your mind creating pictures or ideas that aren't real
  - Your brain is actively creating mental images

### 2. Linking Verbs

Linking verbs don't show action. Instead, they connect the subject to more information about the subject. They're like an equals sign (=) in math.

**What do linking verbs do?**
Linking verbs tell us what someone or something IS, not what they DO. They link (connect) the subject to a description or identification.

#### The Most Common Linking Verb: Forms of "BE"

**Present tense forms:**
- **am** - "I **am** happy." (I = happy)
  - Use "am" only with "I"
  - This tells us what you ARE right now
- **is** - "She **is** a teacher." (She = a teacher)
  - Use "is" with he, she, it, or singular nouns
  - This tells us what someone or something IS
- **are** - "They **are** friends." (They = friends)
  - Use "are" with you, we, they, or plural nouns
  - This tells us what multiple people or things ARE

**Past tense forms:**
- **was** - "He **was** tired." (He = tired, in the past)
  - Use "was" with I, he, she, it, or singular nouns
  - This tells us what someone or something WAS in the past
- **were** - "We **were** excited." (We = excited, in the past)
  - Use "were" with you, we, they, or plural nouns
  - This tells us what people or things WERE in the past

**Other forms:**
- **being** - "You are **being** helpful." (You = helpful, right now)
- **been** - "I have **been** sick." (I = sick, recently)

#### Other Linking Verbs

**Examples with detailed explanations:**
- **seem** - "You **seem** worried." (You = worried, apparently)
  - This means you appear to be worried based on what we can observe
- **appear** - "She **appears** confident." (She = confident, from what we can see)
  - This means she looks confident to us
- **become** - "He **became** a doctor." (He = a doctor, after change)
  - This shows a change from not being a doctor to being a doctor
- **feel** - "I **feel** excited." (I = excited, emotionally)
  - This describes your emotional state
- **look** - "You **look** tired." (You = tired, from appearance)
  - This describes how you appear to others
- **sound** - "That **sounds** interesting." (That = interesting, from what we hear)
  - This describes how something seems based on what we hear

#### How to Test if a Verb is Linking

**The Equals Test:**
Replace the verb with "=" (equals). If the sentence still makes sense, it's a linking verb.

**Examples:**
- "She **is** happy." → "She = happy." ✓ (Makes sense, so "is" is linking)
- "She **runs** fast." → "She = fast." ✗ (Doesn't make sense, so "runs" is action)
- "The music **sounds** loud." → "The music = loud." ✓ (Makes sense, so "sounds" is linking)
- "He **plays** music." → "He = music." ✗ (Doesn't make sense, so "plays" is action)

### 3. Helping Verbs

Helping verbs work together with main verbs to show different meanings like time, possibility, or necessity.

**What do helping verbs do?**
Helping verbs are like assistants - they help the main verb express more complex ideas. They can show:
- When something happens (time)
- Whether something might happen (possibility)
- Whether something should happen (necessity)

#### Common Helping Verb Combinations

**am, is, are + main verb ending in -ing (Present Continuous)**
- "I **am studying**." (happening right now)
  - "am" = helping verb, "studying" = main verb
  - This shows an action happening at this moment
- "She **is reading**." (happening right now)
  - "is" = helping verb, "reading" = main verb
- "They **are playing**." (happening right now)
  - "are" = helping verb, "playing" = main verb

**has, have + past participle (Present Perfect)**
- "I **have finished** my homework." (completed recently)
  - "have" = helping verb, "finished" = main verb
  - This shows something completed in the recent past that affects now
- "She **has eaten** lunch." (completed recently)
  - "has" = helping verb, "eaten" = main verb

**will + main verb (Future)**
- "I **will go** tomorrow." (future action)
  - "will" = helping verb, "go" = main verb
  - This shows something that will happen in the future
- "She **will help** you." (future action)
  - "will" = helping verb, "help" = main verb

**can, could + main verb (Ability/Possibility)**
- "I **can swim**." (ability)
  - "can" = helping verb, "swim" = main verb
  - This shows you have the ability to swim
- "She **could help** if needed." (possibility)
  - "could" = helping verb, "help" = main verb
  - This shows it's possible for her to help

**should, would + main verb (Advice/Politeness)**
- "You **should study**." (advice)
  - "should" = helping verb, "study" = main verb
  - This gives advice about what would be good to do
- "I **would like** some water." (polite request)
  - "would" = helping verb, "like" = main verb
  - This is a polite way to ask for something

---

## Understanding Verb Tenses - When Things Happen

Verb tenses tell us WHEN an action happens. Think of tenses as time stamps for actions.

### Present Tense - Happening Now or Regularly

#### Simple Present

**What is simple present?**
Simple present shows actions that:
- Happen regularly (habits)
- Are always true (facts)
- Describe current states

**Examples with explanations:**
- **Facts:** "The sun **rises** in the east."
  - This is always true, every day
- **Habits:** "I **brush** my teeth every morning."
  - This is something you do regularly
- **Current states:** "She **lives** in Chicago."
  - This describes where she lives right now

#### Present Continuous (Progressive)

**What is present continuous?**
Present continuous shows actions that are happening right now or temporarily.

**How to form it:** am/is/are + verb + ing

**Examples with explanations:**
- **Right now:** "I **am writing** a text message."
  - This is happening at this exact moment
- **Temporary situations:** "He **is staying** with his grandparents this week."
  - This is not permanent, just for this week

#### Present Perfect

**What is present perfect?**
Present perfect shows actions that started in the past but affect the present.

**How to form it:** has/have + past participle

**Examples with explanations:**
- **Past action affecting now:** "I **have finished** my homework." (so now I'm free)
  - The finishing happened in the past, but the result (being free) is now
- **Experience:** "She **has visited** Paris." (in her lifetime)
  - The visiting happened sometime in the past, but we're talking about her experience now

### Past Tense - Already Happened

#### Simple Past

**What is simple past?**
Simple past shows actions that were completed in the past.

**How to form it:**
- Regular verbs: add -ed (walk → walked, play → played)
- Irregular verbs: change form (go → went, eat → ate, see → saw)

**Examples with explanations:**
- "Yesterday, I **walked** to school."
  - This action was completed yesterday
- "She **ate** breakfast an hour ago."
  - The eating was finished an hour ago
- "They **went** to the movies last night."
  - The going happened and ended last night

#### Past Continuous

**What is past continuous?**
Past continuous shows actions that were ongoing in the past.

**How to form it:** was/were + verb + ing

**Examples with explanations:**
- **Ongoing past action:** "I **was watching** TV when you called."
  - The watching was in progress when something else happened
- **Two past actions:** "While she **was cooking**, he **was setting** the table."
  - Both actions were happening at the same time in the past

#### Past Perfect

**What is past perfect?**
Past perfect shows an action that happened before another past action.

**How to form it:** had + past participle

**Examples with explanations:**
- "I **had eaten** dinner before the movie started."
  - First: eating dinner (past perfect)
  - Second: movie starting (simple past)
  - The eating was completely finished before the movie began

### Future Tense - Will Happen

#### Simple Future

**What is simple future?**
Simple future shows actions that will happen later.

**How to form it:**
- will + verb: "I **will call** you tomorrow."
- going to + verb: "We **are going to** have pizza tonight."

**Examples with explanations:**
- "I **will call** you tomorrow."
  - This is a promise or plan for the future
- "We **are going to** have pizza tonight."
  - This is a plan that's already decided

#### Future Continuous

**What is future continuous?**
Future continuous shows actions that will be ongoing at a specific time in the future.

**How to form it:** will be + verb + ing

**Examples with explanations:**
- "This time tomorrow, I **will be flying** to New York."
  - At this exact time tomorrow, the flying will be in progress

### Real-Life Tense Examples

**Comparing the same action in different tenses:**

**Present:** 
- "I **am** hungry." (right now)
- "I **eat** breakfast every day." (habit)

**Past:** 
- "I **was** hungry." (earlier)
- "I **ate** breakfast an hour ago." (completed action)

**Future:** 
- "I **will be** hungry." (later)
- "I **will eat** breakfast tomorrow." (planned action)

---

## Why Understanding Verbs and Tenses Matters

When you understand verbs and tenses, you can:
1. **Express time clearly** - People know when things happen
2. **Tell stories better** - You can show the order of events
3. **Give clear instructions** - You can tell people what to do
4. **Describe situations accurately** - You can explain what's happening
5. **Sound more professional** - Correct verb usage shows education

**Practice Daily:**
- Identify verbs in sentences you read
- Practice changing verbs to different tenses
- Pay attention to when actions happen
- Use helping verbs to express complex ideas

The more you practice with verbs and tenses, the more naturally you'll express time and action in your communication!"""

        # Create the study note
        study_note = StudyNote.objects.create(
            topic=topic,
            title="Part 2: Understanding Verbs and Tenses",
            content=part2_content,
            order=2,
            is_active=True
        )
        
        print(f"✅ Created Part 2: {study_note.title}")
        print(f"📝 Content length: {len(part2_content):,} characters")
        print(f"📖 Word count: ~{len(part2_content.split()):,} words")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Create Part 2 of comprehensive grammar content"""
    success = create_verbs_tenses_content()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("Part 2 (Verbs and Tenses) created successfully!")
        print("Content is comprehensive and teaches from scratch.")
    else:
        print("\n❌ FAILED!")
        print("Could not create the content. Check the error above.")

if __name__ == '__main__':
    main()
