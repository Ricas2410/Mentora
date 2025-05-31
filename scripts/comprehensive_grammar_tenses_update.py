#!/usr/bin/env python
"""
Comprehensive Grammar and Tenses Update
Professional, self-explanatory content with extensive real-life quizzes
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

def update_grammar_content():
    """Update Grammar and Sentence Structure with comprehensive content"""
    print("UPDATING GRAMMAR AND SENTENCE STRUCTURE")
    print("=" * 50)
    
    try:
        # Find the topic
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topic = Topic.objects.get(title="Grammar and Sentence Structure", class_level=class_level)
        
        print(f"Found topic: {topic.title}")
        print(f"Current notes: {topic.study_notes.count()}")
        print(f"Current questions: {topic.questions.count()}")
        
        # Delete existing notes to replace with comprehensive version
        existing_notes = topic.study_notes.all()
        print(f"Removing {existing_notes.count()} existing notes...")
        existing_notes.delete()
        
        # Create comprehensive grammar and tenses content
        comprehensive_content = """# Complete Guide to Grammar and Sentence Structure

## What is Grammar?
Grammar is the set of rules that helps us communicate clearly and effectively. Think of grammar as the "traffic rules" for language - it helps everyone understand each other!

---

## Part 1: Parts of Speech - The Building Blocks

### Nouns - Naming Words
Nouns name people, places, things, or ideas.

**Types of Nouns:**
- **Common nouns:** dog, school, book, happiness (general names)
- **Proper nouns:** Sarah, McDonald's, iPhone, Christmas (specific names - always capitalized)
- **Concrete nouns:** table, pizza, music (things you can see, hear, touch)
- **Abstract nouns:** love, courage, freedom (ideas and feelings, they are not physical things that can be seeen or touched.)

**Real-life examples:**
- "My **sister** goes to **Lincoln Elementary School**." (person + place)
- "The **excitement** about the **concert** was amazing!" (feeling + event)

### Pronouns - Replacement Words
Pronouns replace nouns to avoid repetition.

**Personal Pronouns:**
- **Subject:** I, you, he, she, it, we, they
- **Object:** me, you, him, her, it, us, them
- **Possessive:** my/mine, your/yours, his, her/hers, its, our/ours, their/theirs

**Real-life examples:**
- Instead of: "Sarah gave Sarah's book to Sarah's friend"
- Say: "Sarah gave **her** book to **her** friend"
- Text message: "Can **you** help **me** with **my** homework?"

### Verbs - Action and Being Words

**Action Verbs:** Show what someone or something does
- Physical actions: run, jump, write, cook, dance
- Mental actions: think, believe, remember, understand

**Linking Verbs:** Connect the subject to more information
- Forms of "be": am, is, are, was, were, being, been
- Other linking verbs: seem, appear, become, feel, look, sound

**Helping Verbs:** Work with main verbs
- am/is/are + verb + ing: "I **am studying**"
- has/have + past participle: "She **has finished**"
- will + verb: "We **will go**"

**Real-life examples:**
- "I **am texting** my friend." (helping + main verb)
- "The pizza **smells** delicious." (linking verb)
- "They **scored** the winning goal!" (action verb)

### Adjectives - Describing Words
Adjectives describe nouns and pronouns.

**Types:**
- **Size:** big, small, tiny, huge
- **Color:** red, blue, bright, dark
- **Shape:** round, square, curved
- **Opinion:** beautiful, funny, boring, amazing
- **Number:** one, first, many, several

**Real-life examples:**
- "I bought a **new, red** phone." (age + color)
- "That was the **best** movie ever!" (opinion)
- Social media post: "Had an **amazing** day at the **beautiful** beach!"

### Adverbs - Describing Action Words
Adverbs describe verbs, adjectives, or other adverbs.

**Types:**
- **How:** quickly, slowly, carefully, loudly
- **When:** yesterday, now, soon, always, never
- **Where:** here, there, everywhere, outside
- **How much:** very, quite, extremely, barely

**Real-life examples:**
- "She **quickly** finished her homework." (how)
- "We **always** eat dinner together." (when)
- "The music was **extremely** loud." (how much)

---

## Part 2: Verb Tenses - When Things Happen

### Present Tense - Happening Now

**Simple Present:**
- Facts: "The sun **rises** in the east."
- Habits: "I **brush** my teeth every morning."
- Current states: "She **lives** in Chicago."

**Present Continuous (Progressive):**
- Right now: "I **am writing** a text message."
- Temporary situations: "He **is staying** with his grandparents this week."

