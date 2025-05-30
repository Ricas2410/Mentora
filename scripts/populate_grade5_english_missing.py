#!/usr/bin/env python3
"""
Script to populate missing Grade 5 English Language Arts topics with real-life questions and study notes.
Focuses on: Complex Texts, Research Skills, Poetry Analysis, and Advanced Grammar study notes.
"""

import os
import sys
import django

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, StudyNote, AnswerChoice

def create_question_with_choices(topic, question_data):
    """Helper function to create a question with answer choices"""
    # Extract choices before creating question
    choices = question_data.pop('choices', [])

    # Create the question
    question = Question.objects.create(
        topic=topic,
        question_text=question_data['question_text'],
        question_type=question_data['question_type'],
        correct_answer=question_data['correct_answer'],
        explanation=question_data['explanation'],
        difficulty=question_data['difficulty'],
        points=question_data['points']
    )

    # Create answer choices
    for i, (choice_text, is_correct) in enumerate(choices):
        AnswerChoice.objects.create(
            question=question,
            choice_text=choice_text,
            is_correct=is_correct,
            order=i + 1
        )

    return question

def create_complex_texts_questions():
    """Create questions for Complex Texts topic"""
    try:
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)
        topic = Topic.objects.get(class_level=grade5, title='Complex Texts')

        questions = [
            {
                'question_text': 'Read this passage: "The ancient library stood majestically against the stormy sky, its weathered stones telling stories of centuries past." What does "majestically" mean in this context?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'Majestically means in a grand, impressive, or dignified manner.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Sadly', False),
                    ('Grandly', True),
                    ('Quickly', False),
                    ('Quietly', False)
                ]
            },
            {
                'question_text': 'In the sentence "The scientist\'s hypothesis was both innovative and controversial," what can you infer about the hypothesis?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'The hypothesis was new/creative (innovative) but also caused disagreement (controversial).',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('It was widely accepted', False),
                    ('It was old and outdated', False),
                    ('It was new but caused debate', True),
                    ('It was proven wrong', False)
                ]
            },
            {
                'question_text': 'What is the main purpose of a thesis statement in an essay?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'A thesis statement presents the main argument or central idea of an essay.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('To state the main argument', True),
                    ('To list all the topics', False),
                    ('To conclude the essay', False),
                    ('To introduce the author', False)
                ]
            },
            {
                'question_text': 'When reading a complex text, what should you do if you encounter an unfamiliar word?',
                'question_type': 'multiple_choice',
                'correct_answer': 'd',
                'explanation': 'Using context clues helps you understand unfamiliar words without stopping to look them up.',
                'difficulty': 'easy',
                'points': 1,
                'choices': [
                    ('Skip it completely', False),
                    ('Stop reading immediately', False),
                    ('Guess randomly', False),
                    ('Use context clues to understand it', True)
                ]
            },
            {
                'question_text': 'In a complex text, what is a "theme"?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'A theme is the central message or lesson that the author wants to convey.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('The title of the text', False),
                    ('The main message or lesson', True),
                    ('The number of pages', False),
                    ('The author\'s name', False)
                ]
            },
            {
                'question_text': 'Read this sentence: "The detective carefully examined the mysterious footprints in the garden." What does "examined" mean?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'Examined means to look at something closely and carefully to understand it better.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Ignored completely', False),
                    ('Looked at carefully', True),
                    ('Stepped on', False),
                    ('Cleaned up', False)
                ]
            },
            {
                'question_text': 'When reading a complex text about science, what should you do if you see unfamiliar scientific terms?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'Looking for definitions or explanations in the text helps you understand scientific terms without stopping your reading flow.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Skip the entire paragraph', False),
                    ('Stop reading immediately', False),
                    ('Look for definitions in the text', True),
                    ('Make up your own meaning', False)
                ]
            },
            {
                'question_text': 'In this passage: "The storm clouds gathered ominously overhead, casting dark shadows across the playground," what mood is created?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'Words like "ominously" and "dark shadows" create a threatening, scary mood.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Threatening and scary', True),
                    ('Happy and cheerful', False),
                    ('Calm and peaceful', False),
                    ('Exciting and fun', False)
                ]
            },
            {
                'question_text': 'What is the best way to understand the main idea of a complex paragraph?',
                'question_type': 'multiple_choice',
                'correct_answer': 'd',
                'explanation': 'Reading the paragraph multiple times helps you understand complex ideas better.',
                'difficulty': 'easy',
                'points': 1,
                'choices': [
                    ('Read only the first sentence', False),
                    ('Look at pictures only', False),
                    ('Count the number of words', False),
                    ('Read it several times', True)
                ]
            },
            {
                'question_text': 'In a complex text, what does "analyze" mean?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'To analyze means to break something down into parts to understand it better.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('To memorize exactly', False),
                    ('To read very quickly', False),
                    ('To break down and examine', True),
                    ('To copy word for word', False)
                ]
            },
            {
                'question_text': 'When you encounter a complex text about history, what should you look for first?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'Looking for dates and key events helps you understand the timeline and context of historical texts.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('The longest words', False),
                    ('Dates and key events', True),
                    ('The author\'s opinion only', False),
                    ('Pictures and illustrations only', False)
                ]
            },
            {
                'question_text': 'What does "synthesize information" mean when reading complex texts?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'Synthesizing means combining information from different parts to create a complete understanding.',
                'difficulty': 'hard',
                'points': 3,
                'choices': [
                    ('Combine ideas from different sources', True),
                    ('Read everything twice', False),
                    ('Write down every detail', False),
                    ('Focus on one paragraph only', False)
                ]
            },
            {
                'question_text': 'In complex texts, what are "supporting details"?',
                'question_type': 'multiple_choice',
                'correct_answer': 'd',
                'explanation': 'Supporting details are facts, examples, or evidence that help prove or explain the main idea.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('The title and headings', False),
                    ('The author\'s name', False),
                    ('The number of pages', False),
                    ('Facts that support the main idea', True)
                ]
            }
        ]

        created_count = 0
        for q_data in questions:
            if not Question.objects.filter(topic=topic, question_text=q_data['question_text']).exists():
                create_question_with_choices(topic, q_data.copy())
                created_count += 1

        print(f"    Created {created_count} new questions for Complex Texts")
        return created_count

    except Exception as e:
        print(f"Error creating Complex Texts questions: {e}")
        return 0

