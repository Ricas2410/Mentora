#!/usr/bin/env python3
"""
Grade 5 Content Summary - Show all created content
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, StudyNote

def show_grade5_content_summary():
    """Show comprehensive summary of Grade 5 content"""

    print("🎓 GRADE 5 CONTENT SUMMARY")
    print("=" * 50)

    # Get all subjects with Grade 5 content
    subjects = Subject.objects.filter(classlevels__level_number=5).distinct()

    total_topics = 0
    total_questions = 0
    total_study_notes = 0

    for subject in subjects:
        try:
            grade_5 = ClassLevel.objects.get(subject=subject, level_number=5)
            topics = Topic.objects.filter(class_level=grade_5).order_by('order')

            if topics.exists():
                print(f"\n📚 {subject.name.upper()}")
                print("-" * 30)

                subject_questions = 0
                subject_notes = 0

                for topic in topics:
                    question_count = Question.objects.filter(topic=topic, is_active=True).count()
                    note_count = StudyNote.objects.filter(topic=topic, is_active=True).count()

                    print(f"  📖 {topic.title}")
                    print(f"     Questions: {question_count}")
                    print(f"     Study Notes: {note_count}")

                    subject_questions += question_count
                    subject_notes += note_count
                    total_topics += 1

                print(f"\n  📊 {subject.name} Totals:")
                print(f"     Topics: {topics.count()}")
                print(f"     Questions: {subject_questions}")
                print(f"     Study Notes: {subject_notes}")

                total_questions += subject_questions
                total_study_notes += subject_notes

        except ClassLevel.DoesNotExist:
            continue

    print(f"\n🎯 OVERALL GRADE 5 SUMMARY")
    print("=" * 30)
    print(f"Total Subjects: {subjects.count()}")
    print(f"Total Topics: {total_topics}")
    print(f"Total Questions: {total_questions}")
    print(f"Total Study Notes: {total_study_notes}")

    # Show question types breakdown
    print(f"\n📝 QUESTION TYPES BREAKDOWN")
    print("-" * 30)

    grade_5_topics = Topic.objects.filter(class_level__level_number=5)
    grade_5_questions = Question.objects.filter(topic__in=grade_5_topics, is_active=True)

    question_types = grade_5_questions.values('question_type').distinct()
    for qt in question_types:
        count = grade_5_questions.filter(question_type=qt['question_type']).count()
        print(f"  {qt['question_type'].replace('_', ' ').title()}: {count}")

    # Show difficulty levels
    print(f"\n⭐ DIFFICULTY LEVELS")
    print("-" * 20)

    difficulty_levels = grade_5_questions.values('difficulty').distinct()
    for dl in difficulty_levels:
        count = grade_5_questions.filter(difficulty=dl['difficulty']).count()
        print(f"  {dl['difficulty'].title()}: {count}")

    print(f"\n✅ Grade 5 content is ready for production!")
    print(f"   Students can now take quizzes and learn from study materials.")

if __name__ == '__main__':
    show_grade5_content_summary()
