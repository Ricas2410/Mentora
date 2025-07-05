#!/usr/bin/env python
"""
Simple Topic Population Script
Creates Grade 5 topics without complex content
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

def create_topics():
    """Create Grade 5 topics for all subjects"""
    print("Creating Grade 5 Topics...")
    print("=" * 40)
    
    # Define all topics for each subject
    subjects_topics = {
        "English Language Arts": [
            ('Reading Comprehension', 'Understanding and analyzing what you read'),
            ('Vocabulary and Word Study', 'Learning new words and their meanings'),
            ('Grammar and Sentence Structure', 'Parts of speech, sentence types, and proper grammar'),
            ('Writing Skills', 'Different types of writing and composition techniques'),
            ('Spelling and Phonics', 'Spelling patterns, rules, and sound-letter relationships'),
            ('Literature and Poetry', 'Understanding stories, poems, and literary elements'),
            ('Speaking and Listening', 'Communication skills and presentation techniques'),
            ('Research and Information', 'Finding, evaluating, and using information sources'),
        ],
        "Mathematics": [
            ('Place Value and Number Sense', 'Understanding place value up to millions and number relationships'),
            ('Addition and Subtraction', 'Multi-digit addition and subtraction with regrouping'),
            ('Multiplication and Division', 'Multi-digit multiplication and division strategies'),
            ('Fractions', 'Understanding fractions, equivalent fractions, and operations'),
            ('Decimals', 'Decimal place value, comparing, and basic operations'),
            ('Measurement', 'Length, weight, capacity, time, and temperature'),
            ('Geometry', 'Shapes, angles, lines, and basic geometric concepts'),
            ('Data and Graphs', 'Collecting, organizing, and interpreting data'),
        ],
        "Science": [
            ('Living Things and Their Environment', 'Ecosystems, habitats, and how living things interact'),
            ('Human Body Systems', 'Digestive, respiratory, and circulatory systems'),
            ('Plants and Animals', 'Life cycles, adaptations, and classification'),
            ('Matter and Its Properties', 'States of matter, physical and chemical changes'),
            ('Forces and Motion', 'Gravity, friction, and simple machines'),
            ('Energy and Heat', 'Forms of energy, heat transfer, and conservation'),
            ('Earth and Space', 'Weather, water cycle, and solar system'),
            ('Scientific Method', 'Observation, hypothesis, experiments, and conclusions'),
        ],
        "Social Studies": [
            ('Geography and Maps', 'Understanding maps, continents, and geographic features'),
            ('Communities and Cultures', 'Different communities, traditions, and ways of life'),
            ('Government and Citizenship', 'How government works and being a good citizen'),
            ('Economics and Resources', 'Needs, wants, goods, services, and natural resources'),
            ('History and Time', 'Understanding past, present, future, and historical events'),
            ('World Cultures', 'Learning about different countries and their customs'),
            ('Environment and Society', 'How humans interact with and change the environment'),
            ('Rights and Responsibilities', 'Human rights, responsibilities, and treating others fairly'),
        ],
        "Life Skills": [
            ('Personal Health and Hygiene', 'Taking care of your body and staying healthy'),
            ('Safety and First Aid', 'Staying safe at home, school, and in the community'),
            ('Communication Skills', 'Speaking, listening, and expressing yourself clearly'),
            ('Problem Solving', 'Finding solutions and making good decisions'),
            ('Time Management', 'Organizing your time and being responsible'),
            ('Friendship and Relationships', 'Building healthy relationships and resolving conflicts'),
            ('Money and Budgeting', 'Understanding money, saving, and spending wisely'),
            ('Goal Setting and Achievement', 'Setting goals and working to achieve them'),
        ]
    }
    
    total_created = 0
    
    for subject_name, topics_data in subjects_topics.items():
        print(f"\nProcessing {subject_name}...")
        
        try:
            # Get the subject and class level
            subject = Subject.objects.get(name=subject_name)
            class_level = ClassLevel.objects.get(subject=subject, level_number=5)
            
            # Clear existing topics for this subject/level
            existing_count = class_level.topics.count()
            if existing_count > 0:
                print(f"  Clearing {existing_count} existing topics...")
                class_level.topics.all().delete()
            
            # Create new topics
            created_count = 0
            for order, (title, description) in enumerate(topics_data, 1):
                topic = Topic.objects.create(
                    title=title,
                    class_level=class_level,
                    description=description,
                    order=order,
                    is_active=True
                )
                print(f"  Created: {title}")
                created_count += 1
            
            print(f"  SUCCESS: {created_count} topics created for {subject_name}")
            total_created += created_count
            
        except Subject.DoesNotExist:
            print(f"  ERROR: Subject '{subject_name}' not found!")
        except ClassLevel.DoesNotExist:
            print(f"  ERROR: Grade 5 level not found for {subject_name}!")
        except Exception as e:
            print(f"  ERROR: {str(e)}")
    
    print(f"\nSUMMARY:")
    print(f"Total topics created: {total_created}")
    print(f"Expected: 40 topics (8 per subject x 5 subjects)")
    
    if total_created == 40:
        print("SUCCESS: All Grade 5 topics created successfully!")
    else:
        print(f"WARNING: Only {total_created}/40 topics created")
    
    return total_created == 40

if __name__ == '__main__':
    create_topics()
