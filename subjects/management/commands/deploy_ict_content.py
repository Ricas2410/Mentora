from django.core.management.base import BaseCommand
from django.db import models
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Deploy comprehensive Grade 5 ICT content'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Deploying comprehensive Grade 5 ICT content...")
        
        try:
            # Get ICT subject and Grade 5 level
            ict_subject = Subject.objects.get(name='ICT')
            grade5_ict = ClassLevel.objects.get(subject=ict_subject, level_number=5)
            self.stdout.write(f"✅ Found ICT Grade 5: {grade5_ict}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ ICT subject or Grade 5 level not found: {e}"))
            return
        
        # Deploy content for each topic
        topics = Topic.objects.filter(class_level=grade5_ict, is_active=True).order_by('order')
        
        for topic in topics:
            self.stdout.write(f"\n📚 Deploying content for: {topic.title}")
            self.add_study_notes(topic)
            self.add_quiz_questions(topic)
        
        # Final status
        self.print_final_status(grade5_ict)
        self.stdout.write(self.style.SUCCESS("\n🎉 Grade 5 ICT content deployment completed!"))

    def add_study_notes(self, topic):
        """Add study notes for each topic"""
        
        notes_data = {
            'Computer Basics and Parts': {
                'title': 'Understanding Computer Components and Hardware',
                'content': '''# Understanding Computer Components and Hardware

## What is a Computer?

A computer is like a very smart electronic brain that can help us with many tasks. Just like how your brain has different parts that do different jobs, a computer has different parts called "components" that work together.

### Think of a Computer Like a Human Body:
- **Brain** = Processor (CPU) - thinks and makes decisions
- **Memory** = RAM - remembers things temporarily
- **Storage** = Hard Drive - stores things permanently
- **Eyes** = Monitor - shows you information
- **Hands** = Keyboard and Mouse - lets you control it

## Main Parts of a Computer

### 1. **The System Unit (The Computer's Body)**
This is the main box that contains most of the important parts:

#### **CPU (Central Processing Unit) - The Brain**
- **What it does**: Makes all the calculations and decisions
- **Real-life comparison**: Like the brain in your head
- **Fun fact**: Modern CPUs can do billions of calculations per second!
- **Example**: When you click on a program, the CPU decides what to do

#### **RAM (Random Access Memory) - Short-term Memory**
- **What it does**: Temporarily stores information the computer is currently using
- **Real-life comparison**: Like your short-term memory when doing homework
- **Why it matters**: More RAM = computer can do more things at once
- **Example**: When you open a game, it loads into RAM so it runs fast

#### **Hard Drive/SSD - Long-term Storage**
- **What it does**: Permanently stores all your files, programs, and the operating system
- **Real-life comparison**: Like a filing cabinet or your bedroom closet
- **Types**: 
  - **Hard Drive (HDD)**: Uses spinning disks (older, slower, cheaper)
  - **SSD (Solid State Drive)**: Uses electronic chips (newer, faster, more expensive)
- **Example**: Your photos, games, and homework are stored here

#### **Motherboard - The Highway System**
- **What it does**: Connects all the parts together
- **Real-life comparison**: Like the roads that connect different parts of a city
- **Important**: Everything plugs into the motherboard

#### **Power Supply - The Heart**
- **What it does**: Provides electricity to all parts
- **Real-life comparison**: Like your heart pumping blood to your body
- **Safety note**: Never open the power supply - it can be dangerous!

### 2. **Input Devices (How You Talk to the Computer)**

#### **Keyboard**
- **Purpose**: Type letters, numbers, and commands
- **Types**: 
  - **QWERTY**: Standard layout (named after the first 6 letters)
  - **Gaming keyboards**: Special keys for games
  - **Wireless**: No cables needed
- **Fun keys to know**:
  - **Space bar**: Longest key, adds spaces
  - **Enter**: Confirms what you typed
  - **Backspace**: Deletes mistakes
  - **Shift**: Makes capital letters

#### **Mouse**
- **Purpose**: Point, click, and select things on screen
- **Parts**:
  - **Left button**: Main clicking button
  - **Right button**: Opens special menus
  - **Scroll wheel**: Moves up and down on pages
- **Types**:
  - **Optical**: Uses light to track movement
  - **Wireless**: No cables, uses batteries
  - **Gaming mice**: Extra buttons and faster response

#### **Other Input Devices**:
- **Microphone**: Records your voice
- **Camera/Webcam**: Takes pictures and videos
- **Touchscreen**: Touch directly on the screen
- **Game controllers**: For playing video games

### 3. **Output Devices (How the Computer Talks to You)**

#### **Monitor/Screen**
- **Purpose**: Shows you everything the computer is doing
- **Types**:
  - **LCD**: Thin, uses less electricity
  - **LED**: Brighter colors, very thin
  - **Touchscreen**: You can touch it to control
- **Size**: Measured diagonally (like TVs)
- **Resolution**: How clear and detailed the picture is

#### **Speakers**
- **Purpose**: Play sounds, music, and voices
- **Types**:
  - **Built-in**: Inside the computer or monitor
  - **External**: Separate speakers you can move
  - **Headphones**: Private listening

#### **Printer**
- **Purpose**: Makes paper copies of what's on screen
- **Types**:
  - **Inkjet**: Uses liquid ink, good for photos
  - **Laser**: Uses powder, fast for text
  - **3D Printer**: Makes real objects (very cool!)

## How All the Parts Work Together

### Starting Up Your Computer:
1. **Press power button** → Power supply sends electricity
2. **Motherboard wakes up** → Checks if all parts are working
3. **CPU starts thinking** → Begins loading the operating system
4. **RAM gets ready** → Prepares to hold information
5. **Hard drive spins up** → Gets ready to provide files
6. **Monitor turns on** → Shows you what's happening
7. **Operating system loads** → Windows, Mac, or Linux starts
8. **Desktop appears** → Computer is ready to use!

### When You Open a Program:
1. **You double-click** → Mouse sends signal to CPU
2. **CPU finds the program** → Looks on the hard drive
3. **Program loads into RAM** → For fast access
4. **CPU runs the program** → Follows the program's instructions
5. **Results show on monitor** → You see what's happening
6. **You interact** → Keyboard and mouse send more commands

## Taking Care of Your Computer

### Physical Care:
- **Keep it clean** → Dust can block air and cause overheating
- **Don't eat near it** → Crumbs can damage keyboards
- **Handle gently** → Computers have delicate parts
- **Keep drinks away** → Liquids can destroy electronics
- **Proper ventilation** → Don't block air vents

### Digital Care:
- **Regular updates** → Keep software current for security
- **Antivirus protection** → Protect from harmful programs
- **Regular backups** → Save copies of important files
- **Organize files** → Keep your hard drive tidy
- **Close unused programs** → Don't overload your RAM

## Fun Computer Facts

### Amazing Numbers:
- **First computer**: ENIAC (1946) weighed 30 tons!
- **Modern smartphone**: More powerful than computers that sent humans to the moon
- **Internet**: Connects over 4 billion people worldwide
- **Data creation**: We create 2.5 quintillion bytes of data every day

### Cool Comparisons:
- **Your brain**: Has about 86 billion neurons
- **Modern CPU**: Has billions of transistors (electronic switches)
- **Computer memory**: Like having a perfect photographic memory
- **Computer speed**: Can do in 1 second what would take you years

## Troubleshooting Common Problems

### Computer Won't Start:
1. **Check power cable** → Make sure it's plugged in
2. **Check power button** → Press it firmly
3. **Check monitor** → Make sure it's on and connected
4. **Ask for help** → Get an adult if problems continue

### Computer is Slow:
1. **Close unused programs** → Free up RAM
2. **Restart the computer** → Fresh start often helps
3. **Check for updates** → Install important fixes
4. **Clean up files** → Delete things you don't need

### Can't Hear Sound:
1. **Check volume** → Make sure it's not muted
2. **Check speakers** → Are they plugged in and on?
3. **Check headphones** → Are they connected properly?
4. **Restart audio program** → Close and reopen music/video

Remember: Computers are amazing tools that can help you learn, create, and connect with others. The more you understand how they work, the better you can use them to achieve your goals!'''
            },

            'Operating Systems and Desktop': {
                'title': 'Working with Windows and Applications',
                'content': '''# Working with Windows and Applications

## Understanding Windows (The Boxes on Your Screen)

### What is a Window?
A window is like a frame that shows you what a program is doing. Just like looking through a window in your house to see outside, computer windows let you see inside programs.

### Parts of a Window:
1. **Title Bar** - Shows the name of the program (like "Calculator" or "Paint")
2. **Menu Bar** - Contains lists of things you can do (File, Edit, View)
3. **Toolbar** - Buttons for common actions (Save, Print, Copy)
4. **Content Area** - Where your work appears
5. **Scroll Bars** - Help you see more content by moving up/down or left/right

### Window Controls (The Three Buttons):
- **Minimize (-)** - Hides the window but keeps the program running
- **Maximize (□)** - Makes the window fill the whole screen
- **Close (X)** - Closes the program completely

## Working with Multiple Windows

### Real-Life Example:
Imagine you're doing homework and have:
- A math worksheet open
- A calculator running
- A web browser for research
- A document for writing

Each of these would be in its own window!

### Managing Multiple Windows:
1. **Switching Between Windows** - Click on the window you want to use
2. **Moving Windows** - Drag the title bar to move a window
3. **Resizing Windows** - Drag the corners to make windows bigger or smaller
4. **Arranging Windows** - Put windows side by side to work with both

### The Taskbar - Your Window Manager:
- Shows all open programs as buttons
- Click a button to switch to that program
- Right-click for more options

## Common Desktop Applications

### 1. **File Explorer/Finder**
- **Purpose**: Browse and manage your files
- **Real-life comparison**: Like a filing cabinet for your computer
- **Common tasks**: Finding documents, organizing photos, creating folders

### 2. **Calculator**
- **Purpose**: Do math calculations
- **When to use**: Homework, shopping calculations, converting measurements
- **Tip**: Use keyboard numbers for faster input

### 3. **Paint/Drawing Programs**
- **Purpose**: Create pictures and edit images
- **Real-life comparison**: Like a digital art set with brushes and colors
- **Fun projects**: Birthday cards, posters, comic strips

### 4. **Text Editor (Notepad)**
- **Purpose**: Write simple text without formatting
- **When to use**: Quick notes, lists, simple writing
- **Difference from Word**: No fancy formatting, just plain text

### 5. **Web Browser**
- **Purpose**: Access websites and the internet
- **Examples**: Chrome, Firefox, Safari, Edge
- **Safety tip**: Always ask an adult before visiting new websites

## Keyboard Shortcuts for Faster Work

### Essential Shortcuts:
- **Ctrl + C** - Copy (like using a photocopier)
- **Ctrl + V** - Paste (put the copied item somewhere else)
- **Ctrl + Z** - Undo (take back the last thing you did)
- **Ctrl + S** - Save your work
- **Alt + Tab** - Switch between open programs quickly
- **Windows Key** - Open the Start Menu

### Why Use Shortcuts?
- Faster than using the mouse
- Makes you look like a computer expert!
- Saves time when doing repetitive tasks

## Desktop Organization Tips

### Keep Your Desktop Clean:
1. **Don't put too many icons** - Like keeping your desk tidy
2. **Group similar programs** - Put games together, school programs together
3. **Use folders** - Create folders for different subjects or activities
4. **Regular cleanup** - Delete shortcuts you don't use

### Creating Shortcuts:
- Right-click on a program → "Create Shortcut"
- Drag the shortcut to your desktop
- Name it something you'll remember

## Troubleshooting Common Problems

### When a Program Won't Respond:
1. **Wait a moment** - Sometimes programs need time to think
2. **Try clicking once** - Don't click multiple times rapidly
3. **Use Task Manager** - Ctrl + Alt + Delete to close stuck programs
4. **Ask for help** - Get an adult if problems continue

### When You Can't Find a Program:
1. **Check the taskbar** - It might be minimized
2. **Use the Start Menu search** - Type the program name
3. **Look in All Programs** - Browse through the program list
4. **Check the desktop** - Look for the program icon

Remember: Practice makes perfect! The more you use these skills, the easier they become. Don't be afraid to explore and try new things - you can always undo or ask for help!'''
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
            'Computer Basics and Parts': [
                {
                    'question': 'What is the CPU often called because it makes all the calculations and decisions?',
                    'type': 'multiple_choice',
                    'choices': ['The Heart', 'The Brain', 'The Eyes', 'The Hands'],
                    'correct': 1,
                    'explanation': 'The CPU is called "The Brain" of the computer because it makes all calculations and decisions, just like your brain does for your body.'
                },
                {
                    'question': 'Which part of the computer temporarily stores information that is currently being used?',
                    'type': 'multiple_choice',
                    'choices': ['Hard Drive', 'Monitor', 'RAM', 'Keyboard'],
                    'correct': 2,
                    'explanation': 'RAM (Random Access Memory) temporarily stores information the computer is currently using, like short-term memory.'
                },
                {
                    'question': 'Sarah wants to save her photos permanently. Which computer part stores files for a long time?',
                    'type': 'multiple_choice',
                    'choices': ['RAM', 'CPU', 'Hard Drive/SSD', 'Monitor'],
                    'correct': 2,
                    'explanation': 'The Hard Drive or SSD provides permanent storage for files like photos, documents, and programs.'
                },
                {
                    'question': 'Fill in the blank: The _____ connects all the computer parts together like roads connecting different parts of a city.',
                    'type': 'fill_blank',
                    'correct': 'motherboard',
                    'explanation': 'The motherboard connects all computer components together, acting like a highway system for data.'
                },
                {
                    'question': 'True or False: You should keep food and drinks away from your computer to avoid damage.',
                    'type': 'true_false',
                    'correct': 'true',
                    'explanation': 'True! Food crumbs can damage keyboards and liquids can destroy electronic components.'
                }
            ],

            'Operating Systems and Desktop': [
                {
                    'question': 'What are the three main window control buttons in the top-right corner of most windows?',
                    'type': 'multiple_choice',
                    'choices': ['Save, Copy, Paste', 'Minimize, Maximize, Close', 'File, Edit, View', 'Start, Stop, Pause'],
                    'correct': 1,
                    'explanation': 'The three window control buttons are Minimize (-), Maximize (□), and Close (X).'
                },
                {
                    'question': 'Which keyboard shortcut allows you to quickly switch between open programs?',
                    'type': 'multiple_choice',
                    'choices': ['Ctrl + C', 'Ctrl + V', 'Alt + Tab', 'Ctrl + Z'],
                    'correct': 2,
                    'explanation': 'Alt + Tab is the keyboard shortcut to quickly switch between open programs and windows.'
                },
                {
                    'question': 'What is the main purpose of the taskbar?',
                    'type': 'multiple_choice',
                    'choices': ['To store files', 'To show open programs and switch between them', 'To connect to internet', 'To play music'],
                    'correct': 1,
                    'explanation': 'The taskbar shows all open programs as buttons and allows you to switch between them easily.'
                },
                {
                    'question': 'Fill in the blank: The _____ bar shows the name of the program at the top of each window.',
                    'type': 'fill_blank',
                    'correct': 'title',
                    'explanation': 'The title bar is at the top of each window and shows the name of the program or document.'
                },
                {
                    'question': 'True or False: You can have multiple windows open at the same time on your computer.',
                    'type': 'true_false',
                    'correct': 'true',
                    'explanation': 'Yes, you can have multiple windows open simultaneously and switch between them as needed.'
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
        self.stdout.write("\n=== FINAL GRADE 5 ICT STATUS ===")
        for topic in Topic.objects.filter(class_level=grade5_ict).order_by('order'):
            notes_count = StudyNote.objects.filter(topic=topic).count()
            questions_count = Question.objects.filter(topic=topic).count()
            self.stdout.write(f"{topic.title}: {notes_count} notes, {questions_count} questions")
        
        total_notes = StudyNote.objects.filter(topic__class_level=grade5_ict).count()
        total_questions = Question.objects.filter(topic__class_level=grade5_ict).count()
        self.stdout.write(f"\nTOTAL: {total_notes} notes, {total_questions} questions")
