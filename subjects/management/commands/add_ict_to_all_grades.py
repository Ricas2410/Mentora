from django.core.management.base import BaseCommand
from django.db import models
from subjects.models import Subject, ClassLevel, Topic


class Command(BaseCommand):
    help = 'Add ICT subject to all grades (1-12) with appropriate topics'

    def handle(self, *args, **options):
        self.stdout.write("🖥️ Adding ICT subject to all grades...")
        
        # Create or get ICT subject
        ict_subject, created = Subject.objects.get_or_create(
            name='ICT',
            defaults={
                'description': 'Information and Communication Technology - Digital literacy, computer skills, and technology education',
                'icon': '💻',
                'color': '#6366F1',
                'order': 6,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(f"✅ Created ICT subject")
        else:
            self.stdout.write(f"📝 ICT subject already exists")
        
        # Create class levels for all grades
        self.create_ict_class_levels(ict_subject)
        
        # Create topics for each grade
        self.create_ict_topics_for_all_grades(ict_subject)
        
        self.stdout.write(self.style.SUCCESS("🎉 ICT subject added to all grades successfully!"))

    def create_ict_class_levels(self, ict_subject):
        """Create ICT class levels for grades 1-12"""
        self.stdout.write("📚 Creating ICT class levels for all grades...")
        
        # Define education levels with appropriate pass percentages
        grade_configs = [
            # Elementary School (Grades 1-6)
            {'grades': range(1, 7), 'level_type': 'Elementary', 'age_range': '6-12 years', 'pass_percentage': 60},
            # Middle School (Grades 7-9)
            {'grades': range(7, 10), 'level_type': 'Middle School', 'age_range': '12-15 years', 'pass_percentage': 70},
            # High School (Grades 10-12)
            {'grades': range(10, 13), 'level_type': 'High School', 'age_range': '15-18 years', 'pass_percentage': 75}
        ]
        
        for config in grade_configs:
            for grade in config['grades']:
                class_level, created = ClassLevel.objects.get_or_create(
                    subject=ict_subject,
                    level_number=grade,
                    defaults={
                        'name': f'Grade {grade}',
                        'description': f'{config["level_type"]} ICT - Grade {grade} ({config["age_range"]})',
                        'pass_percentage': config['pass_percentage'],
                        'is_active': True
                    }
                )
                
                if created:
                    self.stdout.write(f"✅ Created ICT Grade {grade}")
                else:
                    self.stdout.write(f"📝 ICT Grade {grade} already exists")

    def create_ict_topics_for_all_grades(self, ict_subject):
        """Create age-appropriate ICT topics for each grade"""
        self.stdout.write("📖 Creating ICT topics for all grades...")
        
        # Define topics for each grade level
        grade_topics = {
            1: [
                'Introduction to Computers',
                'Computer Parts We Can See',
                'Using a Mouse and Keyboard',
                'Basic Computer Safety',
                'Fun with Educational Games'
            ],
            2: [
                'Computer On and Off',
                'Desktop and Icons',
                'Simple Drawing Programs',
                'Keyboard Practice',
                'Digital Citizenship Basics'
            ],
            3: [
                'File and Folder Basics',
                'Simple Word Processing',
                'Internet Safety for Kids',
                'Educational Software',
                'Printing Documents'
            ],
            4: [
                'Advanced File Management',
                'Creating Simple Documents',
                'Internet Research Skills',
                'Email Basics',
                'Digital Art and Creativity'
            ],
            5: [
                'Computer Basics and Parts',
                'Operating Systems and Desktop',
                'File Management and Organization',
                'Word Processing and Documents',
                'Internet Safety and Digital Citizenship',
                'Web Browsing and Online Research',
                'Email and Digital Communication',
                'Introduction to Programming Concepts'
            ],
            6: [
                'Advanced Word Processing',
                'Presentation Software Basics',
                'Spreadsheet Introduction',
                'Digital Research Projects',
                'Online Collaboration Tools',
                'Multimedia Projects',
                'Coding Fundamentals'
            ],
            7: [
                'Advanced Presentation Skills',
                'Spreadsheet Calculations',
                'Database Basics',
                'Web Design Introduction',
                'Digital Media Creation',
                'Programming Logic',
                'Cybersecurity Awareness'
            ],
            8: [
                'Advanced Spreadsheets',
                'Database Management',
                'Web Development Basics',
                'Digital Video Production',
                'Programming with Scratch',
                'Network Fundamentals',
                'Digital Ethics'
            ],
            9: [
                'Advanced Database Design',
                'HTML and CSS Basics',
                'Digital Photography',
                'Introduction to Python',
                'Computer Networks',
                'Data Analysis Basics',
                'Technology and Society'
            ],
            10: [
                'Advanced Web Development',
                'Programming with Python',
                'Data Structures',
                'Computer Graphics',
                'Network Security',
                'Database Programming',
                'IT Project Management'
            ],
            11: [
                'Software Development',
                'Advanced Programming',
                'System Analysis and Design',
                'Mobile App Development',
                'Artificial Intelligence Basics',
                'Cloud Computing',
                'Digital Entrepreneurship'
            ],
            12: [
                'Advanced Software Engineering',
                'Machine Learning Introduction',
                'Cybersecurity Advanced',
                'Big Data Analytics',
                'IoT and Smart Systems',
                'IT Career Preparation',
                'Capstone Technology Project'
            ]
        }
        
        # Create topics for each grade
        for grade, topics in grade_topics.items():
            try:
                class_level = ClassLevel.objects.get(subject=ict_subject, level_number=grade)
                
                for i, topic_title in enumerate(topics):
                    # Determine difficulty and duration based on grade
                    if grade <= 3:
                        difficulty = 'beginner'
                        duration = 30
                    elif grade <= 8:
                        difficulty = 'intermediate'
                        duration = 45
                    else:
                        difficulty = 'advanced'
                        duration = 60
                    
                    topic, created = Topic.objects.get_or_create(
                        class_level=class_level,
                        title=topic_title,
                        defaults={
                            'description': f'Grade {grade} ICT: {topic_title}',
                            'order': i + 1,
                            'estimated_duration': duration,
                            'difficulty_level': difficulty,
                            'is_active': True
                        }
                    )
                    
                    if created:
                        self.stdout.write(f"  ✅ Created topic: Grade {grade} - {topic_title}")
                
            except ClassLevel.DoesNotExist:
                self.stdout.write(f"⚠️ Class level not found for Grade {grade}")

    def print_summary(self):
        """Print summary of created content"""
        try:
            ict_subject = Subject.objects.get(name='ICT')
            class_levels = ClassLevel.objects.filter(subject=ict_subject).count()
            total_topics = Topic.objects.filter(class_level__subject=ict_subject).count()
            
            self.stdout.write("\n=== ICT SUBJECT SUMMARY ===")
            self.stdout.write(f"Class Levels: {class_levels}")
            self.stdout.write(f"Total Topics: {total_topics}")
            
            for grade in range(1, 13):
                try:
                    class_level = ClassLevel.objects.get(subject=ict_subject, level_number=grade)
                    topic_count = Topic.objects.filter(class_level=class_level).count()
                    self.stdout.write(f"Grade {grade}: {topic_count} topics")
                except ClassLevel.DoesNotExist:
                    self.stdout.write(f"Grade {grade}: Not found")
                    
        except Subject.DoesNotExist:
            self.stdout.write("ICT subject not found")
