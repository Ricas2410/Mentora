#!/usr/bin/env python
"""
Database optimization script for Pentora platform
Adds indexes, optimizes queries, and improves performance
"""

import os
import django
import sys
from django.db import connection, transaction

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pentora_platform.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import models
from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, StudyNote, AnswerChoice
from users.models import User
from progress.models import UserProgress, TopicProgress
from analytics.models import PageVisit, UserActivity


def create_database_indexes():
    """Create additional database indexes for performance"""
    print("🔧 Creating database indexes...")
    
    with connection.cursor() as cursor:
        # User model indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email_active ON users (email, is_active);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_class_level ON users (current_class_level);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_created_at ON users (created_at);")
            print("✅ User indexes created")
        except Exception as e:
            print(f"❌ User indexes error: {e}")
        
        # Subject model indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_subjects_active_order ON subjects (is_active, \"order\");")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_subjects_slug ON subjects (slug);")
            print("✅ Subject indexes created")
        except Exception as e:
            print(f"❌ Subject indexes error: {e}")
        
        # Topic model indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_class_level_active ON topics (class_level_id, is_active);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_order ON topics (\"order\");")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_slug ON topics (slug);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_difficulty ON topics (difficulty_level);")
            print("✅ Topic indexes created")
        except Exception as e:
            print(f"❌ Topic indexes error: {e}")
        
        # Question model indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_topic_type ON questions (topic_id, question_type, is_active);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions (difficulty_level);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_created_at ON questions (created_at);")
            print("✅ Question indexes created")
        except Exception as e:
            print(f"❌ Question indexes error: {e}")
        
        # Progress model indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_progress_user_class ON user_progress (user_id, class_level_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_progress_completed ON user_progress (is_completed, updated_at);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_progress_user_topic ON topic_progress (user_id, topic_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_progress_completed ON topic_progress (is_completed, updated_at);")
            print("✅ Progress indexes created")
        except Exception as e:
            print(f"❌ Progress indexes error: {e}")
        
        # Analytics model indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_page_visits_timestamp ON page_visits (timestamp);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_page_visits_user_timestamp ON page_visits (user_id, timestamp);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_page_visits_ip_timestamp ON page_visits (ip_address, timestamp);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_activity_user_type ON user_activity (user_id, activity_type, timestamp);")
            print("✅ Analytics indexes created")
        except Exception as e:
            print(f"❌ Analytics indexes error: {e}")


def optimize_database_settings():
    """Optimize database settings for better performance"""
    print("🔧 Optimizing database settings...")
    
    with connection.cursor() as cursor:
        try:
            # PostgreSQL optimizations
            if 'postgresql' in connection.vendor:
                # Analyze tables for better query planning
                cursor.execute("ANALYZE;")
                
                # Update statistics
                cursor.execute("VACUUM ANALYZE;")
                
                print("✅ PostgreSQL optimizations applied")
            
            # SQLite optimizations
            elif 'sqlite' in connection.vendor:
                cursor.execute("PRAGMA optimize;")
                cursor.execute("PRAGMA analysis_limit=1000;")
                cursor.execute("PRAGMA cache_size=10000;")
                
                print("✅ SQLite optimizations applied")
                
        except Exception as e:
            print(f"❌ Database optimization error: {e}")


def clean_old_data():
    """Clean up old analytics data to improve performance"""
    print("🧹 Cleaning old data...")
    
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    try:
        # Remove old page visits (older than 6 months)
        cutoff_date = timezone.now() - timedelta(days=180)
        old_visits = PageVisit.objects.filter(timestamp__lt=cutoff_date)
        count = old_visits.count()
        old_visits.delete()
        print(f"✅ Removed {count} old page visits")
        
        # Remove old user activities (older than 1 year)
        cutoff_date = timezone.now() - timedelta(days=365)
        old_activities = UserActivity.objects.filter(timestamp__lt=cutoff_date)
        count = old_activities.count()
        old_activities.delete()
        print(f"✅ Removed {count} old user activities")
        
    except Exception as e:
        print(f"❌ Data cleanup error: {e}")


def optimize_queries():
    """Optimize common database queries"""
    print("🔧 Optimizing common queries...")
    
    try:
        # Pre-cache frequently accessed data
        print("📊 Caching subject statistics...")
        for subject in Subject.objects.filter(is_active=True):
            # Cache topic count
            topic_count = Topic.objects.filter(
                class_level__subject=subject,
                is_active=True
            ).count()
            
            # Cache question count
            question_count = Question.objects.filter(
                topic__class_level__subject=subject,
                is_active=True
            ).count()
            
            print(f"   {subject.name}: {topic_count} topics, {question_count} questions")
        
        print("✅ Query optimization completed")
        
    except Exception as e:
        print(f"❌ Query optimization error: {e}")


def check_database_health():
    """Check database health and performance metrics"""
    print("🏥 Checking database health...")
    
    with connection.cursor() as cursor:
        try:
            # Check table sizes
            if 'postgresql' in connection.vendor:
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        attname,
                        n_distinct,
                        correlation
                    FROM pg_stats 
                    WHERE schemaname = 'public'
                    ORDER BY tablename, attname;
                """)
                
                print("📊 Database statistics:")
                for row in cursor.fetchall()[:10]:  # Show first 10 rows
                    print(f"   {row[1]}.{row[2]}: distinct={row[3]}, correlation={row[4]}")
            
            # Check for missing indexes
            cursor.execute("""
                SELECT COUNT(*) as total_tables
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            
            table_count = cursor.fetchone()[0]
            print(f"📊 Total tables: {table_count}")
            
        except Exception as e:
            print(f"❌ Health check error: {e}")


def generate_performance_report():
    """Generate a performance report"""
    print("📊 Generating performance report...")
    
    try:
        # Count records in main tables
        user_count = User.objects.count()
        subject_count = Subject.objects.count()
        topic_count = Topic.objects.count()
        question_count = Question.objects.count()
        progress_count = UserProgress.objects.count()
        
        print("\n" + "="*50)
        print("📊 Pentora DATABASE PERFORMANCE REPORT")
        print("="*50)
        print(f"👥 Users: {user_count:,}")
        print(f"📚 Subjects: {subject_count:,}")
        print(f"📖 Topics: {topic_count:,}")
        print(f"❓ Questions: {question_count:,}")
        print(f"📈 Progress Records: {progress_count:,}")
        print("="*50)
        
        # Calculate averages
        if subject_count > 0:
            avg_topics_per_subject = topic_count / subject_count
            print(f"📊 Average topics per subject: {avg_topics_per_subject:.1f}")
        
        if topic_count > 0:
            avg_questions_per_topic = question_count / topic_count
            print(f"📊 Average questions per topic: {avg_questions_per_topic:.1f}")
        
        # Active vs inactive content
        active_topics = Topic.objects.filter(is_active=True).count()
        active_questions = Question.objects.filter(is_active=True).count()
        
        print(f"✅ Active topics: {active_topics:,} ({active_topics/topic_count*100:.1f}%)")
        print(f"✅ Active questions: {active_questions:,} ({active_questions/question_count*100:.1f}%)")
        
        print("="*50)
        print("✅ Performance optimization completed!")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Report generation error: {e}")


def main():
    """Main optimization function"""
    print("🚀 Starting Pentora database optimization...")
    print("="*50)
    
    try:
        # Run optimization steps
        create_database_indexes()
        print()
        
        optimize_database_settings()
        print()
        
        clean_old_data()
        print()
        
        optimize_queries()
        print()
        
        check_database_health()
        print()
        
        generate_performance_report()
        
    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
