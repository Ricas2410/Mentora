#!/usr/bin/env python3
"""
Comprehensive quiz questions data for Grade 5 and Grade 6 English
Professional questions avoiding duplications and generic content
"""

# Grade 5 Grammar: Tenses Questions (20 questions)
GRADE_5_TENSES = [
    {
        'question_text': 'Which sentence uses the present tense correctly?',
        'question_type': 'multiple_choice',
        'options': ['She walks to school every day.', 'She walked to school every day.', 'She will walk to school every day.', 'She has walked to school every day.'],
        'correct_answer': 'She walks to school every day.',
        'explanation': 'Present tense describes actions happening now or regularly. "Walks" is the present tense form.',
        'difficulty_level': 'beginner'
    },
    {
        'question_text': 'Complete the sentence: Yesterday, I _____ my homework.',
        'question_type': 'multiple_choice',
        'options': ['do', 'did', 'will do', 'doing'],
        'correct_answer': 'did',
        'explanation': '"Yesterday" indicates past time, so we use the past tense "did".',
        'difficulty_level': 'beginner'
    },
    {
        'question_text': 'What tense is used in this sentence: "Tomorrow we will visit the museum"?',
        'question_type': 'multiple_choice',
        'options': ['Past tense', 'Present tense', 'Future tense', 'Present perfect tense'],
        'correct_answer': 'Future tense',
        'explanation': '"Will visit" indicates an action that will happen in the future.',
        'difficulty_level': 'beginner'
    },
    {
        'question_text': 'Choose the correct past tense form: The children _____ in the playground.',
        'question_type': 'multiple_choice',
        'options': ['play', 'played', 'will play', 'playing'],
        'correct_answer': 'played',
        'explanation': 'For regular verbs, we add -ed to form the past tense.',
        'difficulty_level': 'beginner'
    },
    {
        'question_text': 'Which sentence shows future tense?',
        'question_type': 'multiple_choice',
        'options': ['I am reading a book.', 'I read a book yesterday.', 'I will read a book tonight.', 'I have read many books.'],
        'correct_answer': 'I will read a book tonight.',
        'explanation': '"Will read" is the future tense form, indicating an action that will happen later.',
        'difficulty_level': 'beginner'
    },
    {
        'question_text': 'Fill in the blank with the correct present tense verb: My sister _____ beautiful pictures.',
        'question_type': 'fill_in_blank',
        'correct_answer': 'draws',
        'alternative_answers': ['paints', 'creates', 'makes'],
        'explanation': 'Present tense for third person singular (she/he/it) often ends in -s.',
        'difficulty_level': 'intermediate'
    },
    {
        'question_text': 'Which verb form correctly completes: "Last week, we _____ to the zoo"?',
        'question_type': 'multiple_choice',
        'options': ['go', 'went', 'will go', 'going'],
        'correct_answer': 'went',
        'explanation': '"Last week" indicates past time. "Went" is the irregular past tense of "go".',
        'difficulty_level': 'intermediate'
    },
    {
        'question_text': 'Identify the tense: "The students are studying for their test."',
        'question_type': 'multiple_choice',
        'options': ['Simple present', 'Present continuous', 'Past continuous', 'Future continuous'],
        'correct_answer': 'Present continuous',
        'explanation': '"Are studying" shows an action happening right now (present continuous).',
        'difficulty_level': 'intermediate'
    },
    {
        'question_text': 'Complete with future tense: Next summer, my family _____ to Europe.',
        'question_type': 'multiple_choice',
        'options': ['travel', 'traveled', 'will travel', 'traveling'],
        'correct_answer': 'will travel',
        'explanation': '"Next summer" indicates future time, requiring "will travel".',
        'difficulty_level': 'intermediate'
    },
    {
        'question_text': 'Which sentence uses past tense correctly?',
        'question_type': 'multiple_choice',
        'options': ['She sings beautifully yesterday.', 'She sang beautifully yesterday.', 'She will sing beautifully yesterday.', 'She singing beautifully yesterday.'],
        'correct_answer': 'She sang beautifully yesterday.',
        'explanation': '"Yesterday" requires past tense. "Sang" is the correct past tense of "sing".',
        'difficulty_level': 'intermediate'
    },
    {
        'question_text': 'What is the present tense of "bought"?',
        'question_type': 'fill_in_blank',
        'correct_answer': 'buy',
        'alternative_answers': ['buys'],
        'explanation': '"Buy" is the present tense form of the irregular verb "bought".',
        'difficulty_level': 'intermediate'
    },
    {
        'question_text': 'Choose the sentence with correct tense consistency:',
        'question_type': 'multiple_choice',
        'options': ['I wake up early and brush my teeth.', 'I woke up early and brush my teeth.', 'I will wake up early and brushed my teeth.', 'I am waking up early and will brush my teeth.'],
        'correct_answer': 'I wake up early and brush my teeth.',
        'explanation': 'Both actions should be in the same tense for consistency.',
        'difficulty_level': 'advanced'
    },
    {
        'question_text': 'Fill in with the correct form: "Every morning, the birds _____ sweetly."',
        'question_type': 'fill_in_blank',
        'correct_answer': 'sing',
        'alternative_answers': ['chirp', 'tweet'],
        'explanation': '"Every morning" indicates a regular action, requiring present tense.',
        'difficulty_level': 'beginner'
    },
    {
        'question_text': 'Which shows an action that happened before another past action?',
        'question_type': 'multiple_choice',
        'options': ['I ate lunch.', 'I had eaten lunch before the meeting.', 'I will eat lunch.', 'I am eating lunch.'],
        'correct_answer': 'I had eaten lunch before the meeting.',
        'explanation': 'Past perfect tense (had + past participle) shows an action completed before another past action.',
        'difficulty_level': 'advanced'
    },
    {
        'question_text': 'Complete: "Right now, the teacher _____ the lesson."',
        'question_type': 'multiple_choice',
        'options': ['explains', 'explained', 'is explaining', 'will explain'],
        'correct_answer': 'is explaining',
        'explanation': '"Right now" indicates present continuous tense (is/are + -ing).',
        'difficulty_level': 'intermediate'
    },
    {
        'question_text': 'What tense is "I have finished my work"?',
        'question_type': 'multiple_choice',
        'options': ['Simple past', 'Present perfect', 'Past perfect', 'Future perfect'],
        'correct_answer': 'Present perfect',
        'explanation': 'Present perfect uses "have/has + past participle" to show completed actions with present relevance.',
        'difficulty_level': 'advanced'
    },
    {
        'question_text': 'Choose the correct future form: "The concert _____ at 8 PM tomorrow."',
        'question_type': 'multiple_choice',
        'options': ['start', 'started', 'starts', 'will start'],
        'correct_answer': 'starts',
        'explanation': 'For scheduled events, we often use simple present tense even for future time.',
        'difficulty_level': 'advanced'
    },
    {
        'question_text': 'Fill in the past continuous: "While I _____ TV, the phone rang."',
        'question_type': 'fill_in_blank',
        'correct_answer': 'was watching',
        'alternative_answers': ['was viewing'],
        'explanation': 'Past continuous (was/were + -ing) shows an ongoing action interrupted by another action.',
        'difficulty_level': 'advanced'
    },
    {
        'question_text': 'Which sentence uses the simple present for a general truth?',
        'question_type': 'multiple_choice',
        'options': ['Water boils at 100 degrees Celsius.', 'Water is boiling now.', 'Water boiled yesterday.', 'Water will boil tomorrow.'],
        'correct_answer': 'Water boils at 100 degrees Celsius.',
        'explanation': 'Simple present tense is used for scientific facts and general truths.',
        'difficulty_level': 'intermediate'
    },
    {
        'question_text': 'Complete with the correct tense: "By next year, I _____ how to drive."',
        'question_type': 'multiple_choice',
        'options': ['learn', 'learned', 'will learn', 'will have learned'],
        'correct_answer': 'will have learned',
        'explanation': 'Future perfect (will have + past participle) shows an action that will be completed by a specific future time.',
        'difficulty_level': 'advanced'
    }
]

