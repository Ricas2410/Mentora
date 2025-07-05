#!/usr/bin/env python
"""
Comprehensive Grade 5 Science Content Population Script
Creates detailed study notes and quiz questions for all science topics
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

def create_science_content():
    """Create comprehensive Grade 5 Science content"""
    print("🔬 Creating Grade 5 Science Content...")
    
    # Get Science subject and Grade 5 level
    try:
        science_subject = Subject.objects.get(name="Science")
        grade5_science = ClassLevel.objects.get(subject=science_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Science subject or Grade 5 level not found!")
        return
    
    # Science topics for Grade 5
    topics_data = [
        {
            'title': 'Living Things and Their Environment',
            'description': 'Ecosystems, habitats, and how living things interact',
            'order': 1
        },
        {
            'title': 'Human Body Systems',
            'description': 'Digestive, respiratory, and circulatory systems',
            'order': 2
        },
        {
            'title': 'Plants and Animals',
            'description': 'Life cycles, adaptations, and classification',
            'order': 3
        },
        {
            'title': 'Matter and Its Properties',
            'description': 'States of matter, physical and chemical changes',
            'order': 4
        },
        {
            'title': 'Forces and Motion',
            'description': 'Gravity, friction, and simple machines',
            'order': 5
        },
        {
            'title': 'Energy and Heat',
            'description': 'Forms of energy, heat transfer, and conservation',
            'order': 6
        },
        {
            'title': 'Earth and Space',
            'description': 'Weather, water cycle, and solar system',
            'order': 7
        },
        {
            'title': 'Scientific Method',
            'description': 'Observation, hypothesis, experiments, and conclusions',
            'order': 8
        }
    ]
    
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            title=topic_data['title'],
            class_level=grade5_science,
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
        'Living Things and Their Environment': {
            'title': 'Ecosystems and Habitats',
            'content': '''
# Living Things and Their Environment

## What is an Ecosystem?
An ecosystem is a community of living things (plants, animals, bacteria) and non-living things (air, water, soil, rocks) that interact with each other.

### Parts of an Ecosystem
**Living Parts (Biotic):**
- Plants (producers)
- Animals (consumers)
- Bacteria and fungi (decomposers)

**Non-living Parts (Abiotic):**
- Air and gases
- Water
- Soil and rocks
- Sunlight
- Temperature

## Food Chains and Food Webs
### Food Chain Example:
Grass → Rabbit → Fox → Decomposer

**Energy Flow:**
1. **Producers** (plants) make their own food using sunlight
2. **Primary consumers** (herbivores) eat plants
3. **Secondary consumers** (carnivores) eat herbivores
4. **Decomposers** break down dead organisms

### Food Web
A food web shows how multiple food chains connect in an ecosystem.

## Habitats
A habitat is the natural home of a living thing where it finds everything it needs to survive.

### Examples of Habitats:
- **Forest:** Trees, deer, bears, birds
- **Ocean:** Fish, whales, coral, seaweed
- **Desert:** Cacti, lizards, snakes, scorpions
- **Grassland:** Grass, zebras, lions, elephants

## Adaptations
Adaptations are special features that help living things survive in their habitat.

### Examples:
- **Polar bears:** Thick fur for cold weather
- **Cacti:** Store water in thick stems
- **Birds:** Wings for flying, beaks for different foods
- **Fish:** Gills for breathing underwater

## Human Impact on Environment
### Positive Actions:
- Recycling and reducing waste
- Planting trees
- Protecting wildlife
- Using renewable energy

### Negative Actions:
- Pollution (air, water, land)
- Deforestation
- Overfishing
- Littering

## Conservation
We must protect our environment by:
1. Reducing, reusing, and recycling
2. Saving water and energy
3. Protecting animal habitats
4. Learning about nature
'''
        },
        
        'Human Body Systems': {
            'title': 'How Our Body Works',
            'content': '''
# Human Body Systems

## Digestive System
The digestive system breaks down food so our body can use it for energy.

### Parts and Functions:
1. **Mouth:** Teeth chew food, saliva starts digestion
2. **Esophagus:** Tube that carries food to stomach
3. **Stomach:** Mixes food with acid to break it down
4. **Small intestine:** Absorbs nutrients into blood
5. **Large intestine:** Removes water, forms waste

### Digestion Process:
Food → Mouth → Esophagus → Stomach → Small intestine → Large intestine → Waste removal

## Respiratory System
The respiratory system helps us breathe and get oxygen.

### Parts and Functions:
1. **Nose/Mouth:** Air enters here
2. **Trachea:** Windpipe carries air to lungs
3. **Lungs:** Two organs that exchange oxygen and carbon dioxide
4. **Diaphragm:** Muscle that helps lungs expand and contract

### Breathing Process:
- **Inhale:** Diaphragm moves down, lungs expand, air rushes in
- **Exhale:** Diaphragm moves up, lungs contract, air rushes out

## Circulatory System
The circulatory system pumps blood throughout the body.

### Parts and Functions:
1. **Heart:** Four-chambered pump that pushes blood
2. **Blood vessels:** Tubes that carry blood
   - **Arteries:** Carry blood away from heart
   - **Veins:** Carry blood back to heart
   - **Capillaries:** Tiny vessels that connect arteries and veins
3. **Blood:** Carries oxygen, nutrients, and waste

### Blood Flow:
Heart → Arteries → Capillaries → Veins → Heart

## How Systems Work Together
- Digestive system provides nutrients
- Respiratory system provides oxygen
- Circulatory system delivers both to all body parts

## Staying Healthy
### Good Habits:
- Eat nutritious foods
- Exercise regularly
- Get enough sleep
- Drink plenty of water
- Wash hands frequently
- Avoid harmful substances
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
        'Living Things and Their Environment': [
            {
                'question_text': 'What do we call the natural home where a living thing finds everything it needs to survive?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Ecosystem', 'is_correct': False},
                    {'text': 'Habitat', 'is_correct': True},
                    {'text': 'Food chain', 'is_correct': False},
                    {'text': 'Environment', 'is_correct': False}
                ],
                'explanation': 'A habitat is the natural home of a living thing where it finds food, water, shelter, and everything else it needs to survive.'
            },
            {
                'question_text': 'In a food chain, what are plants called?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Consumers', 'is_correct': False},
                    {'text': 'Decomposers', 'is_correct': False},
                    {'text': 'Producers', 'is_correct': True},
                    {'text': 'Predators', 'is_correct': False}
                ],
                'explanation': 'Plants are called producers because they produce (make) their own food using sunlight through photosynthesis.'
            }
        ],
        
        'Human Body Systems': [
            {
                'question_text': 'Which organ pumps blood throughout your body?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Lungs', 'is_correct': False},
                    {'text': 'Heart', 'is_correct': True},
                    {'text': 'Stomach', 'is_correct': False},
                    {'text': 'Brain', 'is_correct': False}
                ],
                'explanation': 'The heart is a four-chambered muscle that pumps blood throughout the body, delivering oxygen and nutrients to all organs.'
            },
            {
                'question_text': 'Where does digestion begin?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Stomach', 'is_correct': False},
                    {'text': 'Small intestine', 'is_correct': False},
                    {'text': 'Mouth', 'is_correct': True},
                    {'text': 'Esophagus', 'is_correct': False}
                ],
                'explanation': 'Digestion begins in the mouth where teeth chew food and saliva starts breaking it down chemically.'
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
    create_science_content()
    print("✅ Grade 5 Science content creation completed!")
