#!/usr/bin/env python
"""
Optimization script for Pentora Platform on Fly.io Free Tier
Reduces memory usage and optimizes performance for minimal resource consumption
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pentora_platform.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.conf import settings
from django.core.cache import cache
from django.db import connection


def optimize_database():
    """Optimize database for free tier"""
    print("🔧 Optimizing database...")
    
    # Run database optimizations
    with connection.cursor() as cursor:
        # Analyze tables for better query performance
        cursor.execute("ANALYZE;")
        
        # Vacuum to reclaim space (PostgreSQL)
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            cursor.execute("VACUUM;")
    
    print("✅ Database optimized")


def clear_unnecessary_data():
    """Clear unnecessary data to save space"""
    print("🧹 Clearing unnecessary data...")
    
    # Clear old cache data
    cache.clear()
    
    # Clear old session data
    from django.contrib.sessions.models import Session
    from django.utils import timezone
    from datetime import timedelta
    
    # Delete sessions older than 7 days
    old_sessions = Session.objects.filter(
        expire_date__lt=timezone.now() - timedelta(days=7)
    )
    deleted_count = old_sessions.count()
    old_sessions.delete()
    
    print(f"✅ Cleared {deleted_count} old sessions")


def optimize_static_files():
    """Optimize static files for production"""
    print("📦 Optimizing static files...")
    
    # Collect static files
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
    
    print("✅ Static files optimized")


def check_memory_usage():
    """Check current memory usage"""
    print("📊 Checking memory usage...")
    
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        
        print(f"Current memory usage: {memory_mb:.2f} MB")
        
        if memory_mb > 200:
            print("⚠️  Warning: Memory usage is high for free tier")
        else:
            print("✅ Memory usage is within free tier limits")
            
    except ImportError:
        print("📊 psutil not available, skipping memory check")


def optimize_settings():
    """Apply runtime optimizations"""
    print("⚙️  Applying runtime optimizations...")
    
    # Disable debug toolbar in production
    if hasattr(settings, 'DEBUG_TOOLBAR_CONFIG'):
        settings.DEBUG_TOOLBAR_CONFIG['SHOW_TOOLBAR_CALLBACK'] = lambda request: False
    
    # Optimize logging
    import logging
    logging.getLogger('django.db.backends').setLevel(logging.WARNING)
    
    print("✅ Runtime optimizations applied")


def main():
    """Main optimization function"""
    print("🚀 Starting Pentora Platform optimization for Fly.io Free Tier...")
    print("=" * 60)
    
    try:
        # Run optimizations
        optimize_settings()
        clear_unnecessary_data()
        optimize_database()
        optimize_static_files()
        check_memory_usage()
        
        print("=" * 60)
        print("🎉 Optimization completed successfully!")
        print("")
        print("💡 Free Tier Tips:")
        print("   - Monitor memory usage regularly")
        print("   - Let the app auto-sleep when inactive")
        print("   - Use S3 for media files to save disk space")
        print("   - Keep database queries optimized")
        print("")
        print("📊 Next steps:")
        print("   1. Deploy to Fly.io: ./deploy.sh")
        print("   2. Monitor resource usage in Fly.io dashboard")
        print("   3. Check logs: flyctl logs")
        
    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
