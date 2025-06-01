from django.core.management.base import BaseCommand
from django.db import models
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Complete Grade 5 ICT content with Email and Programming topics'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Completing Grade 5 ICT content...")
        
        try:
            # Get ICT subject and Grade 5 level
            ict_subject = Subject.objects.get(name='ICT')
            grade5_ict = ClassLevel.objects.get(subject=ict_subject, level_number=5)
            self.stdout.write(f"✅ Found ICT Grade 5: {grade5_ict}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ ICT subject or Grade 5 level not found: {e}"))
            return
        
        # Target the final topics
        target_topics = [
            'Email and Digital Communication',
            'Introduction to Programming Concepts'
        ]
        
        for topic_name in target_topics:
            try:
                topic = Topic.objects.get(title=topic_name, class_level=grade5_ict)
                self.stdout.write(f"\n📚 Adding content to: {topic.title}")
                self.add_study_notes(topic)
                self.add_quiz_questions(topic)
            except Topic.DoesNotExist:
                self.stdout.write(f"⚠️ Topic not found: {topic_name}")
        
        # Final status
        self.print_final_status(grade5_ict)
        self.stdout.write(self.style.SUCCESS("\n🎉 Grade 5 ICT content is now COMPLETE!"))

    def add_study_notes(self, topic):
        """Add comprehensive study notes for each topic"""
        
        notes_data = {
            'Email and Digital Communication': {
                'title': 'Email Basics and Digital Communication',
                'content': '''# Email Basics and Digital Communication

## Understanding Email

### What is Email?
Email (Electronic Mail) is like sending letters through the computer instead of the post office. It's a way to send messages, pictures, and files to people anywhere in the world instantly!

### Real-Life Comparison:
- **Traditional mail**: Write letter → Put in envelope → Mail to post office → Delivered in days
- **Email**: Type message → Click send → Delivered in seconds!

### Parts of an Email Address:
**Example**: sarah.student@school.edu

- **Username**: sarah.student (identifies the person)
- **@ symbol**: Separates username from domain
- **Domain**: school.edu (identifies the email provider/organization)

### Common Email Providers:
- **Gmail**: @gmail.com (Google's email service)
- **Outlook**: @outlook.com (Microsoft's email service)
- **Yahoo**: @yahoo.com (Yahoo's email service)
- **School emails**: Often end with .edu
- **Work emails**: Usually company name like @company.com

## Parts of an Email

### Email Interface Components:

#### **Inbox:**
- **What it is**: Where you receive new emails
- **Like**: Your mailbox at home
- **Organization**: Usually shows newest emails first

#### **Compose/New Email:**
- **What it does**: Creates a new email to send
- **Button location**: Usually says "Compose" or "New"
- **Keyboard shortcut**: Often Ctrl + N

#### **Sent Items:**
- **What it contains**: Copies of emails you've sent
- **Why useful**: Proof you sent something, reference for follow-up

#### **Drafts:**
- **What it stores**: Emails you started but haven't sent yet
- **When to use**: When you need time to think about your message
- **Auto-save**: Most email programs save drafts automatically

#### **Trash/Deleted Items:**
- **What it holds**: Emails you've deleted
- **Recovery**: You can usually get emails back from here
- **Permanent deletion**: Trash is usually emptied automatically after 30 days

### Writing an Email:

#### **Essential Fields:**
- **To**: Email address of the person you're sending to
- **Subject**: Brief description of what your email is about
- **Message body**: Your actual message

#### **Optional Fields:**
- **CC (Carbon Copy)**: Send a copy to someone else
- **BCC (Blind Carbon Copy)**: Send a secret copy (others can't see who got BCC)
- **Attachments**: Files you want to include

## Email Etiquette and Best Practices

### Writing Professional Emails:

#### **Subject Lines:**
- **Be specific**: "Math homework question" not "Question"
- **Keep it short**: Aim for 5-8 words
- **Good examples**:
  - "Grade 5 Science Project Due Date"
  - "Permission slip for field trip"
  - "Thank you for helping with presentation"

#### **Greeting:**
- **Formal**: "Dear Mrs. Johnson," or "Dear Mr. Smith,"
- **Less formal**: "Hi Sarah," or "Hello Tom,"
- **Very casual**: "Hey!" (only for close friends)

#### **Message Body:**
- **Be clear and polite**: Say what you need clearly
- **Use proper spelling**: Check your spelling before sending
- **Be brief**: People are busy, get to the point
- **Use paragraphs**: Break up long messages

#### **Closing:**
- **Formal**: "Sincerely," "Best regards," "Thank you,"
- **Less formal**: "Thanks," "Best," "See you soon,"
- **Sign your name**: Always include your name at the end

### Example Email:
```
To: teacher@school.edu
Subject: Question about tomorrow's math test

Dear Mrs. Johnson,

I hope you're having a good day. I have a question about tomorrow's math test. Will we need to bring our calculators, or will they be provided?

Thank you for your time.

Best regards,
Sarah Student
Grade 5, Room 12
```

## Email Safety and Security

### Protecting Your Email Account:

#### **Strong Passwords:**
- **Use 8+ characters**: Mix letters, numbers, and symbols
- **Don't use personal info**: No birthdays, pet names, or addresses
- **Unique passwords**: Different password for email than other accounts
- **Example**: "MyEmail2024!" (but create your own!)

#### **Two-Factor Authentication:**
- **What it is**: Extra security step after password
- **How it works**: Enter password + code from phone
- **Why important**: Even if someone knows your password, they can't get in
- **Ask an adult**: To help you set this up

### Recognizing Spam and Phishing:

#### **Spam Emails (Junk Mail):**
- **What they are**: Unwanted emails trying to sell things
- **Common signs**: 
  - "You've won a million dollars!"
  - Lots of spelling mistakes
  - Asking for money or personal information
  - From unknown senders

#### **Phishing Emails (Fake Emails):**
- **What they are**: Fake emails pretending to be from real companies
- **Goal**: Steal your passwords or personal information
- **Warning signs**:
  - "Your account will be closed unless you click here"
  - Asking for passwords or personal information
  - Links that don't match the real website
  - Urgent language: "Act now!" "Limited time!"

#### **What to Do:**
1. **Don't click links** in suspicious emails
2. **Don't download attachments** from unknown senders
3. **Don't reply** to spam emails
4. **Tell an adult** if you're unsure about an email
5. **Mark as spam** to help your email filter learn

## Digital Communication Beyond Email

### Other Forms of Digital Communication:

#### **Instant Messaging:**
- **Examples**: WhatsApp, Messenger, Teams Chat
- **Best for**: Quick conversations, immediate responses
- **Etiquette**: Use proper spelling, be respectful

#### **Video Calls:**
- **Examples**: Zoom, Google Meet, Skype
- **Best for**: Face-to-face conversations, group meetings
- **Tips**: Good lighting, quiet background, mute when not talking

#### **Collaborative Documents:**
- **Examples**: Google Docs, Microsoft 365
- **Best for**: Working on projects together
- **Benefits**: Everyone can edit, see changes in real-time

### Choosing the Right Communication Method:

#### **Use Email When:**
- Sending formal messages
- Need a record of the conversation
- Sending files or documents
- Communicating with teachers or adults
- Not urgent (response expected in hours/days)

#### **Use Instant Messaging When:**
- Quick questions
- Casual conversations with friends
- Need immediate response
- Coordinating plans

#### **Use Video Calls When:**
- Complex discussions
- Group projects
- Want to see facial expressions
- Presenting or demonstrating something

## Email Organization and Management

### Keeping Your Inbox Organized:

#### **Folders/Labels:**
- **Create folders** for different topics: School, Family, Friends, Projects
- **Move emails** to appropriate folders after reading
- **Use labels** to categorize emails (if your email supports it)

#### **Email Rules:**
- **Automatic sorting**: Set rules to automatically organize emails
- **Example**: All emails from school automatically go to "School" folder
- **Ask for help**: Get an adult to help set up rules

#### **Regular Cleanup:**
- **Delete old emails** you don't need
- **Empty trash** regularly
- **Unsubscribe** from newsletters you don't read
- **Archive** important emails you want to keep but don't need in inbox

### Search and Find:

#### **Using Search:**
- **Search by sender**: Find all emails from a specific person
- **Search by subject**: Look for emails about specific topics
- **Search by date**: Find emails from a specific time period
- **Use keywords**: Search for specific words in email content

#### **Advanced Search Tips:**
- **Use quotes**: "exact phrase" to find exact words
- **Use filters**: Date range, sender, has attachments
- **Star important emails**: Mark important emails for easy finding

Remember: Email is a powerful tool for communication, but it's important to use it safely and respectfully. Always think before you send, and don't hesitate to ask for help when you need it!'''
            },
            
            'Introduction to Programming Concepts': {
                'title': 'Fun Introduction to Programming and Coding',
                'content': '''# Fun Introduction to Programming and Coding

## What is Programming?

### Understanding Programming:
Programming is like giving instructions to a computer. Just like you might give directions to a friend to get to your house, programming is giving step-by-step directions to a computer to solve problems or create cool things!

### Real-Life Comparison:
- **Recipe**: Step-by-step instructions to make cookies
- **LEGO instructions**: Step-by-step guide to build a castle
- **Programming**: Step-by-step instructions for a computer to create a game

### What Can You Create with Programming?
- **Games**: Like Minecraft, Roblox, or mobile games
- **Websites**: Like YouTube, Google, or your school website
- **Apps**: Like calculator, weather, or drawing apps
- **Robots**: Programming robots to move, dance, or solve puzzles
- **Art**: Creating digital art, animations, and music

## Basic Programming Concepts

### 1. **Algorithms (Step-by-Step Instructions)**

An algorithm is just a fancy word for a list of steps to solve a problem.

#### **Example Algorithm: Making a Peanut Butter Sandwich**
1. Get two slices of bread
2. Open the peanut butter jar
3. Get a knife
4. Put peanut butter on one slice
5. Put the slices together
6. Enjoy your sandwich!

#### **Programming Algorithm: Drawing a Square**
1. Move forward 100 steps
2. Turn right 90 degrees
3. Move forward 100 steps
4. Turn right 90 degrees
5. Move forward 100 steps
6. Turn right 90 degrees
7. Move forward 100 steps
8. Turn right 90 degrees

### 2. **Sequences (Doing Things in Order)**

In programming, the order of instructions matters! Just like getting dressed, you put on socks before shoes.

#### **Good Sequence:**
1. Put on socks
2. Put on shoes
3. Tie shoelaces

#### **Bad Sequence:**
1. Put on shoes
2. Put on socks ← This won't work!
3. Tie shoelaces

### 3. **Loops (Repeating Actions)**

Loops help us repeat actions without writing the same instruction over and over.

#### **Real-Life Loop Example:**
Instead of writing "Brush your teeth" 365 times for a year, we can say:
"Every day for 365 days: Brush your teeth"

#### **Programming Loop Example:**
Instead of writing "Move forward" 10 times, we can say:
"Repeat 10 times: Move forward"

### 4. **Conditions (Making Decisions)**

Conditions help computers make decisions based on different situations.

#### **Real-Life Condition:**
"IF it's raining, THEN take an umbrella, ELSE wear sunglasses"

#### **Programming Condition:**
"IF the character touches a wall, THEN turn around, ELSE keep moving"

### 5. **Variables (Storing Information)**

Variables are like boxes that store information we want to remember and use later.

#### **Real-Life Variables:**
- **Name box**: Contains "Sarah"
- **Age box**: Contains "10"
- **Favorite color box**: Contains "Blue"

#### **Programming Variables:**
- **Score**: Contains "150"
- **Player name**: Contains "SuperGamer"
- **Lives remaining**: Contains "3"

## Programming Languages for Beginners

### Visual Programming Languages:

#### **1. Scratch**
- **What it is**: Drag-and-drop programming language
- **Perfect for**: Complete beginners
- **What you can make**: Games, animations, stories
- **Why it's great**: No typing required, visual blocks
- **Website**: scratch.mit.edu

#### **2. Blockly**
- **What it is**: Google's visual programming language
- **Perfect for**: Learning programming logic
- **What you can make**: Simple programs and puzzles
- **Why it's great**: Teaches real programming concepts

#### **3. Code.org**
- **What it is**: Free programming courses for kids
- **Perfect for**: Structured learning
- **What you can make**: Games with popular characters
- **Why it's great**: Step-by-step tutorials

### Text-Based Languages (For Later):

#### **1. Python**
- **What it is**: Beginner-friendly text programming language
- **Perfect for**: Students ready for real coding
- **What you can make**: Games, websites, data analysis
- **Why it's great**: Easy to read and understand

#### **2. JavaScript**
- **What it is**: Language for making websites interactive
- **Perfect for**: Web development
- **What you can make**: Interactive websites and web games
- **Why it's great**: Runs in web browsers

## Fun Programming Activities

### Activity 1: Human Robot
**Goal**: Understand how specific instructions need to be

**How to play**:
1. One person is the "programmer"
2. One person is the "robot"
3. The programmer gives step-by-step instructions
4. The robot follows EXACTLY what is said
5. Try to get the robot to pick up a pencil

**Example**:
- Programmer: "Move forward"
- Robot: "How many steps?"
- Programmer: "Move forward 3 steps"
- Robot: Moves forward 3 steps
- Programmer: "Turn right"
- Robot: Turns right
- Programmer: "Bend down and pick up the pencil"

### Activity 2: Algorithm Writing
**Goal**: Practice writing clear step-by-step instructions

**Tasks to try**:
1. Write an algorithm for brushing your teeth
2. Write an algorithm for making your bed
3. Write an algorithm for drawing a house
4. Write an algorithm for playing your favorite game

### Activity 3: Pattern Recognition
**Goal**: Identify patterns and loops

**Look for patterns in**:
- Daily routines (wake up, eat breakfast, go to school...)
- Nature (seasons, day/night, plant growth...)
- Games (levels, scoring, character movements...)
- Music (verses, chorus, rhythm...)

## Introduction to Scratch Programming

### Getting Started with Scratch:

#### **1. The Scratch Interface:**
- **Stage**: Where your characters perform
- **Sprites**: Characters or objects in your program
- **Blocks**: Puzzle pieces that create instructions
- **Scripts**: Connected blocks that make programs

#### **2. Types of Blocks:**
- **Motion blocks** (blue): Make sprites move
- **Looks blocks** (purple): Change appearance
- **Sound blocks** (pink): Add music and sound effects
- **Events blocks** (yellow): Start programs when something happens
- **Control blocks** (orange): Loops and conditions
- **Sensing blocks** (light blue): Detect what's happening

### Simple Scratch Projects:

#### **Project 1: Moving Cat**
1. Use "when green flag clicked" block
2. Add "move 10 steps" block
3. Add "if on edge, bounce" block
4. Add "forever" loop around the movement blocks
5. Click the green flag to see your cat move!

#### **Project 2: Color-Changing Sprite**
1. Use "when green flag clicked" block
2. Add "forever" loop
3. Inside the loop, add "change color effect by 25"
4. Add "wait 1 seconds"
5. Watch your sprite change colors!

#### **Project 3: Simple Game**
1. Create a sprite that follows your mouse
2. Create another sprite that moves randomly
3. Use "if touching" block to detect when they meet
4. Add sound effects and score counting

## Problem-Solving with Programming

### Breaking Down Big Problems:

#### **The Programming Process:**
1. **Understand the problem**: What do you want to create?
2. **Break it into smaller parts**: What are the main features?
3. **Plan your solution**: What steps are needed?
4. **Code one part at a time**: Start with the simplest part
5. **Test and debug**: Fix any problems
6. **Add more features**: Build on what works

#### **Example: Creating a Simple Game**
1. **Big problem**: "I want to make a game"
2. **Smaller parts**:
   - Character that moves
   - Objects to collect
   - Score counter
   - Game over condition
3. **Start simple**: Just make the character move
4. **Add features**: One at a time

### Debugging (Fixing Problems):

#### **Common Programming Problems:**
- **Sprite not moving**: Check if movement blocks are connected
- **Sound not playing**: Make sure sound blocks are in the right place
- **Game not starting**: Check if you have "when green flag clicked"
- **Unexpected behavior**: Read through your code step by step

#### **Debugging Tips:**
1. **Read your code carefully**: Does it say what you want?
2. **Test small parts**: Make sure each piece works
3. **Ask for help**: Programming is teamwork!
4. **Try different solutions**: There's usually more than one way
5. **Don't give up**: Every programmer faces problems!

## Programming in Everyday Life

### Where Do We See Programming?

#### **At Home:**
- **Smart TV**: Programming controls channels and apps
- **Microwave**: Programming controls cooking time and power
- **Video games**: Programming creates characters and rules
- **Smartphones**: Programming runs all the apps

#### **At School:**
- **Interactive whiteboards**: Programming responds to touch
- **Educational games**: Programming makes learning fun
- **School websites**: Programming organizes information
- **Attendance systems**: Programming tracks who's present

#### **In the Community:**
- **Traffic lights**: Programming controls when lights change
- **ATM machines**: Programming handles money transactions
- **Store scanners**: Programming reads barcodes
- **GPS navigation**: Programming finds the best routes

### Future Careers in Programming:

#### **Game Developer:**
- Create video games and mobile apps
- Design characters, levels, and gameplay
- Work with artists and designers

#### **Web Developer:**
- Build websites and online applications
- Make websites look good and work well
- Help businesses connect with customers online

#### **App Developer:**
- Create mobile apps for phones and tablets
- Solve problems with technology
- Make life easier for people

#### **Robotics Engineer:**
- Program robots to help people
- Work in factories, hospitals, or space exploration
- Combine programming with engineering

Remember: Programming is like learning a new language - it takes practice, but it's incredibly rewarding! Start with simple projects, be patient with yourself, and most importantly, have fun creating amazing things with code!'''
            }
        }
        
        if topic.title in notes_data:
            note_data = notes_data[topic.title]
            # Get current max order
            max_order = StudyNote.objects.filter(topic=topic).aggregate(
                max_order=models.Max('order')
            )['max_order'] or 0
            
            note, created = StudyNote.objects.get_or_create(
                topic=topic,
                title=note_data['title'],
                defaults={
                    'content': note_data['content'],
                    'order': max_order + 1,
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f"  📝 Added note: {note_data['title']}")
            else:
                self.stdout.write(f"  📝 Note already exists: {note_data['title']}")

    def add_quiz_questions(self, topic):
        """Add quiz questions for each topic"""
        
        questions_data = {
            'Email and Digital Communication': [
                {
                    'question': 'What does the @ symbol in an email address separate?',
                    'type': 'multiple_choice',
                    'choices': ['First and last name', 'Username and domain', 'Subject and message', 'Sender and receiver'],
                    'correct': 1,
                    'explanation': 'The @ symbol separates the username (person) from the domain (email provider or organization).'
                },
                {
                    'question': 'Which part of an email briefly describes what the message is about?',
                    'type': 'multiple_choice',
                    'choices': ['To field', 'Subject line', 'Message body', 'Signature'],
                    'correct': 1,
                    'explanation': 'The subject line gives a brief description of what the email is about, helping the recipient understand the purpose.'
                },
                {
                    'question': 'What should you do if you receive a suspicious email asking for your password?',
                    'type': 'multiple_choice',
                    'choices': ['Reply with your password', 'Click all the links', 'Delete it and tell an adult', 'Forward it to friends'],
                    'correct': 2,
                    'explanation': 'Never give out passwords in emails. Delete suspicious emails and tell a trusted adult about them.'
                },
                {
                    'question': 'Fill in the blank: _____ emails are fake emails that try to steal your personal information.',
                    'type': 'fill_blank',
                    'correct': 'Phishing',
                    'explanation': 'Phishing emails pretend to be from real companies but are actually trying to steal your passwords or personal information.'
                },
                {
                    'question': 'True or False: You should always use proper spelling and be polite when writing emails.',
                    'type': 'true_false',
                    'correct': 'true',
                    'explanation': 'True! Good email etiquette includes proper spelling, grammar, and polite language, especially in formal communications.'
                }
            ],
            
            'Introduction to Programming Concepts': [
                {
                    'question': 'What is an algorithm in programming?',
                    'type': 'multiple_choice',
                    'choices': ['A type of computer', 'Step-by-step instructions to solve a problem', 'A programming language', 'A computer game'],
                    'correct': 1,
                    'explanation': 'An algorithm is a set of step-by-step instructions that tells a computer how to solve a problem or complete a task.'
                },
                {
                    'question': 'Which programming language uses drag-and-drop blocks and is perfect for beginners?',
                    'type': 'multiple_choice',
                    'choices': ['Python', 'JavaScript', 'Scratch', 'HTML'],
                    'correct': 2,
                    'explanation': 'Scratch uses visual drag-and-drop blocks instead of typing code, making it perfect for beginners to learn programming concepts.'
                },
                {
                    'question': 'What do loops help us do in programming?',
                    'type': 'multiple_choice',
                    'choices': ['Delete files', 'Repeat actions', 'Change colors', 'Send emails'],
                    'correct': 1,
                    'explanation': 'Loops allow us to repeat actions multiple times without writing the same instruction over and over again.'
                },
                {
                    'question': 'Fill in the blank: _____ are like boxes that store information we want to remember and use later.',
                    'type': 'fill_blank',
                    'correct': 'Variables',
                    'explanation': 'Variables store information (like numbers, text, or true/false values) that programs can remember and use later.'
                },
                {
                    'question': 'True or False: Programming is only used for making video games.',
                    'type': 'true_false',
                    'correct': 'false',
                    'explanation': 'False! Programming is used for many things including websites, mobile apps, robots, smart devices, and much more than just games.'
                }
            ]
        }
        
        # Add questions for this topic if data exists
        if topic.title in questions_data:
            questions = questions_data[topic.title]
            for i, q_data in enumerate(questions):
                # Get current max order for this topic
                max_order = Question.objects.filter(topic=topic).aggregate(
                    max_order=models.Max('order')
                )['max_order'] or 0
                
                # Check if question already exists
                existing = Question.objects.filter(
                    topic=topic,
                    question_text=q_data['question']
                ).first()
                
                if existing:
                    self.stdout.write(f"  ❓ Question already exists: {q_data['question'][:50]}...")
                    continue
                
                question = Question.objects.create(
                    topic=topic,
                    question_text=q_data['question'],
                    question_type=q_data['type'],
                    difficulty='easy',
                    points=10,
                    order=max_order + i + 1,
                    explanation=q_data.get('explanation', ''),
                    is_active=True
                )
                
                # Create answer choices for multiple choice questions
                if q_data['type'] == 'multiple_choice':
                    for j, choice_text in enumerate(q_data['choices']):
                        AnswerChoice.objects.create(
                            question=question,
                            choice_text=choice_text,
                            is_correct=(j == q_data['correct']),
                            order=j + 1
                        )
                
                self.stdout.write(f"  ❓ Added question: {q_data['question'][:50]}...")

    def print_final_status(self, grade5_ict):
        """Print final status of Grade 5 ICT content"""
        self.stdout.write("\n=== COMPLETE GRADE 5 ICT STATUS ===")
        for topic in Topic.objects.filter(class_level=grade5_ict).order_by('order'):
            notes_count = StudyNote.objects.filter(topic=topic).count()
            questions_count = Question.objects.filter(topic=topic).count()
            self.stdout.write(f"{topic.title}: {notes_count} notes, {questions_count} questions")
        
        total_notes = StudyNote.objects.filter(topic__class_level=grade5_ict).count()
        total_questions = Question.objects.filter(topic__class_level=grade5_ict).count()
        self.stdout.write(f"\nTOTAL: {total_notes} notes, {total_questions} questions")
        self.stdout.write("🎉 Grade 5 ICT curriculum is now COMPLETE with comprehensive content!")
