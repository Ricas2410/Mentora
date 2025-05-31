#!/usr/bin/env python3
"""
Script to update Grade 5 English study notes with comprehensive, educational content
Real-life examples and practical applications for better learning
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

def update_complex_texts_notes(topic, admin_user):
    """Update Complex Texts study notes with comprehensive content"""
    content = """# Understanding Complex Texts

## What Are Complex Texts?
Complex texts are reading materials that challenge you to think deeply and use advanced reading skills. These texts often have:
- **Sophisticated vocabulary** - Words that are not commonly used in everyday conversation
- **Complex sentence structures** - Long sentences with multiple clauses
- **Abstract concepts** - Ideas that require critical thinking to understand
- **Multiple layers of meaning** - Surface meaning and deeper, hidden meanings

## Types of Complex Texts You'll Encounter

### 1. Informational Texts
- **Scientific articles** about discoveries and research
- **Historical documents** like speeches and letters
- **News articles** about current events
- **Biographies** of important people
- **Technical manuals** and instructions

### 2. Literary Texts
- **Classic novels** and short stories
- **Poetry** with figurative language
- **Plays and dramas**
- **Essays** by famous authors

## Reading Strategies for Complex Texts

### Before Reading
1. **Preview the text** - Look at headings, subheadings, and images
2. **Activate prior knowledge** - Think about what you already know about the topic
3. **Set a purpose** - Decide why you're reading this text
4. **Predict** - Make educated guesses about what the text will discuss

### During Reading
1. **Read slowly and carefully** - Don't rush through difficult passages
2. **Use context clues** - Look at surrounding words to understand unfamiliar vocabulary
3. **Visualize** - Create mental pictures of what you're reading
4. **Ask questions** - Wonder about the author's purpose and meaning
5. **Make connections** - Link new information to what you already know
6. **Take notes** - Write down important ideas and unfamiliar words

### After Reading
1. **Summarize** - Retell the main ideas in your own words
2. **Analyze** - Think about the author's purpose and techniques
3. **Evaluate** - Form opinions about the text's quality and message
4. **Reflect** - Consider how the text relates to your life and other readings

## Understanding Text Structure

### Chronological Order
Events are presented in the order they happened in time.
**Signal words:** first, next, then, finally, before, after, during

### Cause and Effect
Shows how one event leads to another.
**Signal words:** because, since, as a result, therefore, consequently

### Compare and Contrast
Examines similarities and differences between two or more things.
**Signal words:** similarly, however, on the other hand, in contrast, likewise

### Problem and Solution
Presents a problem and explains how it was or could be solved.
**Signal words:** problem, solution, challenge, resolve, overcome

### Description
Provides detailed information about a topic.
**Signal words:** for example, such as, including, characteristics, features

## Vocabulary Strategies

### Context Clues
1. **Definition clues** - The meaning is explained in the sentence
2. **Example clues** - Examples help you understand the word
3. **Contrast clues** - The opposite meaning is given
4. **Inference clues** - You must use logic to figure out the meaning

### Word Parts
- **Prefixes** - Word parts added to the beginning (un-, re-, pre-)
- **Suffixes** - Word parts added to the end (-tion, -ment, -ly)
- **Root words** - The main part of the word that carries meaning

## Critical Thinking Skills

### Analyzing Author's Purpose
Ask yourself:
- Why did the author write this?
- What message are they trying to convey?
- Who is the intended audience?
- What techniques did they use to persuade or inform?

### Identifying Bias
Look for:
- One-sided arguments
- Emotional language
- Missing information
- Unfair generalizations

### Making Inferences
Use clues from the text plus your own knowledge to:
- Understand implied meanings
- Predict what might happen next
- Draw logical conclusions

## Real-Life Applications

### Academic Success
- **Research projects** - Understanding complex sources
- **Test preparation** - Analyzing reading passages
- **Essay writing** - Using evidence from complex texts

### Future Career Skills
- **Professional communication** - Reading reports and proposals
- **Problem-solving** - Analyzing complex information
- **Critical thinking** - Evaluating sources and making decisions

## Practice Tips

1. **Start with shorter complex texts** and gradually work up to longer ones
2. **Read a variety of genres** to build different skills
3. **Discuss texts with others** to gain new perspectives
4. **Keep a vocabulary journal** of new words you encounter
5. **Practice regularly** - Complex reading skills improve with consistent effort

