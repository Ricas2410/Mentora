#!/usr/bin/env python
"""
Fix Topic Order Conflicts
Resolves UNIQUE constraint issues with topic order numbers
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote, Question, AnswerChoice

def fix_topic_orders():
    """Fix topic order conflicts by reassigning unique order numbers"""
    print("🔧 Fixing topic order conflicts...")
    
    # Get all class levels
    class_levels = ClassLevel.objects.all()
    
    for class_level in class_levels:
        print(f"\n📚 Processing {class_level.subject.name} - Grade {class_level.level_number}")
        
        # Get all topics for this class level, ordered by current order
        topics = Topic.objects.filter(class_level=class_level).order_by('order', 'id')
        
        # Reassign order numbers starting from 1
        for index, topic in enumerate(topics, 1):
            if topic.order != index:
                print(f"  🔄 Updating '{topic.title}' order from {topic.order} to {index}")
                topic.order = index
                topic.save()
            else:
                print(f"  ✅ '{topic.title}' order {index} is correct")
    
    print("\n✅ Topic order conflicts resolved!")

def check_for_duplicates():
    """Check for any remaining duplicate orders"""
    print("\n🔍 Checking for duplicate topic orders...")
    
    class_levels = ClassLevel.objects.all()
    conflicts_found = False
    
    for class_level in class_levels:
        topics = Topic.objects.filter(class_level=class_level)
        orders = [topic.order for topic in topics]
        
        # Check for duplicates
        seen = set()
        duplicates = set()
        for order in orders:
            if order in seen:
                duplicates.add(order)
            seen.add(order)
        
        if duplicates:
            conflicts_found = True
            print(f"❌ {class_level.subject.name} Grade {class_level.level_number} has duplicate orders: {duplicates}")
        else:
            print(f"✅ {class_level.subject.name} Grade {class_level.level_number} - No conflicts")
    
    if not conflicts_found:
        print("\n🎉 No duplicate topic orders found!")
    
    return not conflicts_found

def reset_all_topic_orders():
    """Reset all topic orders to avoid conflicts"""
    print("🔄 Resetting all topic orders...")
    
    # Get all subjects
    subjects = Subject.objects.all()
    
    for subject in subjects:
        print(f"\n📖 Processing {subject.name}")
        
        # Get all class levels for this subject
        class_levels = ClassLevel.objects.filter(subject=subject).order_by('level_number')
        
        for class_level in class_levels:
            print(f"  📚 Grade {class_level.level_number}")
            
            # Get all topics for this class level
            topics = Topic.objects.filter(class_level=class_level).order_by('id')
            
            # Reassign orders starting from 1
            for index, topic in enumerate(topics, 1):
                topic.order = index
                topic.save()
                print(f"    ✅ '{topic.title}' → order {index}")

if __name__ == '__main__':
    print("TOPIC ORDER CONFLICT RESOLVER")
    print("=" * 50)

    # First, reset all orders to avoid conflicts
    reset_all_topic_orders()

    # Then check for any remaining issues
    if check_for_duplicates():
        print("\nAll topic order conflicts have been resolved!")
        print("You can now run the content population scripts safely.")
    else:
        print("\nSome conflicts may still exist. Running fix again...")
        fix_topic_orders()
        check_for_duplicates()
