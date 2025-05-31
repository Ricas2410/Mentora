#!/usr/bin/env python
"""
Extensive Additional Grade 5 Content
Adds 10-15 more quiz questions per topic and expanded study notes
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

def add_extensive_mathematics_questions():
    """Add 10-15 more questions per mathematics topic"""
    print("🔢 Adding extensive Mathematics questions...")
    
    try:
        math_subject = Subject.objects.get(name="Mathematics")
        grade5_math = ClassLevel.objects.get(subject=math_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Mathematics subject or Grade 5 level not found!")
        return
    
    extensive_questions = {
        'Place Value and Number Sense': [
            {
                'question_text': 'The distance from Earth to Mars is approximately 225,000,000 kilometers. What is the value of the digit 2 in the ten millions place?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '2,000,000', 'is_correct': False},
                    {'text': '20,000,000', 'is_correct': True},
                    {'text': '200,000,000', 'is_correct': False},
                    {'text': '2', 'is_correct': False}
                ],
                'explanation': 'In 225,000,000, the first 2 is in the hundred millions place (200,000,000) and the second 2 is in the ten millions place (20,000,000).'
            },
            {
                'question_text': 'A smartphone costs $1,247. Round this price to the nearest ten dollars for a budget estimate.',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '$1,240', 'is_correct': False},
                    {'text': '$1,250', 'is_correct': True},
                    {'text': '$1,200', 'is_correct': False},
                    {'text': '$1,300', 'is_correct': False}
                ],
                'explanation': 'Look at the ones place (7). Since 7 ≥ 5, round up. $1,247 rounds to $1,250.'
            },
            {
                'question_text': 'Which number comes next in this pattern: 125,000, 130,000, 135,000, ?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '140,000', 'is_correct': True},
                    {'text': '145,000', 'is_correct': False},
                    {'text': '136,000', 'is_correct': False},
                    {'text': '150,000', 'is_correct': False}
                ],
                'explanation': 'The pattern increases by 5,000 each time. 135,000 + 5,000 = 140,000.'
            },
            {
                'question_text': 'A library has 456,789 books. If they want to report this number in the newspaper rounded to the nearest ten thousand, what would they say?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '450,000 books', 'is_correct': False},
                    {'text': '460,000 books', 'is_correct': True},
                    {'text': '400,000 books', 'is_correct': False},
                    {'text': '500,000 books', 'is_correct': False}
                ],
                'explanation': 'Look at the thousands place (6). Since 6 ≥ 5, round up to 460,000.'
            },
            {
                'question_text': 'In the number 3,847,291, which digit is in the hundred thousands place?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '3', 'is_correct': False},
                    {'text': '8', 'is_correct': True},
                    {'text': '4', 'is_correct': False},
                    {'text': '7', 'is_correct': False}
                ],
                'explanation': 'Reading from right to left: 1(ones), 9(tens), 2(hundreds), 7(thousands), 4(ten thousands), 8(hundred thousands), 3(millions).'
            },
            {
                'question_text': 'Compare these populations: City A has 2,847,391 people, City B has 2,874,391 people. Which city has more people?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'City A', 'is_correct': False},
                    {'text': 'City B', 'is_correct': True},
                    {'text': 'They have the same population', 'is_correct': False},
                    {'text': 'Cannot determine', 'is_correct': False}
                ],
                'explanation': 'Compare digit by digit from left: both start with 2,8, but City A has 4 in ten thousands place while City B has 7. Since 7 > 4, City B is larger.'
            },
            {
                'question_text': 'A concert venue sold 67,834 tickets. The manager wants to estimate this to the nearest thousand for planning purposes. What estimate should they use?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '67,000', 'is_correct': False},
                    {'text': '68,000', 'is_correct': True},
                    {'text': '70,000', 'is_correct': False},
                    {'text': '60,000', 'is_correct': False}
                ],
                'explanation': 'Look at the hundreds place (8). Since 8 ≥ 5, round up from 67,000 to 68,000.'
            },
            {
                'question_text': 'Write 4,000,000 + 300,000 + 20,000 + 5,000 + 600 + 70 + 8 in standard form.',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '4,325,678', 'is_correct': True},
                    {'text': '4,320,678', 'is_correct': False},
                    {'text': '4,325,668', 'is_correct': False},
                    {'text': '4,235,678', 'is_correct': False}
                ],
                'explanation': 'Add all the place values: 4,000,000 + 300,000 + 20,000 + 5,000 + 600 + 70 + 8 = 4,325,678.'
            },
            {
                'question_text': 'A school district has 89,456 students. Round this to the nearest hundred for a report.',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '89,400', 'is_correct': False},
                    {'text': '89,500', 'is_correct': True},
                    {'text': '89,000', 'is_correct': False},
                    {'text': '90,000', 'is_correct': False}
                ],
                'explanation': 'Look at the tens place (5). Since 5 ≥ 5, round up from 89,400 to 89,500.'
            },
            {
                'question_text': 'Which of these numbers is closest to 500,000?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '487,234', 'is_correct': False},
                    {'text': '523,891', 'is_correct': False},
                    {'text': '498,765', 'is_correct': True},
                    {'text': '456,789', 'is_correct': False}
                ],
                'explanation': 'Calculate differences: 498,765 is only 1,235 away from 500,000, which is the smallest difference.'
            },
            {
                'question_text': 'A video game has 1,234,567 points as the high score. What is this number in word form?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'One million, two hundred thirty-four thousand, five hundred sixty-seven', 'is_correct': True},
                    {'text': 'One thousand, two hundred thirty-four, five hundred sixty-seven', 'is_correct': False},
                    {'text': 'Twelve million, thirty-four thousand, five hundred sixty-seven', 'is_correct': False},
                    {'text': 'One million, twenty-three thousand, four hundred fifty-six', 'is_correct': False}
                ],
                'explanation': 'Break it down: 1,000,000 (one million) + 234,000 (two hundred thirty-four thousand) + 567 (five hundred sixty-seven).'
            },
            {
                'question_text': 'A factory produces 125,000 toys per month. How many toys do they produce in 3 months?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '375,000', 'is_correct': True},
                    {'text': '350,000', 'is_correct': False},
                    {'text': '425,000', 'is_correct': False},
                    {'text': '300,000', 'is_correct': False}
                ],
                'explanation': 'Multiply: 125,000 × 3 = 375,000 toys in 3 months.'
            }
        ],
        
        'Addition and Subtraction': [
            {
                'question_text': 'A charity event raised money over four days: Monday $12,456, Tuesday $18,789, Wednesday $15,234, Thursday $21,567. What was the total amount raised?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '$68,046', 'is_correct': True},
                    {'text': '$67,046', 'is_correct': False},
                    {'text': '$69,046', 'is_correct': False},
                    {'text': '$68,146', 'is_correct': False}
                ],
                'explanation': 'Add all four amounts: $12,456 + $18,789 + $15,234 + $21,567 = $68,046.'
            },
            {
                'question_text': 'A bookstore had 45,678 books. They sold 18,945 books during a sale. How many books do they have left?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '26,733', 'is_correct': True},
                    {'text': '27,733', 'is_correct': False},
                    {'text': '26,633', 'is_correct': False},
                    {'text': '25,733', 'is_correct': False}
                ],
                'explanation': 'Subtract books sold from total: 45,678 - 18,945 = 26,733 books remaining.'
            },
            {
                'question_text': 'Three friends are saving for a trip: Alex saved $2,847, Sam saved $3,456, and Jordan saved $1,923. How much did they save together?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '$8,226', 'is_correct': True},
                    {'text': '$8,126', 'is_correct': False},
                    {'text': '$8,326', 'is_correct': False},
                    {'text': '$7,226', 'is_correct': False}
                ],
                'explanation': 'Add their savings: $2,847 + $3,456 + $1,923 = $8,226 total.'
            },
            {
                'question_text': 'A movie theater has 25,000 seats. If 18,347 tickets were sold for the evening show, how many seats are empty?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '6,653', 'is_correct': True},
                    {'text': '7,653', 'is_correct': False},
                    {'text': '6,753', 'is_correct': False},
                    {'text': '5,653', 'is_correct': False}
                ],
                'explanation': 'Subtract tickets sold from total seats: 25,000 - 18,347 = 6,653 empty seats.'
            },
            {
                'question_text': 'Estimate the sum of 4,892 + 7,156 + 3,847 by rounding each number to the nearest thousand.',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '16,000', 'is_correct': True},
                    {'text': '15,000', 'is_correct': False},
                    {'text': '17,000', 'is_correct': False},
                    {'text': '14,000', 'is_correct': False}
                ],
                'explanation': 'Round each: 4,892 ≈ 5,000, 7,156 ≈ 7,000, 3,847 ≈ 4,000. Sum: 5,000 + 7,000 + 4,000 = 16,000.'
            },
            {
                'question_text': 'A school needs $75,000 for new computers. They have raised $48,567 so far. How much more do they need?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '$26,433', 'is_correct': True},
                    {'text': '$27,433', 'is_correct': False},
                    {'text': '$25,433', 'is_correct': False},
                    {'text': '$26,533', 'is_correct': False}
                ],
                'explanation': 'Subtract amount raised from goal: $75,000 - $48,567 = $26,433 still needed.'
            },
            {
                'question_text': 'A delivery truck travels 1,456 km on Monday, 2,789 km on Tuesday, and 1,234 km on Wednesday. What is the total distance traveled?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '5,479 km', 'is_correct': True},
                    {'text': '5,379 km', 'is_correct': False},
                    {'text': '5,579 km', 'is_correct': False},
                    {'text': '4,479 km', 'is_correct': False}
                ],
                'explanation': 'Add the three distances: 1,456 + 2,789 + 1,234 = 5,479 km total.'
            },
            {
                'question_text': 'A warehouse had 67,890 items. They shipped out 29,456 items. How many items remain in the warehouse?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '38,434', 'is_correct': True},
                    {'text': '39,434', 'is_correct': False},
                    {'text': '37,434', 'is_correct': False},
                    {'text': '38,534', 'is_correct': False}
                ],
                'explanation': 'Subtract shipped items from total: 67,890 - 29,456 = 38,434 items remaining.'
            },
            {
                'question_text': 'Four schools collected cans for recycling: School A collected 12,345 cans, School B collected 15,678 cans, School C collected 9,876 cans, and School D collected 18,234 cans. What was the total collection?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '56,133 cans', 'is_correct': True},
                    {'text': '55,133 cans', 'is_correct': False},
                    {'text': '57,133 cans', 'is_correct': False},
                    {'text': '56,233 cans', 'is_correct': False}
                ],
                'explanation': 'Add all collections: 12,345 + 15,678 + 9,876 + 18,234 = 56,133 cans total.'
            },
            {
                'question_text': 'A concert venue sold 34,567 tickets in advance and 12,890 tickets at the door. If the venue holds 50,000 people, how many tickets were not sold?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '2,543', 'is_correct': True},
                    {'text': '3,543', 'is_correct': False},
                    {'text': '2,443', 'is_correct': False},
                    {'text': '1,543', 'is_correct': False}
                ],
                'explanation': 'First add tickets sold: 34,567 + 12,890 = 47,457. Then subtract from capacity: 50,000 - 47,457 = 2,543 unsold tickets.'
            }
        ],

        'Multiplication and Division': [
            {
                'question_text': 'A bakery makes 245 cupcakes per day. How many cupcakes do they make in 12 days?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '2,940', 'is_correct': True},
                    {'text': '2,840', 'is_correct': False},
                    {'text': '3,040', 'is_correct': False},
                    {'text': '2,950', 'is_correct': False}
                ],
                'explanation': 'Multiply: 245 × 12 = 2,940 cupcakes. This shows how multiplication helps calculate totals over time.'
            },
            {
                'question_text': 'A school has 1,248 students. If they are divided equally into 24 classes, how many students are in each class?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '52', 'is_correct': True},
                    {'text': '48', 'is_correct': False},
                    {'text': '56', 'is_correct': False},
                    {'text': '50', 'is_correct': False}
                ],
                'explanation': 'Divide: 1,248 ÷ 24 = 52 students per class. Division helps us share quantities equally.'
            },
            {
                'question_text': 'A factory produces 156 toys per hour. How many toys are produced in 8 hours?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '1,248', 'is_correct': True},
                    {'text': '1,148', 'is_correct': False},
                    {'text': '1,348', 'is_correct': False},
                    {'text': '1,228', 'is_correct': False}
                ],
                'explanation': 'Multiply: 156 × 8 = 1,248 toys in 8 hours.'
            },
            {
                'question_text': 'A pizza restaurant uses 2,856 pepperoni slices. If each pizza gets 24 slices, how many pizzas can they make?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '119', 'is_correct': True},
                    {'text': '118', 'is_correct': False},
                    {'text': '120', 'is_correct': False},
                    {'text': '121', 'is_correct': False}
                ],
                'explanation': 'Divide: 2,856 ÷ 24 = 119 pizzas can be made with the available pepperoni.'
            },
            {
                'question_text': 'A movie theater has 18 rows with 45 seats in each row. How many seats are there in total?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '810', 'is_correct': True},
                    {'text': '800', 'is_correct': False},
                    {'text': '820', 'is_correct': False},
                    {'text': '790', 'is_correct': False}
                ],
                'explanation': 'Multiply: 18 × 45 = 810 total seats in the theater.'
            },
            {
                'question_text': 'A library orders 3,456 new books. If they want to display them equally on 16 shelves, how many books go on each shelf?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '216', 'is_correct': True},
                    {'text': '206', 'is_correct': False},
                    {'text': '226', 'is_correct': False},
                    {'text': '215', 'is_correct': False}
                ],
                'explanation': 'Divide: 3,456 ÷ 16 = 216 books per shelf.'
            },
            {
                'question_text': 'A farmer harvests 347 apples from each of his 23 apple trees. How many apples did he harvest in total?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '7,981', 'is_correct': True},
                    {'text': '7,881', 'is_correct': False},
                    {'text': '8,081', 'is_correct': False},
                    {'text': '7,971', 'is_correct': False}
                ],
                'explanation': 'Multiply: 347 × 23 = 7,981 apples total from all trees.'
            },
            {
                'question_text': 'A sports stadium has 4,680 seats. If there are 36 sections with equal seating, how many seats are in each section?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '130', 'is_correct': True},
                    {'text': '120', 'is_correct': False},
                    {'text': '140', 'is_correct': False},
                    {'text': '125', 'is_correct': False}
                ],
                'explanation': 'Divide: 4,680 ÷ 36 = 130 seats per section.'
            },
            {
                'question_text': 'A delivery company makes 89 deliveries per day. How many deliveries do they make in 15 days?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '1,335', 'is_correct': True},
                    {'text': '1,235', 'is_correct': False},
                    {'text': '1,435', 'is_correct': False},
                    {'text': '1,325', 'is_correct': False}
                ],
                'explanation': 'Multiply: 89 × 15 = 1,335 deliveries in 15 days.'
            },
            {
                'question_text': 'A school cafeteria serves 2,184 meals. If they serve the same number of meals each day for 12 days, how many meals do they serve per day?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '182', 'is_correct': True},
                    {'text': '172', 'is_correct': False},
                    {'text': '192', 'is_correct': False},
                    {'text': '180', 'is_correct': False}
                ],
                'explanation': 'Divide: 2,184 ÷ 12 = 182 meals per day.'
            }
        ],

        'Fractions': [
            {
                'question_text': 'Maria ate 2/8 of a chocolate bar and her sister ate 3/8 of the same bar. How much of the chocolate bar did they eat together?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '5/8', 'is_correct': True},
                    {'text': '5/16', 'is_correct': False},
                    {'text': '6/8', 'is_correct': False},
                    {'text': '2/3', 'is_correct': False}
                ],
                'explanation': 'Add fractions with same denominator: 2/8 + 3/8 = 5/8 of the chocolate bar.'
            },
            {
                'question_text': 'A pizza is cut into 12 equal slices. If 7 slices are eaten, what fraction of the pizza remains?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '5/12', 'is_correct': True},
                    {'text': '7/12', 'is_correct': False},
                    {'text': '5/7', 'is_correct': False},
                    {'text': '7/5', 'is_correct': False}
                ],
                'explanation': 'If 7 slices are eaten from 12 total slices, then 12 - 7 = 5 slices remain. So 5/12 of the pizza is left.'
            },
            {
                'question_text': 'Which fraction is equivalent to 6/9?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '2/3', 'is_correct': True},
                    {'text': '3/4', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False},
                    {'text': '4/6', 'is_correct': False}
                ],
                'explanation': 'Simplify 6/9 by dividing both numerator and denominator by 3: 6÷3 = 2 and 9÷3 = 3, so 6/9 = 2/3.'
            },
            {
                'question_text': 'A recipe calls for 3/4 cup of sugar. If you want to make 2 batches, how much sugar do you need?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '1 1/2 cups', 'is_correct': True},
                    {'text': '1 1/4 cups', 'is_correct': False},
                    {'text': '6/8 cups', 'is_correct': False},
                    {'text': '2 cups', 'is_correct': False}
                ],
                'explanation': 'Multiply: 3/4 × 2 = 6/4 = 1 2/4 = 1 1/2 cups of sugar needed.'
            },
            {
                'question_text': 'Compare these fractions: 3/5 and 4/7. Which is larger?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '3/5', 'is_correct': False},
                    {'text': '4/7', 'is_correct': False},
                    {'text': 'They are equal', 'is_correct': False},
                    {'text': '3/5 is larger', 'is_correct': True}
                ],
                'explanation': 'Convert to common denominator: 3/5 = 21/35 and 4/7 = 20/35. Since 21/35 > 20/35, then 3/5 > 4/7.'
            },
            {
                'question_text': 'A class has 24 students. If 3/8 of the students wear glasses, how many students wear glasses?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '9 students', 'is_correct': True},
                    {'text': '8 students', 'is_correct': False},
                    {'text': '6 students', 'is_correct': False},
                    {'text': '12 students', 'is_correct': False}
                ],
                'explanation': 'Find 3/8 of 24: (3/8) × 24 = 72/8 = 9 students wear glasses.'
            },
            {
                'question_text': 'A garden is divided into 10 equal sections. If 4 sections have tomatoes and 3 sections have peppers, what fraction of the garden has vegetables?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '7/10', 'is_correct': True},
                    {'text': '4/10', 'is_correct': False},
                    {'text': '3/10', 'is_correct': False},
                    {'text': '1/2', 'is_correct': False}
                ],
                'explanation': 'Add the fractions: 4/10 (tomatoes) + 3/10 (peppers) = 7/10 of the garden has vegetables.'
            },
            {
                'question_text': 'Which fraction is closest to 1/2?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '5/9', 'is_correct': True},
                    {'text': '2/5', 'is_correct': False},
                    {'text': '3/8', 'is_correct': False},
                    {'text': '1/3', 'is_correct': False}
                ],
                'explanation': 'Convert to decimals: 1/2 = 0.5, 5/9 ≈ 0.56, 2/5 = 0.4, 3/8 = 0.375, 1/3 ≈ 0.33. 5/9 is closest to 0.5.'
            },
            {
                'question_text': 'A book has 240 pages. If you have read 5/8 of the book, how many pages have you read?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '150 pages', 'is_correct': True},
                    {'text': '120 pages', 'is_correct': False},
                    {'text': '180 pages', 'is_correct': False},
                    {'text': '200 pages', 'is_correct': False}
                ],
                'explanation': 'Find 5/8 of 240: (5/8) × 240 = 1200/8 = 150 pages read.'
            },
            {
                'question_text': 'A cake recipe calls for 2/3 cup of flour. If you only have 1/2 cup, how much more flour do you need?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': '1/6 cup', 'is_correct': True},
                    {'text': '1/3 cup', 'is_correct': False},
                    {'text': '1/4 cup', 'is_correct': False},
                    {'text': '1/5 cup', 'is_correct': False}
                ],
                'explanation': 'Subtract: 2/3 - 1/2. Find common denominator: 4/6 - 3/6 = 1/6 cup more flour needed.'
            }
        ]
    }

    # Add questions to existing topics
    for topic_title, questions in extensive_questions.items():
        try:
            topic = Topic.objects.get(title=topic_title, class_level=grade5_math)

            for i, q_data in enumerate(questions):
                question, created = Question.objects.get_or_create(
                    topic=topic,
                    question_text=q_data['question_text'],
                    defaults={
                        'question_type': q_data['question_type'],
                        'explanation': q_data.get('explanation', ''),
                        'order': 200 + i,  # Start from 200 to avoid conflicts
                        'is_active': True
                    }
                )

                if created:
                    print(f"  ❓ Added question to {topic_title}: {q_data['question_text'][:50]}...")

                    # Create answer choices
                    for choice_data in q_data['choices']:
                        AnswerChoice.objects.create(
                            question=question,
                            text=choice_data['text'],
                            is_correct=choice_data['is_correct']
                        )

        except Topic.DoesNotExist:
            print(f"⚠️  Topic '{topic_title}' not found, skipping...")

def add_extensive_science_questions():
    """Add 10-15 more questions per science topic"""
    print("🔬 Adding extensive Science questions...")

    try:
        science_subject = Subject.objects.get(name="Science")
        grade5_science = ClassLevel.objects.get(subject=science_subject, level_number=5)
    except (Subject.DoesNotExist, ClassLevel.DoesNotExist):
        print("❌ Science subject or Grade 5 level not found!")
        return

    extensive_science_questions = {
        'Living Things and Their Environment': [
            {
                'question_text': 'In a forest ecosystem, what would happen if all the wolves (predators) were removed?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'The deer population would increase rapidly', 'is_correct': True},
                    {'text': 'The deer population would decrease', 'is_correct': False},
                    {'text': 'Nothing would change', 'is_correct': False},
                    {'text': 'All plants would die', 'is_correct': False}
                ],
                'explanation': 'Without wolves to control their population, deer would multiply rapidly, potentially overgrazing and damaging the ecosystem.'
            },
            {
                'question_text': 'Which of these animals is a decomposer in an ecosystem?',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Eagle', 'is_correct': False},
                    {'text': 'Rabbit', 'is_correct': False},
                    {'text': 'Mushroom', 'is_correct': True},
                    {'text': 'Grass', 'is_correct': False}
                ],
                'explanation': 'Mushrooms are decomposers that break down dead plants and animals, returning nutrients to the soil.'
            },
            {
                'question_text': 'A polar bear has thick fur and a layer of fat. These are examples of:',
                'question_type': 'multiple_choice',
                'choices': [
                    {'text': 'Adaptations for cold weather', 'is_correct': True},
                    {'text': 'Adaptations for hot weather', 'is_correct': False},
                    {'text': 'Learned behaviors', 'is_correct': False},
                    {'text': 'Diseases', 'is_correct': False}
                ],
                'explanation': 'Thick fur and fat layers are physical adaptations that help polar bears survive in extremely cold Arctic conditions.'
            }
        ]
    }

    # Add science questions to existing topics
    for topic_title, questions in extensive_science_questions.items():
        try:
            topic = Topic.objects.get(title=topic_title, class_level=grade5_science)

            for i, q_data in enumerate(questions):
                question, created = Question.objects.get_or_create(
                    topic=topic,
                    question_text=q_data['question_text'],
                    defaults={
                        'question_type': q_data['question_type'],
                        'explanation': q_data.get('explanation', ''),
                        'order': 200 + i,
                        'is_active': True
                    }
                )

                if created:
                    print(f"  ❓ Added question to {topic_title}: {q_data['question_text'][:50]}...")

                    # Create answer choices
                    for choice_data in q_data['choices']:
                        AnswerChoice.objects.create(
                            question=question,
                            text=choice_data['text'],
                            is_correct=choice_data['is_correct']
                        )

        except Topic.DoesNotExist:
            print(f"⚠️  Topic '{topic_title}' not found, skipping...")

if __name__ == '__main__':
    add_extensive_mathematics_questions()
    add_extensive_science_questions()
    print("✅ Extensive additional content added successfully!")
