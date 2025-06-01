#!/usr/bin/env python
"""
Script to add comprehensive additional Grade 5 ICT content
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice
from django.db import models

def add_comprehensive_ict_content():
    """Add 10+ additional notes and questions for Grade 5 ICT"""
    print("🖥️ Adding comprehensive Grade 5 ICT content...")
    
    try:
        # Get ICT subject and Grade 5 level
        ict_subject = Subject.objects.get(name='ICT')
        grade5_ict = ClassLevel.objects.get(subject=ict_subject, level_number=5)
        print(f"✅ Found ICT Grade 5: {grade5_ict}")
    except:
        print("❌ ICT subject or Grade 5 level not found!")
        return False
    
    # Get all topics
    topics = Topic.objects.filter(class_level=grade5_ict, is_active=True).order_by('order')
    
    for topic in topics:
        print(f"\n📚 Adding content for: {topic.title}")
        add_study_notes_for_topic(topic)
        add_quiz_questions_for_topic(topic)
    
    print("\n🎉 Additional Grade 5 ICT content added successfully!")

def add_study_notes_for_topic(topic):
    """Add comprehensive study notes for each topic"""
    
    study_notes_data = {
        'Operating Systems and Desktop': [
            {
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
        ],
        
        'File Management and Organization': [
            {
                'title': 'Advanced File Organization and Management',
                'content': '''# Advanced File Organization and Management

## Understanding File Types and Extensions

### What are File Extensions?
File extensions are the letters after the dot in a filename. They tell the computer what type of file it is and which program should open it.

### Common File Types for Students:

#### **Document Files:**
- **.docx** - Microsoft Word documents (essays, reports)
- **.pdf** - PDF files (can't be easily changed, good for sharing)
- **.txt** - Plain text files (simple notes)
- **.rtf** - Rich text format (works with many programs)

#### **Image Files:**
- **.jpg/.jpeg** - Photos from cameras and phones
- **.png** - Pictures with transparent backgrounds
- **.gif** - Moving pictures/animations
- **.bmp** - Basic image files

#### **Audio Files:**
- **.mp3** - Music files (most common)
- **.wav** - High-quality sound files
- **.m4a** - Apple music format

#### **Video Files:**
- **.mp4** - Most common video format
- **.avi** - Older video format
- **.mov** - Apple video format

#### **Compressed Files:**
- **.zip** - Compressed folder (makes files smaller)
- **.rar** - Another type of compressed file

## Creating an Effective Folder Structure

### School Organization System:
```
My Documents/
├── School Year 2024-2025/
│   ├── Grade 5/
│   │   ├── Mathematics/
│   │   │   ├── Homework/
│   │   │   ├── Tests/
│   │   │   └── Projects/
│   │   ├── English/
│   │   │   ├── Essays/
│   │   │   ├── Reading/
│   │   │   └── Vocabulary/
│   │   ├── Science/
│   │   │   ├── Experiments/
│   │   │   ├── Reports/
│   │   │   └── Pictures/
│   │   ├── Social Studies/
│   │   └── ICT/
│   └── Completed Work/
├── Personal/
│   ├── Photos/
│   │   ├── Family/
│   │   ├── Friends/
│   │   └── Vacations/
│   ├── Music/
│   └── Games/
└── Projects/
    ├── Art Projects/
    ├── Science Fair/
    └── Presentations/
```

### Why This Organization Works:
1. **Year-based** - Easy to find old work
2. **Subject separation** - No mixing of different classes
3. **Type-based subfolders** - Homework separate from tests
4. **Personal vs. School** - Clear boundaries

## File Naming Best Practices

### Good File Names:
- **Math_Homework_Week5_2024.docx**
- **Science_Volcano_Project_Final.pdf**
- **English_Essay_MyPet_Draft1.docx**
- **Family_Vacation_Beach_2024.jpg**

### Bad File Names:
- **homework.docx** (too vague)
- **untitled1.docx** (meaningless)
- **asdfgh.jpg** (random letters)
- **new document (1).docx** (default name)

### File Naming Rules:
1. **Be specific** - Include subject, assignment, date
2. **Use underscores or dashes** - Instead of spaces
3. **Include version numbers** - Draft1, Draft2, Final
4. **Add dates** - YYYY-MM-DD format works best
5. **Avoid special characters** - No / \\ : * ? " < > |

## Advanced File Operations

### Copying vs. Moving Files:

#### **Copying (Ctrl + C, Ctrl + V):**
- **What it does**: Makes a duplicate of the file
- **When to use**: When you want the file in two places
- **Example**: Copying a photo to share with friends while keeping the original

#### **Moving (Cut: Ctrl + X, Paste: Ctrl + V):**
- **What it does**: Moves the file from one location to another
- **When to use**: When you want to reorganize files
- **Example**: Moving completed homework from "In Progress" to "Completed" folder

### Creating Shortcuts:
- **What it is**: A link to a file or program
- **Advantage**: Quick access without moving the original
- **How to create**: Right-click → "Create Shortcut"
- **Real-life example**: Like having a bookmark to your favorite page

### Compressing Files (Making ZIP Files):
- **Purpose**: Make files smaller for easier sharing
- **When to use**: Sending multiple files via email
- **How to**: Select files → Right-click → "Send to" → "Compressed folder"
- **Benefit**: Faster uploads and downloads

## Backup and Safety Strategies

### The 3-2-1 Backup Rule:
- **3** copies of important files
- **2** different types of storage (computer + USB)
- **1** copy stored somewhere else (cloud or different location)

### Backup Options for Students:

#### **USB Flash Drives:**
- **Pros**: Portable, works on any computer
- **Cons**: Can be lost or broken
- **Best for**: Daily homework backup

#### **Cloud Storage:**
- **Examples**: Google Drive, OneDrive, iCloud
- **Pros**: Accessible from anywhere, automatic backup
- **Cons**: Needs internet connection
- **Best for**: Important projects and documents

#### **External Hard Drives:**
- **Pros**: Lots of storage space
- **Cons**: More expensive, less portable
- **Best for**: Photos, videos, large projects

### What to Backup:
1. **School assignments** - All homework and projects
2. **Personal photos** - Family memories
3. **Creative work** - Art, stories, videos you've made
4. **Important documents** - Certificates, awards

### Backup Schedule:
- **Daily**: Current homework to USB or cloud
- **Weekly**: All school work to external drive
- **Monthly**: Complete backup of everything important

## File Recovery and Problem Solving

### When Files Go Missing:

#### **Check the Recycle Bin:**
1. Double-click the Recycle Bin icon
2. Look for your file
3. Right-click and select "Restore" if found

#### **Use Search Function:**
1. Click Start Menu
2. Type the file name or part of it
3. Look through search results
4. Check "Modified Date" to find recent files

#### **Check Recent Files:**
1. Open the program that created the file
2. Look in "File" → "Recent" or "Open Recent"
3. Click on the file name to open it

### Preventing File Loss:
1. **Save frequently** - Ctrl + S every few minutes
2. **Use descriptive names** - Easier to find later
3. **Organize immediately** - Don't leave files on desktop
4. **Regular backups** - Follow the backup schedule

### File Corruption (When Files Won't Open):
1. **Try different programs** - Sometimes another program can open it
2. **Check file extension** - Make sure it's correct
3. **Restore from backup** - This is why backups are important!
4. **Ask for help** - Get an adult or teacher to assist

Remember: Good file management is like keeping your room organized - it takes a little effort every day, but it saves lots of time when you need to find something important!'''
            }
        ]
    }
    
    # Add notes for this topic if data exists
    if topic.title in study_notes_data:
        notes = study_notes_data[topic.title]
        for note_data in notes:
            # Get current max order for this topic
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
                print(f"  📝 Added note: {note_data['title']}")
            else:
                print(f"  📝 Note already exists: {note_data['title']}")

def add_quiz_questions_for_topic(topic):
    """Add comprehensive quiz questions for each topic"""

    questions_data = {
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
        ],

        'File Management and Organization': [
            {
                'question': 'What does the file extension .docx indicate?',
                'type': 'multiple_choice',
                'choices': ['A picture file', 'A Microsoft Word document', 'A music file', 'A video file'],
                'correct': 1,
                'explanation': '.docx is the file extension for Microsoft Word documents, commonly used for essays and reports.'
            },
            {
                'question': 'Which of these is the best way to name a school assignment file?',
                'type': 'multiple_choice',
                'choices': ['homework.docx', 'Math_Homework_Week5_2024.docx', 'untitled1.docx', 'new document.docx'],
                'correct': 1,
                'explanation': 'Good file names are specific and include the subject, assignment type, and date for easy identification.'
            },
            {
                'question': 'What is the difference between copying and moving a file?',
                'type': 'multiple_choice',
                'choices': ['No difference', 'Copying makes a duplicate, moving relocates the original', 'Moving makes a duplicate, copying relocates', 'Both delete the original file'],
                'correct': 1,
                'explanation': 'Copying creates a duplicate while keeping the original, moving relocates the file to a new location.'
            },
            {
                'question': 'Fill in the blank: A _____ file contains multiple files compressed together to save space.',
                'type': 'fill_blank',
                'correct': 'zip',
                'explanation': 'A ZIP file is a compressed folder that contains multiple files, making them smaller for easier sharing.'
            },
            {
                'question': 'True or False: It is important to backup your important files regularly.',
                'type': 'true_false',
                'correct': 'true',
                'explanation': 'Regular backups protect your important files from being lost due to computer problems or accidents.'
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

            print(f"  ❓ Added question: {q_data['question'][:50]}...")

if __name__ == '__main__':
    add_comprehensive_ict_content()
