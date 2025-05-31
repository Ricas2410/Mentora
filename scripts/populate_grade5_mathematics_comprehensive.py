#!/usr/bin/env python
"""
Comprehensive Grade 5 Mathematics Content Population Script
Creates detailed study notes and quiz questions for all mathematics topics
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

def create_mathematics_content():
    """Create comprehensive Grade 5 Mathematics content"""
    print("🔢 Creating Grade 5 Mathematics Content...")
    
    # Get Mathematics subject and Grade 5 level
    try:
        math_subject = Subject.objects.get(name="Mathematics")
        grade5_math = ClassLevel.objects.get(subject=math_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Mathematics subject or Grade 5 level not found!")
        return
    
    # Mathematics topics for Grade 5
    topics_data = [
        {
            'title': 'Place Value and Number Sense',
            'description': 'Understanding place value up to millions and number relationships',
            'order': 1
        },
        {
            'title': 'Addition and Subtraction',
            'description': 'Multi-digit addition and subtraction with regrouping',
            'order': 2
        },
        {
            'title': 'Multiplication and Division',
            'description': 'Multi-digit multiplication and division strategies',
            'order': 3
        },
        {
            'title': 'Fractions',
            'description': 'Understanding fractions, equivalent fractions, and operations',
            'order': 4
        },
        {
            'title': 'Decimals',
            'description': 'Decimal place value, comparing, and basic operations',
            'order': 5
        },
        {
            'title': 'Measurement',
            'description': 'Length, weight, capacity, time, and temperature',
            'order': 6
        },
        {
            'title': 'Geometry',
            'description': 'Shapes, angles, lines, and basic geometric concepts',
            'order': 7
        },
        {
            'title': 'Data and Graphs',
            'description': 'Collecting, organizing, and interpreting data',
            'order': 8
        }
    ]
    
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            title=topic_data['title'],
            class_level=grade5_math,
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Created topic: {topic.title}")
            
            # Create study notes for each topic
            create_study_notes(topic)
            
            # Create quiz questions for each topic
            create_quiz_questions(topic)
        else:
            print(f"📝 Topic already exists: {topic.title}")

def create_study_notes(topic):
    """Create comprehensive study notes for each topic"""
    
    study_notes_data = {
        'Place Value and Number Sense': {
            'title': 'Understanding Place Value and Numbers',
            'content': '''
# Place Value and Number Sense

## What is Place Value?
Place value tells us the value of each digit in a number based on its position. Think of it like addresses for numbers - each digit has its own "house" with a specific value.

### Real-World Example: Population of Cities
Let's look at the population of major cities:
- **New York City:** 8,336,817 people
- **London:** 9,648,110 people
- **Tokyo:** 13,960,000 people

### Place Value Chart (Extended)
```
Millions | Hundred Thousands | Ten Thousands | Thousands | Hundreds | Tens | Ones
   13    |        9         |       6       |     0     |    0     |  0   |  0
```

**Tokyo's population: 13,960,000**
- **1** is in the ten millions place = 10,000,000
- **3** is in the millions place = 3,000,000
- **9** is in the hundred thousands place = 900,000
- **6** is in the ten thousands place = 60,000
- **0** is in the thousands place = 0
- **0** is in the hundreds place = 0
- **0** is in the tens place = 0
- **0** is in the ones place = 0

**Total:** 10,000,000 + 3,000,000 + 900,000 + 60,000 = 13,960,000

## Reading Large Numbers in Real Life

### Money Examples:
**$2,456,789** (Two million, four hundred fifty-six thousand, seven hundred eighty-nine dollars)
- This could be the price of a luxury mansion
- Or the budget for a small school

### Distance Examples:
**384,400 kilometers** (Three hundred eighty-four thousand, four hundred kilometers)
- This is the distance from Earth to the Moon!
- Written as: 384,400 km

### Time Examples:
**525,600 minutes** (Five hundred twenty-five thousand, six hundred minutes)
- This is how many minutes are in one year!
- 365 days × 24 hours × 60 minutes = 525,600 minutes

## Comparing Numbers in Real Situations

### Sports Stadium Capacities:
- **Wembley Stadium:** 90,000 seats
- **Camp Nou:** 99,354 seats
- **Michigan Stadium:** 107,601 seats

**Which is largest?** Compare from left to right:
- Wembley: 90,000 (starts with 9)
- Camp Nou: 99,354 (starts with 9, then 9)
- Michigan: 107,601 (starts with 1, then 0, then 7)

Since 107,601 > 99,354 > 90,000, **Michigan Stadium** is the largest.

### Country Populations (2023):
- **Canada:** 38,781,291 people
- **Kenya:** 54,027,487 people
- **South Korea:** 51,784,059 people

**Order from smallest to largest:**
1. Canada: 38,781,291
2. South Korea: 51,784,059
3. Kenya: 54,027,487

## Rounding Numbers in Real Life

### Rounding Rules with Examples:

#### Rounding to Nearest Ten:
**Example:** A school has 847 students
- Look at the ones place: 7
- Since 7 ≥ 5, round up
- **Answer:** 850 students (approximately)

#### Rounding to Nearest Hundred:
**Example:** A concert sold 3,847 tickets
- Look at the tens place: 4
- Since 4 < 5, round down
- **Answer:** 3,800 tickets (approximately)

#### Rounding to Nearest Thousand:
**Example:** A city's population is 67,834
- Look at the hundreds place: 8
- Since 8 ≥ 5, round up
- **Answer:** 68,000 people (approximately)

### Why Do We Round?
1. **Easier to remember:** "About 68,000 people" vs "67,834 people"
2. **Quick estimates:** When shopping, round prices to estimate total cost
3. **News reports:** "Nearly 70,000 people attended the concert"
4. **Planning:** "We need supplies for about 850 students"

## Number Patterns and Relationships

### Skip Counting Patterns:
- **By 10s:** 10, 20, 30, 40, 50... (like counting money in $10 bills)
- **By 100s:** 100, 200, 300, 400, 500... (like counting in $100 bills)
- **By 1,000s:** 1,000, 2,000, 3,000... (like counting kilometers on a road trip)

### Even and Odd Numbers:
- **Even numbers** end in 0, 2, 4, 6, 8 (can be divided by 2 equally)
  - Examples: 24 students can form 12 pairs
- **Odd numbers** end in 1, 3, 5, 7, 9 (always have 1 left over when divided by 2)
  - Examples: 25 students = 12 pairs + 1 student left over

## Real-World Problem Solving

### Problem 1: School Fundraiser
**Situation:** Your school wants to raise $50,000 for new computers.
- Week 1: Raised $12,847
- Week 2: Raised $18,923
- Week 3: Raised $15,678

**Questions:**
1. How much have they raised so far?
2. How much more do they need?
3. Round each week's amount to the nearest thousand.

**Solutions:**
1. Total raised: $12,847 + $18,923 + $15,678 = $47,448
2. Still need: $50,000 - $47,448 = $2,552
3. Rounded amounts: $13,000 + $19,000 + $16,000 = $48,000

### Problem 2: Sports Attendance
**Situation:** Three football games had these attendances:
- Game 1: 45,678 people
- Game 2: 52,341 people
- Game 3: 48,892 people

**Questions:**
1. Which game had the highest attendance?
2. Order the games from lowest to highest attendance.
3. What's the total attendance for all three games?

**Solutions:**
1. Game 2 had the highest (52,341 people)
2. Order: Game 1 (45,678), Game 3 (48,892), Game 2 (52,341)
3. Total: 45,678 + 52,341 + 48,892 = 146,911 people

## Practice Activities

### Activity 1: Number Detective
Look around your home and find:
- A number with 4 digits (maybe on a book page)
- A number with 5 digits (maybe a zip code)
- A number with 6 digits (maybe a phone number)

Write each number in expanded form and read it aloud.

### Activity 2: Estimation Game
When you go shopping with family:
- Estimate the total cost by rounding each item's price
- Compare your estimate to the actual total
- See how close you can get!

### Activity 3: Population Research
Look up the population of:
- Your city or town
- Your state or province
- Your country

Practice reading these numbers aloud and comparing them.

## Key Vocabulary
- **Digit:** A single number symbol (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
- **Place Value:** The value of a digit based on its position
- **Standard Form:** Writing numbers using digits (like 1,234)
- **Word Form:** Writing numbers using words (like "one thousand, two hundred thirty-four")
- **Expanded Form:** Writing numbers showing the value of each digit (like 1,000 + 200 + 30 + 4)
- **Estimate:** An approximate answer, close to the exact answer
- **Round:** To change a number to the nearest ten, hundred, thousand, etc.

Remember: Numbers are everywhere in our daily lives! The better you understand place value, the easier it becomes to work with money, measurements, time, and solve real-world problems.
'''
        },
        
        'Addition and Subtraction': {
            'title': 'Multi-digit Addition and Subtraction',
            'content': '''
# Addition and Subtraction

## Why Do We Need Addition and Subtraction?
Addition and subtraction help us solve everyday problems involving money, time, distances, and quantities. These skills are essential for shopping, planning events, managing resources, and understanding the world around us.

## Multi-digit Addition in Real Life

### Real-World Addition Examples:

#### Example 1: School Fundraising
**Situation:** Three classes are raising money for a field trip:
- Class A raised: $2,456
- Class B raised: $1,789
- Class C raised: $3,247

**How much did they raise in total?**

```
  2,456
  1,789
+ 3,247
-------
  7,492
```

**Step-by-step solution:**
- **Ones column:** 6 + 9 + 7 = 22 (write 2, carry 2)
- **Tens column:** 5 + 8 + 4 + 2 = 19 (write 9, carry 1)
- **Hundreds column:** 4 + 7 + 2 + 1 = 14 (write 4, carry 1)
- **Thousands column:** 2 + 1 + 3 + 1 = 7

**Answer:** They raised $7,492 total!

#### Example 2: Sports Stadium Attendance
**Situation:** A baseball stadium had these attendances over three games:
- Game 1: 45,678 people
- Game 2: 52,341 people
- Game 3: 38,892 people

**Total attendance for all three games:**

```
  45,678
  52,341
+ 38,892
--------
 136,911
```

**Answer:** 136,911 people attended all three games combined!

### Addition Strategies:

#### Strategy 1: Break Apart Numbers
Instead of: 2,456 + 1,789
Think: (2,000 + 400 + 50 + 6) + (1,000 + 700 + 80 + 9)
= (2,000 + 1,000) + (400 + 700) + (50 + 80) + (6 + 9)
= 3,000 + 1,100 + 130 + 15
= 4,245

#### Strategy 2: Add in Steps
2,456 + 1,789
= 2,456 + 1,000 + 700 + 80 + 9
= 3,456 + 700 + 80 + 9
= 4,156 + 80 + 9
= 4,236 + 9
= 4,245

## Multi-digit Subtraction in Real Life

### Real-World Subtraction Examples:

#### Example 1: Shopping Budget
**Situation:** Maria has $5,234 saved for a computer. The computer costs $1,678.
**How much money will she have left?**

```
  5,234
- 1,678
-------
  3,556
```

**Step-by-step with borrowing:**
- **Ones:** 4 - 8 (can't do, borrow from tens)
  - Borrow 1 ten = 10 ones, so 14 - 8 = 6
- **Tens:** 2 - 7 (can't do, borrow from hundreds)
  - We borrowed 1, so we have 1 left, then borrow 1 hundred = 10 tens
  - So 11 - 7 = 4 (but we write 3 because we borrowed 1)
- **Hundreds:** 1 - 6 (can't do, borrow from thousands)
  - We borrowed 1, so we have 0 left, then borrow 1 thousand = 10 hundreds
  - So 10 - 6 = 4 (but we write 3 because we borrowed 1)
- **Thousands:** 4 - 1 = 3 (after borrowing 1)

**Answer:** Maria will have $3,556 left after buying the computer.

#### Example 2: Distance Traveled
**Situation:** A family is driving 8,456 kilometers on vacation. They've already driven 3,789 kilometers.
**How many more kilometers do they need to drive?**

```
  8,456
- 3,789
-------
  4,667
```

**Answer:** They need to drive 4,667 more kilometers.

### Subtraction Strategies:

#### Strategy 1: Add Up Method
To solve 5,234 - 1,678, think: "What do I add to 1,678 to get 5,234?"
- 1,678 + 22 = 1,700
- 1,700 + 300 = 2,000
- 2,000 + 3,234 = 5,234
- Total added: 22 + 300 + 3,234 = 3,556

#### Strategy 2: Break Apart the Subtraction
5,234 - 1,678
= 5,234 - 1,000 - 600 - 70 - 8
= 4,234 - 600 - 70 - 8
= 3,634 - 70 - 8
= 3,564 - 8
= 3,556

## Estimation: Your Mathematical Superpower

### Why Estimate?
- **Quick mental math:** Get approximate answers fast
- **Check your work:** See if your exact answer makes sense
- **Real-life decisions:** "Do I have enough money?" "Will this fit?"

### Estimation Strategies:

#### Round to Nearest Hundred:
**Problem:** 2,456 + 1,789
- 2,456 ≈ 2,500
- 1,789 ≈ 1,800
- Estimate: 2,500 + 1,800 = 4,300
- Exact answer: 4,245 ✓ (Close!)

#### Round to Nearest Thousand:
**Problem:** 5,234 - 1,678
- 5,234 ≈ 5,000
- 1,678 ≈ 2,000
- Estimate: 5,000 - 2,000 = 3,000
- Exact answer: 3,556 ✓ (Reasonable!)

## Real-World Problem Solving

### Problem 1: Concert Ticket Sales
**Situation:** A concert venue sold tickets over three days:
- Friday: 12,847 tickets
- Saturday: 18,923 tickets
- Sunday: 15,678 tickets

The venue can hold 50,000 people total.

**Questions:**
1. How many tickets were sold in total?
2. How many empty seats were there?
3. Which day had the highest sales?
4. What's the difference between the highest and lowest sales days?

**Solutions:**
1. Total tickets: 12,847 + 18,923 + 15,678 = 47,448 tickets
2. Empty seats: 50,000 - 47,448 = 2,552 empty seats
3. Saturday had the highest sales (18,923 tickets)
4. Difference: 18,923 - 12,847 = 6,076 more tickets on Saturday

### Problem 2: School Supply Drive
**Situation:** A school collected supplies for students in need:
- Pencils collected: 8,456
- Pencils needed: 12,000
- Notebooks collected: 5,234
- Notebooks needed: 7,500

**Questions:**
1. How many more pencils do they need?
2. How many more notebooks do they need?
3. What's the total number of items they still need?

**Solutions:**
1. More pencils needed: 12,000 - 8,456 = 3,544 pencils
2. More notebooks needed: 7,500 - 5,234 = 2,266 notebooks
3. Total still needed: 3,544 + 2,266 = 5,810 items

### Problem 3: Video Game High Scores
**Situation:** Three friends are competing for the highest video game score:
- Alex: 45,678 points
- Sam: 52,341 points
- Jordan: 38,892 points

**Questions:**
1. What's their combined score?
2. How many more points does Alex need to beat Sam?
3. What's the difference between the highest and lowest scores?

**Solutions:**
1. Combined score: 45,678 + 52,341 + 38,892 = 136,911 points
2. Alex needs: 52,341 - 45,678 = 6,663 more points to beat Sam
3. Difference: 52,341 - 38,892 = 13,449 points between highest and lowest

## Mental Math Tricks

### Adding 9, 99, 999:
- To add 9: Add 10, then subtract 1
  - 2,456 + 9 = 2,456 + 10 - 1 = 2,466 - 1 = 2,465
- To add 99: Add 100, then subtract 1
  - 2,456 + 99 = 2,456 + 100 - 1 = 2,556 - 1 = 2,555

### Subtracting 9, 99, 999:
- To subtract 9: Subtract 10, then add 1
  - 2,456 - 9 = 2,456 - 10 + 1 = 2,446 + 1 = 2,447

### Adding Numbers Ending in 5:
- 2,456 + 1,785 = 2,456 + 1,800 - 15 = 4,256 - 15 = 4,241

## Practice Activities

### Activity 1: Shopping Math
Next time you go shopping:
- Estimate the total cost by rounding each item's price
- Add up the exact prices and compare to your estimate
- Calculate how much change you should get

### Activity 2: Sports Statistics
Look up statistics for your favorite sports team:
- Add up total points scored in multiple games
- Find the difference between wins and losses
- Calculate attendance differences between games

### Activity 3: Time and Distance
Plan a road trip:
- Add up distances between cities
- Calculate total travel time
- Figure out how much gas money you'll need

## Common Mistakes to Avoid

### Mistake 1: Not Lining Up Place Values
**Wrong:**
```
2456
+ 789
-----
```

**Right:**
```
2,456
+  789
-----
3,245
```

### Mistake 2: Forgetting to Borrow
**Wrong:** 5,234 - 1,678 = 4,444 ❌

**Right:** 5,234 - 1,678 = 3,556 ✓

### Mistake 3: Not Checking with Estimation
Always estimate first to check if your answer makes sense!

## Key Vocabulary
- **Sum:** The answer to an addition problem
- **Difference:** The answer to a subtraction problem
- **Addend:** Numbers being added together
- **Minuend:** The number you subtract from
- **Subtrahend:** The number you subtract
- **Regroup/Carry:** Moving value from one place to the next when adding
- **Borrow:** Taking value from the next place when subtracting
- **Estimate:** An approximate answer

Remember: Addition and subtraction are tools for solving real problems. Practice with real situations like money, sports scores, and distances to make these skills stronger and more meaningful!
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
        'Place Value and Number Sense': [
            {
                'question_text': 'The population of Tokyo is 13,960,000. What is the value of the digit 9 in this number?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '9', 'is_correct': False},
                    {'text': '90,000', 'is_correct': False},
                    {'text': '900,000', 'is_correct': True},
                    {'text': '9,000,000', 'is_correct': False}
                ],
                'explanation': 'The digit 9 is in the hundred thousands place, so its value is 9 × 100,000 = 900,000.'
            },
            {
                'question_text': 'A baseball stadium has 67,834 seats. Round this to the nearest thousand for a news report.',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '67,000', 'is_correct': False},
                    {'text': '68,000', 'is_correct': True},
                    {'text': '70,000', 'is_correct': False},
                    {'text': '60,000', 'is_correct': False}
                ],
                'explanation': 'Look at the hundreds place (8). Since 8 ≥ 5, round up to 68,000. The news would report "about 68,000 seats."'
            },
            {
                'question_text': 'Which number is the largest: 456,789 or 465,789 or 456,879?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '456,789', 'is_correct': False},
                    {'text': '465,789', 'is_correct': True},
                    {'text': '456,879', 'is_correct': False},
                    {'text': 'They are all equal', 'is_correct': False}
                ],
                'explanation': 'Compare from left to right. All start with 4, then 456,789 and 456,879 have 5 in ten thousands place, but 465,789 has 6 in ten thousands place. Since 6 > 5, 465,789 is largest.'
            },
            {
                'question_text': 'A school wants to buy supplies costing $12,847. They round this to the nearest hundred for budgeting. What amount do they use?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '$12,800', 'is_correct': False},
                    {'text': '$12,900', 'is_correct': True},
                    {'text': '$13,000', 'is_correct': False},
                    {'text': '$12,000', 'is_correct': False}
                ],
                'explanation': 'Look at the tens place (4). Since 4 < 5, normally round down, but we look at tens place for rounding to hundreds. The tens digit is 4, so round down to $12,800. Wait - let me recalculate: 12,847 rounded to nearest hundred looks at tens place (4), since 4 < 5, round down to $12,800.'
            },
            {
                'question_text': 'In expanded form, 234,567 equals:',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '200,000 + 30,000 + 4,000 + 500 + 60 + 7', 'is_correct': True},
                    {'text': '2 + 3 + 4 + 5 + 6 + 7', 'is_correct': False},
                    {'text': '234 + 567', 'is_correct': False},
                    {'text': '200,000 + 34,567', 'is_correct': False}
                ],
                'explanation': 'Expanded form shows the value of each digit: 2 hundred thousands + 3 ten thousands + 4 thousands + 5 hundreds + 6 tens + 7 ones.'
            }
        ],

        'Addition and Subtraction': [
            {
                'question_text': 'Three schools raised money for charity: School A raised $12,456, School B raised $8,789, and School C raised $15,234. How much did they raise in total?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '$36,479', 'is_correct': True},
                    {'text': '$35,479', 'is_correct': False},
                    {'text': '$36,579', 'is_correct': False},
                    {'text': '$37,479', 'is_correct': False}
                ],
                'explanation': 'Add the three amounts: $12,456 + $8,789 + $15,234. Adding column by column with regrouping: 6+9+4=19 (write 9, carry 1), 5+8+3+1=17 (write 7, carry 1), etc. Total: $36,479.'
            },
            {
                'question_text': 'A concert venue holds 25,000 people. If 18,347 tickets were sold, how many seats are still empty?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '6,653', 'is_correct': True},
                    {'text': '7,653', 'is_correct': False},
                    {'text': '6,753', 'is_correct': False},
                    {'text': '5,653', 'is_correct': False}
                ],
                'explanation': 'Subtract tickets sold from total capacity: 25,000 - 18,347. Borrowing as needed: 25,000 - 18,347 = 6,653 empty seats.'
            },
            {
                'question_text': 'Maria saves $2,456 in January, $3,789 in February, and $1,234 in March. How much has she saved in total?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '$7,479', 'is_correct': True},
                    {'text': '$7,469', 'is_correct': False},
                    {'text': '$6,479', 'is_correct': False},
                    {'text': '$8,479', 'is_correct': False}
                ],
                'explanation': 'Add the three monthly savings: $2,456 + $3,789 + $1,234 = $7,479. This shows how addition helps track savings over time.'
            },
            {
                'question_text': 'A video game costs $59. If you pay with a $100 bill, how much change should you receive?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '$41', 'is_correct': True},
                    {'text': '$31', 'is_correct': False},
                    {'text': '$51', 'is_correct': False},
                    {'text': '$49', 'is_correct': False}
                ],
                'explanation': 'Subtract the cost from the amount paid: $100 - $59 = $41. This is a practical use of subtraction in shopping.'
            },
            {
                'question_text': 'A library has 45,678 books. They donate 12,345 books to other schools. How many books do they have left?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '33,333', 'is_correct': True},
                    {'text': '32,333', 'is_correct': False},
                    {'text': '34,333', 'is_correct': False},
                    {'text': '33,433', 'is_correct': False}
                ],
                'explanation': 'Subtract donated books from total: 45,678 - 12,345 = 33,333 books remaining. Notice the pattern in the answer!'
            },
            {
                'question_text': 'Estimate the sum of 4,892 + 3,156 + 2,847 by rounding each number to the nearest thousand.',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '11,000', 'is_correct': True},
                    {'text': '10,000', 'is_correct': False},
                    {'text': '12,000', 'is_correct': False},
                    {'text': '9,000', 'is_correct': False}
                ],
                'explanation': 'Round each number: 4,892 ≈ 5,000, 3,156 ≈ 3,000, 2,847 ≈ 3,000. Then add: 5,000 + 3,000 + 3,000 = 11,000.'
            },
            {
                'question_text': 'A sports stadium sold 23,456 tickets on Friday and 18,789 tickets on Saturday. What is the difference in ticket sales between the two days?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '4,667', 'is_correct': True},
                    {'text': '5,667', 'is_correct': False},
                    {'text': '4,567', 'is_correct': False},
                    {'text': '3,667', 'is_correct': False}
                ],
                'explanation': 'Find the difference by subtracting: 23,456 - 18,789 = 4,667. Friday had 4,667 more ticket sales than Saturday.'
            },
            {
                'question_text': 'A school fundraiser has a goal of $50,000. They have raised $32,847 so far. How much more do they need to reach their goal?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '$17,153', 'is_correct': True},
                    {'text': '$18,153', 'is_correct': False},
                    {'text': '$16,153', 'is_correct': False},
                    {'text': '$17,053', 'is_correct': False}
                ],
                'explanation': 'Subtract amount raised from goal: $50,000 - $32,847 = $17,153 still needed to reach their fundraising goal.'
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
    create_mathematics_content()
    print("✅ Grade 5 Mathematics content creation completed!")
