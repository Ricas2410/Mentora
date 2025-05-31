#!/usr/bin/env python
"""
Comprehensive Grade 5 Life Skills Content Population Script
Creates detailed study notes and quiz questions for all life skills topics
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

def create_life_skills_content():
    """Create comprehensive Grade 5 Life Skills content"""
    print("🌟 Creating Grade 5 Life Skills Content...")
    
    # Get Life Skills subject and Grade 5 level
    try:
        life_subject = Subject.objects.get(name="Life Skills")
        grade5_life = ClassLevel.objects.get(subject=life_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Life Skills subject or Grade 5 level not found!")
        return
    
    # Life Skills topics for Grade 5
    topics_data = [
        {
            'title': 'Personal Health and Hygiene',
            'description': 'Taking care of your body and staying healthy',
            'order': 1
        },
        {
            'title': 'Safety and First Aid',
            'description': 'Staying safe at home, school, and in the community',
            'order': 2
        },
        {
            'title': 'Communication Skills',
            'description': 'Speaking, listening, and expressing yourself clearly',
            'order': 3
        },
        {
            'title': 'Problem Solving',
            'description': 'Finding solutions and making good decisions',
            'order': 4
        },
        {
            'title': 'Time Management',
            'description': 'Organizing your time and being responsible',
            'order': 5
        },
        {
            'title': 'Friendship and Relationships',
            'description': 'Building healthy relationships and resolving conflicts',
            'order': 6
        },
        {
            'title': 'Money and Budgeting',
            'description': 'Understanding money, saving, and spending wisely',
            'order': 7
        },
        {
            'title': 'Goal Setting and Achievement',
            'description': 'Setting goals and working to achieve them',
            'order': 8
        }
    ]
    
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            title=topic_data['title'],
            class_level=grade5_life,
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
        'Personal Health and Hygiene': {
            'title': 'Taking Care of Your Body',
            'content': '''
# Personal Health and Hygiene

## Why is Personal Hygiene Important?
Good hygiene helps you:
- Stay healthy and prevent illness
- Feel confident and good about yourself
- Make friends and be accepted by others
- Show respect for yourself and others

## Daily Hygiene Habits

### 1. Brushing Your Teeth
**When:** Twice a day (morning and before bed)
**How:**
- Use fluoride toothpaste
- Brush for 2 minutes
- Brush all surfaces of teeth
- Don't forget your tongue!
- Replace toothbrush every 3 months

### 2. Washing Your Hands
**When to wash:**
- Before eating
- After using the bathroom
- After playing outside
- After coughing or sneezing
- After touching animals

**How to wash:**
- Use soap and warm water
- Scrub for 20 seconds (sing "Happy Birthday" twice)
- Clean under fingernails
- Dry with clean towel

### 3. Bathing/Showering
**How often:** Daily or every other day
**Steps:**
- Use soap or body wash
- Wash hair with shampoo
- Clean all parts of your body
- Rinse thoroughly
- Dry with clean towel

### 4. Hair Care
- Wash hair regularly
- Brush or comb daily
- Keep hair neat and tidy
- Trim regularly to keep healthy

## Healthy Eating
### Balanced Diet Includes:
**Fruits and Vegetables:** 5 servings per day
- Apples, bananas, carrots, broccoli
- Provide vitamins and minerals

**Whole Grains:** 
- Brown rice, whole wheat bread, oatmeal
- Give you energy

**Protein:**
- Meat, fish, eggs, beans, nuts
- Help build strong muscles

**Dairy:**
- Milk, cheese, yogurt
- Build strong bones and teeth

**Water:** 6-8 glasses per day
- Keeps your body hydrated

### Foods to Limit:
- Sugary drinks and candy
- Fast food and fried foods
- Too much salt

## Exercise and Physical Activity
### Benefits of Exercise:
- Strengthens muscles and bones
- Improves heart health
- Helps you sleep better
- Reduces stress
- Helps maintain healthy weight

### Types of Exercise:
**Aerobic (Cardio):**
- Running, swimming, dancing, cycling
- Makes your heart stronger

**Strength Training:**
- Push-ups, climbing, carrying things
- Makes muscles stronger

**Flexibility:**
- Stretching, yoga
- Helps you move better

### How Much Exercise:
- At least 60 minutes of activity every day
- Can be broken into smaller chunks
- Include activities you enjoy

## Sleep and Rest
### Why Sleep is Important:
- Helps your body grow and repair
- Improves memory and learning
- Boosts immune system
- Helps control emotions

### Good Sleep Habits:
- Go to bed at the same time each night
- Get 9-11 hours of sleep
- Keep bedroom cool, dark, and quiet
- Avoid screens 1 hour before bed
- Have a bedtime routine

## Mental Health
### Taking Care of Your Mind:
- Talk about your feelings
- Practice deep breathing when stressed
- Do activities you enjoy
- Spend time with friends and family
- Ask for help when needed

### Managing Emotions:
- It's normal to feel different emotions
- Count to 10 when angry
- Take deep breaths when worried
- Talk to trusted adults about problems
'''
        },
        
        'Safety and First Aid': {
            'title': 'Staying Safe and Helping Others',
            'content': '''
# Safety and First Aid

## Home Safety

### Kitchen Safety
**Do:**
- Wash hands before cooking
- Clean up spills immediately
- Turn pot handles toward the stove
- Use oven mitts for hot items

**Don't:**
- Leave cooking food unattended
- Put metal in microwave
- Touch hot surfaces
- Run with sharp objects

### Fire Safety
**Prevention:**
- Don't play with matches or lighters
- Keep flammable items away from heat
- Check smoke detector batteries

**If there's a fire:**
- Get out immediately
- Stay low (smoke rises)
- Feel doors before opening
- Meet at family meeting place
- Call 911 from safe location

### Electrical Safety
- Don't touch electrical outlets with wet hands
- Unplug appliances when not in use
- Don't overload outlets
- Tell adults about damaged cords

## School Safety

### Playground Safety
- Use equipment properly
- Take turns and share
- Tell teacher about broken equipment
- Be kind to others

### Classroom Safety
- Walk, don't run in hallways
- Keep backpack and supplies organized
- Follow teacher's instructions
- Report bullying to adults

## Internet Safety

### Online Rules:
- Never share personal information (address, phone, school)
- Don't meet online friends in person
- Tell adults about inappropriate content
- Use strong passwords
- Be kind online (no cyberbullying)

### Social Media Safety:
- Only accept friend requests from people you know
- Think before you post
- Don't share photos without permission
- Report inappropriate behavior

## Basic First Aid

### For Small Cuts:
1. Wash hands first
2. Clean the cut with water
3. Apply pressure to stop bleeding
4. Cover with clean bandage
5. Tell an adult

### For Burns:
1. Run cool water over burn for 10 minutes
2. Don't use ice
3. Cover with clean cloth
4. Get adult help for serious burns

### For Nosebleeds:
1. Sit up straight
2. Lean slightly forward
3. Pinch soft part of nose
4. Hold for 10 minutes
5. Breathe through mouth

### When to Get Adult Help:
- Any serious injury
- If someone is unconscious
- Severe bleeding
- Difficulty breathing
- Poisoning

## Emergency Numbers
**Important numbers to know:**
- Emergency: 911 (or local emergency number)
- Parents' phone numbers
- Trusted neighbor or relative
- Poison Control Center

## Stranger Safety

### Safe Adults:
- Parents and family members
- Teachers and school staff
- Police officers in uniform
- Store employees (when with parents)

### Stranger Safety Rules:
- Never go anywhere with a stranger
- Don't accept gifts from strangers
- Stay with your group
- If lost, find a safe adult (police, store employee)
- Trust your feelings - if something feels wrong, get help

### What to do if approached by stranger:
1. Say "NO" loudly
2. Run to safety
3. Tell a trusted adult immediately
4. Remember: it's not your fault
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
        'Personal Health and Hygiene': [
            {
                'question_text': 'How long should you brush your teeth?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '30 seconds', 'is_correct': False},
                    {'text': '1 minute', 'is_correct': False},
                    {'text': '2 minutes', 'is_correct': True},
                    {'text': '5 minutes', 'is_correct': False}
                ],
                'explanation': 'You should brush your teeth for 2 minutes to properly clean all surfaces and remove plaque and bacteria.'
            },
            {
                'question_text': 'How many hours of sleep should a 10-year-old get each night?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '6-7 hours', 'is_correct': False},
                    {'text': '7-8 hours', 'is_correct': False},
                    {'text': '9-11 hours', 'is_correct': True},
                    {'text': '12-14 hours', 'is_correct': False}
                ],
                'explanation': 'Children aged 6-13 need 9-11 hours of sleep each night for proper growth, learning, and health.'
            }
        ],
        
        'Safety and First Aid': [
            {
                'question_text': 'What should you do FIRST if you get a small cut?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Put on a bandage', 'is_correct': False},
                    {'text': 'Wash your hands', 'is_correct': True},
                    {'text': 'Apply pressure', 'is_correct': False},
                    {'text': 'Call 911', 'is_correct': False}
                ],
                'explanation': 'Always wash your hands first before treating any wound to prevent infection.'
            },
            {
                'question_text': 'What is the emergency phone number in most countries?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '411', 'is_correct': False},
                    {'text': '911', 'is_correct': True},
                    {'text': '311', 'is_correct': False},
                    {'text': '511', 'is_correct': False}
                ],
                'explanation': '911 is the emergency number in the United States and Canada. Other countries may have different emergency numbers like 112 or 999.'
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
    create_life_skills_content()
    print("✅ Grade 5 Life Skills content creation completed!")
