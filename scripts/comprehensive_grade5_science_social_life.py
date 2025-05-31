#!/usr/bin/env python
"""
Comprehensive Grade 5 Content - Science, Social Studies, and Life Skills
Adds real-life questions and detailed study notes
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice

def add_comprehensive_science_content():
    """Add comprehensive content for all Science topics"""
    print("Adding comprehensive Science content...")
    
    try:
        subject = Subject.objects.get(name="Science")
        class_level = ClassLevel.objects.get(subject=subject, level_number=5)
    except:
        print("  ERROR: Science subject not found!")
        return False
    
    # Content for Science topics
    content_data = {
        'Living Things and Their Environment': {
            'notes': [
                {
                    'title': 'Ecosystems Around Us',
                    'content': """# Living Things and Their Environment

## What is an Ecosystem?
An ecosystem is like a neighborhood where plants, animals, and non-living things all work together.

## Parts of an Ecosystem

### Living Things (Biotic Factors)
1. **Producers** - Plants that make their own food using sunlight
   - Trees, grass, flowers, algae
   - They are like the "restaurants" of nature

2. **Primary Consumers** - Animals that eat plants
   - Rabbits, deer, caterpillars, cows
   - They are herbivores (plant-eaters)

3. **Secondary Consumers** - Animals that eat other animals
   - Foxes, birds, frogs, spiders
   - They are carnivores (meat-eaters)

4. **Decomposers** - Break down dead things
   - Bacteria, mushrooms, worms
   - They are nature's recyclers

### Non-Living Things (Abiotic Factors)
- Water, air, soil, sunlight, temperature, rocks

## Real-Life Ecosystem Examples

### Your Backyard Ecosystem
- **Producers:** Grass, trees, flowers
- **Primary Consumers:** Squirrels eating nuts, caterpillars eating leaves
- **Secondary Consumers:** Birds eating insects, cats hunting mice
- **Decomposers:** Worms in soil, bacteria breaking down fallen leaves

### School Playground Ecosystem
- **Producers:** Trees providing shade, grass on the field
- **Consumers:** Birds in trees, insects in grass
- **Non-living:** Playground equipment, concrete, sunlight

### Pond Ecosystem
- **Producers:** Water plants, algae
- **Primary Consumers:** Small fish eating plants, tadpoles
- **Secondary Consumers:** Larger fish, frogs, ducks
- **Decomposers:** Bacteria in water and mud

## Food Chains in Real Life
A food chain shows who eats whom:

**Forest Food Chain:**
Acorn → Squirrel → Hawk → Decomposers

**Ocean Food Chain:**
Algae → Small Fish → Tuna → Shark → Decomposers

## How Humans Affect Ecosystems
- **Positive:** Planting trees, creating parks, recycling
- **Negative:** Pollution, cutting down forests, littering

## Protecting Our Environment
- Don't litter - it harms animals and plants
- Recycle paper, plastic, and cans
- Turn off lights to save energy
- Plant flowers and trees
- Use less water"""
                }
            ],
            'questions': [
                {
                    'question_text': 'In your school cafeteria, leftover food scraps are composted. What role do the bacteria and worms in the compost play in the ecosystem?',
                    'choices': [
                        {'text': 'Producers - they make food', 'is_correct': False},
                        {'text': 'Primary consumers - they eat plants', 'is_correct': False},
                        {'text': 'Secondary consumers - they eat animals', 'is_correct': False},
                        {'text': 'Decomposers - they break down dead material', 'is_correct': True}
                    ],
                    'explanation': 'Bacteria and worms are decomposers. They break down dead plants and animals, returning nutrients to the soil so new plants can grow.'
                },
                {
                    'question_text': 'You notice that after a new shopping mall was built, there are fewer birds in the nearby forest. What most likely happened?',
                    'choices': [
                        {'text': 'The birds moved to better nesting areas', 'is_correct': False},
                        {'text': 'Their habitat was destroyed or disturbed', 'is_correct': True},
                        {'text': 'The birds became afraid of people', 'is_correct': False},
                        {'text': 'There is more food available now', 'is_correct': False}
                    ],
                    'explanation': 'When natural areas are developed, animals lose their homes, food sources, and nesting places. This is called habitat destruction.'
                },
                {
                    'question_text': 'Your family starts a vegetable garden. What do the plants in your garden need from the environment to survive?',
                    'choices': [
                        {'text': 'Only water and soil', 'is_correct': False},
                        {'text': 'Only sunlight and air', 'is_correct': False},
                        {'text': 'Water, soil, sunlight, air, and nutrients', 'is_correct': True},
                        {'text': 'Only fertilizer from the store', 'is_correct': False}
                    ],
                    'explanation': 'Plants need multiple things from their environment: water and nutrients from soil, sunlight for energy, and carbon dioxide from air to make food.'
                }
            ]
        },
        'Human Body Systems': {
            'notes': [
                {
                    'title': 'How Your Body Works',
                    'content': """# Human Body Systems

## Your Body is Amazing!
Your body has different systems that work together like a team to keep you healthy and alive.

## Digestive System - Your Body's Food Processor

### What It Does
Breaks down food so your body can use it for energy and growth.

### Main Parts
- **Mouth:** Teeth chop food, saliva starts breaking it down
- **Stomach:** Mixes food with acid to break it down more
- **Small Intestine:** Absorbs nutrients into your blood
- **Large Intestine:** Gets rid of waste

