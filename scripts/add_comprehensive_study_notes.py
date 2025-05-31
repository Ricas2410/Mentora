#!/usr/bin/env python
"""
Add Comprehensive Study Notes for Grade 5 Topics
Expands existing study notes with much more detailed content and examples
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

def add_comprehensive_mathematics_notes():
    """Add comprehensive study notes for mathematics topics"""
    print("📚 Adding comprehensive Mathematics study notes...")
    
    try:
        math_subject = Subject.objects.get(name="Mathematics")
        grade5_math = ClassLevel.objects.get(subject=math_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Mathematics subject or Grade 5 level not found!")
        return
    
    comprehensive_notes = {
        'Multiplication and Division': {
            'title': 'Mastering Multiplication and Division',
            'content': '''
# Multiplication and Division

## Understanding Multiplication
Multiplication is repeated addition. When we multiply, we're adding the same number multiple times.

### Real-World Examples of Multiplication

#### Example 1: School Supplies
**Situation:** Your teacher needs to buy pencils for the class. There are 24 students, and each student needs 6 pencils.

**Question:** How many pencils does the teacher need to buy?

**Solution:** 24 students × 6 pencils each = 144 pencils total

**Why multiplication works:** Instead of adding 6 + 6 + 6... (24 times), we multiply!

#### Example 2: Sports Teams
**Situation:** A basketball league has 12 teams. Each team has 15 players.

**Question:** How many players are in the league?

**Solution:** 12 teams × 15 players each = 180 players total

### Multiplication Strategies

#### Strategy 1: Break Apart Numbers (Distributive Property)
**Problem:** 23 × 15

**Method:** Break apart one number
- 23 × 15 = 23 × (10 + 5)
- = (23 × 10) + (23 × 5)
- = 230 + 115
- = 345

#### Strategy 2: Use Known Facts
**Problem:** 25 × 16

**Method:** Use easier numbers
- 25 × 16 = 25 × 4 × 4
- = (25 × 4) × 4
- = 100 × 4
- = 400

#### Strategy 3: Standard Algorithm
**Problem:** 347 × 23

```
    347
  ×  23
  -----
  1041  (347 × 3)
+ 6940  (347 × 20)
  -----
  7981
```

**Step by step:**
1. 347 × 3 = 1,041
2. 347 × 20 = 6,940
3. Add: 1,041 + 6,940 = 7,981

## Understanding Division
Division is the opposite of multiplication. It's about sharing equally or finding how many groups you can make.

### Real-World Examples of Division

#### Example 1: Pizza Party
**Situation:** You have 144 slices of pizza to share equally among 24 students.

**Question:** How many slices does each student get?

**Solution:** 144 ÷ 24 = 6 slices per student

**Check:** 24 students × 6 slices each = 144 slices ✓

#### Example 2: Field Trip Transportation
**Situation:** 180 students need to go on a field trip. Each bus holds 45 students.

**Question:** How many buses are needed?

**Solution:** 180 ÷ 45 = 4 buses needed

### Division Strategies

#### Strategy 1: Use Multiplication Facts
**Problem:** 144 ÷ 12

**Think:** "What number times 12 equals 144?"
- 12 × ? = 144
- 12 × 12 = 144
- So 144 ÷ 12 = 12

#### Strategy 2: Break Apart Numbers
**Problem:** 168 ÷ 14

**Method:** Use easier divisions
- 168 ÷ 14 = (140 + 28) ÷ 14
- = (140 ÷ 14) + (28 ÷ 14)
- = 10 + 2
- = 12

#### Strategy 3: Long Division
**Problem:** 2,856 ÷ 24

```
    119
   ----
24)2856
   24
   ---
    45
    24
    ---
    216
    216
    ---
      0
```

**Steps:**
1. 24 goes into 28 once (1), remainder 4
2. Bring down 5: 24 goes into 45 once (1), remainder 21
3. Bring down 6: 24 goes into 216 nine times (9), remainder 0
4. Answer: 119

## Multiplication and Division Relationship

### Fact Families
Numbers that work together in multiplication and division:
- 6 × 8 = 48
- 8 × 6 = 48
- 48 ÷ 6 = 8
- 48 ÷ 8 = 6

### Checking Your Work
**Always check division with multiplication:**
- If 144 ÷ 12 = 12, then 12 × 12 should equal 144 ✓

## Word Problem Strategies

### Multiplication Keywords:
- "times" → 5 times as many
- "each" → 6 pencils each
- "per" → 25 miles per hour
- "total" → total cost
- "altogether" → altogether there are

### Division Keywords:
- "shared equally" → divided among
- "groups of" → how many groups
- "each" → how many in each group
- "average" → total divided by number of items

### Problem-Solving Steps:
1. **Read carefully** - What is the question asking?
2. **Identify the operation** - Multiplication or division?
3. **Find the numbers** - What numbers do I need?
4. **Solve** - Do the calculation
5. **Check** - Does the answer make sense?

## Real-World Applications

### Money Problems
**Example:** Movie tickets cost $12 each. How much do 15 tickets cost?
- 15 × $12 = $180 total cost

### Time Problems
**Example:** A factory produces 156 toys per hour. How many toys in 8 hours?
- 156 × 8 = 1,248 toys

### Measurement Problems
**Example:** A recipe serves 6 people and uses 3 cups of flour. How much flour for 24 people?
- 24 ÷ 6 = 4 (four times as many people)
- 3 × 4 = 12 cups of flour needed

## Mental Math Tricks

### Multiplying by 10, 100, 1000:
- 47 × 10 = 470 (add one zero)
- 47 × 100 = 4,700 (add two zeros)
- 47 × 1,000 = 47,000 (add three zeros)

### Multiplying by 5:
- 24 × 5 = 24 × 10 ÷ 2 = 240 ÷ 2 = 120

### Multiplying by 25:
- 16 × 25 = 16 × 100 ÷ 4 = 1,600 ÷ 4 = 400

### Dividing by 10, 100, 1000:
- 470 ÷ 10 = 47 (remove one zero)
- 4,700 ÷ 100 = 47 (remove two zeros)
- 47,000 ÷ 1,000 = 47 (remove three zeros)

## Common Mistakes to Avoid

### Multiplication Mistakes:
1. **Forgetting to carry:** 47 × 8 = 376 (not 316)
2. **Wrong place value:** 23 × 45 = 1,035 (not 1,035)
3. **Adding instead of multiplying:** 6 groups of 8 = 48 (not 14)

### Division Mistakes:
1. **Wrong remainder:** 25 ÷ 4 = 6 R1 (not 6 R5)
2. **Forgetting remainder:** 23 ÷ 5 = 4 R3 (not just 4)
3. **Wrong operation:** "Share 20 cookies among 4 friends" = 20 ÷ 4 = 5 each

## Practice Activities

### Activity 1: Restaurant Math
- Menu prices: Burger $8, Fries $3, Drink $2
- Calculate total cost for different numbers of meals
- If 6 friends each order a burger, how much total?

### Activity 2: Sports Statistics
- A basketball player scores 18 points per game
- How many points in 12 games?
- If a team scores 144 points in 8 games, what's the average per game?

### Activity 3: Shopping Scenarios
- T-shirts cost $15 each, how much for 7 shirts?
- You have $120, how many $15 shirts can you buy?

Remember: Multiplication and division are everywhere in daily life! The more you practice with real situations, the stronger these skills become.
'''
        },
        
        'Fractions': {
            'title': 'Understanding Fractions in Real Life',
            'content': '''
# Understanding Fractions

## What Are Fractions?
A fraction represents part of a whole. It shows how many equal parts we have out of the total number of parts.

### Fraction Parts:
- **Numerator** (top number): How many parts we have
- **Denominator** (bottom number): Total number of equal parts
- **Fraction bar**: Means "divided by"

**Example:** 3/4 means 3 parts out of 4 equal parts total

## Real-World Fraction Examples

### Example 1: Pizza Fractions
**Situation:** You order a pizza cut into 8 equal slices.
- You eat 3 slices → You ate 3/8 of the pizza
- 5 slices remain → 5/8 of the pizza is left
- Check: 3/8 + 5/8 = 8/8 = 1 whole pizza ✓

### Example 2: Time Fractions
**Situation:** There are 60 minutes in an hour.
- 15 minutes = 15/60 = 1/4 of an hour
- 30 minutes = 30/60 = 1/2 of an hour
- 45 minutes = 45/60 = 3/4 of an hour

### Example 3: Money Fractions
**Situation:** You have $1.00 (100 cents).
- 25 cents = 25/100 = 1/4 of a dollar
- 50 cents = 50/100 = 1/2 of a dollar
- 75 cents = 75/100 = 3/4 of a dollar

## Types of Fractions

### Proper Fractions
- Numerator is smaller than denominator
- Value is less than 1
- Examples: 1/2, 3/4, 5/8, 7/10

### Improper Fractions
- Numerator is larger than or equal to denominator
- Value is 1 or greater
- Examples: 5/4, 7/3, 9/9, 11/5

### Mixed Numbers
- Whole number plus a proper fraction
- Examples: 1 1/2, 2 3/4, 5 2/3

### Converting Between Forms:
**Improper to Mixed:** 11/4 = 2 3/4 (11 ÷ 4 = 2 remainder 3)
**Mixed to Improper:** 2 3/4 = 11/4 (2 × 4 + 3 = 11)

## Equivalent Fractions
Different fractions that represent the same amount.

### Finding Equivalent Fractions:
**Method 1: Multiply top and bottom by same number**
- 1/2 = 2/4 = 3/6 = 4/8 = 5/10

**Method 2: Divide top and bottom by same number**
- 6/8 = 3/4 (divide both by 2)
- 10/15 = 2/3 (divide both by 5)

### Real-Life Example:
**Cooking:** A recipe calls for 1/2 cup of milk, but you only have a 1/4 cup measure.
- 1/2 = 2/4
- So you need 2 scoops of the 1/4 cup measure!

## Comparing Fractions

### Same Denominator:
**Easy!** Compare numerators
- 3/8 vs 5/8 → 5/8 is larger (5 > 3)

### Different Denominators:
**Method 1: Find common denominator**
- Compare 2/3 and 3/4
- 2/3 = 8/12 and 3/4 = 9/12
- Since 9/12 > 8/12, then 3/4 > 2/3

**Method 2: Convert to decimals**
- 2/3 ≈ 0.67 and 3/4 = 0.75
- Since 0.75 > 0.67, then 3/4 > 2/3

### Real-Life Example:
**Sports:** Which is better, making 3/5 of your free throws or 7/10?
- 3/5 = 6/10 and 7/10 = 7/10
- 7/10 > 6/10, so 7/10 is better!

## Adding and Subtracting Fractions

### Same Denominator:
**Rule:** Add/subtract numerators, keep denominator same
- 2/7 + 3/7 = 5/7
- 6/8 - 2/8 = 4/8 = 1/2

### Different Denominators:
**Step 1:** Find common denominator
**Step 2:** Convert fractions
**Step 3:** Add/subtract numerators

**Example:** 1/3 + 1/4
- Common denominator: 12
- 1/3 = 4/12 and 1/4 = 3/12
- 4/12 + 3/12 = 7/12

### Real-Life Example:
**Baking:** A recipe needs 1/3 cup sugar and 1/4 cup brown sugar.
- Total sugar: 1/3 + 1/4 = 4/12 + 3/12 = 7/12 cup

## Multiplying Fractions

### Rule: Multiply numerators, multiply denominators
- 2/3 × 1/4 = 2/12 = 1/6

### With Whole Numbers:
- 3 × 2/5 = 6/5 = 1 1/5

### Real-Life Examples:

#### Example 1: Recipe Scaling
**Problem:** A recipe serves 4 people and uses 2/3 cup flour. How much flour for 2 people?
- 2 people is 1/2 of 4 people
- 2/3 × 1/2 = 2/6 = 1/3 cup flour

#### Example 2: Fabric Cutting
**Problem:** You need 3/4 yard of fabric, but you want to make 2/3 of the project.
- 3/4 × 2/3 = 6/12 = 1/2 yard needed

## Dividing Fractions

### Rule: Multiply by the reciprocal (flip the second fraction)
- 2/3 ÷ 1/4 = 2/3 × 4/1 = 8/3 = 2 2/3

### Real-Life Example:
**Sharing:** You have 3/4 of a pizza. If each person gets 1/8 of the whole pizza, how many people can you feed?
- 3/4 ÷ 1/8 = 3/4 × 8/1 = 24/4 = 6 people

## Fractions in Everyday Life

### Cooking and Baking:
- Measuring ingredients: 1/2 cup, 3/4 teaspoon
- Scaling recipes: doubling means multiplying by 2
- Portion control: 1/4 of the cake

### Sports and Games:
- Shooting percentage: made 7 out of 10 shots = 7/10
- Game completion: finished 3/4 of the levels
- Time remaining: 1/3 of the game left

### Money and Shopping:
- Sales: 1/4 off means 75% of original price
- Tips: 1/5 of the bill = 20% tip
- Savings: saved 2/5 of your allowance

### Time Management:
- 1/2 hour = 30 minutes
- 3/4 of the day = 18 hours
- 1/6 of a year = 2 months

## Problem-Solving Strategies

### Step 1: Understand the Problem
- What is the whole?
- What part are we talking about?
- What operation do we need?

### Step 2: Draw Pictures
- Use circles, rectangles, or number lines
- Shade the parts you're working with

### Step 3: Use Real Objects
- Cut up paper plates for pizza problems
- Use measuring cups for cooking problems
- Use clocks for time problems

### Step 4: Check Your Answer
- Does it make sense?
- Is it reasonable?
- Can you verify with a different method?

## Common Mistakes to Avoid

### Mistake 1: Adding denominators
**Wrong:** 1/3 + 1/4 = 2/7 ❌
**Right:** 1/3 + 1/4 = 4/12 + 3/12 = 7/12 ✓

### Mistake 2: Not simplifying
**Incomplete:** 6/8 (should be 3/4)
**Complete:** 6/8 = 3/4 ✓

### Mistake 3: Confusing operations
**Division:** How many 1/4s in 3/4? → 3/4 ÷ 1/4 = 3
**Multiplication:** What is 1/4 of 3/4? → 3/4 × 1/4 = 3/16

Remember: Fractions are everywhere! The more you notice them in daily life, the better you'll understand them. Practice with real situations like cooking, sports, and time to make fractions meaningful and memorable.
'''
        }
    }
    
    # Add comprehensive notes to existing topics
    for topic_title, note_data in comprehensive_notes.items():
        try:
            topic = Topic.objects.get(title=topic_title, class_level=grade5_math)
            
            # Check if comprehensive note already exists
            existing_note = StudyNote.objects.filter(
                topic=topic,
                title=note_data['title']
            ).first()
            
            if not existing_note:
                study_note = StudyNote.objects.create(
                    topic=topic,
                    title=note_data['title'],
                    content=note_data['content'],
                    order=2,  # Second note for the topic
                    is_active=True
                )
                print(f"  📚 Added comprehensive note for {topic_title}: {note_data['title']}")
            else:
                print(f"  📝 Comprehensive note already exists for {topic_title}")
                
        except Topic.DoesNotExist:
            print(f"⚠️  Topic '{topic_title}' not found, skipping...")

if __name__ == '__main__':
    add_comprehensive_mathematics_notes()
    print("✅ Comprehensive study notes added successfully!")
