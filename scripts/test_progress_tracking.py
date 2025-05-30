#!/usr/bin/env python3
"""
Test script to verify progress tracking is working correctly
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from users.models import User
from subjects.models import Subject, ClassLevel, Topic
from progress.models import UserProgress, TopicProgress
from content.models import Question, Quiz, QuizAnswer

def test_progress_tracking():
    """Test the progress tracking system"""
    print("🧪 Testing Progress Tracking System")
    print("=" * 50)

    # Get test user
    test_user = User.objects.filter(username='testuser').first()
    if not test_user:
        test_user = User.objects.filter(is_superuser=False).first()

    if not test_user:
        print("❌ No test user found. Please create a regular user first.")
        return

    print(f"📝 Testing with user: {test_user.username}")
    print(f"📚 Current class level: {test_user.current_class_level}")

    # Get English subject and Grade 5
    try:
        english_subject = Subject.objects.get(name__icontains='English')
        grade_5 = ClassLevel.objects.get(subject=english_subject, level_number=5)
        print(f"✅ Found: {english_subject.name} - {grade_5.name}")
    except Exception as e:
        print(f"❌ Error finding subject/grade: {e}")
        return

    # Check user progress for Grade 5
    user_progress, created = UserProgress.objects.get_or_create(
        user=test_user,
        class_level=grade_5,
        defaults={'is_started': True}
    )

    if created:
        print("📊 Created new UserProgress record")
    else:
        print("📊 Found existing UserProgress record")

    print(f"   - Topics completed: {user_progress.topics_completed}/{user_progress.total_topics}")
    print(f"   - Completion percentage: {user_progress.completion_percentage:.1f}%")
    print(f"   - Is completed: {user_progress.is_completed}")

    # Get topics for Grade 5 English
    topics = Topic.objects.filter(class_level=grade_5, is_active=True)
    print(f"\n📚 Available topics: {topics.count()}")

    for topic in topics:
        print(f"\n🎯 Topic: {topic.title}")

        # Check topic progress
        topic_progress, created = TopicProgress.objects.get_or_create(
            user=test_user,
            topic=topic,
            defaults={'is_started': False}
        )

        print(f"   - Is started: {topic_progress.is_started}")
        print(f"   - Is completed: {topic_progress.is_completed}")
        print(f"   - Best quiz score: {topic_progress.best_quiz_score}%")
        print(f"   - Quiz completed: {topic_progress.quiz_completed}")

        # Check questions count
        questions_count = Question.objects.filter(topic=topic, is_active=True).count()
        print(f"   - Available questions: {questions_count}")

        # Check quiz attempts
        quiz_attempts = Quiz.objects.filter(user=test_user, topic=topic).count()
        print(f"   - Quiz attempts: {quiz_attempts}")

        if quiz_attempts > 0:
            latest_quiz = Quiz.objects.filter(user=test_user, topic=topic).order_by('-started_at').first()
            print(f"   - Latest quiz score: {latest_quiz.percentage:.1f}%")
            print(f"   - Latest quiz passed: {latest_quiz.percentage >= 60}")

    # Update progress
    print(f"\n🔄 Updating progress...")
    user_progress.update_progress()
    user_progress.refresh_from_db()

    print(f"   - Updated topics completed: {user_progress.topics_completed}/{user_progress.total_topics}")
    print(f"   - Updated completion percentage: {user_progress.completion_percentage:.1f}%")
    print(f"   - Updated is completed: {user_progress.is_completed}")

    # Check grade promotion eligibility
    print(f"\n🎓 Grade Promotion Check:")
    current_grade = test_user.current_class_level or 5
    current_grade_subjects = Subject.objects.filter(
        classlevels__level_number=current_grade,
        is_active=True
    ).distinct()

    print(f"   - Current grade: {current_grade}")
    print(f"   - Subjects in current grade: {current_grade_subjects.count()}")

    all_completed = True
    for subject in current_grade_subjects:
        try:
            class_level = ClassLevel.objects.get(subject=subject, level_number=current_grade)
            progress = UserProgress.objects.get(user=test_user, class_level=class_level)
            print(f"   - {subject.name}: {progress.completion_percentage:.1f}% ({'✅' if progress.is_completed else '❌'})")
            if not progress.is_completed:
                all_completed = False
        except (ClassLevel.DoesNotExist, UserProgress.DoesNotExist):
            print(f"   - {subject.name}: No progress found ❌")
            all_completed = False

    print(f"   - Ready for promotion: {'✅' if all_completed else '❌'}")

    print(f"\n✅ Progress tracking test completed!")

if __name__ == '__main__':
    test_progress_tracking()
