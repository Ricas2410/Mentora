#!/usr/bin/env python
"""
Comprehensive Grade 5 Social Studies Content Population Script
Creates detailed study notes and quiz questions for all social studies topics
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

def create_social_studies_content():
    """Create comprehensive Grade 5 Social Studies content"""
    print("🌍 Creating Grade 5 Social Studies Content...")
    
    # Get Social Studies subject and Grade 5 level
    try:
        social_subject = Subject.objects.get(name="Social Studies")
        grade5_social = ClassLevel.objects.get(subject=social_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Social Studies subject or Grade 5 level not found!")
        return
    
    # Social Studies topics for Grade 5
    topics_data = [
        {
            'title': 'Geography and Maps',
            'description': 'Understanding maps, continents, and geographic features',
            'order': 1
        },
        {
            'title': 'Communities and Cultures',
            'description': 'Different communities, traditions, and ways of life',
            'order': 2
        },
        {
            'title': 'Government and Citizenship',
            'description': 'How government works and being a good citizen',
            'order': 3
        },
        {
            'title': 'Economics and Resources',
            'description': 'Needs, wants, goods, services, and natural resources',
            'order': 4
        },
        {
            'title': 'History and Time',
            'description': 'Understanding past, present, future, and historical events',
            'order': 5
        },
        {
            'title': 'World Cultures',
            'description': 'Learning about different countries and their customs',
            'order': 6
        },
        {
            'title': 'Environment and Society',
            'description': 'How humans interact with and change the environment',
            'order': 7
        },
        {
            'title': 'Rights and Responsibilities',
            'description': 'Human rights, responsibilities, and treating others fairly',
            'order': 8
        }
    ]
    
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            title=topic_data['title'],
            class_level=grade5_social,
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Created topic: {topic.title}")
            create_study_notes(topic)
            create_quiz_questions(topic)
        else:
            print(f"📝 Topic already exists: {topic.title}")

def create_study_notes(topic):
    """Create comprehensive study notes for each topic"""
    
    study_notes_data = {
        'Geography and Maps': {
            'title': 'Understanding Our World Through Maps',
            'content': '''
# Geography and Maps

## What is Geography?
Geography is the study of Earth's surface, including land, water, air, and the distribution of life on Earth, including human life and the effects of human activity.

## Types of Maps
### Physical Maps
- Show natural features like mountains, rivers, lakes, and deserts
- Use colors: blue for water, green for low land, brown for mountains

### Political Maps
- Show countries, states, cities, and borders
- Use different colors for different countries or regions

### Climate Maps
- Show weather patterns and temperature zones
- Help us understand what the weather is like in different places

## Map Elements
Every good map has these important parts:

### 1. Title
- Tells you what the map shows
- Example: "Map of North America"

### 2. Legend (Map Key)
- Explains what symbols and colors mean
- Shows scale and measurements

### 3. Compass Rose
- Shows directions: North, South, East, West
- Helps you navigate and understand location

### 4. Scale
- Shows how distances on the map relate to real distances
- Example: 1 inch = 100 miles

## The Seven Continents
1. **Asia** - Largest continent, includes China, India, Japan
2. **Africa** - Second largest, includes Egypt, Kenya, South Africa
3. **North America** - Includes USA, Canada, Mexico
4. **South America** - Includes Brazil, Argentina, Peru
5. **Antarctica** - Coldest continent, mostly ice
6. **Europe** - Includes France, Germany, Italy
7. **Australia/Oceania** - Smallest continent

## The Five Oceans
1. **Pacific Ocean** - Largest ocean
2. **Atlantic Ocean** - Second largest
3. **Indian Ocean** - Third largest
4. **Arctic Ocean** - Smallest, very cold
5. **Southern Ocean** - Surrounds Antarctica

## Geographic Features
### Landforms:
- **Mountains:** Very high land (Example: Mount Everest)
- **Hills:** High land, smaller than mountains
- **Plains:** Flat, low land good for farming
- **Valleys:** Low land between hills or mountains
- **Plateaus:** High, flat land

### Water Features:
- **Rivers:** Moving water that flows to the sea
- **Lakes:** Bodies of water surrounded by land
- **Bays:** Parts of oceans that curve into land
- **Islands:** Land completely surrounded by water

## Using Maps in Daily Life
- Finding directions when traveling
- Understanding weather reports
- Learning about other countries
- Planning trips and adventures
- Understanding news from around the world
'''
        },
        
        'Communities and Cultures': {
            'title': 'Different Ways People Live',
            'content': '''
# Communities and Cultures

## What is a Community?
A community is a group of people who live in the same area and share common interests, values, or goals.

## Types of Communities
### Urban Communities (Cities)
**Characteristics:**
- Many people live close together
- Tall buildings and apartments
- Public transportation (buses, trains)
- Many jobs and businesses
- Hospitals, schools, libraries

**Examples:** New York City, London, Tokyo

### Suburban Communities
**Characteristics:**
- Houses with yards
- Quieter than cities
- People often drive cars
- Shopping centers and malls
- Good schools and parks

### Rural Communities (Countryside)
**Characteristics:**
- Fewer people, more space
- Farms and open land
- People know each other well
- Closer to nature
- May be far from stores and hospitals

## What is Culture?
Culture includes the beliefs, customs, arts, food, and way of life of a group of people.

## Elements of Culture
### 1. Language
- How people communicate
- Different countries speak different languages
- Some places have multiple languages

### 2. Food
- Traditional dishes and cooking methods
- Example: Pizza from Italy, Tacos from Mexico, Sushi from Japan

### 3. Clothing
- Traditional dress and everyday clothes
- Example: Kilts from Scotland, Saris from India

### 4. Celebrations and Holidays
- Special days that are important to different groups
- Example: Christmas, Diwali, Chinese New Year, Ramadan

### 5. Arts and Music
- Traditional dances, songs, and artwork
- Example: Flamenco dancing from Spain, Drums from Africa

### 6. Religion and Beliefs
- What people believe about life and the world
- Different religions: Christianity, Islam, Judaism, Hinduism, Buddhism

## Family Structures
### Nuclear Family
- Parents and their children living together

### Extended Family
- Includes grandparents, aunts, uncles, cousins

### Single-Parent Family
- One parent raising children

### Blended Family
- Families that combine when parents remarry

## Respecting Differences
### Why Diversity is Important:
- We learn from each other
- Different perspectives solve problems better
- Makes life more interesting
- Helps us understand the world

### How to Show Respect:
- Listen to others' ideas
- Ask questions to learn more
- Don't make assumptions
- Treat everyone fairly
- Celebrate differences

## Community Helpers
People who work to make our community better:
- Teachers (help us learn)
- Police officers (keep us safe)
- Firefighters (protect from fires)
- Doctors and nurses (keep us healthy)
- Mail carriers (deliver mail)
- Garbage collectors (keep communities clean)
'''
        }
    }
    
    if topic.title in study_notes_data:
        note_data = study_notes_data[topic.title]
        study_note, created = StudyNote.objects.get_or_create(
            topic=topic,
            title=note_data['title'],
            defaults={
                'content': note_data['content'],
                'order': 1,
                'is_active': True
            }
        )
        
        if created:
            print(f"  📚 Created study note: {note_data['title']}")

def create_quiz_questions(topic):
    """Create quiz questions for each topic"""
    
    questions_data = {
        'Geography and Maps': [
            {
                'question_text': 'What is the largest continent on Earth?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Africa', 'is_correct': False},
                    {'text': 'Asia', 'is_correct': True},
                    {'text': 'North America', 'is_correct': False},
                    {'text': 'Europe', 'is_correct': False}
                ],
                'explanation': 'Asia is the largest continent, covering about 30% of Earth\'s land area and home to over 4 billion people.'
            },
            {
                'question_text': 'What part of a map shows what the symbols and colors mean?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Compass rose', 'is_correct': False},
                    {'text': 'Scale', 'is_correct': False},
                    {'text': 'Legend', 'is_correct': True},
                    {'text': 'Title', 'is_correct': False}
                ],
                'explanation': 'The legend (also called map key) explains what all the symbols, colors, and markings on a map represent.'
            }
        ],
        
        'Communities and Cultures': [
            {
                'question_text': 'What type of community has many tall buildings and public transportation?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Rural', 'is_correct': False},
                    {'text': 'Urban', 'is_correct': True},
                    {'text': 'Suburban', 'is_correct': False},
                    {'text': 'Agricultural', 'is_correct': False}
                ],
                'explanation': 'Urban communities (cities) are characterized by tall buildings, many people living close together, and public transportation systems.'
            },
            {
                'question_text': 'Which of these is NOT typically part of culture?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Language', 'is_correct': False},
                    {'text': 'Food traditions', 'is_correct': False},
                    {'text': 'Weather patterns', 'is_correct': True},
                    {'text': 'Celebrations', 'is_correct': False}
                ],
                'explanation': 'Weather patterns are part of geography and climate, not culture. Culture includes language, food, celebrations, beliefs, and customs.'
            }
        ]
    }
    
    if topic.title in questions_data:
        for i, q_data in enumerate(questions_data[topic.title]):
            question, created = Question.objects.get_or_create(
                topic=topic,
                question_text=q_data['question_text'],
                defaults={
                    'question_type': q_data['question_type'],
                    'explanation': q_data.get('explanation', ''),
                    'order': i + 1,
                    'is_active': True
                }
            )
            
            if created:
                print(f"  ❓ Created question: {q_data['question_text'][:50]}...")
                
                # Create answer choices
                for choice_data in q_data['choices']:
                    AnswerChoice.objects.create(
                        question=question,
                        text=choice_data['text'],
                        is_correct=choice_data['is_correct']
                    )

if __name__ == '__main__':
    create_social_studies_content()
    print("✅ Grade 5 Social Studies content creation completed!")
