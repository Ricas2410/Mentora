#!/usr/bin/env python
"""
Update Spelling and Phonics with Comprehensive, Self-Explanatory Content
Professional content that students can understand independently
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

def update_phonics_content():
    """Update Spelling and Phonics with comprehensive, self-explanatory content"""
    print("UPDATING SPELLING AND PHONICS WITH COMPREHENSIVE CONTENT")
    print("=" * 60)
    
    try:
        # Find the topic
        subject = Subject.objects.get(name="English Language Arts")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
        topic = Topic.objects.get(title="Spelling and Phonics", class_level=class_level)
        
        print(f"Found topic: {topic.title}")
        
        # Delete existing notes to replace with comprehensive version
        existing_notes = topic.study_notes.all()
        print(f"Removing {existing_notes.count()} existing notes...")
        existing_notes.delete()
        
        # Create comprehensive phonics content
        comprehensive_content = """# Complete Guide to Spelling and Phonics

## What is Phonics?
Phonics is the relationship between letters (what you see) and sounds (what you hear). Understanding phonics helps you:
- **Read new words** by sounding them out
- **Spell words correctly** by knowing which letters make which sounds
- **Become a confident reader and writer**

Think of phonics as a secret code - once you know the code, you can unlock any word!

---

## Part 1: Letter Sounds (Phonemes)

### Single Letter Sounds
Each letter has a sound. Here are the most common sounds:

**Vowels (A, E, I, O, U):**
- **A:** /a/ as in "apple," "cat," "hat"
- **E:** /e/ as in "egg," "bed," "red"  
- **I:** /i/ as in "igloo," "sit," "big"
- **O:** /o/ as in "octopus," "hot," "dog"
- **U:** /u/ as in "umbrella," "cup," "run"

**Consonants:** Each has its own sound
- **B:** /b/ as in "ball," "baby," "crab"
- **C:** /k/ as in "cat," "car," "cup" (hard c)
- **D:** /d/ as in "dog," "door," "red"
- **F:** /f/ as in "fish," "fun," "leaf"
- **G:** /g/ as in "go," "big," "frog" (hard g)

### Practice Tip:
Say each sound out loud while looking at the letter. This helps your brain connect what you see with what you hear.

---

## Part 2: Letter Combinations (Digraphs)

Sometimes two letters work together to make one sound:

### Consonant Digraphs
- **CH:** /ch/ as in "chair," "cheese," "lunch"
- **SH:** /sh/ as in "ship," "fish," "wash"
- **TH:** /th/ as in "think," "bath," "three"
- **WH:** /wh/ as in "whale," "when," "white"
- **PH:** /f/ as in "phone," "graph," "elephant"

### Vowel Digraphs
- **AI:** /ay/ as in "rain," "train," "pain"
- **EA:** /ee/ as in "beach," "read," "team"
- **OA:** /oh/ as in "boat," "coat," "road"
- **EE:** /ee/ as in "tree," "see," "free"
- **OO:** /oo/ as in "moon," "food," "cool"

### Memory Trick:
"When two vowels go walking, the first one does the talking!" This means the first vowel usually says its name (long sound).

---

## Part 3: Blends (Two Sounds Together)

Blends are when you hear both letter sounds, but they're said quickly together:

### Beginning Blends
- **BL:** "black," "blue," "blow"
- **BR:** "brown," "bread," "bring"
- **CL:** "class," "clean," "close"
- **CR:** "crab," "cry," "cross"
- **DR:** "drive," "drop," "dream"
- **FL:** "flag," "fly," "flower"
- **FR:** "frog," "free," "friend"
- **GL:** "glad," "glass," "glue"
- **GR:** "green," "grow," "grass"
- **PL:** "play," "please," "plant"
- **PR:** "pretty," "price," "print"
- **SC:** "school," "scare," "score"
- **SK:** "skip," "sky," "skin"
- **SL:** "slow," "sleep," "slide"
- **SM:** "small," "smile," "smell"
- **SN:** "snow," "snake," "snack"
- **SP:** "spin," "speak," "sport"
- **ST:** "stop," "start," "story"
- **SW:** "swim," "sweet," "swing"
- **TR:** "tree," "try," "truck"
- **TW:** "twelve," "twin," "twist"