**Present Perfect:**
- Past action affecting now: "I **have finished** my homework." (so now I'm free)
- Experience: "She **has visited** Paris." (in her lifetime)

### Past Tense - Already Happened

**Simple Past:**
- Completed actions: "Yesterday, I **walked** to school."
- Regular verbs add -ed: walk → walked, play → played
- Irregular verbs change: go → went, eat → ate, see → saw

**Past Continuous:**
- Ongoing past action: "I **was watching** TV when you called."
- Two past actions: "While she **was cooking**, he **was setting** the table."

**Past Perfect:**
- Earlier past action: "I **had eaten** dinner before the movie started."

### Future Tense - Will Happen

**Simple Future:**
- Will + verb: "I **will call** you tomorrow."
- Going to + verb: "We **are going to** have pizza tonight."

**Future Continuous:**
- Ongoing future action: "This time tomorrow, I **will be flying** to New York."

**Real-life Tense Examples:**
- **Present:** "I **am** hungry." / "I **eat** breakfast every day."
- **Past:** "I **was** hungry." / "I **ate** breakfast an hour ago."
- **Future:** "I **will be** hungry." / "I **will eat** breakfast tomorrow."

---

## Part 3: Sentence Structure

### Complete Sentences
Every complete sentence needs:
1. **Subject:** Who or what the sentence is about
2. **Predicate:** What the subject does or is

**Examples:**
- "**Dogs** **bark**." (simple subject + simple predicate)
- "**My little sister** **loves chocolate ice cream**." (complete subject + complete predicate)

### Types of Sentences by Purpose

**Declarative (Statement):** Tells something
- "The movie starts at 7 PM."
- "I finished my homework."

**Interrogative (Question):** Asks something
- "What time does the movie start?"
- "Did you finish your homework?"

**Imperative (Command):** Tells someone to do something
- "Please close the door."
- "Turn off your phone."

**Exclamatory:** Shows strong emotion
- "What an amazing game!"
- "I can't believe we won!"

### Sentence Patterns

**Simple Sentences:** One independent clause
- "I like pizza."
- "The cat slept on the couch."

**Compound Sentences:** Two independent clauses joined by conjunctions
- "I like pizza, **but** my sister prefers burgers."
- "We studied hard, **so** we passed the test."

**Complex Sentences:** Independent clause + dependent clause
- "**When** the bell rings, class is over."
- "I'll help you **if** you need it."

---

## Part 4: Common Grammar Rules

### Subject-Verb Agreement
Subjects and verbs must match in number.

**Singular subjects** use singular verbs:
- "She **walks** to school." ✓
- "She **walk** to school." ✗

**Plural subjects** use plural verbs:
- "They **walk** to school." ✓
- "They **walks** to school." ✗

**Tricky situations:**
- "Everyone **is** here." (Everyone = singular)
- "The team **is** winning." (Team = one unit)
- "Five dollars **is** enough." (Amount = singular)

### Pronoun Agreement
Pronouns must match their antecedents.

**Examples:**
- "Each student should bring **his or her** lunch." ✓
- "Each student should bring **their** lunch." ✓ (now acceptable)
- "The dog wagged **its** tail." ✓
- "The dog wagged **it's** tail." ✗ (it's = it is)

### Capitalization Rules
- **First word** of sentences: "**T**he game was exciting."
- **Proper nouns:** **M**ary, **C**hicago, **M**onday, **D**ecember
- **Titles:** **D**r. Smith, **P**resident Lincoln
- **Important words in titles:** "**T**he **L**ion **K**ing"

### Punctuation Essentials

**Periods (.):** End statements
- "I love reading books."

**Question marks (?):** End questions
- "What's your favorite book?"

**Exclamation points (!):** Show strong emotion
- "That's incredible!"

**Commas (,):** Separate items, clauses, and phrases
- Lists: "I need apples, bananas, and oranges."
- Before conjunctions: "I studied hard, but the test was difficult."
- After introductory words: "However, I still passed."

**Apostrophes ('):** Show possession or contractions
- Possession: "Sarah's book," "the dogs' toys"
- Contractions: "don't" (do not), "we're" (we are)

---

## Part 5: Common Mistakes to Avoid

### Your vs. You're
- **Your:** Shows ownership - "Is this **your** phone?"
- **You're:** Means "you are" - "**You're** going to love this movie!"

### Its vs. It's
- **Its:** Shows ownership - "The dog wagged **its** tail."
- **It's:** Means "it is" - "**It's** raining outside."

### There, Their, They're
- **There:** Place - "Put the book over **there**."
- **Their:** Ownership - "**Their** car is blue."
- **They're:** Means "they are" - "**They're** coming to dinner."

### Who vs. Whom
- **Who:** Subject - "**Who** is calling?"
- **Whom:** Object - "To **whom** should I give this?"
- **Tip:** If you can answer with "he," use "who." If you can answer with "him," use "whom."

---

## Part 6: Real-Life Grammar Applications

### Text Messages and Social Media
- Use complete sentences when possible
- Avoid excessive abbreviations in formal contexts
- Proofread before sending important messages

### School Writing
- Always use proper capitalization and punctuation
- Check subject-verb agreement
- Vary your sentence types for interest

### Speaking
- Use proper grammar in presentations and formal conversations
- Practice using different tenses correctly
- Pay attention to pronoun usage

### Future Success
- Good grammar helps in job interviews
- Clear communication builds better relationships
- Writing skills are essential in most careers

---

## Remember: Practice Makes Perfect!

Grammar might seem complicated, but with practice, it becomes natural. Start by focusing on one rule at a time, and soon you'll be using proper grammar without even thinking about it!

**Daily Practice Tips:**
- Read aloud to hear how sentences should sound
- Write in a journal using different tenses
- Pay attention to grammar in books and articles
- Ask for feedback on your writing
- Don't be afraid to make mistakes - that's how you learn!"""

        # Create the new comprehensive study note
        study_note = StudyNote.objects.create(
            topic=topic,
            title="Complete Guide to Grammar and Sentence Structure",
            content=comprehensive_content,
            order=1,
            is_active=True
        )
        
        print(f"✅ Created comprehensive study note: {study_note.title}")
        print(f"📝 Content length: {len(comprehensive_content):,} characters")
        print(f"📖 Word count: ~{len(comprehensive_content.split()):,} words")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Update grammar content"""
    success = update_grammar_content()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("Grammar and Sentence Structure now has comprehensive, self-explanatory content!")
        print("Next: Run the quiz addition script to add extensive real-life quizzes.")
    else:
        print("\n❌ FAILED!")
        print("Could not update the content. Check the error above.")

if __name__ == '__main__':
    main()