def create_research_skills_questions():
    """Create questions for Research Skills topic"""
    try:
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)
        topic = Topic.objects.get(class_level=grade5, title='Research Skills')

        questions = [
            {
                'question_text': 'What is the first step when starting a research project?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'Choosing a clear topic helps focus your research and makes it more manageable.',
                'difficulty': 'easy',
                'points': 1,
                'choices': [
                    ('Choose a clear topic', True),
                    ('Write the conclusion', False),
                    ('Find any random information', False),
                    ('Start writing immediately', False)
                ]
            },
            {
                'question_text': 'Which source would be most reliable for a school research project?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'Educational websites (.edu) are typically more reliable and fact-checked than social media or personal blogs.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('A friend\'s social media post', False),
                    ('A random blog', False),
                    ('An educational website', True),
                    ('An advertisement', False)
                ]
            },
            {
                'question_text': 'When taking notes from a source, what should you always include?',
                'question_type': 'multiple_choice',
                'correct_answer': 'd',
                'explanation': 'Recording where information comes from helps you cite sources properly and verify facts.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Only the interesting parts', False),
                    ('Your personal opinions', False),
                    ('Exact copies of everything', False),
                    ('The source information', True)
                ]
            },
            {
                'question_text': 'What does it mean to "cite a source"?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'Citing means giving credit to the original author or source of information you used.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('To copy everything exactly', False),
                    ('To give credit to the original author', True),
                    ('To disagree with the information', False),
                    ('To change the information', False)
                ]
            },
            {
                'question_text': 'Why is it important to use multiple sources when researching?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'Multiple sources help you get a complete picture and verify that information is accurate.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('To get a complete and accurate picture', True),
                    ('To make the project longer', False),
                    ('To confuse the reader', False),
                    ('To copy more information', False)
                ]
            },
            {
                'question_text': 'You are researching "healthy eating for kids" for a school project. Which website would be most trustworthy?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'Government health websites (.gov) provide reliable, fact-checked information about health topics.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('A candy company\'s website', False),
                    ('The Department of Health website', True),
                    ('A random food blog', False),
                    ('A social media post', False)
                ]
            },
            {
                'question_text': 'When researching animals for a science project, what information should you record about each source?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'Recording complete source information helps you cite properly and find the source again if needed.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Only the website name', False),
                    ('Just the interesting facts', False),
                    ('Author, title, date, and website', True),
                    ('Only the pictures', False)
                ]
            },
            {
                'question_text': 'You find conflicting information about recycling in two different sources. What should you do?',
                'question_type': 'multiple_choice',
                'correct_answer': 'd',
                'explanation': 'Finding a third source helps you verify which information is correct when sources disagree.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Use the first source you found', False),
                    ('Ignore both sources', False),
                    ('Make up your own facts', False),
                    ('Look for a third reliable source', True)
                ]
            },
            {
                'question_text': 'What is the best way to organize your research notes?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'Organizing notes by topic or question makes it easier to find information when writing your project.',
                'difficulty': 'easy',
                'points': 1,
                'choices': [
                    ('Group by topic or question', True),
                    ('Write everything in one long paragraph', False),
                    ('Copy everything exactly as written', False),
                    ('Only write down website names', False)
                ]
            },
            {
                'question_text': 'When researching for a project about your local community, which would be the best primary source?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'Interviewing community members gives you firsthand information directly from people who live there.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('A movie about communities', False),
                    ('Interviewing local residents', True),
                    ('A general encyclopedia article', False),
                    ('A story book about neighborhoods', False)
                ]
            },
            {
                'question_text': 'What should you do if you can\'t find enough information about your research topic?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'Changing your search terms or making your topic more specific can help you find better information.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Give up on the project', False),
                    ('Make up information', False),
                    ('Try different search words', True),
                    ('Use only one source', False)
                ]
            },
            {
                'question_text': 'Why is it important to check when a website was last updated?',
                'question_type': 'multiple_choice',
                'correct_answer': 'd',
                'explanation': 'Recent updates mean the information is more likely to be current and accurate.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('To see how old the computer is', False),
                    ('To count the number of visitors', False),
                    ('To find the website owner', False),
                    ('To make sure information is current', True)
                ]
            },
            {
                'question_text': 'When taking notes from a book for your research, what is the most important thing to remember?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'Writing in your own words shows you understand the information and helps avoid copying.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Write in your own words', True),
                    ('Copy everything exactly', False),
                    ('Only write down page numbers', False),
                    ('Use the same sentences as the book', False)
                ]
            }
        ]

        created_count = 0
        for q_data in questions:
            if not Question.objects.filter(topic=topic, question_text=q_data['question_text']).exists():
                create_question_with_choices(topic, q_data.copy())
                created_count += 1

        print(f"    Created {created_count} new questions for Research Skills")
        return created_count

    except Exception as e:
        print(f"Error creating Research Skills questions: {e}")
        return 0

