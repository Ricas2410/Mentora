#!/usr/bin/env python
"""
Deployment script for Pentora platform
This script helps with common deployment tasks
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment...")
    
    # Check if .env file exists
    if not Path('.env').exists():
        print("❌ .env file not found. Please copy .env.example to .env and configure it.")
        return False
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not detected. Please activate your virtual environment.")
        return False
    
    print("✅ Environment check passed")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def run_migrations():
    """Run database migrations"""
    run_command("python manage.py makemigrations", "Creating migrations")
    return run_command("python manage.py migrate", "Running migrations")

def collect_static():
    """Collect static files"""
    return run_command("python manage.py collectstatic --noinput", "Collecting static files")

def create_superuser():
    """Create superuser if needed"""
    print("\n👤 Creating superuser...")
    print("Please follow the prompts to create an admin user:")
    os.system("python manage.py createsuperuser")

def run_tests():
    """Run tests"""
    return run_command("python manage.py test", "Running tests")

def main():
    """Main deployment function"""
    print("🚀 Pentora Deployment Script")
    print("=" * 40)
    
    if not check_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations")
        sys.exit(1)
    
    # Collect static files
    if not collect_static():
        print("❌ Failed to collect static files")
        sys.exit(1)
    
    # Ask if user wants to create superuser
    create_admin = input("\n❓ Do you want to create a superuser? (y/n): ").lower().strip()
    if create_admin == 'y':
        create_superuser()
    
    # Ask if user wants to run tests
    run_test = input("\n❓ Do you want to run tests? (y/n): ").lower().strip()
    if run_test == 'y':
        if not run_tests():
            print("⚠️  Some tests failed, but deployment can continue")
    
    print("\n🎉 Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Configure your web server (nginx, apache, etc.)")
    print("2. Set up SSL certificates")
    print("3. Configure your domain name")
    print("4. Set up monitoring and backups")
    print("\n🌐 Your application should be ready to run!")
    print("Run: python manage.py runserver")

if __name__ == "__main__":
    main()