### Real-Life Example
When you eat a sandwich:
1. Your teeth break it into small pieces
2. Your stomach churns it like a washing machine
3. Your intestines take out the good stuff your body needs
4. The leftover waste is removed when you go to the bathroom

## Respiratory System - Your Body's Air Supply

### What It Does
Brings oxygen into your body and removes carbon dioxide.

### Main Parts
- **Nose/Mouth:** Air enters here
- **Lungs:** Two spongy organs that exchange gases
- **Diaphragm:** Muscle that helps you breathe

### Real-Life Example
When you run:
1. You breathe faster to get more oxygen
2. Your lungs work harder to supply oxygen to your muscles
3. Your heart pumps faster to deliver oxygen through your blood

## Circulatory System - Your Body's Highway

### What It Does
Carries blood, oxygen, and nutrients throughout your body.

### Main Parts
- **Heart:** Pumps blood (beats about 100,000 times per day!)
- **Blood Vessels:** Tubes that carry blood everywhere
- **Blood:** Carries oxygen and nutrients

### Real-Life Example
When you get a cut:
1. Blood comes out (you can see it's red because of oxygen)
2. Your body sends special cells to heal the cut
3. Your heart keeps pumping to deliver healing materials

## How Systems Work Together

### When You Exercise
- **Respiratory:** Breathes faster to get more oxygen
- **Circulatory:** Heart beats faster to pump blood
- **Digestive:** Provides energy from food you ate earlier

### When You Eat
- **Digestive:** Breaks down food
- **Circulatory:** Carries nutrients to all body parts
- **Respiratory:** Provides oxygen needed to use the nutrients

## Keeping Your Body Systems Healthy
- **Eat healthy foods:** Fruits, vegetables, whole grains
- **Exercise regularly:** Makes your heart and lungs stronger
- **Get enough sleep:** Helps your body repair itself
- **Drink water:** Helps all systems work properly
- **Wash your hands:** Prevents germs from making you sick"""
                }
            ],
            'questions': [
                {
                    'question_text': 'After eating lunch, you feel full and satisfied. Which body system is primarily responsible for breaking down your food?',
                    'choices': [
                        {'text': 'Respiratory system', 'is_correct': False},
                        {'text': 'Circulatory system', 'is_correct': False},
                        {'text': 'Digestive system', 'is_correct': True},
                        {'text': 'Nervous system', 'is_correct': False}
                    ],
                    'explanation': 'The digestive system breaks down food into nutrients your body can use. It includes your mouth, stomach, and intestines.'
                },
                {
                    'question_text': 'During PE class, you notice your heart beating faster and you\'re breathing harder. Why does this happen?',
                    'choices': [
                        {'text': 'Your body needs more oxygen and nutrients for your muscles', 'is_correct': True},
                        {'text': 'Your body is trying to cool down', 'is_correct': False},
                        {'text': 'Your digestive system is working harder', 'is_correct': False},
                        {'text': 'You are getting sick', 'is_correct': False}
                    ],
                    'explanation': 'When you exercise, your muscles need more oxygen and energy. Your respiratory system breathes faster and your circulatory system pumps faster to meet this need.'
                }
            ]
        }
    }
    
    # Add content for each topic
    topics_added = 0
    for topic_title, data in content_data.items():
        try:
            topic = Topic.objects.get(title=topic_title, class_level=class_level)
            
            # Add study notes
            for note_data in data['notes']:
                note, created = StudyNote.objects.get_or_create(
                    topic=topic,
                    title=note_data['title'],
                    defaults={
                        'content': note_data['content'],
                        'order': 1
                    }
                )
                if created:
                    print(f"  Added note: {note_data['title']}")
            
            # Add questions
            for i, q_data in enumerate(data['questions']):
                question, created = Question.objects.get_or_create(
                    topic=topic,
                    question_text=q_data['question_text'],
                    defaults={
                        'question_type': 'multiple_choice',
                        'explanation': q_data.get('explanation', ''),
                        'order': i + 1,
                        'time_limit': 45,
                        'is_active': True
                    }
                )
                
                if created:
                    print(f"  Added question: {q_data['question_text'][:50]}...")
                    
                    # Add answer choices
                    for j, choice_data in enumerate(q_data['choices']):
                        AnswerChoice.objects.create(
                            question=question,
                            choice_text=choice_data['text'],
                            is_correct=choice_data['is_correct'],
                            order=j + 1
                        )
            
            topics_added += 1
            
        except Topic.DoesNotExist:
            print(f"  WARNING: Topic '{topic_title}' not found")
    
    print(f"  Science: {topics_added} topics updated")
    return topics_added > 0

def main():
    """Add comprehensive content to Science, Social Studies, and Life Skills"""
    print("COMPREHENSIVE GRADE 5 CONTENT - SCIENCE, SOCIAL STUDIES, LIFE SKILLS")
    print("=" * 70)
    
    subjects_completed = 0
    
    # Science
    if add_comprehensive_science_content():
        subjects_completed += 1
    
    # TODO: Add Social Studies and Life Skills content
    
    print(f"\nSUMMARY:")
    print(f"Subjects completed: {subjects_completed}")
    print("Real-life science content added!")

if __name__ == '__main__':
    main()
