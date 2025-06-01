#!/usr/bin/env python
"""
Script to populate Grade 5 ICT with comprehensive real-life content
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice
from users.models import User

def create_grade5_ict_content():
    """Create comprehensive Grade 5 ICT content"""
    print("🖥️ Creating Grade 5 ICT comprehensive content...")
    
    try:
        # Get ICT subject and Grade 5 level
        ict_subject = Subject.objects.get(name='ICT')
        grade5_ict = ClassLevel.objects.get(subject=ict_subject, level_number=5)
        print(f"✅ Found ICT Grade 5: {grade5_ict}")
    except:
        print("❌ ICT subject or Grade 5 level not found!")
        return False
    
    # Define comprehensive ICT topics for Grade 5
    topics_data = [
        {
            'title': 'Computer Basics and Parts',
            'description': 'Understanding computer components and how they work together',
            'order': 1
        },
        {
            'title': 'Operating Systems and Desktop',
            'description': 'Learning to navigate Windows, Mac, or Linux desktop environments',
            'order': 2
        },
        {
            'title': 'File Management and Organization',
            'description': 'Creating, saving, organizing, and finding files and folders',
            'order': 3
        },
        {
            'title': 'Word Processing and Documents',
            'description': 'Creating and formatting documents using word processors',
            'order': 4
        },
        {
            'title': 'Internet Safety and Digital Citizenship',
            'description': 'Safe and responsible use of the internet and digital tools',
            'order': 5
        },
        {
            'title': 'Web Browsing and Online Research',
            'description': 'Using web browsers to find reliable information online',
            'order': 6
        },
        {
            'title': 'Email and Digital Communication',
            'description': 'Sending emails and communicating safely online',
            'order': 7
        },
        {
            'title': 'Introduction to Programming Concepts',
            'description': 'Basic programming logic using visual tools like Scratch',
            'order': 8
        }
    ]
    
    # Create topics
    for topic_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            title=topic_data['title'],
            class_level=grade5_ict,
            defaults={
                'description': topic_data['description'],
                'order': topic_data['order'],
                'estimated_duration': 45,
                'difficulty_level': 'beginner',
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
    """Create comprehensive study notes for each ICT topic"""
    
    study_notes_data = {
        'Computer Basics and Parts': [
            {
                'title': 'Understanding Computer Components',
                'content': '''# Computer Basics and Parts

## What is a Computer?
A computer is an electronic device that processes information and helps us with many tasks like:
- Writing documents and letters
- Playing educational games
- Watching videos and listening to music
- Communicating with friends and family
- Learning new things online

## Main Parts of a Computer

### 1. **Monitor (Screen)**
- Shows us everything the computer is doing
- Like a TV screen but for computers
- Can be flat (LCD/LED) or curved
- **Real-life example**: Just like how you watch cartoons on TV, you see your work on the computer monitor

### 2. **Keyboard**
- Has letters, numbers, and special keys
- Used for typing words and commands
- **QWERTY layout** - named after the first 6 letters
- **Real-life example**: Like a typewriter but connected to a computer

### 3. **Mouse**
- Helps us point and click on things
- Has left and right buttons
- Some have a scroll wheel in the middle
- **Real-life example**: Like using your finger to point at things, but the mouse does it on screen

### 4. **CPU (Central Processing Unit)**
- The "brain" of the computer
- Processes all the information
- Usually inside the computer case
- **Real-life example**: Like your brain that thinks and makes decisions

### 5. **Memory (RAM)**
- Temporary storage for things the computer is working on
- More memory = computer works faster
- **Real-life example**: Like your desk where you keep books you're currently reading

### 6. **Storage (Hard Drive)**
- Permanent storage for files, photos, and programs
- Keeps information even when computer is turned off
- **Real-life example**: Like a filing cabinet where you store important papers

## Input and Output Devices

### Input Devices (Things that send information TO the computer):
- Keyboard - for typing
- Mouse - for pointing and clicking
- Microphone - for recording sound
- Camera - for taking pictures
- Scanner - for copying documents

### Output Devices (Things that show information FROM the computer):
- Monitor - shows pictures and text
- Speakers - play sounds and music
- Printer - prints documents on paper
- Headphones - for private listening

## Taking Care of Your Computer
1. **Keep it clean** - Dust the screen and keyboard regularly
2. **Handle with care** - Don't drop or hit the computer
3. **Proper shutdown** - Always turn off properly, don't just unplug
4. **Avoid food and drinks** - Keep them away from the computer
5. **Use surge protectors** - Protect from power surges

## Fun Facts About Computers
- The first computer was as big as a room!
- Modern smartphones are more powerful than computers from 30 years ago
- The word "computer" originally meant a person who did calculations
- The first computer mouse was made of wood!

Remember: Computers are tools that help us learn, create, and communicate. The more you practice, the better you'll become at using them!'''
            }
        ],
        
        'Operating Systems and Desktop': [
            {
                'title': 'Navigating Your Computer Desktop',
                'content': '''# Operating Systems and Desktop

## What is an Operating System?
An operating system (OS) is like the manager of your computer. It helps all the parts work together and lets you use different programs.

## Common Operating Systems
1. **Windows** - Made by Microsoft (most common)
2. **macOS** - Made by Apple (for Mac computers)
3. **Linux** - Free and open-source
4. **Chrome OS** - Made by Google (for Chromebooks)

## Understanding the Desktop

### Desktop Elements:
- **Wallpaper/Background** - The picture you see behind everything
- **Icons** - Small pictures that represent programs or files
- **Taskbar/Dock** - Bar at bottom (Windows) or side (Mac) showing open programs
- **Start Menu** - Access to all programs and settings (Windows)
- **Recycle Bin/Trash** - Where deleted files go temporarily

### Desktop Icons:
- **My Computer/This PC** - Access to all drives and folders
- **Documents** - Where you save your work
- **Pictures** - Where photos are stored
- **Music** - Where audio files are kept
- **Videos** - Where video files are stored

## Using the Start Menu (Windows)
1. Click the **Start button** (Windows logo)
2. See recently used programs
3. Access **All Programs** to find any software
4. Use **Search** to quickly find files or programs
5. Access **Settings** to change computer preferences

## Working with Windows
- **Opening a window** - Double-click an icon or program
- **Moving a window** - Click and drag the title bar
- **Resizing a window** - Drag the corners or edges
- **Minimizing** - Click the minus (-) button to hide
- **Maximizing** - Click the square button to make full screen
- **Closing** - Click the X button to close completely

## Real-Life Desktop Organization Tips
1. **Keep it clean** - Don't put too many icons on desktop
2. **Group similar items** - Put related programs together
3. **Use folders** - Organize files like you organize your room
4. **Regular cleanup** - Delete shortcuts you don't use

## Practice Activities
1. **Change your wallpaper** - Right-click desktop → Personalize
2. **Arrange icons** - Drag them to organize
3. **Open multiple windows** - Practice switching between them
4. **Use the search function** - Find a program or file

## Keyboard Shortcuts (Time-savers!)
- **Ctrl + C** - Copy
- **Ctrl + V** - Paste
- **Ctrl + Z** - Undo
- **Alt + Tab** - Switch between open programs
- **Windows Key** - Open Start Menu

Remember: Your desktop is like your workspace. Keep it organized and you'll work more efficiently!'''
            }
        ],

        'File Management and Organization': [
            {
                'title': 'Creating and Organizing Files and Folders',
                'content': '''# File Management and Organization

## What are Files and Folders?

### Files
- **Documents** you create (like a school report)
- **Pictures** you take or download
- **Music** files you listen to
- **Videos** you watch
- **Programs** that run on your computer

### Folders
- **Containers** that hold files
- Like **digital filing cabinets**
- Help keep your computer organized
- Can contain other folders too!

## Real-Life Example
Think of your computer like your bedroom:
- **Files** = Individual items (books, toys, clothes)
- **Folders** = Storage containers (drawers, boxes, shelves)
- **Desktop** = Your desk surface
- **Recycle Bin** = Trash can

## Creating Files and Folders

### Creating a New Folder:
1. **Right-click** on empty space
2. Select **"New"** → **"Folder"**
3. **Type a name** for your folder
4. Press **Enter**

### Creating a New File:
1. **Right-click** on empty space
2. Select **"New"** → Choose file type (Document, Text file, etc.)
3. **Name your file**
4. Press **Enter**

## File Naming Best Practices
1. **Use clear names** - "Math Homework Week 1" not "homework"
2. **No special characters** - Avoid / \\ : * ? " < > |
3. **Use spaces or underscores** - "My_Project" or "My Project"
4. **Include dates** - "Science Report 2024-03-15"
5. **Keep it short** - Under 255 characters

## Organizing Your Files

### Create a Folder Structure:
```
Documents/
├── School Work/
│   ├── Math/
│   ├── Science/
│   ├── English/
│   └── ICT/
├── Personal/
│   ├── Pictures/
│   ├── Music/
│   └── Games/
└── Projects/
    ├── Art Projects/
    └── Science Fair/
```

## File Operations

### Copying Files:
1. **Right-click** the file
2. Select **"Copy"**
3. Go to destination folder
4. **Right-click** and select **"Paste"**

### Moving Files:
1. **Right-click** the file
2. Select **"Cut"**
3. Go to destination folder
4. **Right-click** and select **"Paste"**

### Deleting Files:
1. **Right-click** the file
2. Select **"Delete"**
3. File goes to **Recycle Bin**
4. **Empty Recycle Bin** to permanently delete

## Finding Lost Files

### Using Search:
1. Click **Start Menu**
2. Type the **file name**
3. Look through **search results**

### Check Common Locations:
- **Desktop** - Files saved to desktop
- **Documents** - Default save location
- **Downloads** - Files from internet
- **Recent Files** - Recently opened files

## File Extensions (File Types)
- **.txt** - Text files
- **.doc/.docx** - Word documents
- **.jpg/.png** - Picture files
- **.mp3** - Music files
- **.mp4** - Video files
- **.pdf** - PDF documents

## Safety Tips
1. **Regular backups** - Copy important files to USB or cloud
2. **Don't delete system files** - Only delete files you created
3. **Check before deleting** - Make sure you don't need the file
4. **Use antivirus** - Protect against harmful files

## Practice Exercise
Create this folder structure on your computer:
```
My School Work/
├── Grade 5/
│   ├── Math/
│   ├── Science/
│   ├── English/
│   ├── ICT/
│   └── Art/
└── Projects/
    ├── Current/
    └── Completed/
```

Remember: Good file organization saves time and prevents lost work!'''
            }
        ]
    }
    
    # Get the notes for this topic
    if topic.title in study_notes_data:
        notes = study_notes_data[topic.title]
        for note_data in notes:
            StudyNote.objects.get_or_create(
                topic=topic,
                title=note_data['title'],
                defaults={
                    'content': note_data['content'],
                    'order': 1
                }
            )
            print(f"  📝 Added note: {note_data['title']}")

def create_quiz_questions(topic):
    """Create realistic quiz questions for each ICT topic"""
    
    questions_data = {
        'Computer Basics and Parts': [
            {
                'question': 'Which part of the computer is called the "brain" because it processes all information?',
                'type': 'multiple_choice',
                'choices': ['Monitor', 'CPU (Central Processing Unit)', 'Keyboard', 'Mouse'],
                'correct': 1,
                'explanation': 'The CPU (Central Processing Unit) is called the brain of the computer because it processes all the information and instructions.'
            },
            {
                'question': 'What is the main purpose of a computer monitor?',
                'type': 'multiple_choice',
                'choices': ['To type letters', 'To store files', 'To display information on screen', 'To connect to internet'],
                'correct': 2,
                'explanation': 'A monitor displays visual information from the computer, showing text, images, and videos on screen.'
            },
            {
                'question': 'Which device would you use to type a letter to your friend?',
                'type': 'multiple_choice',
                'choices': ['Mouse', 'Monitor', 'Keyboard', 'Speakers'],
                'correct': 2,
                'explanation': 'A keyboard is used for typing letters, numbers, and symbols to create documents and messages.'
            },
            {
                'question': 'Sarah wants to listen to music on her computer without disturbing others. Which output device should she use?',
                'type': 'multiple_choice',
                'choices': ['Speakers', 'Headphones', 'Monitor', 'Printer'],
                'correct': 1,
                'explanation': 'Headphones allow private listening without disturbing others around you.'
            },
            {
                'question': 'What is the difference between RAM (memory) and storage (hard drive)?',
                'type': 'multiple_choice',
                'choices': ['RAM is permanent, storage is temporary', 'RAM is temporary, storage is permanent', 'They are the same thing', 'RAM is only for games'],
                'correct': 1,
                'explanation': 'RAM is temporary memory that loses data when the computer is turned off, while storage (hard drive) keeps data permanently.'
            },
            {
                'question': 'Which of these is an input device that helps you point and click on things on the screen?',
                'type': 'multiple_choice',
                'choices': ['Printer', 'Mouse', 'Speakers', 'Monitor'],
                'correct': 1,
                'explanation': 'A mouse is an input device that allows you to point, click, and select items on the computer screen.'
            },
            {
                'question': 'Tom wants to print his homework. Which type of device is a printer?',
                'type': 'multiple_choice',
                'choices': ['Input device', 'Output device', 'Storage device', 'Processing device'],
                'correct': 1,
                'explanation': 'A printer is an output device because it takes information from the computer and outputs it onto paper.'
            },
            {
                'question': 'What should you do to take good care of your computer?',
                'type': 'multiple_choice',
                'choices': ['Keep food and drinks nearby', 'Never turn it off', 'Keep it clean and dust-free', 'Hit it when it\'s slow'],
                'correct': 2,
                'explanation': 'Keeping your computer clean and dust-free helps it work properly and last longer.'
            },
            {
                'question': 'Which part of the computer stores your files, photos, and programs permanently?',
                'type': 'multiple_choice',
                'choices': ['RAM', 'Monitor', 'Hard Drive/Storage', 'Keyboard'],
                'correct': 2,
                'explanation': 'The hard drive or storage device keeps your files, photos, and programs permanently, even when the computer is turned off.'
            },
            {
                'question': 'If you want to take a photo with your computer, which input device would you use?',
                'type': 'multiple_choice',
                'choices': ['Microphone', 'Camera/Webcam', 'Speakers', 'Printer'],
                'correct': 1,
                'explanation': 'A camera or webcam is an input device that captures images and videos for the computer.'
            }
        ],

        'Operating Systems and Desktop': [
            {
                'question': 'What is an operating system?',
                'type': 'multiple_choice',
                'choices': ['A computer game', 'Software that manages the computer', 'A type of keyboard', 'A computer virus'],
                'correct': 1,
                'explanation': 'An operating system is software that manages all the computer\'s hardware and software, acting like the computer\'s manager.'
            },
            {
                'question': 'Which of these is a popular operating system made by Microsoft?',
                'type': 'multiple_choice',
                'choices': ['macOS', 'Linux', 'Windows', 'Android'],
                'correct': 2,
                'explanation': 'Windows is the operating system created by Microsoft and is used on many computers worldwide.'
            },
            {
                'question': 'Where do deleted files go when you delete them on Windows?',
                'type': 'multiple_choice',
                'choices': ['They disappear forever', 'Recycle Bin', 'Start Menu', 'Desktop'],
                'correct': 1,
                'explanation': 'Deleted files go to the Recycle Bin first, where they can be restored if needed before being permanently deleted.'
            },
            {
                'question': 'What keyboard shortcut can you use to copy something?',
                'type': 'multiple_choice',
                'choices': ['Ctrl + V', 'Ctrl + C', 'Ctrl + Z', 'Ctrl + X'],
                'correct': 1,
                'explanation': 'Ctrl + C is the keyboard shortcut for copying text, files, or other items.'
            },
            {
                'question': 'Lisa wants to switch between two open programs quickly. Which keyboard shortcut should she use?',
                'type': 'multiple_choice',
                'choices': ['Ctrl + C', 'Alt + Tab', 'Ctrl + V', 'Windows Key'],
                'correct': 1,
                'explanation': 'Alt + Tab allows you to quickly switch between open programs and windows.'
            }
        ],

        'File Management and Organization': [
            {
                'question': 'What is a folder?',
                'type': 'multiple_choice',
                'choices': ['A type of file', 'A container that holds files', 'A computer program', 'A keyboard key'],
                'correct': 1,
                'explanation': 'A folder is a container that holds and organizes files, similar to a physical folder that holds papers.'
            },
            {
                'question': 'Which file extension indicates a picture file?',
                'type': 'multiple_choice',
                'choices': ['.txt', '.jpg', '.mp3', '.doc'],
                'correct': 1,
                'explanation': '.jpg is a common file extension for picture/image files.'
            },
            {
                'question': 'What is the best way to name your school files?',
                'type': 'multiple_choice',
                'choices': ['Use random letters', 'Use clear, descriptive names', 'Use only numbers', 'Don\'t name them'],
                'correct': 1,
                'explanation': 'Using clear, descriptive names helps you find and organize your files easily.'
            },
            {
                'question': 'How do you create a new folder?',
                'type': 'multiple_choice',
                'choices': ['Double-click on desktop', 'Right-click and select New → Folder', 'Press Enter', 'Click the Start button'],
                'correct': 1,
                'explanation': 'Right-clicking and selecting New → Folder is the standard way to create a new folder.'
            },
            {
                'question': 'What should you do before deleting an important file?',
                'type': 'multiple_choice',
                'choices': ['Delete it immediately', 'Make sure you don\'t need it anymore', 'Rename it first', 'Move it to desktop'],
                'correct': 1,
                'explanation': 'Always make sure you don\'t need a file anymore before deleting it to avoid losing important work.'
            }
        ]
    }
    
    # Create questions for this topic
    if topic.title in questions_data:
        questions = questions_data[topic.title]
        for i, q_data in enumerate(questions):
            question = Question.objects.create(
                topic=topic,
                question_text=q_data['question'],
                question_type=q_data['type'],
                difficulty='easy',
                points=10,
                order=i + 1,
                explanation=q_data.get('explanation', ''),
                is_active=True
            )
            
            # Create answer choices
            for j, choice_text in enumerate(q_data['choices']):
                AnswerChoice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=(j == q_data['correct']),
                    order=j + 1
                )
            
            print(f"  ❓ Added question: {q_data['question'][:50]}...")

if __name__ == '__main__':
    create_grade5_ict_content()
    print("🎉 Grade 5 ICT content creation completed!")