def create_poetry_analysis_questions():
    """Create questions for Poetry Analysis topic"""
    try:
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)
        topic = Topic.objects.get(class_level=grade5, title='Poetry Analysis')

        questions = [
            {
                'question_text': 'What is a "stanza" in poetry?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'A stanza is a group of lines in a poem, similar to a paragraph in prose.',
                'difficulty': 'easy',
                'points': 1,
                'choices': [
                    ('A single word', False),
                    ('A group of lines', True),
                    ('The title', False),
                    ('The poet\'s name', False)
                ]
            },
            {
                'question_text': 'In the line "The wind whispered through the trees," what literary device is being used?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'Personification gives human qualities (whispering) to non-human things (wind).',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Personification', True),
                    ('Alliteration', False),
                    ('Rhyme', False),
                    ('Repetition', False)
                ]
            },
            {
                'question_text': 'What is the "mood" of a poem?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'Mood is the feeling or atmosphere that the poem creates for the reader.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('The number of lines', False),
                    ('The poet\'s age', False),
                    ('The feeling it creates', True),
                    ('The rhyme pattern', False)
                ]
            },
            {
                'question_text': 'Which words rhyme in this line: "The cat sat on the mat"?',
                'question_type': 'multiple_choice',
                'correct_answer': 'd',
                'explanation': 'Cat, sat, and mat all end with the same sound (-at), making them rhyme.',
                'difficulty': 'easy',
                'points': 1,
                'choices': [
                    ('The and on', False),
                    ('Cat and the', False),
                    ('Sat and on', False),
                    ('Cat, sat, and mat', True)
                ]
            },
            {
                'question_text': 'What is alliteration?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'Alliteration is when words close together start with the same sound, like "big blue balloon."',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Words that rhyme', False),
                    ('Words that start with the same sound', True),
                    ('Very long words', False),
                    ('Words that mean the same thing', False)
                ]
            },
            {
                'question_text': 'Read this line from a poem: "The golden sun danced across the sparkling waves." What two literary devices are used here?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'The sun "dancing" is personification (giving human actions to non-human things), and "golden" and "sparkling" are imagery (descriptive words that help you picture the scene).',
                'difficulty': 'hard',
                'points': 3,
                'choices': [
                    ('Personification and imagery', True),
                    ('Rhyme and repetition', False),
                    ('Alliteration and metaphor', False),
                    ('Simile and onomatopoeia', False)
                ]
            },
            {
                'question_text': 'In a poem about friendship, which line shows the theme best?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'This line directly expresses the value and importance of friendship, which would be the theme.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('My friend has brown hair', False),
                    ('We met at school yesterday', False),
                    ('True friends are treasures beyond gold', True),
                    ('The playground was very crowded', False)
                ]
            },
            {
                'question_text': 'What is a metaphor?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'A metaphor directly compares two things by saying one thing IS another, without using "like" or "as".',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('A comparison using "like" or "as"', False),
                    ('Saying one thing IS another thing', True),
                    ('Words that sound the same', False),
                    ('Repeating the same word', False)
                ]
            },
            {
                'question_text': 'Read this poem line: "The classroom buzzed like a busy beehive." What type of comparison is this?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'This is a simile because it uses "like" to compare the classroom to a beehive.',
                'difficulty': 'easy',
                'points': 1,
                'choices': [
                    ('Simile', True),
                    ('Metaphor', False),
                    ('Personification', False),
                    ('Alliteration', False)
                ]
            },
            {
                'question_text': 'In poetry, what does "rhythm" mean?',
                'question_type': 'multiple_choice',
                'correct_answer': 'd',
                'explanation': 'Rhythm is the pattern of beats or sounds in a poem, like the beat in music.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('The number of stanzas', False),
                    ('The rhyming words', False),
                    ('The poem\'s topic', False),
                    ('The pattern of beats', True)
                ]
            },
            {
                'question_text': 'Which line contains onomatopoeia?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'Onomatopoeia uses words that sound like the noise they describe. "Crash" sounds like the actual sound.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('The beautiful blue butterfly', False),
                    ('She runs like the wind', False),
                    ('The thunder went crash and boom', True),
                    ('My heart is full of joy', False)
                ]
            },
            {
                'question_text': 'When analyzing a poem about nature, what should you look for to understand the poet\'s feelings?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'The words a poet chooses (word choice) reveal their feelings and attitude toward the subject.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('Only the number of lines', False),
                    ('The poet\'s word choices', True),
                    ('The poem\'s title only', False),
                    ('How long the poem is', False)
                ]
            },
            {
                'question_text': 'Read this line: "The old oak tree stood like a wise grandfather, watching over the children." What does this comparison suggest about the tree?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'Comparing the tree to a wise grandfather suggests it is protective, caring, and has been there for a long time.',
                'difficulty': 'medium',
                'points': 2,
                'choices': [
                    ('It is protective and caring', True),
                    ('It is young and small', False),
                    ('It is dangerous and scary', False),
                    ('It is colorful and bright', False)
                ]
            }
        ]

        created_count = 0
        for q_data in questions:
            if not Question.objects.filter(topic=topic, question_text=q_data['question_text']).exists():
                create_question_with_choices(topic, q_data.copy())
                created_count += 1

        print(f"    Created {created_count} new questions for Poetry Analysis")
        return created_count

    except Exception as e:
        print(f"Error creating Poetry Analysis questions: {e}")
        return 0

