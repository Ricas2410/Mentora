"""
CSV Sample Data Generator for Educational Content Import
"""
import csv
import io
from .csv_import import get_csv_template


def generate_sample_csv():
    """Generate clean, professional sample CSV data for questions only"""

    return [
        # Multiple Choice Questions
        {
            'subject_name': 'Mathematics',
            'class_level_name': 'Grade 1',
            'topic_title': 'Numbers 1-20',
            'question_text': 'What number comes after 5?',
            'question_type': 'multiple_choice',
            'correct_answer': 'b',
            'explanation': 'When counting, 6 comes after 5',
            'difficulty': 'easy',
            'points': '1',
            'time_limit': '30',
            'choice_a': '4',
            'choice_b': '6',
            'choice_c': '7',
            'choice_d': '8'
        },
        {
            'subject_name': 'Mathematics',
            'class_level_name': 'Grade 1',
            'topic_title': 'Basic Addition',
            'question_text': 'What is 2 + 3?',
            'question_type': 'multiple_choice',
            'correct_answer': 'c',
            'explanation': '2 + 3 equals 5',
            'difficulty': 'easy',
            'points': '1',
            'time_limit': '45',
            'choice_a': '4',
            'choice_b': '6',
            'choice_c': '5',
            'choice_d': '7'
        },
        # Fill in the Blank Questions
        {
            'subject_name': 'Mathematics',
            'class_level_name': 'Grade 1',
            'topic_title': 'Numbers 1-20',
            'question_text': 'Fill in the missing number: 1, 2, 3, __, 5',
            'question_type': 'fill_blank',
            'correct_answer': '4',
            'explanation': 'The missing number in the sequence is 4',
            'difficulty': 'easy',
            'points': '1',
            'time_limit': '30',
            'choice_a': '',
            'choice_b': '',
            'choice_c': '',
            'choice_d': ''
        },
        # True/False Questions
        {
            'subject_name': 'English Language Arts',
            'class_level_name': 'Grade 1',
            'topic_title': 'Alphabet and Phonics',
            'question_text': 'The letter A comes before B in the alphabet.',
            'question_type': 'true_false',
            'correct_answer': 'true',
            'explanation': 'A comes before B in alphabetical order',
            'difficulty': 'easy',
            'points': '1',
            'time_limit': '20',
            'choice_a': '',
            'choice_b': '',
            'choice_c': '',
            'choice_d': ''
        },
        # Short Answer Questions
        {
            'subject_name': 'English Language Arts',
            'class_level_name': 'Grade 1',
            'topic_title': 'Alphabet and Phonics',
            'question_text': 'What is the first letter of the alphabet?',
            'question_type': 'short_answer',
            'correct_answer': 'A',
            'explanation': 'A is the first letter of the alphabet',
            'difficulty': 'easy',
            'points': '1',
            'time_limit': '30',
            'choice_a': '',
            'choice_b': '',
            'choice_c': '',
            'choice_d': ''
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
            'Available subjects: English Language Arts, Mathematics, Science, Social Studies, Life Skills',
            'Class levels: Grade 1, Grade 2, Grade 3, ... Grade 12',
            'Question types: multiple_choice, fill_blank, true_false, short_answer',
            'Multiple choice: requires correct_answer (a,b,c,d) and choice_a through choice_d',
            'Fill blank/Short answer: requires correct_answer text',
            'True/False: correct_answer should be true/false, t/f, or 1/0',
            'Time limit is per question in seconds (default: 45)',
            'Difficulty levels: easy, medium, hard'
        ]
    }
