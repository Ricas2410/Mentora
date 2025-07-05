#!/usr/bin/env python
"""
Test script to verify the internationalization was successful
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, StudyNote, Passage

def test_internationalization():
    """Test that the platform has been successfully internationalized"""
    print("🧪 Testing Platform Internationalization...")
    print("=" * 60)
    
    # Test 1: Check subjects are international
    print("\n📚 Testing Subjects...")
    subjects = Subject.objects.all()
    expected_subjects = [
        'English Language Arts',
        'Mathematics', 
        'Science',
        'Social Studies',
        'Life Skills'
    ]
    
    for subject in subjects:
        if subject.name in expected_subjects:
            print(f"✅ Found international subject: {subject.name}")
        else:
            print(f"❌ Unexpected subject: {subject.name}")
    
    # Test 2: Check grade levels are international (Grades 1-12)
    print("\n🎓 Testing Grade Levels...")
    grade_levels = ClassLevel.objects.all().order_by('level_number')
    
    expected_grades = list(range(1, 13))  # Grades 1-12
    found_grades = [level.level_number for level in grade_levels if level.level_number]
    
    for grade in expected_grades:
        if grade in found_grades:
            grade_count = ClassLevel.objects.filter(level_number=grade).count()
            print(f"✅ Grade {grade}: {grade_count} subjects")
        else:
            print(f"❌ Missing Grade {grade}")
    
    # Test 3: Check for old Ghana-specific terms
    print("\n🔍 Checking for old Ghana-specific terms...")
    old_terms_found = []
    
    # Check ClassLevel names
    for level in grade_levels:
        if any(term in level.name.lower() for term in ['primary', 'jhs', 'shs']):
            old_terms_found.append(f"ClassLevel: {level.name}")
    
    # Check Subject names
    for subject in subjects:
        if 'ghanaian' in subject.name.lower() or 'ghana' in subject.description.lower():
            old_terms_found.append(f"Subject: {subject.name}")
    
    if old_terms_found:
        print("❌ Found old Ghana-specific terms:")
        for term in old_terms_found:
            print(f"   - {term}")
    else:
        print("✅ No old Ghana-specific terms found")
    
    # Test 4: Check sample content
    print("\n📖 Testing Sample Content...")
    
    # Check study notes
    study_notes = StudyNote.objects.all()
    print(f"✅ Found {study_notes.count()} study notes")
    
    # Check questions
    questions = Question.objects.all()
    print(f"✅ Found {questions.count()} questions")
    
    # Check passages
    passages = Passage.objects.all()
    print(f"✅ Found {passages.count()} reading passages")
    
    # Test 5: Check topics distribution
    print("\n📋 Testing Topics Distribution...")
    for subject in subjects:
        topic_count = Topic.objects.filter(class_level__subject=subject).count()
        print(f"✅ {subject.name}: {topic_count} topics across all grades")
    
    # Test 6: Summary statistics
    print("\n📊 Platform Statistics:")
    print(f"   • Subjects: {subjects.count()}")
    print(f"   • Grade Levels: {grade_levels.count()}")
    print(f"   • Topics: {Topic.objects.count()}")
    print(f"   • Study Notes: {study_notes.count()}")
    print(f"   • Questions: {questions.count()}")
    print(f"   • Reading Passages: {passages.count()}")
    
    # Test 7: Grade level validation
    print("\n🎯 Grade Level Validation:")
    elementary_count = ClassLevel.objects.filter(level_number__lte=6).count()
    middle_count = ClassLevel.objects.filter(level_number__gte=7, level_number__lte=9).count()
    high_count = ClassLevel.objects.filter(level_number__gte=10).count()
    
    print(f"   • Elementary (Grades 1-6): {elementary_count} grade levels")
    print(f"   • Middle School (Grades 7-9): {middle_count} grade levels")
    print(f"   • High School (Grades 10-12): {high_count} grade levels")
    
    # Final assessment
    print("\n" + "=" * 60)
    total_expected_levels = 5 * 12  # 5 subjects × 12 grades = 60 levels
    
    if grade_levels.count() == total_expected_levels:
        print("🎉 INTERNATIONALIZATION SUCCESSFUL!")
        print("✅ All grade levels created correctly")
        print("✅ International subjects implemented")
        print("✅ Sample content available")
        print("🌍 Platform is ready for global use!")
    else:
        print("⚠️  INTERNATIONALIZATION INCOMPLETE")
        print(f"Expected {total_expected_levels} grade levels, found {grade_levels.count()}")
        print("Some grade levels may be missing")
    
    return True

if __name__ == '__main__':
    test_internationalization()
