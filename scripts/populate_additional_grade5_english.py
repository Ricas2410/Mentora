#!/usr/bin/env python3
"""
Script to add 15-20 additional real-life questions to each Grade 5 English topic
Avoiding duplications and generic content
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice
from users.models import User
from django.db import transaction

def create_question_with_choices(topic, question_data, admin_user):
    """Helper function to create a question with multiple choice answers"""
    with transaction.atomic():
        # Check if question already exists
        if Question.objects.filter(topic=topic, question_text=question_data['question_text']).exists():
            return False

        question = Question.objects.create(
            topic=topic,
            question_text=question_data['question_text'],
            question_type='multiple_choice',
            difficulty=question_data.get('difficulty', 'medium'),
            correct_answer=question_data['correct_answer'],
            explanation=question_data['explanation'],
            order=Question.objects.filter(topic=topic).count() + 1,
            points=question_data.get('points', 1),
            time_limit=45,
            explanation_display_time=5,
            is_active=True,
            created_by=admin_user
        )

        # Create answer choices
        for i, (choice_text, is_correct) in enumerate(question_data['choices']):
            AnswerChoice.objects.create(
                question=question,
                choice_text=choice_text,
                is_correct=is_correct,
                order=i + 1
            )

        return True

def populate_complex_texts_questions(topic, admin_user):
    """Add 20 additional Complex Texts questions"""
    questions = [
        {
            'question_text': 'Read this passage: "The scientist carefully examined the fossil, noting its intricate details and estimating its age to be millions of years old." What does "intricate" mean?',
            'choices': [
                ('Simple and basic', False),
                ('Complex and detailed', True),
                ('Large and heavy', False),
                ('Old and broken', False)
            ],
            'correct_answer': 'Complex and detailed',
            'explanation': 'Intricate means having many complex details or parts that are carefully arranged.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'In the sentence "The thunderous applause echoed through the auditorium," what literary device is being used?',
            'choices': [
                ('Metaphor', False),
                ('Simile', False),
                ('Personification', True),
                ('Alliteration', False)
            ],
            'correct_answer': 'Personification',
            'explanation': 'Personification gives human qualities (echoing) to non-human things (applause).',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the main purpose of the first paragraph in most informational texts?',
            'choices': [
                ('To provide detailed examples', False),
                ('To introduce the main topic', True),
                ('To give the conclusion', False),
                ('To list all the facts', False)
            ],
            'correct_answer': 'To introduce the main topic',
            'explanation': 'The first paragraph typically introduces the main topic and gives readers an overview of what to expect.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Read: "Despite the challenging weather conditions, the hikers persevered and reached the summit." What does "persevered" mean?',
            'choices': [
                ('Gave up quickly', False),
                ('Continued despite difficulties', True),
                ('Moved very slowly', False),
                ('Complained loudly', False)
            ],
            'correct_answer': 'Continued despite difficulties',
            'explanation': 'Persevered means to continue trying despite facing challenges or obstacles.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence shows cause and effect relationship?',
            'choices': [
                ('The cat is sleeping on the couch.', False),
                ('Because it rained, the game was cancelled.', True),
                ('Sarah likes both pizza and pasta.', False),
                ('The book has 200 pages.', False)
            ],
            'correct_answer': 'Because it rained, the game was cancelled.',
            'explanation': 'This sentence shows cause (rain) and effect (game cancelled) with the word "because".',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'In a biography, what type of information would you expect to find?',
            'choices': [
                ('Made-up stories about fictional characters', False),
                ('Real events from someone\'s life', True),
                ('Instructions for making something', False),
                ('Opinions about current events', False)
            ],
            'correct_answer': 'Real events from someone\'s life',
            'explanation': 'A biography tells the true story of a real person\'s life and experiences.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What does it mean when a text has a "chronological" structure?',
            'choices': [
                ('Events are arranged by importance', False),
                ('Events are arranged in time order', True),
                ('Events are arranged alphabetically', False),
                ('Events are arranged randomly', False)
            ],
            'correct_answer': 'Events are arranged in time order',
            'explanation': 'Chronological structure means events are organized in the order they happened in time.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Read: "The ancient castle loomed ominously over the village below." What mood does this sentence create?',
            'choices': [
                ('Happy and cheerful', False),
                ('Dark and threatening', True),
                ('Calm and peaceful', False),
                ('Exciting and fun', False)
            ],
            'correct_answer': 'Dark and threatening',
            'explanation': 'Words like "loomed" and "ominously" create a dark, threatening mood.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which transition word shows contrast or difference?',
            'choices': [
                ('Furthermore', False),
                ('However', True),
                ('Additionally', False),
                ('Similarly', False)
            ],
            'correct_answer': 'However',
            'explanation': 'However is used to show contrast or introduce an opposing idea.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'In the sentence "The protagonist faced numerous obstacles," what does "protagonist" mean?',
            'choices': [
                ('The villain of the story', False),
                ('The main character', True),
                ('A minor character', False),
                ('The narrator', False)
            ],
            'correct_answer': 'The main character',
            'explanation': 'The protagonist is the main character in a story, around whom the plot revolves.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the purpose of a glossary in a textbook?',
            'choices': [
                ('To list the chapters', False),
                ('To define important terms', True),
                ('To show pictures', False),
                ('To give the author\'s biography', False)
            ],
            'correct_answer': 'To define important terms',
            'explanation': 'A glossary provides definitions of important or difficult terms used in the text.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Read: "The evidence clearly demonstrates that recycling reduces waste." What type of text structure is this?',
            'choices': [
                ('Narrative', False),
                ('Argumentative', True),
                ('Descriptive', False),
                ('Procedural', False)
            ],
            'correct_answer': 'Argumentative',
            'explanation': 'This sentence presents evidence to support a claim, which is characteristic of argumentative text.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence uses formal language appropriate for academic writing?',
            'choices': [
                ('This stuff is really cool and awesome!', False),
                ('The research indicates significant improvements.', True),
                ('I think this is pretty neat.', False),
                ('It\'s totally amazing how this works.', False)
            ],
            'correct_answer': 'The research indicates significant improvements.',
            'explanation': 'Formal language uses precise, objective terms and avoids casual expressions.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the main difference between fact and opinion?',
            'choices': [
                ('Facts are longer than opinions', False),
                ('Facts can be proven, opinions cannot', True),
                ('Facts are more interesting than opinions', False),
                ('Facts are written by experts only', False)
            ],
            'correct_answer': 'Facts can be proven, opinions cannot',
            'explanation': 'Facts are statements that can be verified or proven true, while opinions are personal beliefs.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'In the phrase "crystal clear water," what type of figurative language is used?',
            'choices': [
                ('Metaphor', True),
                ('Simile', False),
                ('Personification', False),
                ('Onomatopoeia', False)
            ],
            'correct_answer': 'Metaphor',
            'explanation': 'This is a metaphor comparing the clarity of water to the transparency of crystal.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What should you do first when reading a complex informational text?',
            'choices': [
                ('Read every word carefully', False),
                ('Preview headings and subheadings', True),
                ('Start with the conclusion', False),
                ('Look up every unknown word', False)
            ],
            'correct_answer': 'Preview headings and subheadings',
            'explanation': 'Previewing headings helps you understand the text structure and main topics before reading.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Read: "The data reveals a significant correlation between study time and test scores." What does "correlation" mean?',
            'choices': [
                ('A difference between two things', False),
                ('A relationship between two things', True),
                ('A conflict between two things', False),
                ('A separation of two things', False)
            ],
            'correct_answer': 'A relationship between two things',
            'explanation': 'Correlation refers to a relationship or connection between two variables or factors.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which element is most important for understanding the author\'s purpose?',
            'choices': [
                ('The length of the text', False),
                ('The choice of words and tone', True),
                ('The number of paragraphs', False),
                ('The size of the font', False)
            ],
            'correct_answer': 'The choice of words and tone',
            'explanation': 'Word choice and tone reveal the author\'s attitude and purpose for writing.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the best strategy for understanding difficult vocabulary in context?',
            'choices': [
                ('Skip the word completely', False),
                ('Use surrounding clues to guess meaning', True),
                ('Replace it with any word', False),
                ('Stop reading immediately', False)
            ],
            'correct_answer': 'Use surrounding clues to guess meaning',
            'explanation': 'Context clues from surrounding sentences help determine the meaning of unfamiliar words.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'In academic texts, what is the purpose of topic sentences?',
            'choices': [
                ('To end each paragraph', False),
                ('To introduce the main idea of a paragraph', True),
                ('To provide examples only', False),
                ('To ask questions', False)
            ],
            'correct_answer': 'To introduce the main idea of a paragraph',
            'explanation': 'Topic sentences state the main idea that the rest of the paragraph will support or explain.',
            'difficulty': 'medium',
            'points': 2
        }
    ]

    created_count = 0
    for q_data in questions:
        if create_question_with_choices(topic, q_data, admin_user):
            created_count += 1

    print(f"    Created {created_count} new Complex Texts questions")

def populate_advanced_grammar_questions(topic, admin_user):
    """Add 20 additional Advanced Grammar questions"""
    questions = [
        {
            'question_text': 'Which sentence correctly uses a semicolon?',
            'choices': [
                ('I like pizza; and pasta too.', False),
                ('The weather is nice; we should go outside.', True),
                ('She ran fast; because she was late.', False),
                ('My favorite color; is blue.', False)
            ],
            'correct_answer': 'The weather is nice; we should go outside.',
            'explanation': 'Semicolons connect two related independent clauses that could stand alone as sentences.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Identify the subordinate clause in: "Although it was raining, we went to the park."',
            'choices': [
                ('Although it was raining', True),
                ('we went to the park', False),
                ('it was raining', False),
                ('went to the park', False)
            ],
            'correct_answer': 'Although it was raining',
            'explanation': 'A subordinate clause begins with a subordinating conjunction like "although" and cannot stand alone.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence uses the correct form of "who" or "whom"?',
            'choices': [
                ('Who did you give the book to?', False),
                ('To whom did you give the book?', True),
                ('Whom gave you the book?', False),
                ('Who did gave the book?', False)
            ],
            'correct_answer': 'To whom did you give the book?',
            'explanation': 'Use "whom" when it is the object of a verb or preposition. "Whom" receives the action.',
            'difficulty': 'hard',
            'points': 3
        },
        {
            'question_text': 'Which sentence contains a dangling modifier?',
            'choices': [
                ('Running quickly, Sarah caught the bus.', False),
                ('Running quickly, the bus was caught by Sarah.', True),
                ('Sarah, running quickly, caught the bus.', False),
                ('The bus was caught by Sarah, who was running quickly.', False)
            ],
            'correct_answer': 'Running quickly, the bus was caught by Sarah.',
            'explanation': 'A dangling modifier occurs when the modifier doesn\'t clearly relate to the word it\'s supposed to modify.',
            'difficulty': 'hard',
            'points': 3
        },
        {
            'question_text': 'Choose the sentence with correct parallel structure:',
            'choices': [
                ('She likes swimming, running, and to bike.', False),
                ('She likes swimming, running, and biking.', True),
                ('She likes to swim, running, and biking.', False),
                ('She likes swimming, to run, and biking.', False)
            ],
            'correct_answer': 'She likes swimming, running, and biking.',
            'explanation': 'Parallel structure means using the same grammatical form for items in a series.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence correctly uses an apostrophe?',
            'choices': [
                ('The dog wagged it\'s tail happily.', False),
                ('The dog wagged its tail happily.', True),
                ('The dogs\' tail wagged happily.', False),
                ('The dog wagged its\' tail happily.', False)
            ],
            'correct_answer': 'The dog wagged its tail happily.',
            'explanation': '"Its" is possessive and doesn\'t need an apostrophe. "It\'s" means "it is."',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Identify the type of sentence: "Stop running in the hallway!"',
            'choices': [
                ('Declarative', False),
                ('Interrogative', False),
                ('Imperative', True),
                ('Exclamatory', False)
            ],
            'correct_answer': 'Imperative',
            'explanation': 'Imperative sentences give commands or make requests. They often have an understood subject "you."',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which word is the indirect object in: "Mom gave Sarah a present"?',
            'choices': [
                ('Mom', False),
                ('gave', False),
                ('Sarah', True),
                ('present', False)
            ],
            'correct_answer': 'Sarah',
            'explanation': 'The indirect object tells us to whom or for whom the action is done. Sarah receives the present.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Choose the sentence with the correct use of "affect" or "effect":',
            'choices': [
                ('The rain will effect our picnic plans.', False),
                ('The rain will affect our picnic plans.', True),
                ('The affect of rain on our picnic was disappointing.', False),
                ('Rain has a bad affect on outdoor activities.', False)
            ],
            'correct_answer': 'The rain will affect our picnic plans.',
            'explanation': '"Affect" is usually a verb meaning to influence. "Effect" is usually a noun meaning result.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence uses a colon correctly?',
            'choices': [
                ('I need: milk, eggs, and bread.', False),
                ('I need three things: milk, eggs, and bread.', True),
                ('I need three things, milk: eggs, and bread.', False),
                ('I need three: things milk, eggs, and bread.', False)
            ],
            'correct_answer': 'I need three things: milk, eggs, and bread.',
            'explanation': 'A colon introduces a list when preceded by a complete sentence.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What type of clause is "that we studied yesterday" in: "The lesson that we studied yesterday was difficult"?',
            'choices': [
                ('Independent clause', False),
                ('Adjective clause', True),
                ('Adverb clause', False),
                ('Noun clause', False)
            ],
            'correct_answer': 'Adjective clause',
            'explanation': 'An adjective clause modifies a noun. "That we studied yesterday" describes "lesson."',
            'difficulty': 'hard',
            'points': 3
        },
        {
            'question_text': 'Which sentence correctly uses "lay" or "lie"?',
            'choices': [
                ('I will lay down for a nap.', False),
                ('I will lie down for a nap.', True),
                ('The book is laying on the table.', False),
                ('Please lay down and rest.', False)
            ],
            'correct_answer': 'I will lie down for a nap.',
            'explanation': '"Lie" means to recline (no direct object). "Lay" means to place something (needs direct object).',
            'difficulty': 'hard',
            'points': 3
        },
        {
            'question_text': 'Identify the gerund in: "Swimming is my favorite exercise."',
            'choices': [
                ('Swimming', True),
                ('is', False),
                ('favorite', False),
                ('exercise', False)
            ],
            'correct_answer': 'Swimming',
            'explanation': 'A gerund is a verb form ending in -ing that functions as a noun. Here, "swimming" is the subject.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence has correct subject-verb agreement?',
            'choices': [
                ('Neither the teacher nor the students was ready.', False),
                ('Neither the teacher nor the students were ready.', True),
                ('Neither the teachers nor the student were ready.', False),
                ('Neither the teachers nor the students was ready.', False)
            ],
            'correct_answer': 'Neither the teacher nor the students were ready.',
            'explanation': 'With "neither...nor," the verb agrees with the subject closest to it. "Students" is plural.',
            'difficulty': 'hard',
            'points': 3
        },
        {
            'question_text': 'What is the function of "quickly" in: "She ran quickly to catch the bus"?',
            'choices': [
                ('Adjective modifying "she"', False),
                ('Adverb modifying "ran"', True),
                ('Noun serving as object', False),
                ('Verb showing action', False)
            ],
            'correct_answer': 'Adverb modifying "ran"',
            'explanation': 'Adverbs modify verbs, adjectives, or other adverbs. "Quickly" tells how she ran.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Choose the sentence with correct capitalization:',
            'choices': [
                ('We studied the civil war in History class.', False),
                ('We studied the Civil War in history class.', True),
                ('We studied the civil war in history class.', False),
                ('We studied the Civil War in History Class.', False)
            ],
            'correct_answer': 'We studied the Civil War in history class.',
            'explanation': 'Proper nouns like "Civil War" are capitalized, but common nouns like "history class" are not.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence uses quotation marks correctly?',
            'choices': [
                ('"I love reading," she said.', True),
                ('"I love reading", she said.', False),
                ('"I love reading." she said.', False),
                ('I love reading, "she said."', False)
            ],
            'correct_answer': '"I love reading," she said.',
            'explanation': 'The comma goes inside the quotation marks when the quote is followed by a dialogue tag.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What type of pronoun is "myself" in: "I made this myself"?',
            'choices': [
                ('Personal pronoun', False),
                ('Reflexive pronoun', True),
                ('Demonstrative pronoun', False),
                ('Interrogative pronoun', False)
            ],
            'correct_answer': 'Reflexive pronoun',
            'explanation': 'Reflexive pronouns end in -self or -selves and refer back to the subject.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which sentence contains a misplaced modifier?',
            'choices': [
                ('I saw a dog walking down the street with spots.', True),
                ('I saw a spotted dog walking down the street.', False),
                ('Walking down the street, I saw a spotted dog.', False),
                ('I saw a dog with spots walking down the street.', False)
            ],
            'correct_answer': 'I saw a dog walking down the street with spots.',
            'explanation': 'The modifier "with spots" is misplaced - it seems to modify "street" instead of "dog."',
            'difficulty': 'hard',
            'points': 3
        },
        {
            'question_text': 'Choose the sentence that correctly uses "fewer" or "less":',
            'choices': [
                ('There are less students in class today.', False),
                ('There are fewer students in class today.', True),
                ('I have less pencils than you.', False),
                ('She has fewer homework than me.', False)
            ],
            'correct_answer': 'There are fewer students in class today.',
            'explanation': 'Use "fewer" with countable nouns (students). Use "less" with uncountable nouns (water, time).',
            'difficulty': 'medium',
            'points': 2
        }
    ]

    created_count = 0
    for q_data in questions:
        if create_question_with_choices(topic, q_data, admin_user):
            created_count += 1

    print(f"    Created {created_count} new Advanced Grammar questions")

def populate_research_skills_questions(topic, admin_user):
    """Add 15 additional Research Skills questions"""
    questions = [
        {
            'question_text': 'What is the most reliable source for a school research project?',
            'choices': [
                ('A random blog post', False),
                ('An encyclopedia or educational website', True),
                ('A social media post', False),
                ('A friend\'s opinion', False)
            ],
            'correct_answer': 'An encyclopedia or educational website',
            'explanation': 'Encyclopedias and educational websites are written by experts and fact-checked for accuracy.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'When researching online, what should you check first about a website?',
            'choices': [
                ('How colorful it looks', False),
                ('Who wrote the information', True),
                ('How many pictures it has', False),
                ('How long the articles are', False)
            ],
            'correct_answer': 'Who wrote the information',
            'explanation': 'Checking the author helps determine if the source is credible and trustworthy.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the best way to organize information you find during research?',
            'choices': [
                ('Write everything on one big piece of paper', False),
                ('Use note cards or organize by topic', True),
                ('Just remember it in your head', False),
                ('Copy everything exactly as written', False)
            ],
            'correct_answer': 'Use note cards or organize by topic',
            'explanation': 'Organizing information by topic makes it easier to find and use when writing.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Why is it important to use multiple sources for research?',
            'choices': [
                ('To make your bibliography longer', False),
                ('To get different perspectives and verify facts', True),
                ('To confuse your readers', False),
                ('To make your report longer', False)
            ],
            'correct_answer': 'To get different perspectives and verify facts',
            'explanation': 'Multiple sources help ensure accuracy and provide a complete understanding of the topic.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What should you do if you find conflicting information in different sources?',
            'choices': [
                ('Use the first source you found', False),
                ('Check additional reliable sources', True),
                ('Ignore the conflicting information', False),
                ('Make up your own facts', False)
            ],
            'correct_answer': 'Check additional reliable sources',
            'explanation': 'When sources conflict, checking more reliable sources helps determine what information is accurate.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is plagiarism?',
            'choices': [
                ('Using your own ideas', False),
                ('Using someone else\'s work without giving credit', True),
                ('Reading multiple sources', False),
                ('Taking notes while researching', False)
            ],
            'correct_answer': 'Using someone else\'s work without giving credit',
            'explanation': 'Plagiarism is using someone else\'s words or ideas without properly crediting the original author.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'When taking notes from a source, what is the most important thing to remember?',
            'choices': [
                ('Copy everything word for word', False),
                ('Write the information in your own words', True),
                ('Only write down page numbers', False),
                ('Don\'t write anything down', False)
            ],
            'correct_answer': 'Write the information in your own words',
            'explanation': 'Paraphrasing (writing in your own words) shows understanding and helps avoid plagiarism.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What information should you always record about your sources?',
            'choices': [
                ('Only the title', False),
                ('Author, title, date, and where you found it', True),
                ('Only the website address', False),
                ('Just the main ideas', False)
            ],
            'correct_answer': 'Author, title, date, and where you found it',
            'explanation': 'Complete source information is needed to create proper citations and find the source again.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which keyword search would be most effective for finding information about "recycling plastic bottles"?',
            'choices': [
                ('plastic', False),
                ('recycling plastic bottles', True),
                ('bottles', False),
                ('environment', False)
            ],
            'correct_answer': 'recycling plastic bottles',
            'explanation': 'Specific keywords that include all important terms give the most relevant search results.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is a bibliography?',
            'choices': [
                ('A summary of your research', False),
                ('A list of all sources you used', True),
                ('The introduction to your report', False),
                ('A collection of pictures', False)
            ],
            'correct_answer': 'A list of all sources you used',
            'explanation': 'A bibliography lists all the sources you consulted during your research.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'When is the best time to evaluate if a source is reliable?',
            'choices': [
                ('After you finish your project', False),
                ('Before you use the information', True),
                ('Only if someone asks you to', False),
                ('Never - all sources are reliable', False)
            ],
            'correct_answer': 'Before you use the information',
            'explanation': 'Evaluating sources before using them prevents including unreliable information in your work.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What makes a website ending in .edu more reliable than one ending in .com?',
            'choices': [
                ('It has better pictures', False),
                ('It\'s from an educational institution', True),
                ('It loads faster', False),
                ('It has more advertisements', False)
            ],
            'correct_answer': 'It\'s from an educational institution',
            'explanation': '.edu websites belong to educational institutions and typically contain academic, peer-reviewed content.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Why should you check the date when a source was published?',
            'choices': [
                ('Older information is always better', False),
                ('To make sure the information is current', True),
                ('Dates don\'t matter for research', False),
                ('New information is always wrong', False)
            ],
            'correct_answer': 'To make sure the information is current',
            'explanation': 'Current information is important, especially for topics that change over time like technology or science.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What should you do if you can\'t find enough information on your research topic?',
            'choices': [
                ('Make up information to fill the gaps', False),
                ('Try different keywords or broaden your topic', True),
                ('Give up on the project', False),
                ('Use the same source multiple times', False)
            ],
            'correct_answer': 'Try different keywords or broaden your topic',
            'explanation': 'Using different search terms or expanding your topic can help you find more relevant sources.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the purpose of an outline when organizing research?',
            'choices': [
                ('To make your paper look longer', False),
                ('To organize your ideas before writing', True),
                ('To confuse your readers', False),
                ('To avoid doing research', False)
            ],
            'correct_answer': 'To organize your ideas before writing',
            'explanation': 'An outline helps organize your research and ideas into a logical structure for writing.',
            'difficulty': 'medium',
            'points': 2
        }
    ]

    created_count = 0
    for q_data in questions:
        if create_question_with_choices(topic, q_data, admin_user):
            created_count += 1

    print(f"    Created {created_count} new Research Skills questions")

def populate_poetry_analysis_questions(topic, admin_user):
    """Add 15 additional Poetry Analysis questions"""
    questions = [
        {
            'question_text': 'What is the rhyme scheme of these lines: "The cat sat on the mat / The dog ran in the fog"?',
            'choices': [
                ('AABB', False),
                ('ABAB', True),
                ('ABBA', False),
                ('AAAA', False)
            ],
            'correct_answer': 'ABAB',
            'explanation': 'Mat (A) and fog (B) don\'t rhyme, but mat rhymes with cat and fog rhymes with dog, creating ABAB pattern.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'In the line "The wind whispered through the trees," what literary device is used?',
            'choices': [
                ('Metaphor', False),
                ('Personification', True),
                ('Simile', False),
                ('Alliteration', False)
            ],
            'correct_answer': 'Personification',
            'explanation': 'Personification gives human qualities (whispering) to non-human things (wind).',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is alliteration?',
            'choices': [
                ('Words that rhyme at the end', False),
                ('Repetition of beginning consonant sounds', True),
                ('Comparing two things using "like" or "as"', False),
                ('Giving human qualities to objects', False)
            ],
            'correct_answer': 'Repetition of beginning consonant sounds',
            'explanation': 'Alliteration is the repetition of the same consonant sound at the beginning of words.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which line contains a simile?',
            'choices': [
                ('The moon is a silver coin', False),
                ('Her voice is like music', True),
                ('The stars danced in the sky', False),
                ('Time flies quickly', False)
            ],
            'correct_answer': 'Her voice is like music',
            'explanation': 'A simile compares two things using "like" or "as." This compares voice to music using "like."',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the mood of this line: "Dark clouds gathered ominously overhead"?',
            'choices': [
                ('Happy and cheerful', False),
                ('Threatening and gloomy', True),
                ('Calm and peaceful', False),
                ('Exciting and energetic', False)
            ],
            'correct_answer': 'Threatening and gloomy',
            'explanation': 'Words like "dark," "gathered," and "ominously" create a threatening, gloomy mood.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'In poetry, what is a stanza?',
            'choices': [
                ('A single word', False),
                ('A group of lines', True),
                ('The title of the poem', False),
                ('The poet\'s name', False)
            ],
            'correct_answer': 'A group of lines',
            'explanation': 'A stanza is a group of lines in a poem, similar to a paragraph in prose.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What does rhythm in poetry refer to?',
            'choices': [
                ('The meaning of the words', False),
                ('The pattern of stressed and unstressed syllables', True),
                ('The length of the poem', False),
                ('The poet\'s feelings', False)
            ],
            'correct_answer': 'The pattern of stressed and unstressed syllables',
            'explanation': 'Rhythm is the musical quality created by the pattern of stressed and unstressed syllables.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which line contains onomatopoeia?',
            'choices': [
                ('The beautiful butterfly flew by', False),
                ('The bee buzzed loudly', True),
                ('The flower smelled sweet', False),
                ('The sun shone brightly', False)
            ],
            'correct_answer': 'The bee buzzed loudly',
            'explanation': 'Onomatopoeia uses words that imitate sounds. "Buzzed" imitates the sound a bee makes.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is the theme of a poem?',
            'choices': [
                ('The rhyme scheme', False),
                ('The main message or lesson', True),
                ('The number of stanzas', False),
                ('The poet\'s age', False)
            ],
            'correct_answer': 'The main message or lesson',
            'explanation': 'Theme is the central message, lesson, or meaning that the poet wants to convey.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'In the metaphor "Life is a journey," what two things are being compared?',
            'choices': [
                ('Life and death', False),
                ('Life and a journey', True),
                ('Journey and travel', False),
                ('Life and happiness', False)
            ],
            'correct_answer': 'Life and a journey',
            'explanation': 'This metaphor directly compares life to a journey, suggesting life has a path with destinations.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is free verse poetry?',
            'choices': [
                ('Poetry that costs nothing', False),
                ('Poetry without regular rhyme or rhythm', True),
                ('Poetry about freedom', False),
                ('Poetry written by prisoners', False)
            ],
            'correct_answer': 'Poetry without regular rhyme or rhythm',
            'explanation': 'Free verse poetry doesn\'t follow traditional patterns of rhyme, rhythm, or meter.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'Which words in "Sally sells seashells" create alliteration?',
            'choices': [
                ('Sally, sells, seashells', True),
                ('sells, seashells', False),
                ('Sally, seashells', False),
                ('None of them', False)
            ],
            'correct_answer': 'Sally, sells, seashells',
            'explanation': 'All three words begin with the "s" sound, creating alliteration throughout the phrase.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is imagery in poetry?',
            'choices': [
                ('Pictures drawn next to poems', False),
                ('Descriptive language that appeals to the senses', True),
                ('The poet\'s photograph', False),
                ('Rhyming words', False)
            ],
            'correct_answer': 'Descriptive language that appeals to the senses',
            'explanation': 'Imagery uses descriptive language to help readers see, hear, feel, taste, or smell what\'s described.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'In the line "The classroom was a zoo," what does this metaphor suggest?',
            'choices': [
                ('There were animals in the classroom', False),
                ('The classroom was noisy and chaotic', True),
                ('The classroom was outside', False),
                ('Students were studying animals', False)
            ],
            'correct_answer': 'The classroom was noisy and chaotic',
            'explanation': 'Comparing the classroom to a zoo suggests it was wild, noisy, and out of control.',
            'difficulty': 'medium',
            'points': 2
        },
        {
            'question_text': 'What is repetition in poetry used for?',
            'choices': [
                ('To make poems longer', False),
                ('To emphasize important ideas', True),
                ('To confuse readers', False),
                ('To save time writing', False)
            ],
            'correct_answer': 'To emphasize important ideas',
            'explanation': 'Repetition draws attention to key words or ideas and creates emphasis and rhythm.',
            'difficulty': 'medium',
            'points': 2
        }
    ]

    created_count = 0
    for q_data in questions:
        if create_question_with_choices(topic, q_data, admin_user):
            created_count += 1

    print(f"    Created {created_count} new Poetry Analysis questions")

def main():
    """Main function to populate additional questions"""
    try:
        # Get admin user
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No admin user found. Please create a superuser first.")
            return

        # Get Grade 5 English
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)

        print(f"📚 Adding additional questions to Grade 5 English topics...")

        # Get topics
        topics = {
            'complex_texts': Topic.objects.get(class_level=grade5, title='Complex Texts'),
            'advanced_grammar': Topic.objects.get(class_level=grade5, title='Advanced Grammar'),
            'research_skills': Topic.objects.get(class_level=grade5, title='Research Skills'),
            'poetry_analysis': Topic.objects.get(class_level=grade5, title='Poetry Analysis'),
        }

        # Populate questions for each topic
        populate_complex_texts_questions(topics['complex_texts'], admin_user)
        populate_advanced_grammar_questions(topics['advanced_grammar'], admin_user)
        populate_research_skills_questions(topics['research_skills'], admin_user)
        populate_poetry_analysis_questions(topics['poetry_analysis'], admin_user)

        print("✅ Successfully added additional questions to Grade 5 English topics!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
