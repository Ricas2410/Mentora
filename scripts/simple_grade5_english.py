#!/usr/bin/env python3
"""
Simple script to populate Grade 5 English Language Arts missing content.
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
from content.models import Question, StudyNote

def main():
    """Main function to populate missing content"""
    print("📚 Creating missing Grade 5 English Language Arts content...")

    try:
        # Get the subject and class level
        english = Subject.objects.get(name='English Language Arts')
        grade5 = ClassLevel.objects.get(subject=english, level_number=5)

        # Get topics that need questions
        complex_texts = Topic.objects.get(class_level=grade5, title='Complex Texts')
        research_skills = Topic.objects.get(class_level=grade5, title='Research Skills')
        poetry_analysis = Topic.objects.get(class_level=grade5, title='Poetry Analysis')

        print(f"Found topics:")
        print(f"  - Complex Texts: {complex_texts.id}")
        print(f"  - Research Skills: {research_skills.id}")
        print(f"  - Poetry Analysis: {poetry_analysis.id}")

        # Create questions for Complex Texts
        complex_questions = [
            {
                'question_text': 'Read this passage: "The ancient library stood majestically against the stormy sky, its weathered stones telling stories of centuries past." What does "majestically" mean in this context?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'Majestically means in a grand, impressive, or dignified manner.',
                'difficulty': 'medium',
                'points': 2,
                'choice_a': 'Sadly',
                'choice_b': 'Grandly',
                'choice_c': 'Quickly',
                'choice_d': 'Quietly'
            },
            {
                'question_text': 'In the sentence "The scientist\'s hypothesis was both innovative and controversial," what can you infer about the hypothesis?',
                'question_type': 'multiple_choice',
                'correct_answer': 'c',
                'explanation': 'The hypothesis was new/creative (innovative) but also caused disagreement (controversial).',
                'difficulty': 'medium',
                'points': 2,
                'choice_a': 'It was widely accepted',
                'choice_b': 'It was old and outdated',
                'choice_c': 'It was new but caused debate',
                'choice_d': 'It was proven wrong'
            },
            {
                'question_text': 'What is the main purpose of a thesis statement in an essay?',
                'question_type': 'multiple_choice',
                'correct_answer': 'a',
                'explanation': 'A thesis statement presents the main argument or central idea of an essay.',
                'difficulty': 'medium',
                'points': 2,
                'choice_a': 'To state the main argument',
                'choice_b': 'To list all the topics',
                'choice_c': 'To conclude the essay',
                'choice_d': 'To introduce the author'
            },
            {
                'question_text': 'When reading a complex text, what should you do if you encounter an unfamiliar word?',
                'question_type': 'multiple_choice',
                'correct_answer': 'd',
                'explanation': 'Using context clues helps you understand unfamiliar words without stopping to look them up.',
                'difficulty': 'easy',
                'points': 1,
                'choice_a': 'Skip it completely',
                'choice_b': 'Stop reading immediately',
                'choice_c': 'Guess randomly',
                'choice_d': 'Use context clues to understand it'
            },
            {
                'question_text': 'In a complex text, what is a "theme"?',
                'question_type': 'multiple_choice',
                'correct_answer': 'b',
                'explanation': 'A theme is the central message or lesson that the author wants to convey.',
                'difficulty': 'medium',
                'points': 2,
                'choice_a': 'The title of the text',
                'choice_b': 'The main message or lesson',
                'choice_c': 'The number of pages',
                'choice_d': 'The author\'s name'
            }
        ]

        created_count = 0
        for q_data in complex_questions:
            if not Question.objects.filter(topic=complex_texts, question_text=q_data['question_text']).exists():
                Question.objects.create(topic=complex_texts, **q_data)
                created_count += 1

        print(f"    Created {created_count} new questions for Complex Texts")

        print(f"\n✅ Successfully created {created_count} questions!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