Remember: Reading complex texts is like building muscle - the more you practice, the stronger your reading skills become!"""

    # Update or create the study note
    study_note, created = StudyNote.objects.update_or_create(
        topic=topic,
        title="Understanding Complex Texts - Complete Guide",
        defaults={
            'content': content,
            'order': 1,
            'is_active': True,
            'created_by': admin_user
        }
    )

    action = "Created" if created else "Updated"
    print(f"    {action} comprehensive study note for Complex Texts")

def update_advanced_grammar_notes(topic, admin_user):
    """Update Advanced Grammar study notes with comprehensive content"""
    content = """# Advanced Grammar Concepts

## Understanding Sentence Structure

### Simple Sentences
A simple sentence has one independent clause (complete thought).
**Examples:**
- The dog barked.
- Sarah completed her homework quickly.
- The beautiful sunset painted the sky orange and pink.

### Compound Sentences
Two or more independent clauses joined by coordinating conjunctions (FANBOYS: for, and, nor, but, or, yet, so).
**Examples:**
- I wanted to go to the movies, but I had too much homework.
- The rain stopped, and the sun came out.
- We can walk to school, or we can take the bus.

### Complex Sentences
One independent clause and one or more dependent clauses.
**Examples:**
- Because it was raining, we stayed inside. (dependent clause first)
- We stayed inside because it was raining. (independent clause first)
- The book that I borrowed from the library was fascinating.

### Compound-Complex Sentences
Two or more independent clauses and one or more dependent clauses.
**Example:** Although it was late, we finished our project, and we felt proud of our work.

## Advanced Punctuation

### Semicolons (;)
1. **Connect related independent clauses:**
   - The weather was perfect; we decided to have a picnic.
2. **Separate items in a complex list:**
   - We visited Paris, France; Rome, Italy; and Madrid, Spain.

### Colons (:)
1. **Introduce a list after a complete sentence:**
   - I need three things: milk, eggs, and bread.
2. **Introduce an explanation or example:**
   - She had one goal: to become a doctor.

### Dashes (—)
1. **Show sudden breaks in thought:**
   - The weather was beautiful—until it started raining.
2. **Emphasize information:**
   - My favorite subject—mathematics—requires lots of practice.

## Subject-Verb Agreement

### Basic Rules
1. **Singular subjects take singular verbs:**
   - The cat sleeps on the couch.
2. **Plural subjects take plural verbs:**
   - The cats sleep on the couch.

### Tricky Situations
1. **Subjects joined by "and" are usually plural:**
   - Tom and Jerry are cartoon characters.
2. **Subjects joined by "or" or "nor" agree with the closest subject:**
   - Neither the teacher nor the students were ready.
3. **Collective nouns can be singular or plural:**
   - The team is winning. (acting as one unit)
   - The team are arguing among themselves. (acting as individuals)

## Pronoun Usage

### Pronoun-Antecedent Agreement
The pronoun must agree with its antecedent in number and gender.
**Examples:**
- Each student must bring his or her pencil. (singular)
- The students must bring their pencils. (plural)

### Common Pronoun Problems
1. **Who vs. Whom:**
   - Who is the subject: Who is coming to dinner?
   - Whom is the object: To whom did you give the book?

2. **Its vs. It's:**
   - Its = possessive: The dog wagged its tail.
   - It's = it is: It's raining outside.

## Modifiers

### Adjectives vs. Adverbs
- **Adjectives modify nouns:** The quick runner won the race.
- **Adverbs modify verbs, adjectives, or other adverbs:** She ran quickly.

### Misplaced Modifiers
Place modifiers close to the words they modify.
**Incorrect:** I saw a dog walking down the street with spots.
**Correct:** I saw a spotted dog walking down the street.

### Dangling Modifiers
Make sure the modifier has a clear word to modify.
**Incorrect:** Running quickly, the bus was missed.
**Correct:** Running quickly, Sarah missed the bus.

## Parallel Structure

Keep similar elements in the same grammatical form.
**Incorrect:** She likes swimming, running, and to bike.
**Correct:** She likes swimming, running, and biking.

## Advanced Verb Forms

### Perfect Tenses
1. **Present Perfect:** I have finished my homework.
2. **Past Perfect:** I had finished my homework before dinner.
3. **Future Perfect:** I will have finished my homework by tomorrow.

### Progressive Tenses
1. **Present Progressive:** I am working on my project.
2. **Past Progressive:** I was working when you called.
3. **Future Progressive:** I will be working tomorrow.

## Common Grammar Mistakes to Avoid

