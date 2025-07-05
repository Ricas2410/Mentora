#!/usr/bin/env python3
"""
Deployment script to fix static files and media issues on Fly.io
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def main():
    print("🚀 Starting deployment fixes for Pentora Platform...")
    print("=" * 60)
    
    # Step 1: Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("❌ Failed to collect static files. Exiting.")
        sys.exit(1)
    
    # Step 2: Run migrations
    if not run_command("python manage.py migrate --noinput", "Running database migrations"):
        print("❌ Failed to run migrations. Exiting.")
        sys.exit(1)
    
    # Step 3: Check if fly CLI is installed
    if not run_command("fly version", "Checking Fly CLI installation"):
        print("❌ Fly CLI not found. Please install it first.")
        print("Visit: https://fly.io/docs/hands-on/install-flyctl/")
        sys.exit(1)
    
    # Step 4: Deploy to Fly.io
    print("🚀 Deploying to Fly.io...")
    print("This will take a few minutes...")
    
    if not run_command("fly deploy", "Deploying to Fly.io"):
        print("❌ Deployment failed. Check the logs above.")
        sys.exit(1)
    
    print("=" * 60)
    print("✅ Deployment completed successfully!")
    print("🌐 Your site should be available at: https://pentora.fly.dev")
    print("🔍 Test static files at: https://pentora.fly.dev/test-static/")
    print("")
    print("📋 Next steps:")
    print("1. Check if static files are loading correctly")
    print("2. Test media file uploads")
    print("3. Monitor the application logs: fly logs")
    print("")
    print("🔧 If you encounter issues:")
    print("- Check logs: fly logs")
    print("- SSH into the app: fly ssh console")
    print("- Restart the app: fly apps restart")

if __name__ == "__main__":
    main() 