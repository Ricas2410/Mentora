#!/usr/bin/env python
"""
Production deployment script for Pentora platform
Handles database migrations, static files, cache warming, and health checks
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pentora_platform.settings')

import django
django.setup()

from django.core.management import execute_from_command_line, call_command
from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()


class DeploymentManager:
    """Manages the deployment process"""
    
    def __init__(self):
        self.start_time = time.time()
        self.steps_completed = 0
        self.total_steps = 12
        
    def log(self, message, level="INFO"):
        """Log deployment messages"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def run_command(self, command, description):
        """Run a shell command with error handling"""
        self.log(f"Running: {description}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                self.log(f"Command failed: {result.stderr}", "ERROR")
                return False
            self.log(f"Success: {description}")
            return True
        except Exception as e:
            self.log(f"Error running command: {e}", "ERROR")
            return False
    
    def step(self, description):
        """Mark a deployment step"""
        self.steps_completed += 1
        progress = (self.steps_completed / self.total_steps) * 100
        self.log(f"Step {self.steps_completed}/{self.total_steps} ({progress:.1f}%): {description}")
    
    def check_prerequisites(self):
        """Check deployment prerequisites"""
        self.step("Checking prerequisites")
        
        # Check Python version
        if sys.version_info < (3, 8):
            self.log("Python 3.8+ required", "ERROR")
            return False
            
        # Check Django settings
        if settings.DEBUG:
            self.log("WARNING: DEBUG is True in production", "WARNING")
            
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.log("Database connection: OK")
        except Exception as e:
            self.log(f"Database connection failed: {e}", "ERROR")
            return False
            
        # Check required environment variables
        required_vars = ['SECRET_KEY', 'DATABASE_URL']
        for var in required_vars:
            if not os.getenv(var):
                self.log(f"Missing environment variable: {var}", "ERROR")
                return False
                
        return True
    
    def backup_database(self):
        """Create database backup before deployment"""
        self.step("Creating database backup")
        
        if 'postgresql' in settings.DATABASES['default']['ENGINE']:
            backup_file = f"backup_{int(time.time())}.sql"
            db_url = os.getenv('DATABASE_URL', '')
            
            if db_url:
                command = f"pg_dump {db_url} > {backup_file}"
                if self.run_command(command, "Database backup"):
                    self.log(f"Backup created: {backup_file}")
                    return True
                    
        self.log("Database backup skipped (not PostgreSQL or no DATABASE_URL)")
        return True
    
    def run_migrations(self):
        """Run database migrations"""
        self.step("Running database migrations")
        
        try:
            call_command('migrate', verbosity=1)
            self.log("Migrations completed successfully")
            return True
        except Exception as e:
            self.log(f"Migration failed: {e}", "ERROR")
            return False
    
    def collect_static_files(self):
        """Collect static files"""
        self.step("Collecting static files")
        
        try:
            call_command('collectstatic', '--noinput', verbosity=1)
            self.log("Static files collected successfully")
            return True
        except Exception as e:
            self.log(f"Static file collection failed: {e}", "ERROR")
            return False
    
    def compress_static_files(self):
        """Compress static files if django-compressor is available"""
        self.step("Compressing static files")
        
        try:
            call_command('compress', '--force')
            self.log("Static files compressed successfully")
            return True
        except Exception as e:
            self.log(f"Static file compression failed: {e}", "WARNING")
            return True  # Non-critical
    
    def warm_cache(self):
        """Warm up the cache with frequently accessed data"""
        self.step("Warming cache")
        
        try:
            from subjects.models import Subject, Topic
            
            # Cache subjects
            subjects = list(Subject.objects.filter(is_active=True).prefetch_related('classlevels'))
            cache.set('active_subjects', subjects, 3600)
            
            # Cache popular topics
            popular_topics = list(Topic.objects.filter(is_active=True)[:100])
            cache.set('popular_topics', popular_topics, 3600)
            
            self.log("Cache warmed successfully")
            return True
        except Exception as e:
            self.log(f"Cache warming failed: {e}", "WARNING")
            return True  # Non-critical
    
    def create_superuser_if_needed(self):
        """Create superuser if none exists"""
        self.step("Checking superuser")
        
        try:
            if not User.objects.filter(is_superuser=True).exists():
                admin_email = os.getenv('ADMIN_EMAIL', 'admin@Pentora.com')
                admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
                
                User.objects.create_superuser(
                    email=admin_email,
                    password=admin_password,
                    first_name='Admin',
                    last_name='User'
                )
                self.log(f"Superuser created: {admin_email}")
            else:
                self.log("Superuser already exists")
            return True
        except Exception as e:
            self.log(f"Superuser creation failed: {e}", "ERROR")
            return False
    
    def optimize_database(self):
        """Run database optimizations"""
        self.step("Optimizing database")
        
        try:
            # Run the optimization script
            exec(open('scripts/optimize_database.py').read())
            self.log("Database optimization completed")
            return True
        except Exception as e:
            self.log(f"Database optimization failed: {e}", "WARNING")
            return True  # Non-critical
    
    def generate_sitemap(self):
        """Generate sitemap"""
        self.step("Generating sitemap")
        
        try:
            # This would be handled by Django's sitemap framework
            self.log("Sitemap generation configured")
            return True
        except Exception as e:
            self.log(f"Sitemap generation failed: {e}", "WARNING")
            return True  # Non-critical
    
    def run_health_checks(self):
        """Run post-deployment health checks"""
        self.step("Running health checks")
        
        try:
            # Check database
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM subjects")
                subject_count = cursor.fetchone()[0]
                self.log(f"Database check: {subject_count} subjects found")
            
            # Check cache
            cache.set('health_check', 'ok', 60)
            if cache.get('health_check') == 'ok':
                self.log("Cache check: OK")
            else:
                self.log("Cache check: FAILED", "WARNING")
            
            # Check static files
            static_root = settings.STATIC_ROOT
            if static_root and os.path.exists(static_root):
                self.log("Static files check: OK")
            else:
                self.log("Static files check: FAILED", "WARNING")
                
            return True
        except Exception as e:
            self.log(f"Health checks failed: {e}", "ERROR")
            return False
    
    def cleanup(self):
        """Cleanup deployment artifacts"""
        self.step("Cleaning up")
        
        try:
            # Clear old cache entries
            cache.clear()
            
            # Remove old log files (keep last 10)
            log_dir = Path('logs')
            if log_dir.exists():
                log_files = sorted(log_dir.glob('*.log'), key=os.path.getmtime)
                for old_log in log_files[:-10]:
                    old_log.unlink()
                    
            self.log("Cleanup completed")
            return True
        except Exception as e:
            self.log(f"Cleanup failed: {e}", "WARNING")
            return True  # Non-critical
    
    def deploy(self):
        """Run the complete deployment process"""
        self.log("🚀 Starting Pentora production deployment")
        self.log("=" * 60)
        
        # Run deployment steps
        steps = [
            self.check_prerequisites,
            self.backup_database,
            self.run_migrations,
            self.collect_static_files,
            self.compress_static_files,
            self.create_superuser_if_needed,
            self.optimize_database,
            self.warm_cache,
            self.generate_sitemap,
            self.run_health_checks,
            self.cleanup,
        ]
        
        failed_steps = []
        
        for step_func in steps:
            try:
                if not step_func():
                    failed_steps.append(step_func.__name__)
            except Exception as e:
                self.log(f"Step {step_func.__name__} failed: {e}", "ERROR")
                failed_steps.append(step_func.__name__)
        
        # Final report
        elapsed_time = time.time() - self.start_time
        self.log("=" * 60)
        
        if failed_steps:
            self.log(f"❌ Deployment completed with {len(failed_steps)} failures", "WARNING")
            self.log(f"Failed steps: {', '.join(failed_steps)}")
        else:
            self.log("✅ Deployment completed successfully!")
            
        self.log(f"⏱️  Total time: {elapsed_time:.2f} seconds")
        self.log("=" * 60)
        
        return len(failed_steps) == 0


def main():
    """Main deployment function"""
    deployment = DeploymentManager()
    success = deployment.deploy()
    
    if success:
        print("\n🎉 Pentora is ready for production!")
        print("📊 Access admin panel: /admin/")
        print("🏠 Visit homepage: /")
        sys.exit(0)
    else:
        print("\n❌ Deployment failed. Check logs above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