# Grade 5 Grammar: Nouns Questions (20 questions)
GRADE_5_NOUNS = [
    {
        'question_text': 'Which word is a proper noun?',
        'question_type': 'multiple_choice',
        'options': ['city', 'London', 'building', 'street'],
        'correct_answer': 'London',
        'explanation': 'Proper nouns are specific names of people, places, or things and are always capitalized.',
        'difficulty_level': 'beginner'
    },
    {
        'question_text': 'What is the plural form of "child"?',
        'question_type': 'multiple_choice',
        'options': ['childs', 'childes', 'children', 'child'],
        'correct_answer': 'children',
        'explanation': '"Children" is the irregular plural form of "child".',
        'difficulty_level': 'beginner'
    },
    {
        'question_text': 'Identify the common noun in this sentence: "Sarah bought a beautiful dress."',
        'question_type': 'multiple_choice',
        'options': ['Sarah', 'bought', 'beautiful', 'dress'],
        'correct_answer': 'dress',
        'explanation': 'Common nouns are general names for people, places, or things. "Dress" is a common noun.',
        'difficulty_level': 'beginner'
    },
    {
        'question_text': 'Which noun is countable?',
        'question_type': 'multiple_choice',
        'options': ['water', 'happiness', 'books', 'music'],
        'correct_answer': 'books',
        'explanation': 'Countable nouns can be counted and have plural forms. "Books" can be counted.',
        'difficulty_level': 'intermediate'
    },
    {
        'question_text': 'What type of noun is "team"?',
        'question_type': 'multiple_choice',
        'options': ['Proper noun', 'Abstract noun', 'Collective noun', 'Material noun'],
        'correct_answer': 'Collective noun',
        'explanation': 'Collective nouns refer to groups of people, animals, or things. "Team" is a group of people.',
        'difficulty_level': 'intermediate'
    }
]

# Continue with more data structures for other topics...
# This file will be extended with the complete question sets
