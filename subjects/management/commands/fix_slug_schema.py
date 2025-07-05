from django.core.management.base import BaseCommand
from django.db import connection
from django.utils.text import slugify
from subjects.models import Subject, Topic


class Command(BaseCommand):
    help = 'Fix missing slug columns in subjects and topics tables'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing slug schema issues...")
        
        cursor = connection.cursor()
        
        # Check if slug column exists in subjects table
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'subjects' AND column_name = 'slug';
        """)
        subjects_has_slug = cursor.fetchone()
        
        # Check if slug column exists in topics table
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'topics' AND column_name = 'slug';
        """)
        topics_has_slug = cursor.fetchone()
        
        # Add slug column to subjects table if missing
        if not subjects_has_slug:
            self.stdout.write("📝 Adding slug column to subjects table...")
            cursor.execute("""
                ALTER TABLE subjects 
                ADD COLUMN slug VARCHAR(120) NULL;
            """)
            
            # Create unique index
            cursor.execute("""
                CREATE UNIQUE INDEX subjects_slug_unique 
                ON subjects(slug) 
                WHERE slug IS NOT NULL;
            """)
            
            # Populate slug values for existing subjects
            self.stdout.write("📝 Populating slug values for existing subjects...")
            subjects = Subject.objects.all()
            for subject in subjects:
                base_slug = slugify(subject.name)
                slug = base_slug
                counter = 1
                
                # Ensure unique slug
                while Subject.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                subject.slug = slug
                subject.save()
            
            self.stdout.write("✅ Fixed subjects slug column")
        else:
            self.stdout.write("✅ Subjects slug column already exists")
        
        # Add slug column to topics table if missing
        if not topics_has_slug:
            self.stdout.write("📝 Adding slug column to topics table...")
            cursor.execute("""
                ALTER TABLE topics 
                ADD COLUMN slug VARCHAR(220) NULL;
            """)
            
            # Populate slug values for existing topics
            self.stdout.write("📝 Populating slug values for existing topics...")
            topics = Topic.objects.all()
            for topic in topics:
                base_slug = slugify(topic.title)
                slug = base_slug
                counter = 1
                
                # Ensure unique slug within the same class level
                while Topic.objects.filter(slug=slug, class_level=topic.class_level).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                topic.slug = slug
                topic.save()
            
            self.stdout.write("✅ Fixed topics slug column")
        else:
            self.stdout.write("✅ Topics slug column already exists")
        
        self.stdout.write(self.style.SUCCESS("🎉 Schema fix completed successfully!"))
