#!/usr/bin/env python
"""
Windows-Safe Grade 5 Content Population
Handles database conflicts gracefully without emoji characters
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice

def clear_existing_grade5_content():
    """Clear all existing Grade 5 content to avoid conflicts"""
    print("Clearing existing Grade 5 content...")
    
    grade5_levels = ClassLevel.objects.filter(level_number=5)
    total_cleared = 0
    
    for level in grade5_levels:
        topic_count = level.topics.count()
        if topic_count > 0:
            print(f"  Clearing {level.subject.name} Grade 5: {topic_count} topics")
            level.topics.all().delete()
            total_cleared += topic_count
        else:
            print(f"  {level.subject.name} Grade 5: Already clean")
    
    print(f"Total topics cleared: {total_cleared}")
    return True

def fix_all_topic_orders():
    """Fix topic orders across all grades to prevent conflicts"""
    print("Fixing topic orders across all grades...")
    
    all_levels = ClassLevel.objects.all()
    fixed_count = 0
    
    for level in all_levels:
        topics = Topic.objects.filter(class_level=level).order_by('id')
        if topics.exists():
            for i, topic in enumerate(topics, 1):
                if topic.order != i:
                    topic.order = i
                    topic.save()
                    fixed_count += 1
            print(f"  Fixed {level.subject.name} Grade {level.level_number}: {topics.count()} topics")
    
    print(f"Total topic orders fixed: {fixed_count}")
    return True

def safe_create_topic(title, class_level, description, preferred_order=None):
    """Safely create a topic with automatic order assignment"""
    # Check if topic already exists
    existing_topic = Topic.objects.filter(title=title, class_level=class_level).first()
    if existing_topic:
        return existing_topic, False
    
    # Find next available order
    existing_orders = set(Topic.objects.filter(class_level=class_level).values_list('order', flat=True))
    
    if preferred_order and preferred_order not in existing_orders:
        order = preferred_order
    else:
        order = 1
        while order in existing_orders:
            order += 1
    
    # Create topic
    topic = Topic.objects.create(
        title=title,
        class_level=class_level,
        description=description,
        order=order,
        is_active=True
    )
    
    return topic, True

def populate_english_content():
    """Populate English Language Arts content safely"""
    print("Creating Grade 5 English Language Arts Content...")
    
    try:
        english_subject = Subject.objects.get(name="English Language Arts")
        grade5_english = ClassLevel.objects.get(subject=english_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("ERROR: English Language Arts subject or Grade 5 level not found!")
        return False
    
    topics_data = [
        ('Reading Comprehension', 'Understanding and analyzing what you read'),
        ('Vocabulary and Word Study', 'Learning new words and their meanings'),
        ('Grammar and Sentence Structure', 'Parts of speech, sentence types, and proper grammar'),
        ('Writing Skills', 'Different types of writing and composition techniques'),
        ('Spelling and Phonics', 'Spelling patterns, rules, and sound-letter relationships'),
        ('Literature and Poetry', 'Understanding stories, poems, and literary elements'),
        ('Speaking and Listening', 'Communication skills and presentation techniques'),
        ('Research and Information', 'Finding, evaluating, and using information sources'),
    ]
    
    created_count = 0
    for i, (title, description) in enumerate(topics_data, 1):
        topic, created = safe_create_topic(title, grade5_english, description, i)
        if created:
            print(f"  Created topic: {title}")
            created_count += 1
        else:
            print(f"  Topic already exists: {title}")
    
    print(f"English Language Arts: {created_count} new topics created")
    return True

def populate_mathematics_content():
    """Populate Mathematics content safely"""
    print("Creating Grade 5 Mathematics Content...")
    
    try:
        math_subject = Subject.objects.get(name="Mathematics")
        grade5_math = ClassLevel.objects.get(subject=math_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("ERROR: Mathematics subject or Grade 5 level not found!")
        return False
    
    topics_data = [
        ('Place Value and Number Sense', 'Understanding place value up to millions and number relationships'),
        ('Addition and Subtraction', 'Multi-digit addition and subtraction with regrouping'),
        ('Multiplication and Division', 'Multi-digit multiplication and division strategies'),
        ('Fractions', 'Understanding fractions, equivalent fractions, and operations'),
        ('Decimals', 'Decimal place value, comparing, and basic operations'),
        ('Measurement', 'Length, weight, capacity, time, and temperature'),
        ('Geometry', 'Shapes, angles, lines, and basic geometric concepts'),
        ('Data and Graphs', 'Collecting, organizing, and interpreting data'),
    ]
    
    created_count = 0
    for i, (title, description) in enumerate(topics_data, 1):
        topic, created = safe_create_topic(title, grade5_math, description, i)
        if created:
            print(f"  Created topic: {title}")
            created_count += 1
        else:
            print(f"  Topic already exists: {title}")
    
    print(f"Mathematics: {created_count} new topics created")
    return True

def populate_science_content():
    """Populate Science content safely"""
    print("Creating Grade 5 Science Content...")
    
    try:
        science_subject = Subject.objects.get(name="Science")
        grade5_science = ClassLevel.objects.get(subject=science_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("ERROR: Science subject or Grade 5 level not found!")
        return False
    
    topics_data = [
        ('Living Things and Their Environment', 'Ecosystems, habitats, and how living things interact'),
        ('Human Body Systems', 'Digestive, respiratory, and circulatory systems'),
        ('Plants and Animals', 'Life cycles, adaptations, and classification'),
        ('Matter and Its Properties', 'States of matter, physical and chemical changes'),
        ('Forces and Motion', 'Gravity, friction, and simple machines'),
        ('Energy and Heat', 'Forms of energy, heat transfer, and conservation'),
        ('Earth and Space', 'Weather, water cycle, and solar system'),
        ('Scientific Method', 'Observation, hypothesis, experiments, and conclusions'),
    ]
    
    created_count = 0
    for i, (title, description) in enumerate(topics_data, 1):
        topic, created = safe_create_topic(title, grade5_science, description, i)
        if created:
            print(f"  Created topic: {title}")
            created_count += 1
        else:
            print(f"  Topic already exists: {title}")
    
    print(f"Science: {created_count} new topics created")
    return True

def populate_social_studies_content():
    """Populate Social Studies content safely"""
    print("Creating Grade 5 Social Studies Content...")
    
    try:
        social_subject = Subject.objects.get(name="Social Studies")
        grade5_social = ClassLevel.objects.get(subject=social_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("ERROR: Social Studies subject or Grade 5 level not found!")
        return False
    
    topics_data = [
        ('Geography and Maps', 'Understanding maps, continents, and geographic features'),
        ('Communities and Cultures', 'Different communities, traditions, and ways of life'),
        ('Government and Citizenship', 'How government works and being a good citizen'),
        ('Economics and Resources', 'Needs, wants, goods, services, and natural resources'),
        ('History and Time', 'Understanding past, present, future, and historical events'),
        ('World Cultures', 'Learning about different countries and their customs'),
        ('Environment and Society', 'How humans interact with and change the environment'),
        ('Rights and Responsibilities', 'Human rights, responsibilities, and treating others fairly'),
    ]
    
    created_count = 0
    for i, (title, description) in enumerate(topics_data, 1):
        topic, created = safe_create_topic(title, grade5_social, description, i)
        if created:
            print(f"  Created topic: {title}")
            created_count += 1
        else:
            print(f"  Topic already exists: {title}")
    
    print(f"Social Studies: {created_count} new topics created")
    return True

def populate_life_skills_content():
    """Populate Life Skills content safely"""
    print("Creating Grade 5 Life Skills Content...")
    
    try:
        life_subject = Subject.objects.get(name="Life Skills")
        grade5_life = ClassLevel.objects.get(subject=life_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("ERROR: Life Skills subject or Grade 5 level not found!")
        return False
    
    topics_data = [
        ('Personal Health and Hygiene', 'Taking care of your body and staying healthy'),
        ('Safety and First Aid', 'Staying safe at home, school, and in the community'),
        ('Communication Skills', 'Speaking, listening, and expressing yourself clearly'),
        ('Problem Solving', 'Finding solutions and making good decisions'),
        ('Time Management', 'Organizing your time and being responsible'),
        ('Friendship and Relationships', 'Building healthy relationships and resolving conflicts'),
        ('Money and Budgeting', 'Understanding money, saving, and spending wisely'),
        ('Goal Setting and Achievement', 'Setting goals and working to achieve them'),
    ]
    
    created_count = 0
    for i, (title, description) in enumerate(topics_data, 1):
        topic, created = safe_create_topic(title, grade5_life, description, i)
        if created:
            print(f"  Created topic: {title}")
            created_count += 1
        else:
            print(f"  Topic already exists: {title}")
    
    print(f"Life Skills: {created_count} new topics created")
    return True

def main():
    """Run all content population safely"""
    print("WINDOWS-SAFE GRADE 5 CONTENT POPULATION")
    print("=" * 50)
    
    # Step 1: Clear existing content
    print("\nStep 1: Clearing existing Grade 5 content...")
    clear_existing_grade5_content()
    
    # Step 2: Fix topic orders
    print("\nStep 2: Fixing topic orders...")
    fix_all_topic_orders()
    
    # Step 3: Populate content
    print("\nStep 3: Populating Grade 5 content...")
    
    subjects = [
        ("English Language Arts", populate_english_content),
        ("Mathematics", populate_mathematics_content),
        ("Science", populate_science_content),
        ("Social Studies", populate_social_studies_content),
        ("Life Skills", populate_life_skills_content),
    ]
    
    success_count = 0
    
    for subject_name, populate_func in subjects:
        print(f"\nProcessing {subject_name}...")
        try:
            if populate_func():
                success_count += 1
                print(f"SUCCESS: {subject_name} completed!")
            else:
                print(f"FAILED: {subject_name} failed!")
        except Exception as e:
            print(f"ERROR: {subject_name} error: {str(e)}")
    
    print(f"\nSUMMARY:")
    print(f"Successful: {success_count}/5 subjects")
    print(f"Failed: {5 - success_count}/5 subjects")
    
    if success_count == 5:
        print(f"\nALL SUBJECTS COMPLETED SUCCESSFULLY!")
        print(f"Grade 5 topics are now ready!")
    else:
        print(f"\nSome subjects failed. Check the errors above.")

if __name__ == '__main__':
    main()