### 1. Sentence Fragments
**Incorrect:** Because I was tired.
**Correct:** I went to bed early because I was tired.

### 2. Run-on Sentences
**Incorrect:** I love reading books they transport me to different worlds.
**Correct:** I love reading books because they transport me to different worlds.

### 3. Comma Splices
**Incorrect:** It's raining, I'll stay inside.
**Correct:** It's raining, so I'll stay inside.

## Real-Life Applications

### Academic Writing
- **Essays and reports** require proper grammar for clarity
- **Research papers** need advanced sentence structures
- **Presentations** benefit from varied sentence types

### Professional Communication
- **Business emails** require proper punctuation and grammar
- **Job applications** must be grammatically correct
- **Professional reports** need clear, well-structured sentences

### Creative Writing
- **Stories and poems** use advanced grammar for effect
- **Dialogue** requires proper punctuation
- **Descriptive writing** benefits from varied sentence structures

## Practice Strategies

1. **Read quality literature** to see grammar in action
2. **Write regularly** and focus on one grammar concept at a time
3. **Edit your work** carefully, checking for specific grammar rules
4. **Use grammar resources** like style guides and online tools
5. **Ask for feedback** from teachers and peers

Remember: Good grammar is like a clear window—it lets your ideas shine through without distraction!"""

    # Update or create the study note
    study_note, created = StudyNote.objects.update_or_create(
        topic=topic,
        title="Advanced Grammar Concepts - Complete Guide",
        defaults={
            'content': content,
            'order': 1,
            'is_active': True,
            'created_by': admin_user
        }
    )

    action = "Created" if created else "Updated"
    print(f"    {action} comprehensive study note for Advanced Grammar")

def update_research_skills_notes(topic, admin_user):
    """Update Research Skills study notes with comprehensive content"""
    content = """# Research Skills for Students

## What is Research?
Research is the process of finding, evaluating, and using information to answer questions or solve problems. Good research skills help you:
- **Find reliable information** from trustworthy sources
- **Organize your findings** in a logical way
- **Present your discoveries** clearly to others
- **Avoid plagiarism** by giving proper credit

## The Research Process

### Step 1: Choose and Narrow Your Topic
1. **Start broad, then narrow down:**
   - Broad: Animals
   - Narrower: Endangered animals
   - Specific: How climate change affects polar bears

2. **Make sure your topic is:**
   - **Interesting** to you
   - **Appropriate** for your assignment
   - **Manageable** in scope
   - **Researchable** with available sources

### Step 2: Ask Research Questions
Good research questions guide your investigation:
- **What** happened?
- **Who** was involved?
- **When** did it occur?
- **Where** did it take place?
- **Why** did it happen?
- **How** did it work?

**Example:** If researching polar bears:
- How has Arctic ice loss affected polar bear populations?
- What adaptations help polar bears survive in their environment?

### Step 3: Find and Evaluate Sources

#### Types of Sources
1. **Primary Sources** (firsthand information):
   - Interviews with experts
   - Original documents and letters
   - Photographs and artifacts
   - Scientific studies and experiments

2. **Secondary Sources** (information about primary sources):
   - Encyclopedia articles
   - Textbooks
   - News articles
   - Documentary films

#### Evaluating Source Reliability
Ask these questions:
1. **Authority:** Who wrote this? Are they an expert?
2. **Accuracy:** Is the information correct and factual?
3. **Objectivity:** Is the author biased or fair?
4. **Currency:** Is the information current and up-to-date?
5. **Coverage:** Does it cover the topic thoroughly?

#### Website Evaluation
- **.edu** = Educational institutions (usually reliable)
- **.gov** = Government websites (usually reliable)
- **.org** = Organizations (check credibility)
- **.com** = Commercial sites (be more careful)

### Step 4: Take Effective Notes

#### Note-Taking Strategies
1. **Use your own words** (paraphrasing)
2. **Record source information** immediately
3. **Organize by topic** or research question
4. **Use quotation marks** for exact quotes
5. **Include page numbers** for reference

#### Note-Taking Methods
1. **Index cards** - One idea per card
2. **Digital notes** - Use apps or documents
3. **Graphic organizers** - Visual organization
4. **Cornell notes** - Structured format

### Step 5: Organize Your Information

#### Creating an Outline
1. **Introduction** - Hook, background, thesis
2. **Body paragraphs** - Main points with evidence
3. **Conclusion** - Summary and final thoughts

#### Grouping Information
- **By topic** - All information about one aspect together
- **By importance** - Most important points first
- **By chronology** - In time order
- **By comparison** - Similarities and differences

