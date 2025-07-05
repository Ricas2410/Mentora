from django.core.management.base import BaseCommand
from django.db import transaction
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice
import random


class Command(BaseCommand):
    help = 'Add sample study notes and questions to some topics'

    def handle(self, *args, **options):
        self.stdout.write('📝 Adding sample content to topics...')
        
        with transaction.atomic():
            # Add study notes to some Grade 1 topics
            self.add_grade1_content()
            
            # Add study notes to some Grade 2 topics
            self.add_grade2_content()
            
        self.stdout.write(
            self.style.SUCCESS('🎉 Successfully added sample content!')
        )

    def add_grade1_content(self):
        """Add content for Grade 1 topics"""
        self.stdout.write('📚 Adding Grade 1 content...')
        
        # English Grade 1 - Alphabet and Phonics
        try:
            topic = Topic.objects.get(
                title='Alphabet and Phonics',
                class_level__level_number=1,
                class_level__subject__name='English Language'
            )
            
            study_note, created = StudyNote.objects.get_or_create(
                topic=topic,
                title='Learning the Alphabet',
                defaults={
                    'content': '''
# Learning the Alphabet

## The English Alphabet
The English alphabet has 26 letters:
- **Capital letters**: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
- **Small letters**: a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z

## Letter Sounds
Each letter makes a sound:
- **A** says "ah" like in "apple"
- **B** says "buh" like in "ball"
- **C** says "kuh" like in "cat"

## Practice
Try to say each letter and its sound!
                    ''',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write('  ✅ Added study note: Learning the Alphabet')
                
        except Topic.DoesNotExist:
            self.stdout.write('  ❌ Topic not found: Alphabet and Phonics')

        # Mathematics Grade 1 - Numbers 1-20
        try:
            topic = Topic.objects.get(
                title='Numbers 1-20',
                class_level__level_number=1,
                class_level__subject__name='Mathematics'
            )
            
            study_note, created = StudyNote.objects.get_or_create(
                topic=topic,
                title='Counting Numbers 1-20',
                defaults={
                    'content': '''
# Counting Numbers 1-20

## Numbers in Order
Let's learn to count from 1 to 20:

1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20

## Number Words
- 1 = one
- 2 = two  
- 3 = three
- 4 = four
- 5 = five
- 10 = ten
- 20 = twenty

## Practice
Count objects around you:
- How many fingers do you have?
- How many toes do you have?
- Count the chairs in your room!
                    ''',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write('  ✅ Added study note: Counting Numbers 1-20')
                
        except Topic.DoesNotExist:
            self.stdout.write('  ❌ Topic not found: Numbers 1-20')

        # Science Grade 1 - Living and Non-living Things
        try:
            topic = Topic.objects.get(
                title='Living and Non-living Things',
                class_level__level_number=1,
                class_level__subject__name='Science'
            )
            
            study_note, created = StudyNote.objects.get_or_create(
                topic=topic,
                title='What is Living and Non-living?',
                defaults={
                    'content': '''
# Living and Non-living Things

## Living Things
Living things are things that are alive. They:
- **Grow** bigger over time
- **Move** by themselves
- **Eat** food or make their own food
- **Breathe** air or water
- Have **babies** (reproduce)

### Examples of Living Things:
- People (you and me!)
- Animals (dogs, cats, birds, fish)
- Plants (trees, flowers, grass)

## Non-living Things
Non-living things are not alive. They:
- Do **not** grow
- Do **not** move by themselves
- Do **not** eat
- Do **not** breathe
- Do **not** have babies

### Examples of Non-living Things:
- Rocks and stones
- Water
- Toys
- Books
- Cars

## Fun Activity
Look around your room. Can you find 3 living things and 3 non-living things?
                    ''',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write('  ✅ Added study note: What is Living and Non-living?')
                
        except Topic.DoesNotExist:
            self.stdout.write('  ❌ Topic not found: Living and Non-living Things')

    def add_grade2_content(self):
        """Add content for Grade 2 topics"""
        self.stdout.write('📚 Adding Grade 2 content...')
        
        # English Grade 2 - Reading Comprehension
        try:
            topic = Topic.objects.get(
                title='Reading Comprehension',
                class_level__level_number=2,
                class_level__subject__name='English Language'
            )
            
            study_note, created = StudyNote.objects.get_or_create(
                topic=topic,
                title='How to Understand What You Read',
                defaults={
                    'content': '''
# Reading Comprehension

## What is Reading Comprehension?
Reading comprehension means understanding what you read. It's not just saying the words - it's knowing what the story or text is about!

## Tips for Better Reading:
1. **Read slowly** - Don't rush!
2. **Think about the story** - What is happening?
3. **Ask questions** - Who? What? Where? When? Why?
4. **Picture it in your mind** - Imagine the story like a movie
5. **Read it again** if you don't understand

## Practice Story
**The Little Cat**

Mimi is a small black cat. She lives in a big house with her family. Every morning, Mimi likes to sit by the window and watch the birds. She dreams of playing with them in the garden.

### Questions:
- What is the cat's name?
- What color is the cat?
- Where does she like to sit?
- What does she watch?

## Remember
Good readers think about what they read!
                    ''',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write('  ✅ Added study note: How to Understand What You Read')
                
        except Topic.DoesNotExist:
            self.stdout.write('  ❌ Topic not found: Reading Comprehension')

        # Mathematics Grade 2 - Addition and Subtraction
        try:
            topic = Topic.objects.get(
                title='Addition and Subtraction',
                class_level__level_number=2,
                class_level__subject__name='Mathematics'
            )
            
            study_note, created = StudyNote.objects.get_or_create(
                topic=topic,
                title='Adding and Subtracting Numbers',
                defaults={
                    'content': '''
# Addition and Subtraction

## Addition (+)
Addition means putting numbers together to make a bigger number.
- We use the **+** sign for addition
- The answer is called the **sum**

### Examples:
- 5 + 3 = 8
- 12 + 6 = 18
- 25 + 14 = 39

## Subtraction (-)
Subtraction means taking away numbers to make a smaller number.
- We use the **-** sign for subtraction  
- The answer is called the **difference**

### Examples:
- 8 - 3 = 5
- 15 - 7 = 8
- 30 - 12 = 18

## Tips for Adding:
1. Start with the bigger number
2. Count up from there
3. Use your fingers if needed!

## Tips for Subtracting:
1. Start with the first number
2. Count backwards
3. Think: "What do I need to add to get the first number?"

## Practice
Try these problems:
- 14 + 5 = ?
- 20 - 8 = ?
- 16 + 13 = ?
                    ''',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write('  ✅ Added study note: Adding and Subtracting Numbers')
                
        except Topic.DoesNotExist:
            self.stdout.write('  ❌ Topic not found: Addition and Subtraction')

        # Social Studies Grade 2 - Our Neighborhood  
        try:
            topic = Topic.objects.get(
                title='Our Neighborhood',
                class_level__level_number=2,
                class_level__subject__name='Social Studies'
            )
            
            study_note, created = StudyNote.objects.get_or_create(
                topic=topic,
                title='Understanding Our Community',
                defaults={
                    'content': '''
# Our Neighborhood

## What is a Neighborhood?
A neighborhood is the area where you live. It includes your house and all the houses, buildings, and places around you.

## Places in Our Neighborhood:
- **Houses** - Where families live
- **Schools** - Where children learn
- **Shops** - Where we buy things we need
- **Hospital/Clinic** - Where we go when we are sick
- **Post Office** - Where we send and receive letters
- **Police Station** - Where police officers work to keep us safe
- **Fire Station** - Where firefighters work
- **Parks** - Where we play and have fun

## Community Helpers:
These are people who help make our neighborhood a good place to live:
- **Teachers** - Help us learn
- **Doctors** - Help us stay healthy
- **Police Officers** - Keep us safe
- **Firefighters** - Put out fires and help in emergencies
- **Shop Owners** - Sell us things we need
- **Postman** - Brings us letters and packages

## Being a Good Neighbor:
- Be kind to everyone
- Keep your area clean
- Help others when you can
- Follow the rules
- Say "hello" and "thank you"

## Activity
Draw a map of your neighborhood. Include your house and 3 other important places!
                    ''',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write('  ✅ Added study note: Understanding Our Community')
                
        except Topic.DoesNotExist:
            self.stdout.write('  ❌ Topic not found: Our Neighborhood')
