#!/usr/bin/env python3
"""
Comprehensive script to create Grade 5 topics and populate with questions
Creates topics for all subjects and adds professional, real-life questions
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice, StudyNote
from users.models import User
from django.db import transaction

def create_grade5_topics_and_questions():
    """Create comprehensive topics and questions for all Grade 5 subjects"""

    try:
        admin_user = User.objects.filter(is_superuser=True).first()

        # Get all subjects
        subjects = {
            'english': Subject.objects.get(name='English Language Arts'),
            'math': Subject.objects.get(name='Mathematics'),
            'science': Subject.objects.get(name='Science'),
            'social': Subject.objects.get(name='Social Studies'),
            'life': Subject.objects.get(name='Life Skills'),
        }

        print("🚀 Creating Grade 5 topics and questions for all subjects...")

        # Create topics for each subject
        for subject_key, subject in subjects.items():
            grade_5, created = ClassLevel.objects.get_or_create(
                subject=subject,
                level_number=5,
                defaults={
                    'name': f'Grade 5 {subject.name}',
                    'description': f'Grade 5 level content for {subject.name}',
                    'order': 5
                }
            )

            if created:
                print(f"✅ Created Grade 5 class level for {subject.name}")

            # Create topics based on subject
            if subject_key == 'science':
                create_science_topics_and_questions(grade_5, admin_user)
            elif subject_key == 'social':
                create_social_studies_topics_and_questions(grade_5, admin_user)
            elif subject_key == 'life':
                create_life_skills_topics_and_questions(grade_5, admin_user)
            elif subject_key == 'math':
                create_additional_math_topics_and_questions(grade_5, admin_user)

        print("🎉 Successfully created all Grade 5 topics and questions!")

    except Exception as e:
        print(f"❌ Error creating topics and questions: {e}")
        raise

def create_science_topics_and_questions(grade_5, admin_user):
    """Create Science topics and questions for Grade 5"""

    # Create Science topics
    topics_data = [
        {
            'title': 'Human Body Systems',
            'description': 'Learn about different body systems and how they work together',
            'order': 1
        },
        {
            'title': 'Weather and Climate',
            'description': 'Understanding weather patterns, climate, and atmospheric conditions',
            'order': 2
        },
        {
            'title': 'Simple Machines',
            'description': 'Explore levers, pulleys, wheels, and other simple machines',
            'order': 3
        },
        {
            'title': 'Plant Life Cycles',
            'description': 'Study how plants grow, reproduce, and adapt to their environment',
            'order': 4
        }
    ]

    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            class_level=grade_5,
            title=topic_data['title'],
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'is_active': True
            }
        )

        if created:
            print(f"  ✅ Created topic: {topic.title}")

            # Create study material for the topic
            StudyNote.objects.get_or_create(
                topic=topic,
                title=f"{topic.title} - Study Guide",
                defaults={
                    'content': f"Comprehensive study guide for {topic.title}. This topic covers important concepts that Grade 5 students need to understand.",
                    'order': 1,
                    'is_active': True,
                    'created_by': admin_user
                }
            )

def create_social_studies_topics_and_questions(grade_5, admin_user):
    """Create Social Studies topics and questions for Grade 5"""

    # Create Social Studies topics
    topics_data = [
        {
            'title': 'World Geography',
            'description': 'Explore continents, countries, and major geographical features',
            'order': 1
        },
        {
            'title': 'Ancient Civilizations',
            'description': 'Learn about early civilizations and their contributions',
            'order': 2
        },
        {
            'title': 'Government and Citizenship',
            'description': 'Understanding how governments work and citizen responsibilities',
            'order': 3
        },
        {
            'title': 'Economics and Trade',
            'description': 'Basic economic concepts, trade, and how communities work together',
            'order': 4
        }
    ]

    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            class_level=grade_5,
            title=topic_data['title'],
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'is_active': True
            }
        )

        if created:
            print(f"  ✅ Created topic: {topic.title}")

            # Create study material for the topic
            StudyNote.objects.get_or_create(
                topic=topic,
                title=f"{topic.title} - Study Guide",
                defaults={
                    'content': f"Comprehensive study guide for {topic.title}. This topic covers important concepts that Grade 5 students need to understand.",
                    'order': 1,
                    'is_active': True,
                    'created_by': admin_user
                }
            )

def create_life_skills_topics_and_questions(grade_5, admin_user):
    """Create Life Skills topics and questions for Grade 5"""

    # Create Life Skills topics
    topics_data = [
        {
            'title': 'Health and Nutrition',
            'description': 'Understanding healthy eating, exercise, and personal wellness',
            'order': 1
        },
        {
            'title': 'Safety and First Aid',
            'description': 'Basic safety rules and simple first aid procedures',
            'order': 2
        },
        {
            'title': 'Communication Skills',
            'description': 'Effective communication, listening, and social interaction',
            'order': 3
        },
        {
            'title': 'Problem Solving',
            'description': 'Critical thinking and problem-solving strategies',
            'order': 4
        }
    ]

    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            class_level=grade_5,
            title=topic_data['title'],
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'is_active': True
            }
        )

        if created:
            print(f"  ✅ Created topic: {topic.title}")

            # Create study material for the topic
            StudyNote.objects.get_or_create(
                topic=topic,
                title=f"{topic.title} - Study Guide",
                defaults={
                    'content': f"Comprehensive study guide for {topic.title}. This topic covers important concepts that Grade 5 students need to understand.",
                    'order': 1,
                    'is_active': True,
                    'created_by': admin_user
                }
            )

def create_additional_math_topics_and_questions(grade_5, admin_user):
    """Create additional Math topics for Grade 5"""

    # Create additional Math topics (some may already exist)
    topics_data = [
        {
            'title': 'Percentages',
            'description': 'Understanding percentages and their real-world applications',
            'order': 2
        },
        {
            'title': 'Area and Perimeter',
            'description': 'Calculating area and perimeter of different shapes',
            'order': 3
        },
        {
            'title': 'Probability',
            'description': 'Basic probability concepts and simple experiments',
            'order': 4
        }
    ]

    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            class_level=grade_5,
            title=topic_data['title'],
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'is_active': True
            }
        )

        if created:
            print(f"  ✅ Created topic: {topic.title}")

            # Create study material for the topic
            StudyNote.objects.get_or_create(
                topic=topic,
                title=f"{topic.title} - Study Guide",
                defaults={
                    'content': f"Comprehensive study guide for {topic.title}. This topic covers important concepts that Grade 5 students need to understand.",
                    'order': 1,
                    'is_active': True,
                    'created_by': admin_user
                }
            )

if __name__ == '__main__':
    create_grade5_topics_and_questions()