## Search Strategies

### Using Keywords Effectively
1. **Start with main concepts** from your research question
2. **Use synonyms** if first search doesn't work
3. **Combine keywords** with AND, OR, NOT
4. **Use quotation marks** for exact phrases

**Example:** "polar bear habitat" AND "climate change"

### Library Resources
1. **Online catalog** - Find books and materials
2. **Databases** - Access articles and journals
3. **Reference section** - Encyclopedias and almanacs
4. **Librarian help** - Expert assistance

### Internet Search Tips
1. **Use multiple search engines** (Google, Bing, Yahoo)
2. **Try different keyword combinations**
3. **Look beyond the first page** of results
4. **Use advanced search features**
5. **Check multiple sources** for the same information

## Avoiding Plagiarism

### What is Plagiarism?
Using someone else's words, ideas, or work without giving them credit. This includes:
- **Copying text** without quotation marks
- **Paraphrasing** without citing the source
- **Using images** without permission
- **Submitting someone else's work** as your own

### How to Avoid Plagiarism
1. **Always cite your sources** when you use information from them
2. **Use quotation marks** for exact words
3. **Paraphrase in your own words** and still cite the source
4. **Keep track of sources** as you research
5. **When in doubt, cite it**

### Citation Basics
Include this information for each source:
- **Author's name**
- **Title of work**
- **Publication date**
- **Publisher or website**
- **Page numbers** (for books/articles)
- **URL and access date** (for websites)

## Research Tools and Technology

### Digital Tools
1. **Citation managers** - Help organize sources
2. **Note-taking apps** - Digital organization
3. **Cloud storage** - Access from anywhere
4. **Collaboration tools** - Work with others

### Traditional Tools
1. **Library card catalog** - Find physical books
2. **Print encyclopedias** - Reliable reference
3. **Newspapers and magazines** - Current events
4. **Interviews** - Primary source information

## Presenting Your Research

### Writing Your Report
1. **Introduction** - Grab attention and state your thesis
2. **Body** - Present evidence and analysis
3. **Conclusion** - Summarize findings and implications
4. **Bibliography** - List all sources used

### Other Presentation Formats
- **Oral presentations** with visual aids
- **Posters** with key information
- **Digital presentations** with multimedia
- **Infographics** showing data visually

## Real-Life Applications

### Academic Success
- **School projects** require research skills
- **Science fair projects** need reliable sources
- **History reports** use primary and secondary sources
- **Current events** understanding requires source evaluation

### Future Career Skills
- **Problem-solving** in any job requires research
- **Decision-making** needs reliable information
- **Innovation** builds on existing knowledge
- **Communication** requires credible evidence

### Personal Life
- **Making purchases** - research products and reviews
- **Health decisions** - find reliable medical information
- **Travel planning** - research destinations and options
- **Hobbies** - learn new skills and techniques

## Practice Tips

1. **Start with topics you're interested in**
2. **Practice with short research projects**
3. **Use a variety of source types**
4. **Keep a research journal** of what you learn
5. **Ask for help** when you need it
6. **Check your work** for accuracy and completeness

Remember: Good research skills are like detective work - you're gathering clues to solve a mystery or answer important questions!"""

    # Update or create the study note
    study_note, created = StudyNote.objects.update_or_create(
        topic=topic,
        title="Research Skills for Students - Complete Guide",
        defaults={
            'content': content,
            'order': 1,
            'is_active': True,
            'created_by': admin_user
        }
    )

    action = "Created" if created else "Updated"
    print(f"    {action} comprehensive study note for Research Skills")

def main():
    """Main function to update study notes"""
    try:
        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No admin user found. Please create a superuser first.")
            return

        # Get Grade 5 English
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)

        print(f"📚 Updating comprehensive study notes for Grade 5 English topics...")

        # Get topics
        topics = {
            'complex_texts': Topic.objects.get(class_level=grade5, title='Complex Texts'),
            'advanced_grammar': Topic.objects.get(class_level=grade5, title='Advanced Grammar'),
            'research_skills': Topic.objects.get(class_level=grade5, title='Research Skills'),
        }

        # Update study notes for each topic
        update_complex_texts_notes(topics['complex_texts'], admin_user)
        update_advanced_grammar_notes(topics['advanced_grammar'], admin_user)
        update_research_skills_notes(topics['research_skills'], admin_user)

        print("✅ Successfully updated comprehensive study notes!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