def create_study_notes():
    """Create study notes for topics that need them"""
    try:
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)

        # Study notes data
        notes_data = [
            {
                'topic_title': 'Complex Texts',
                'title': 'Understanding Complex Texts',
                'content': '''# Understanding Complex Texts

## What are Complex Texts?
Complex texts are reading materials that challenge students with:
- Advanced vocabulary
- Sophisticated sentence structures
- Multiple themes or ideas
- Abstract concepts

## Reading Strategies
1. **Preview the text** - Look at headings, images, and structure
2. **Read actively** - Ask questions as you read
3. **Use context clues** - Figure out unknown words from surrounding text
4. **Take notes** - Write down main ideas and questions
5. **Reread difficult parts** - Don't be afraid to read sections multiple times

## Key Elements to Look For
- **Main idea** - What is the text mainly about?
- **Supporting details** - What evidence supports the main idea?
- **Author's purpose** - Why did the author write this?
- **Theme** - What lesson or message is being shared?

## Tips for Success
- Don't worry if you don't understand everything at first
- Look up important words you don't know
- Discuss the text with others
- Connect the text to your own experiences'''
            },
            {
                'topic_title': 'Research Skills',
                'title': 'Research Skills for Students',
                'content': '''# Research Skills for Students

## The Research Process
1. **Choose a topic** - Pick something specific and interesting
2. **Ask questions** - What do you want to learn?
3. **Find sources** - Look for reliable information
4. **Take notes** - Record important facts and ideas
5. **Organize information** - Put your findings in order
6. **Share your findings** - Present what you learned

## Good Sources vs. Bad Sources
### Good Sources:
- Educational websites (.edu)
- Library books
- Encyclopedias
- News articles from trusted sources
- Expert interviews

### Be Careful With:
- Social media posts
- Personal blogs
- Websites trying to sell something
- Information without an author listed

## Taking Good Notes
- Write in your own words
- Include where you found the information
- Note the date you found it
- Organize by topic or question

## Citing Sources
Always give credit when you use someone else's ideas:
- Include the author's name
- Include the title of the source
- Include when it was published
- Include where you found it'''
            },
            {
                'topic_title': 'Poetry Analysis',
                'title': 'Understanding and Analyzing Poetry',
                'content': '''# Understanding and Analyzing Poetry

## Elements of Poetry
### Structure
- **Lines** - Individual rows of text
- **Stanzas** - Groups of lines (like paragraphs)
- **Rhyme scheme** - Pattern of rhyming words

### Sound Devices
- **Rhyme** - Words that sound alike (cat/hat)
- **Alliteration** - Same starting sounds (big blue balloon)
- **Rhythm** - The beat or flow of the poem

### Literary Devices
- **Metaphor** - Comparing two things without using "like" or "as"
- **Simile** - Comparing using "like" or "as"
- **Personification** - Giving human qualities to non-human things

## How to Analyze a Poem
1. **Read it aloud** - Listen to the sounds and rhythm
2. **Look for patterns** - Notice rhymes and repetition
3. **Identify the speaker** - Who is talking in the poem?
4. **Find the theme** - What is the main message?
5. **Notice imagery** - What pictures does the poem create?

## Questions to Ask
- What is this poem about?
- How does it make me feel?
- What words or phrases stand out?
- What is the poet trying to tell me?
- How do the sounds add to the meaning?'''
            },
            {
                'topic_title': 'Advanced Grammar',
                'title': 'Advanced Grammar Concepts',
                'content': '''# Advanced Grammar Concepts

## Complex Sentence Structures
### Compound Sentences
- Join two complete thoughts with conjunctions (and, but, or, so)
- Example: "I studied hard, and I passed the test."

### Complex Sentences
- One main idea + one dependent clause
- Example: "Because I studied hard, I passed the test."

## Advanced Punctuation
### Semicolons (;)
- Connect related complete thoughts
- Example: "I love reading; books take me to new worlds."

### Colons (:)
- Introduce lists, explanations, or quotes
- Example: "I need three things: pencil, paper, and eraser."

## Verb Moods
### Indicative
- States facts: "The dog runs fast."

### Imperative
- Gives commands: "Run fast!"

### Subjunctive
- Expresses wishes or hypotheticals: "If I were rich, I would travel."

## Advanced Word Usage
### Homophones
- Words that sound the same but have different meanings
- Examples: there/their/they're, to/too/two

### Commonly Confused Words
- Affect vs. Effect
- Accept vs. Except
- Loose vs. Lose'''
            }
        ]

        created_count = 0
        for note_data in notes_data:
            topic = Topic.objects.get(class_level=grade5, title=note_data['topic_title'])

            if not StudyNote.objects.filter(topic=topic, title=note_data['title']).exists():
                StudyNote.objects.create(
                    topic=topic,
                    title=note_data['title'],
                    content=note_data['content']
                )
                created_count += 1
                print(f"    Created study note for {note_data['topic_title']}")

        return created_count

    except Exception as e:
        print(f"Error creating study notes: {e}")
        return 0

def main():
    """Main function to populate all missing content"""
    print("📚 Creating missing Grade 5 English Language Arts content...")

    total_questions = 0
    total_notes = 0

    # Create questions for topics that need them
    total_questions += create_complex_texts_questions()
    total_questions += create_research_skills_questions()
    total_questions += create_poetry_analysis_questions()

    # Create study notes
    total_notes += create_study_notes()

    print(f"\n✅ Successfully created:")
    print(f"   📝 {total_questions} new questions")
    print(f"   📖 {total_notes} new study notes")
    print(f"\n🎓 Grade 5 English Language Arts is now fully populated!")

if __name__ == '__main__':
    main()