### Ending Blends
- **-ND:** "hand," "send," "kind"
- **-NT:** "want," "went," "plant"
- **-ST:** "best," "fast," "list"
- **-LT:** "salt," "belt," "melt"
- **-MP:** "jump," "camp," "lamp"

---

## Part 4: Long and Short Vowel Sounds

### Short Vowel Sounds (Quick and Crisp)
- **A:** "cat," "bat," "map" - sounds like /a/
- **E:** "bed," "red," "pen" - sounds like /e/
- **I:** "sit," "big," "win" - sounds like /i/
- **O:** "hot," "dog," "box" - sounds like /o/
- **U:** "cup," "run," "bus" - sounds like /u/

### Long Vowel Sounds (Say Their Names)
- **A:** "cake," "name," "play" - sounds like "ay"
- **E:** "tree," "see," "beach" - sounds like "ee"
- **I:** "bike," "time," "fly" - sounds like "eye"
- **O:** "boat," "home," "go" - sounds like "oh"
- **U:** "cute," "use," "music" - sounds like "you"

### The Magic E Rule
When a word ends with 'e', it often makes the vowel before it say its name (long sound):
- **cap** → **cape** (short a becomes long a)
- **bit** → **bite** (short i becomes long i)
- **hop** → **hope** (short o becomes long o)
- **cut** → **cute** (short u becomes long u)

---

## Part 5: Common Spelling Patterns

### The -CK Pattern
Use 'ck' after short vowels at the end of words:
- "back," "neck," "sick," "rock," "duck"

### The -TCH Pattern  
Use 'tch' after short vowels:
- "catch," "fetch," "pitch," "watch," "hutch"

### Double Letters
Double the consonant after short vowels:
- "bell," "kiss," "doll," "buzz," "egg"

---

## Part 6: Tricky Spelling Rules

### Rule 1: I Before E
"I before E, except after C, or when sounding like A as in neighbor and weigh"

**Examples:**
- **I before E:** believe, achieve, piece, field
- **E before I after C:** receive, ceiling, deceive
- **Sounds like A:** eight, weight, vein

**Common Exceptions:** weird, their, height, either

### Rule 2: Drop the E
When adding endings that start with vowels, drop the silent E:
- **make** + **ing** = making
- **hope** + **ed** = hoped
- **care** + **ing** = caring

### Rule 3: Change Y to I
When a word ends in Y after a consonant, change Y to I before adding endings:
- **happy** + **ness** = happiness
- **carry** + **ed** = carried
- **try** + **ed** = tried

### Rule 4: Doubling Rule
When adding endings to words with one syllable, one vowel, and one consonant, double the final consonant:
- **run** + **ing** = running
- **hop** + **ed** = hopped
- **big** + **est** = biggest

---

## Part 7: Syllables - Breaking Words Apart

A syllable is a word part with one vowel sound. Breaking long words into syllables makes them easier to read and spell.

### Types of Syllables:

1. **Closed Syllable:** Ends with a consonant, vowel is short
   - "cat," "pen," "sit"

2. **Open Syllable:** Ends with a vowel, vowel is long
   - "me," "go," "hi"

3. **Magic E Syllable:** Ends with consonant + e, first vowel is long
   - "cake," "bike," "home"

4. **Vowel Team Syllable:** Two vowels together
   - "rain," "boat," "team"

### Syllable Division Rules:
- **Between double consonants:** "rabbit" = rab-bit
- **Between different consonants:** "basket" = bas-ket
- **Before single consonant:** "tiger" = ti-ger

---

## Part 8: Prefixes and Suffixes

### Common Prefixes (Beginning Parts)
- **un-** = not (unhappy, unlock, unfair)
- **re-** = again (rewrite, redo, return)
- **pre-** = before (preview, prepay, preschool)
- **dis-** = not/opposite (disagree, dislike, disappear)
- **mis-** = wrong (mistake, misplace, misunderstand)

