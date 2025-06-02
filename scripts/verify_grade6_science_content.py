#!/usr/bin/env python3
"""
Verification script to check Grade 6 Science content creation.
This script verifies that all topics, notes, and questions were created successfully.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice

def verify_grade6_science_content():
    """Verify that Grade 6 Science content was created successfully"""
    print("🔍 Verifying Grade 6 Science content...")
    
    try:
        # Check if Science subject exists
        science_subject = Subject.objects.get(name="Science")
        print(f"✅ Science subject found: {science_subject.name}")
        
        # Check if Grade 6 Science class level exists
        grade6_science = ClassLevel.objects.get(
            subject=science_subject,
            level_number=6
        )
        print(f"✅ Grade 6 Science class level found: {grade6_science.name}")
        
        # Check topics
        topics = Topic.objects.filter(class_level=grade6_science, is_active=True)
        print(f"\n📚 Topics found: {topics.count()}")
        
        total_questions = 0
        total_notes = 0
        
        for topic in topics:
            notes_count = StudyNote.objects.filter(topic=topic, is_active=True).count()
            questions_count = Question.objects.filter(topic=topic, is_active=True).count()
            
            print(f"  📖 {topic.title}")
            print(f"    📝 Study notes: {notes_count}")
            print(f"    ❓ Questions: {questions_count}")
            
            # Check answer choices for questions
            questions = Question.objects.filter(topic=topic, is_active=True)
            for question in questions[:3]:  # Check first 3 questions
                choices_count = AnswerChoice.objects.filter(question=question).count()
                correct_choices = AnswerChoice.objects.filter(question=question, is_correct=True).count()
                print(f"      🔸 '{question.question_text[:50]}...' - {choices_count} choices, {correct_choices} correct")
            
            if questions_count > 3:
                print(f"      ... and {questions_count - 3} more questions")
            
            total_questions += questions_count
            total_notes += notes_count
            print()
        
        print(f"📊 Summary:")
        print(f"  📚 Total topics: {topics.count()}")
        print(f"  📝 Total study notes: {total_notes}")
        print(f"  ❓ Total questions: {total_questions}")
        
        # Expected counts
        expected_topics = 5
        expected_notes = 5  # One note per topic
        expected_questions = 92  # 30+30+30+1+1
        
        if topics.count() >= expected_topics:
            print(f"✅ Topics count OK ({topics.count()}/{expected_topics})")
        else:
            print(f"⚠️ Topics count low ({topics.count()}/{expected_topics})")
            
        if total_notes >= expected_notes:
            print(f"✅ Study notes count OK ({total_notes}/{expected_notes})")
        else:
            print(f"⚠️ Study notes count low ({total_notes}/{expected_notes})")
            
        if total_questions >= expected_questions:
            print(f"✅ Questions count OK ({total_questions}/{expected_questions})")
        else:
            print(f"⚠️ Questions count low ({total_questions}/{expected_questions})")
        
        print(f"\n🎉 Grade 6 Science content verification completed!")
        return True
        
    except Subject.DoesNotExist:
        print("❌ Science subject not found!")
        return False
    except ClassLevel.DoesNotExist:
        print("❌ Grade 6 Science class level not found!")
        return False
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")
        return False

if __name__ == '__main__':
    verify_grade6_science_content()
