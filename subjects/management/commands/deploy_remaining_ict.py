from django.core.management.base import BaseCommand
from django.db import models
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice


class Command(BaseCommand):
    help = 'Deploy remaining Grade 5 ICT content (Word Processing and Internet Safety)'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Deploying remaining Grade 5 ICT content...")
        
        try:
            # Get ICT subject and Grade 5 level
            ict_subject = Subject.objects.get(name='ICT')
            grade5_ict = ClassLevel.objects.get(subject=ict_subject, level_number=5)
            self.stdout.write(f"✅ Found ICT Grade 5: {grade5_ict}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ ICT subject or Grade 5 level not found: {e}"))
            return
        
        # Deploy content for specific topics
        topic_names = ['Word Processing and Documents', 'Internet Safety and Digital Citizenship']
        
        for topic_name in topic_names:
            try:
                topic = Topic.objects.get(title=topic_name, class_level=grade5_ict)
                self.stdout.write(f"\n📚 Deploying content for: {topic.title}")
                self.add_study_notes(topic)
                self.add_quiz_questions(topic)
            except Topic.DoesNotExist:
                self.stdout.write(f"⚠️ Topic not found: {topic_name}")
        
        # Final status
        self.print_final_status(grade5_ict)
        self.stdout.write(self.style.SUCCESS("\n🎉 Remaining Grade 5 ICT content deployment completed!"))

    def add_study_notes(self, topic):
        """Add study notes for each topic"""
        
        notes_data = {
            'Word Processing and Documents': {
                'title': 'Creating and Formatting Documents',
                'content': '''# Word Processing and Documents

## What is Word Processing?

Word processing is like having a super-smart typewriter that can help you write, edit, and make your documents look professional. Instead of using pen and paper, you type on a computer and can easily make changes without starting over!

### Popular Word Processing Programs:
- **Microsoft Word** - Most common, used in schools and offices
- **Google Docs** - Works in web browsers, great for sharing
- **LibreOffice Writer** - Free alternative to Microsoft Word
- **Apple Pages** - For Mac computers

## Getting Started with Documents

### Creating a New Document:
1. **Open your word processor** (like Microsoft Word)
2. **Choose "New Document"** or "Blank Document"
3. **Start typing!** The cursor shows where your text will appear
4. **Save your work** regularly (Ctrl + S)

### Real-Life Example:
Think of creating a document like writing a letter to your friend, but instead of using paper and pen, you're using a computer that can help you:
- Fix spelling mistakes automatically
- Change the size and style of your writing
- Add pictures and colors
- Print multiple copies easily

## Basic Text Formatting

### Changing Text Appearance:

#### **Font (Text Style):**
- **Arial** - Clean and easy to read
- **Times New Roman** - Traditional, good for school reports
- **Comic Sans** - Fun and casual
- **Calibri** - Modern default font

#### **Font Size:**
- **12 point** - Standard size for most documents
- **14-16 point** - Good for titles
- **10-11 point** - Smaller text for footnotes
- **18+ point** - Large text for posters

#### **Text Effects:**
- **Bold** (Ctrl + B) - Makes text darker and thicker
- **Italic** (Ctrl + I) - Slants text to the right
- **Underline** (Ctrl + U) - Draws a line under text
- **Color** - Changes text color for emphasis

### When to Use Different Formatting:
- **Bold** - For headings and important words
- **Italic** - For book titles or emphasis
- **Underline** - For links or special terms
- **Larger fonts** - For titles and headings

## Essential Word Processing Skills

### Text Selection and Editing:

#### **Selecting Text:**
- **Click and drag** - Select specific words or sentences
- **Double-click** - Select a whole word
- **Triple-click** - Select a whole paragraph
- **Ctrl + A** - Select all text in the document

#### **Copy, Cut, and Paste:**
- **Copy (Ctrl + C)** - Make a duplicate to use elsewhere
- **Cut (Ctrl + X)** - Remove text but keep it to paste elsewhere
- **Paste (Ctrl + V)** - Put copied or cut text in a new location

#### **Undo and Redo:**
- **Undo (Ctrl + Z)** - Take back the last thing you did
- **Redo (Ctrl + Y)** - Put back what you just undid

### Find and Replace:
- **Find (Ctrl + F)** - Search for specific words in your document
- **Replace (Ctrl + H)** - Change all instances of one word to another
- **Example**: Change "color" to "colour" throughout your document

## Saving and File Management

### Saving Your Work:

#### **Save (Ctrl + S):**
- **Save frequently** - Every few minutes
- **Choose a clear filename** - "Science_Report_Volcanoes_2024.docx"
- **Pick the right location** - Documents folder, USB drive, etc.

#### **Save As:**
- **Create a copy** with a different name
- **Change file format** (Word to PDF, etc.)
- **Save to a different location**

### File Formats:
- **.docx** - Microsoft Word format (most common)
- **.pdf** - Can't be easily edited, good for sharing final versions
- **.txt** - Plain text, no formatting
- **.rtf** - Rich text format, works with many programs

Remember: Word processing is a skill that improves with practice. Start with simple documents and gradually try more advanced features. Don't be afraid to experiment - you can always undo changes or start over!'''
            },
            
            'Internet Safety and Digital Citizenship': {
                'title': 'Staying Safe Online and Being a Good Digital Citizen',
                'content': '''# Staying Safe Online and Being a Good Digital Citizen

## What is Digital Citizenship?

Digital citizenship means being a responsible, respectful, and safe person when using technology and the internet. Just like being a good citizen in your community, being a good digital citizen means following rules and treating others well online.

### The Golden Rule Online:
**Treat others online the same way you want to be treated in real life.**

## Internet Safety Basics

### Personal Information - Keep It Private!

#### **Never Share These Online:**
- **Full name** - Use only your first name or a nickname
- **Home address** - This tells strangers where you live
- **Phone number** - Only family should have this
- **School name** - This helps strangers find you
- **Passwords** - Never tell anyone except parents/guardians
- **Photos of yourself** - Ask an adult before posting pictures

#### **Why Keep Information Private?**
- **Strangers might try to find you** - Not everyone online is friendly
- **Identity theft** - Bad people can pretend to be you
- **Cyberbullying** - People might use your information to hurt you
- **Family safety** - Protecting your information protects your family too

### Password Safety

#### **Creating Strong Passwords:**
- **Use 8+ characters** - Longer is stronger
- **Mix letters, numbers, symbols** - Like "MyDog123!"
- **Don't use personal info** - No birthdays or pet names
- **Make it memorable** - Use a sentence like "I love pizza 2 much!"

#### **Password Rules:**
- **Different passwords for different sites** - Don't reuse passwords
- **Never share passwords** - Except with parents/guardians
- **Change passwords if compromised** - If someone else knows it
- **Use password managers** - Let adults help you set this up

### Recognizing Online Dangers

#### **Cyberbullying - When People Are Mean Online:**

**What it looks like:**
- Mean messages or comments
- Sharing embarrassing photos without permission
- Excluding someone from online groups on purpose
- Spreading rumors or lies about someone

**What to do:**
1. **Don't respond** - Don't fight back with mean messages
2. **Save evidence** - Take screenshots of mean messages
3. **Block the person** - Most sites let you block bullies
4. **Tell a trusted adult** - Parents, teachers, or school counselors
5. **Report to the website** - Most sites have report buttons

#### **Online Predators - Dangerous Strangers:**

**Warning signs:**
- Asking for personal information
- Wanting to meet in person
- Asking you to keep secrets from parents
- Sending inappropriate pictures or messages
- Offering gifts or money

**What to do:**
1. **Never meet online friends in person** - Without parent permission
2. **Tell an adult immediately** - If someone makes you uncomfortable
3. **Don't accept gifts** - From people you only know online
4. **Trust your feelings** - If something feels wrong, it probably is

## Being Respectful Online

### Digital Etiquette (Good Online Manners)

#### **In Messages and Comments:**
- **Use kind words** - Be polite and friendly
- **Think before you type** - Would you say this in person?
- **Use proper spelling** - Show respect by writing clearly
- **Don't type in ALL CAPS** - It looks like you're shouting
- **Respect different opinions** - It's okay to disagree nicely

#### **When Sharing Content:**
- **Give credit** - Say where you found pictures or information
- **Ask permission** - Before sharing someone else's photos or work
- **Check facts** - Don't spread false information
- **Respect privacy** - Don't share other people's personal information

Remember: The internet is an amazing tool for learning, creating, and connecting with others. By being safe, respectful, and kind online, you help make the internet a better place for everyone!'''
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
            'Word Processing and Documents': [
                {
                    'question': 'Which keyboard shortcut is used to save your document?',
                    'type': 'multiple_choice',
                    'choices': ['Ctrl + C', 'Ctrl + S', 'Ctrl + P', 'Ctrl + V'],
                    'correct': 1,
                    'explanation': 'Ctrl + S is the keyboard shortcut to save your document. You should save frequently to avoid losing your work.'
                },
                {
                    'question': 'What does the Bold formatting do to text?',
                    'type': 'multiple_choice',
                    'choices': ['Makes text slanted', 'Makes text darker and thicker', 'Draws a line under text', 'Changes text color'],
                    'correct': 1,
                    'explanation': 'Bold formatting makes text darker and thicker, which helps emphasize important words or headings.'
                },
                {
                    'question': 'Emma is writing a school report. What font size should she use for the main body text?',
                    'type': 'multiple_choice',
                    'choices': ['8 point', '12 point', '18 point', '24 point'],
                    'correct': 1,
                    'explanation': '12 point is the standard font size for body text in most documents, making it easy to read.'
                },
                {
                    'question': 'Fill in the blank: To undo the last action you performed, press _____ + Z.',
                    'type': 'fill_blank',
                    'correct': 'Ctrl',
                    'explanation': 'Ctrl + Z is the keyboard shortcut to undo the last action you performed in most programs.'
                },
                {
                    'question': 'True or False: You should only save your document when you are completely finished writing.',
                    'type': 'true_false',
                    'correct': 'false',
                    'explanation': 'False! You should save your document frequently (every few minutes) to avoid losing your work if something goes wrong.'
                }
            ],
            
            'Internet Safety and Digital Citizenship': [
                {
                    'question': 'Which of these should you NEVER share online?',
                    'type': 'multiple_choice',
                    'choices': ['Your favorite color', 'Your home address', 'Your favorite book', 'Your hobby'],
                    'correct': 1,
                    'explanation': 'You should never share your home address online because it tells strangers where you live, which is dangerous.'
                },
                {
                    'question': 'What should you do if someone online asks to meet you in person?',
                    'type': 'multiple_choice',
                    'choices': ['Meet them right away', 'Ask your parents first', 'Give them your address', 'Share your phone number'],
                    'correct': 1,
                    'explanation': 'You should always ask your parents or guardians before meeting anyone you only know from online.'
                },
                {
                    'question': 'Tom receives a mean message online. What should he do first?',
                    'type': 'multiple_choice',
                    'choices': ['Send a mean message back', 'Tell a trusted adult', 'Share it with friends', 'Ignore it completely'],
                    'correct': 1,
                    'explanation': 'When experiencing cyberbullying, the first step is to tell a trusted adult who can help handle the situation properly.'
                },
                {
                    'question': 'Fill in the blank: A strong password should have at least _____ characters.',
                    'type': 'fill_blank',
                    'correct': '8',
                    'explanation': 'Strong passwords should have at least 8 characters and include a mix of letters, numbers, and symbols.'
                },
                {
                    'question': 'True or False: It is okay to use the same password for all your online accounts.',
                    'type': 'true_false',
                    'correct': 'false',
                    'explanation': 'False! You should use different passwords for different accounts to keep them more secure.'
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
