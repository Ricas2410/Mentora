#!/usr/bin/env python
"""
Script to clean up duplicate class levels and reorganize the database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, StudyNote, Passage
from progress.models import UserProgress, TopicProgress

def cleanup_database():
    """Clean up duplicate class levels and reorganize data"""
    print("🧹 Starting database cleanup...")
    print("=" * 60)
    
    # Step 1: Remove duplicate class levels
    print("\n📋 Removing duplicate class levels...")
    
    subjects = Subject.objects.all()
    for subject in subjects:
        print(f"\nProcessing subject: {subject.name}")
        
        # Get all class levels for this subject
        class_levels = ClassLevel.objects.filter(subject=subject).order_by('level_number', 'created_at')
        
        # Group by level_number
        level_groups = {}
        for level in class_levels:
            if level.level_number not in level_groups:
                level_groups[level.level_number] = []
            level_groups[level.level_number].append(level)
        
        # Keep only the first one for each level_number, delete duplicates
        for level_number, levels in level_groups.items():
            if len(levels) > 1:
                print(f"  Found {len(levels)} duplicates for Grade {level_number}")
                
                # Keep the first one (oldest)
                keep_level = levels[0]
                duplicates = levels[1:]
                
                # Move topics and progress from duplicates to the kept level
                for duplicate in duplicates:
                    # Move topics
                    topics = Topic.objects.filter(class_level=duplicate)
                    for topic in topics:
                        topic.class_level = keep_level
                        topic.save()
                        print(f"    Moved topic: {topic.title}")
                    
                    # Move user progress
                    progress_records = UserProgress.objects.filter(class_level=duplicate)
                    for progress in progress_records:
                        # Check if progress already exists for the kept level
                        existing = UserProgress.objects.filter(
                            user=progress.user,
                            class_level=keep_level
                        ).first()
                        
                        if not existing:
                            progress.class_level = keep_level
                            progress.save()
                            print(f"    Moved progress for user: {progress.user.full_name}")
                        else:
                            # Merge progress data
                            if progress.is_completed and not existing.is_completed:
                                existing.is_completed = True
                                existing.completed_at = progress.completed_at
                                existing.save()
                            progress.delete()
                    
                    # Delete the duplicate
                    print(f"    Deleted duplicate: {duplicate.name}")
                    duplicate.delete()
    
    # Step 2: Ensure all subjects have all grade levels (1-12)
    print("\n📚 Ensuring all subjects have complete grade levels...")
    
    for subject in subjects:
        print(f"\nChecking subject: {subject.name}")
        
        for grade in range(1, 13):
            level, created = ClassLevel.objects.get_or_create(
                subject=subject,
                level_number=grade,
                defaults={
                    'name': f'Grade {grade}',
                    'description': f'{subject.name} for Grade {grade} students',
                    'is_active': True
                }
            )
            
            if created:
                print(f"  Created missing Grade {grade}")
    
    # Step 3: Clean up orphaned records
    print("\n🗑️ Cleaning up orphaned records...")
    
    # Remove questions without topics
    orphaned_questions = Question.objects.filter(topic__isnull=True)
    if orphaned_questions.exists():
        count = orphaned_questions.count()
        orphaned_questions.delete()
        print(f"  Removed {count} orphaned questions")
    
    # Remove study notes without topics
    orphaned_notes = StudyNote.objects.filter(topic__isnull=True)
    if orphaned_notes.exists():
        count = orphaned_notes.count()
        orphaned_notes.delete()
        print(f"  Removed {count} orphaned study notes")
    
    # Remove topic progress without topics
    orphaned_progress = TopicProgress.objects.filter(topic__isnull=True)
    if orphaned_progress.exists():
        count = orphaned_progress.count()
        orphaned_progress.delete()
        print(f"  Removed {count} orphaned topic progress records")
    
    # Step 4: Final statistics
    print("\n📊 Final Database Statistics:")
    print(f"   • Subjects: {Subject.objects.count()}")
    print(f"   • Class Levels: {ClassLevel.objects.count()}")
    print(f"   • Topics: {Topic.objects.count()}")
    print(f"   • Questions: {Question.objects.count()}")
    print(f"   • Study Notes: {StudyNote.objects.count()}")
    print(f"   • Reading Passages: {Passage.objects.count()}")
    
    # Verify no duplicates remain
    print("\n🔍 Verifying no duplicates remain...")
    for subject in subjects:
        duplicates = ClassLevel.objects.filter(subject=subject).values('level_number').annotate(
            count=models.Count('level_number')
        ).filter(count__gt=1)
        
        if duplicates.exists():
            print(f"  ⚠️ Still has duplicates in {subject.name}")
        else:
            print(f"  ✅ {subject.name} - clean")
    
    print("\n" + "=" * 60)
    print("🎉 Database cleanup completed successfully!")
    return True

if __name__ == '__main__':
    from django.db import models
    cleanup_database()
