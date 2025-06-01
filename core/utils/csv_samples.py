"""
CSV Sample Data Generator for Educational Content Import
"""
import csv
import io
from .csv_import import get_csv_template


def generate_sample_csv():
    """Generate clean, professional sample CSV data for questions using existing Grade 5 content"""

    return [
        # ICT Grade 5 - Computer Basics Multiple Choice
        {
            'subject_name': 'ICT',
            'class_level_name': 'Grade 5',
            'topic_title': 'Computer Basics and Parts',
            'question_text': 'Which part of the computer is called the "brain" because it processes all information?',
            'question_type': 'multiple_choice',
            'correct_answer': 'b',
            'explanation': 'The CPU (Central Processing Unit) is called the brain of the computer because it processes all the information and instructions.',
            'difficulty': 'easy',
            'points': '10',
            'time_limit': '45',
            'choice_a': 'Monitor',
            'choice_b': 'CPU (Central Processing Unit)',
            'choice_c': 'Keyboard',
            'choice_d': 'Mouse'
        },
        {
            'subject_name': 'ICT',
            'class_level_name': 'Grade 5',
            'topic_title': 'Internet Safety and Digital Citizenship',
            'question_text': 'Which of these should you NEVER share online?',
            'question_type': 'multiple_choice',
            'correct_answer': 'b',
            'explanation': 'Personal information like your home address should never be shared online for safety reasons.',
            'difficulty': 'easy',
            'points': '10',
            'time_limit': '45',
            'choice_a': 'Your favorite color',
            'choice_b': 'Your home address',
            'choice_c': 'Your favorite book',
            'choice_d': 'Your favorite animal'
        },
        # Mathematics Grade 5 - Fractions
        {
            'subject_name': 'Mathematics',
            'class_level_name': 'Grade 5',
            'topic_title': 'Fractions',
            'question_text': 'What is 1/2 + 1/4?',
            'question_type': 'multiple_choice',
            'correct_answer': 'c',
            'explanation': 'To add fractions, find a common denominator. 1/2 = 2/4, so 2/4 + 1/4 = 3/4',
            'difficulty': 'medium',
            'points': '10',
            'time_limit': '60',
            'choice_a': '1/6',
            'choice_b': '2/6',
            'choice_c': '3/4',
            'choice_d': '1/3'
        },
        # English Grade 5 - Fill in the Blank
        {
            'subject_name': 'English Language Arts',
            'class_level_name': 'Grade 5',
            'topic_title': 'Grammar and Sentence Structure',
            'question_text': 'Fill in the blank with the correct verb: Yesterday, I _____ to the store.',
            'question_type': 'fill_blank',
            'correct_answer': 'went',
            'explanation': 'Past tense of "go" is "went" when referring to something that happened yesterday.',
            'difficulty': 'easy',
            'points': '10',
            'time_limit': '45',
            'choice_a': '',
            'choice_b': '',
            'choice_c': '',
            'choice_d': ''
        },
        # Science Grade 5 - True/False
        {
            'subject_name': 'Science',
            'class_level_name': 'Grade 5',
            'topic_title': 'Matter and Its Properties',
            'question_text': 'Water can exist in three states: solid, liquid, and gas.',
            'question_type': 'true_false',
            'correct_answer': 'true',
            'explanation': 'Water exists as ice (solid), liquid water, and water vapor (gas).',
            'difficulty': 'easy',
            'points': '10',
            'time_limit': '30',
            'choice_a': '',
            'choice_b': '',
            'choice_c': '',
            'choice_d': ''
        },
        # Social Studies Grade 5 - Short Answer
        {
            'subject_name': 'Social Studies',
            'class_level_name': 'Grade 5',
            'topic_title': 'Geography and Maps',
            'question_text': 'What tool do we use to find directions on a map?',
            'question_type': 'short_answer',
            'correct_answer': 'compass rose',
            'explanation': 'A compass rose shows the cardinal directions (North, South, East, West) on a map.',
            'difficulty': 'easy',
            'points': '10',
            'time_limit': '45',
            'choice_a': '',
            'choice_b': '',
            'choice_c': '',
            'choice_d': ''
        },
        # Life Skills Grade 5
        {
            'subject_name': 'Life Skills',
            'class_level_name': 'Grade 5',
            'topic_title': 'Personal Health and Hygiene',
            'question_text': 'How many times per day should you brush your teeth?',
            'question_type': 'multiple_choice',
            'correct_answer': 'b',
            'explanation': 'Dentists recommend brushing teeth at least twice a day - morning and night.',
            'difficulty': 'easy',
            'points': '10',
            'time_limit': '30',
            'choice_a': 'Once',
            'choice_b': 'Twice',
            'choice_c': 'Three times',
            'choice_d': 'Four times'
        }
    ]


def create_csv_content():
    """Create CSV content string for questions template download"""
    template = get_csv_template('questions')
    sample_data = generate_sample_csv()

    if not template:
        return None

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=template)

    # Write header
    writer.writeheader()

    # Write sample data
    for row in sample_data:
        # Ensure all template fields are present
        csv_row = {}
        for field in template:
            csv_row[field] = row.get(field, '')
        writer.writerow(csv_row)

    return output.getvalue()


def get_import_instructions():
    """Get instructions for questions import"""
    return {
        'title': 'Questions Import Instructions',
        'description': 'Import quiz questions for existing topics',
        'required_fields': ['subject_name', 'class_level_name', 'topic_title', 'question_text', 'question_type'],
        'optional_fields': ['explanation', 'difficulty', 'points', 'time_limit'],
        'notes': [
            'Subject, Class Level, and Topic must exist before importing questions',
            'Available subjects: English Language Arts, Mathematics, Science, Social Studies, Life Skills, ICT',
            'Class levels: Grade 1, Grade 2, Grade 3, ... Grade 12',
            'Question types: multiple_choice, fill_blank, true_false, short_answer',
            'Multiple choice: requires correct_answer (a,b,c,d) and choice_a through choice_d',
            'Fill blank/Short answer: requires correct_answer text',
            'True/False: correct_answer should be true/false, t/f, or 1/0',
            'Time limit is per question in seconds (default: 45)',
            'Difficulty levels: easy, medium, hard',
            'Points: Default is 10 points per question',
            'Missing topics will be auto-created if they don\'t exist',
            'Use the sample data as a reference for proper formatting'
        ]
    }
