from django.core.management.base import BaseCommand
from django.db import models
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Add comprehensive content to remaining Grade 5 ICT topics'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Expanding Grade 5 ICT content...")
        
        try:
            # Get ICT subject and Grade 5 level
            ict_subject = Subject.objects.get(name='ICT')
            grade5_ict = ClassLevel.objects.get(subject=ict_subject, level_number=5)
            self.stdout.write(f"✅ Found ICT Grade 5: {grade5_ict}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ ICT subject or Grade 5 level not found: {e}"))
            return
        
        # Target topics that need content
        target_topics = [
            'File Management and Organization',
            'Web Browsing and Online Research',
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
        self.stdout.write(self.style.SUCCESS("\n🎉 Grade 5 ICT expansion completed!"))

    def add_study_notes(self, topic):
        """Add comprehensive study notes for each topic"""
        
        notes_data = {
            'File Management and Organization': {
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
            },
            
            'Web Browsing and Online Research': {
                'title': 'Safe and Effective Web Browsing',
                'content': '''# Safe and Effective Web Browsing

## Understanding Web Browsers

### What is a Web Browser?
A web browser is like a window to the internet. It's a program that lets you visit websites, watch videos, read articles, and explore the online world safely.

### Popular Web Browsers:
- **Google Chrome** - Most popular, fast and user-friendly
- **Mozilla Firefox** - Good privacy features
- **Microsoft Edge** - Built into Windows computers
- **Safari** - Default browser on Apple devices
- **Opera** - Has built-in features like VPN

### Parts of a Web Browser:

#### **Address Bar (URL Bar):**
- **What it is**: The box at the top where you type website addresses
- **Example**: www.google.com or www.nationalgeographic.com
- **Tip**: You can also search directly from here

#### **Tabs:**
- **What they do**: Let you have multiple websites open at once
- **How to use**: Click the "+" to open a new tab
- **Keyboard shortcut**: Ctrl + T for new tab

#### **Back and Forward Buttons:**
- **Back (←)**: Go to the previous page you visited
- **Forward (→)**: Go forward if you've gone back
- **Keyboard shortcut**: Alt + ← (back), Alt + → (forward)

#### **Refresh Button:**
- **What it does**: Reloads the current page
- **When to use**: If a page isn't loading properly
- **Keyboard shortcut**: F5 or Ctrl + R

#### **Bookmarks:**
- **What they are**: Saved links to your favorite websites
- **How to create**: Click the star icon in the address bar
- **Why useful**: Quick access to sites you visit often

## Safe Browsing Practices

### Recognizing Safe Websites:

#### **Look for HTTPS:**
- **What it means**: The "S" stands for "Secure"
- **How to check**: Look for "https://" at the beginning of the web address
- **Visual cue**: Many browsers show a lock icon 🔒
- **Why important**: Your information is protected

#### **Check the Web Address:**
- **Spelling matters**: Make sure the website name is spelled correctly
- **Be careful of**: Sites that look similar to real ones but have small differences
- **Example**: "gooogle.com" instead of "google.com"

#### **Trust Indicators:**
- **Professional appearance**: Real websites look well-designed
- **Contact information**: Legitimate sites have "About Us" and contact details
- **No excessive pop-ups**: Good sites don't bombard you with ads

### Avoiding Dangerous Content:

#### **Red Flags to Watch For:**
- **Pop-ups that won't close** - Don't click on them
- **"You've won a prize!"** - Usually fake
- **Requests for personal information** - Never give out private details
- **Download prompts** - Only download from trusted sources
- **Scary warnings** - "Your computer is infected!" (usually fake)

#### **What to Do if You See Something Inappropriate:**
1. **Close the page immediately** - Don't keep looking
2. **Tell a trusted adult** - Parent, teacher, or guardian
3. **Don't click on anything** - Just close the browser tab
4. **It's not your fault** - Sometimes bad content appears accidentally

## Effective Online Research

### Planning Your Research:

#### **Before You Start:**
1. **Know what you're looking for** - Write down your research question
2. **Think of keywords** - What words describe your topic?
3. **Set a time limit** - Don't get distracted by other interesting things
4. **Have a plan** - What information do you need to find?

#### **Example Research Plan:**
- **Topic**: Volcanoes
- **Keywords**: volcano, eruption, lava, magma, types of volcanoes
- **Questions**: How do volcanoes form? What are different types? Where are they found?
- **Time limit**: 30 minutes

### Using Search Engines Effectively:

#### **Google Search Tips:**
- **Use specific keywords**: "types of volcanoes" instead of just "volcanoes"
- **Use quotes for exact phrases**: "how volcanoes form"
- **Add more words to narrow results**: "volcanoes for kids" or "volcano facts grade 5"
- **Use the minus sign to exclude**: "volcanoes -video" (if you don't want videos)

#### **Advanced Search Features:**
- **Image search**: Click "Images" to find pictures
- **News search**: Click "News" for recent articles
- **Time filters**: Click "Tools" → "Any time" to find recent information
- **Safe search**: Should be turned on to filter inappropriate content

### Evaluating Information Quality:

#### **Good Sources vs. Bad Sources:**

**Good Sources:**
- **Educational websites**: .edu domains (universities, schools)
- **Government sites**: .gov domains (official information)
- **Established organizations**: National Geographic, Smithsonian, BBC
- **Recent information**: Check the date it was published
- **Author information**: Shows who wrote the content

**Be Careful Of:**
- **Wikipedia**: Good starting point, but verify information elsewhere
- **Blogs**: Personal opinions, may not be factual
- **Old information**: Science and technology change quickly
- **Biased sources**: Sites trying to sell something or promote one viewpoint
- **No author listed**: Who wrote this? Are they qualified?

#### **The CRAAP Test for Websites:**
- **C**urrency: Is the information recent?
- **R**elevance: Does it answer your question?
- **A**uthority: Who wrote it? Are they an expert?
- **A**ccuracy: Can you verify the information elsewhere?
- **P**urpose: Why was this written? To inform, sell, or persuade?

### Organizing Your Research:

#### **Taking Notes:**
- **Write in your own words** - Don't just copy and paste
- **Note the source** - Write down where you found the information
- **Use bullet points** - Easier to read and organize
- **Ask questions** - What else do you want to know?

#### **Keeping Track of Sources:**
- **Bookmark useful sites** - Save them for later reference
- **Write down website names** - You might need to cite them
- **Take screenshots** - Of important diagrams or charts
- **Print important pages** - If you need them offline

## Browser Tools and Features

### Useful Browser Features:

#### **History:**
- **What it is**: A list of websites you've visited
- **How to access**: Ctrl + H
- **Why useful**: Find a site you visited but forgot to bookmark

#### **Downloads:**
- **What it shows**: Files you've downloaded from the internet
- **How to access**: Ctrl + J
- **Safety tip**: Only download files from trusted sources

#### **Zoom:**
- **Make text bigger**: Ctrl + Plus (+)
- **Make text smaller**: Ctrl + Minus (-)
- **Reset to normal**: Ctrl + 0
- **Why useful**: Easier reading for different screen sizes

#### **Find on Page:**
- **How to use**: Ctrl + F
- **What it does**: Searches for specific words on the current page
- **Why helpful**: Quickly find information on long pages

### Managing Tabs and Windows:

#### **Tab Management:**
- **New tab**: Ctrl + T
- **Close tab**: Ctrl + W
- **Reopen closed tab**: Ctrl + Shift + T
- **Switch between tabs**: Ctrl + Tab

#### **Window Management:**
- **New window**: Ctrl + N
- **Close window**: Alt + F4
- **Switch between windows**: Alt + Tab

## Research Project Example

### Step-by-Step Research Process:

#### **Topic**: "Animals of the Rainforest"

1. **Plan** (5 minutes):
   - What animals live in rainforests?
   - What do they eat?
   - How do they survive?
   - Keywords: rainforest animals, tropical animals, Amazon animals

2. **Search** (15 minutes):
   - Start with: "rainforest animals for kids"
   - Visit: National Geographic Kids, World Wildlife Fund
   - Look for: Pictures, facts, habitat information

3. **Evaluate** (5 minutes):
   - Check: Are these educational sites?
   - Verify: Do multiple sources say the same thing?
   - Note: When was this information published?

4. **Organize** (10 minutes):
   - Create: A simple outline
   - List: 5-10 interesting animals
   - Note: One fact about each animal
   - Save: Bookmark useful websites

5. **Review** (5 minutes):
   - Check: Do I have enough information?
   - Ask: What questions do I still have?
   - Plan: What should I research next?

Remember: The internet is full of amazing information, but it's important to be safe, smart, and critical about what you find. Always verify important information with multiple sources, and don't hesitate to ask for help when you need it!'''
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
            ],
            
            'Web Browsing and Online Research': [
                {
                    'question': 'What does "https://" at the beginning of a web address indicate?',
                    'type': 'multiple_choice',
                    'choices': ['The website is fast', 'The website is secure', 'The website is popular', 'The website is free'],
                    'correct': 1,
                    'explanation': 'HTTPS means the website is secure and your information is protected when you visit it.'
                },
                {
                    'question': 'Which keyboard shortcut opens a new tab in your web browser?',
                    'type': 'multiple_choice',
                    'choices': ['Ctrl + N', 'Ctrl + T', 'Ctrl + W', 'Ctrl + R'],
                    'correct': 1,
                    'explanation': 'Ctrl + T opens a new tab in your web browser, allowing you to visit multiple websites.'
                },
                {
                    'question': 'When doing online research, which type of website is generally most reliable?',
                    'type': 'multiple_choice',
                    'choices': ['Personal blogs', 'Educational websites (.edu)', 'Social media posts', 'Advertisement sites'],
                    'correct': 1,
                    'explanation': 'Educational websites (.edu) are generally more reliable because they are created by schools and universities.'
                },
                {
                    'question': 'Fill in the blank: When you want to search for an exact phrase, put it in _____.',
                    'type': 'fill_blank',
                    'correct': 'quotes',
                    'explanation': 'Using quotes around a phrase tells the search engine to look for those exact words in that exact order.'
                },
                {
                    'question': 'True or False: You should always verify important information by checking multiple sources.',
                    'type': 'true_false',
                    'correct': 'true',
                    'explanation': 'True! Checking multiple sources helps ensure the information is accurate and reliable.'
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
        self.stdout.write("\n=== UPDATED GRADE 5 ICT STATUS ===")
        for topic in Topic.objects.filter(class_level=grade5_ict).order_by('order'):
            notes_count = StudyNote.objects.filter(topic=topic).count()
            questions_count = Question.objects.filter(topic=topic).count()
            self.stdout.write(f"{topic.title}: {notes_count} notes, {questions_count} questions")
        
        total_notes = StudyNote.objects.filter(topic__class_level=grade5_ict).count()
        total_questions = Question.objects.filter(topic__class_level=grade5_ict).count()
        self.stdout.write(f"\nTOTAL: {total_notes} notes, {total_questions} questions")
