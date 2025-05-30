#!/usr/bin/env python
"""
Script to internationalize the Mentora platform
- Removes Ghana-specific references
- Updates to international grade system (Grades 1-12)
- Clears existing data and repopulates with international content
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from django.db import transaction
from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice, StudyNote, Passage
from users.models import User
from progress.models import UserProgress, TopicProgress, StudySession, Achievement

def clear_existing_data():
    """Clear all existing educational data"""
    print("🧹 Clearing existing data...")

    with transaction.atomic():
        # Clear content data
        Achievement.objects.all().delete()
        StudySession.objects.all().delete()
        TopicProgress.objects.all().delete()
        UserProgress.objects.all().delete()

        AnswerChoice.objects.all().delete()
        Question.objects.all().delete()
        StudyNote.objects.all().delete()
        Passage.objects.all().delete()

        # Clear subjects data
        Topic.objects.all().delete()
        ClassLevel.objects.all().delete()
        Subject.objects.all().delete()

        print("✅ All existing educational data cleared")

def create_international_subjects():
    """Create international subjects"""
    print("🌍 Creating international subjects...")

    subjects_data = [
        {
            'name': 'English Language Arts',
            'description': 'Reading, writing, grammar, literature, and communication skills',
            'icon': '📚',
            'color': '#10B981',
            'order': 1
        },
        {
            'name': 'Mathematics',
            'description': 'Numbers, algebra, geometry, statistics, and problem-solving',
            'icon': '🔢',
            'color': '#3B82F6',
            'order': 2
        },
        {
            'name': 'Science',
            'description': 'Biology, chemistry, physics, and earth sciences',
            'icon': '🔬',
            'color': '#8B5CF6',
            'order': 3
        },
        {
            'name': 'Social Studies',
            'description': 'History, geography, civics, and cultural studies',
            'icon': '🌍',
            'color': '#F59E0B',
            'order': 4
        },
        {
            'name': 'Life Skills',
            'description': 'Health, safety, values, and practical life skills',
            'icon': '🌱',
            'color': '#EF4444',
            'order': 5
        }
    ]

    created_subjects = {}
    for subject_data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            name=subject_data['name'],
            defaults={
                'description': subject_data['description'],
                'icon': subject_data['icon'],
                'color': subject_data['color'],
                'order': subject_data['order'],
                'is_active': True
            }
        )
        created_subjects[subject_data['name']] = subject
        print(f"✅ Created subject: {subject_data['name']}")

    return created_subjects

def create_international_grade_levels(subjects):
    """Create international grade levels (Grades 1-12)"""
    print("📚 Creating international grade levels...")

    # Define education levels
    grade_levels = [
        # Elementary School (Grades 1-6)
        {'grades': range(1, 7), 'level_type': 'Elementary', 'age_range': '6-12 years'},
        # Middle School (Grades 7-9)
        {'grades': range(7, 10), 'level_type': 'Middle School', 'age_range': '12-15 years'},
        # High School (Grades 10-12)
        {'grades': range(10, 13), 'level_type': 'High School', 'age_range': '15-18 years'}
    ]

    created_levels = {}

    for subject_name, subject in subjects.items():
        created_levels[subject_name] = {}

        for level_info in grade_levels:
            for grade in level_info['grades']:
                # Determine pass percentage based on grade level
                if grade <= 3:
                    pass_percentage = 60  # Lower grades
                elif grade <= 6:
                    pass_percentage = 65  # Elementary
                elif grade <= 9:
                    pass_percentage = 70  # Middle school
                else:
                    pass_percentage = 75  # High school

                class_level, created = ClassLevel.objects.get_or_create(
                    subject=subject,
                    level_number=grade,
                    defaults={
                        'name': f'Grade {grade}',
                        'description': f'{level_info["level_type"]} - Grade {grade} ({level_info["age_range"]})',
                        'pass_percentage': pass_percentage,
                        'is_active': True
                    }
                )
                created_levels[subject_name][grade] = class_level

                if created:
                    print(f"✅ Created {subject_name} - Grade {grade}")

    return created_levels

def create_sample_topics(grade_levels):
    """Create sample topics for each grade level"""
    print("📖 Creating sample topics...")

    # Sample topics for English Language Arts
    english_topics = {
        1: ['Alphabet and Phonics', 'Simple Words', 'Basic Reading', 'Listening Skills'],
        2: ['Sight Words', 'Simple Sentences', 'Story Reading', 'Basic Writing'],
        3: ['Reading Comprehension', 'Grammar Basics', 'Creative Writing', 'Vocabulary Building'],
        4: ['Advanced Reading', 'Parts of Speech', 'Essay Writing', 'Literature Introduction'],
        5: ['Complex Texts', 'Advanced Grammar', 'Research Skills', 'Poetry Analysis'],
        6: ['Critical Reading', 'Writing Techniques', 'Public Speaking', 'Media Literacy'],
        7: ['Literary Analysis', 'Persuasive Writing', 'Research Papers', 'Drama Studies'],
        8: ['Advanced Literature', 'Argumentative Essays', 'Presentation Skills', 'Language Arts'],
        9: ['World Literature', 'Advanced Composition', 'Critical Thinking', 'Communication'],
        10: ['Classic Literature', 'Academic Writing', 'Rhetoric', 'Language Analysis'],
        11: ['Contemporary Literature', 'Advanced Essays', 'Debate Skills', 'Literary Criticism'],
        12: ['College Prep Writing', 'Advanced Analysis', 'Research Methods', 'Communication Arts']
    }

    # Sample topics for Mathematics
    math_topics = {
        1: ['Numbers 1-20', 'Basic Addition', 'Basic Subtraction', 'Shapes'],
        2: ['Numbers 1-100', 'Two-digit Addition', 'Two-digit Subtraction', 'Time'],
        3: ['Multiplication Tables', 'Division Basics', 'Fractions', 'Measurement'],
        4: ['Multi-digit Operations', 'Decimals', 'Geometry', 'Data Analysis'],
        5: ['Advanced Fractions', 'Percentages', 'Area and Perimeter', 'Probability'],
        6: ['Ratios and Proportions', 'Integers', 'Coordinate Plane', 'Statistics'],
        7: ['Pre-Algebra', 'Linear Equations', 'Geometry Proofs', 'Data Analysis'],
        8: ['Algebra I', 'Functions', 'Pythagorean Theorem', 'Scientific Notation'],
        9: ['Algebra II', 'Quadratic Equations', 'Trigonometry Basics', 'Statistics'],
        10: ['Geometry', 'Advanced Algebra', 'Trigonometry', 'Mathematical Modeling'],
        11: ['Pre-Calculus', 'Advanced Functions', 'Sequences and Series', 'Probability'],
        12: ['Calculus Introduction', 'Advanced Statistics', 'Mathematical Analysis', 'Applied Math']
    }

    # Create topics for English Language Arts
    english_subject = grade_levels['English Language Arts']
    for grade, topics in english_topics.items():
        if grade in english_subject:
            class_level = english_subject[grade]
            for i, topic_title in enumerate(topics):
                Topic.objects.get_or_create(
                    class_level=class_level,
                    title=topic_title,
                    defaults={
                        'description': f'Grade {grade} {topic_title} curriculum',
                        'order': i + 1,
                        'estimated_duration': 45 + (grade * 2),  # Longer for higher grades
                        'difficulty_level': 'beginner' if grade <= 3 else 'intermediate' if grade <= 8 else 'advanced',
                        'is_active': True
                    }
                )

    # Create topics for Mathematics
    math_subject = grade_levels['Mathematics']
    for grade, topics in math_topics.items():
        if grade in math_subject:
            class_level = math_subject[grade]
            for i, topic_title in enumerate(topics):
                Topic.objects.get_or_create(
                    class_level=class_level,
                    title=topic_title,
                    defaults={
                        'description': f'Grade {grade} {topic_title} curriculum',
                        'order': i + 1,
                        'estimated_duration': 50 + (grade * 2),
                        'difficulty_level': 'beginner' if grade <= 3 else 'intermediate' if grade <= 8 else 'advanced',
                        'is_active': True
                    }
                )

    print("✅ Sample topics created for all grade levels")

def create_admin_user():
    """Create or update admin user"""
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@mentora.edu',
            'first_name': 'System',
            'last_name': 'Administrator',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✅ Created admin user")
    else:
        print("📖 Admin user already exists")

    return admin_user

def main():
    """Main internationalization process"""
    print("🌍 Starting Mentora Platform Internationalization...")
    print("=" * 60)

    # Step 1: Clear existing data
    clear_existing_data()

    # Step 2: Create admin user
    admin_user = create_admin_user()

    # Step 3: Create international subjects
    subjects = create_international_subjects()

    # Step 4: Create international grade levels
    grade_levels = create_international_grade_levels(subjects)

    # Step 5: Create sample topics
    create_sample_topics(grade_levels)

    print("\n" + "=" * 60)
    print("🎉 Platform internationalization completed successfully!")
    print("\n📊 Summary:")
    print(f"   • {Subject.objects.count()} subjects created")
    print(f"   • {ClassLevel.objects.count()} grade levels created")
    print(f"   • {Topic.objects.count()} topics created")
    print("\n🌍 The platform now uses international grade levels (Grades 1-12)")
    print("🚀 Ready for global use!")

if __name__ == '__main__':
    main()