### Common Suffixes (Ending Parts)
- **-ing** = action happening now (running, playing, reading)
- **-ed** = action in the past (walked, jumped, played)
- **-er** = person who does (teacher, runner, player)
- **-est** = most (biggest, fastest, tallest)
- **-ly** = in this way (quickly, slowly, carefully)
- **-ful** = full of (helpful, colorful, peaceful)
- **-less** = without (careless, hopeless, fearless)

---

## Part 9: Homophones - Words That Sound the Same

Homophones sound identical but have different meanings and spellings:

### Common Homophones:
- **to/too/two:** "I want **to** go **too**, but **two** people are already going."
- **there/their/they're:** "**They're** going **there** to get **their** books."
- **your/you're:** "**You're** going to love **your** new bike."
- **its/it's:** "**It's** time to feed the dog **its** dinner."
- **hear/here:** "Come **here** so you can **hear** the music."

### Memory Tricks:
- **There** has "here" in it (place)
- **Their** has "heir" in it (ownership)
- **They're** = they are (contraction)

---

## Part 10: Reading Strategies Using Phonics

### When You See a New Word:
1. **Look for parts you know** (prefixes, suffixes, root words)
2. **Break it into syllables** (smaller chunks)
3. **Sound out each part** using phonics rules
4. **Blend the sounds together** to say the whole word
5. **Check if it makes sense** in the sentence

### Example: "unhappiness"
1. **un-** (prefix meaning "not")
2. **happy** (root word you know)
3. **-ness** (suffix meaning "state of being")
4. Put together: "not in a state of being happy"

---

## Part 11: Spelling Strategies

### Look, Say, Cover, Write, Check Method:
1. **Look** at the word carefully
2. **Say** the word out loud
3. **Cover** the word
4. **Write** the word from memory
5. **Check** your spelling against the original

### Memory Devices:
- **Mnemonics:** "Big Elephants Can Always Understand Small Elephants" (because)
- **Word families:** If you know "light," you can spell "night," "right," "sight"
- **Visualization:** Picture the word in your mind

### Common Spelling Mistakes to Avoid:
- **Silent letters:** "knee" (silent k), "lamb" (silent b)
- **Double letters:** "necessary," "embarrass," "accommodate"
- **Confusing endings:** "-tion" vs "-sion" (action vs mansion)

---

## Part 12: Practice Activities You Can Do

### Daily Practice Ideas:
1. **Word sorts:** Group words by spelling patterns
2. **Rhyme time:** Find words that rhyme and notice spelling patterns
3. **Syllable clapping:** Clap out syllables in words you hear
4. **Sound hunting:** Find objects that start with specific sounds
5. **Word building:** Use letter tiles to build words

### Reading Practice:
- Read aloud daily to practice phonics skills
- Point to words as you read them
- Sound out unfamiliar words using phonics rules
- Keep a list of new words you learn

### Writing Practice:
- Write in a journal daily
- Try spelling words before looking them up
- Use new vocabulary words in sentences
- Practice writing word families

---

## Remember: Phonics is a Tool, Not a Rule!

English has many exceptions, but phonics gives you a great starting point. When phonics doesn't work:
- **Ask someone** for help
- **Look it up** in a dictionary
- **Remember the word** for next time
- **Don't give up** - every reader faces tricky words!

The more you practice, the more automatic these skills become. Soon you'll be reading and spelling like a pro! 🌟"""

        # Create the new comprehensive study note
        study_note = StudyNote.objects.create(
            topic=topic,
            title="Complete Guide to Spelling and Phonics",
            content=comprehensive_content,
            order=1,
            is_active=True
        )
        
        print(f"✅ Created comprehensive study note: {study_note.title}")
        print(f"📝 Content length: {len(comprehensive_content)} characters")
        print("🎯 Content is now self-explanatory and professional!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Update phonics content"""
    success = update_phonics_content()
    
    if success:
        print("\n🎉 SUCCESS!")
        print("Spelling and Phonics now has comprehensive, self-explanatory content!")
        print("Students can learn independently without needing help elsewhere.")
    else:
        print("\n❌ FAILED!")
        print("Could not update the content. Check the error above.")

if __name__ == '__main__':
    main()
