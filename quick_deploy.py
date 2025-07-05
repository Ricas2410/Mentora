#!/usr/bin/env python3
"""
Quick deployment script for static files fixes
"""
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    print("🚀 Quick Deploy - Static Files Fixes")
    print("=" * 50)
    
    # Step 1: Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("❌ Failed to collect static files")
        return
    
    # Step 2: Deploy to Fly.io
    print("🚀 Deploying to Fly.io...")
    print("This will take a few minutes...")
    
    if not run_command("fly deploy", "Deploying to Fly.io"):
        print("❌ Deployment failed")
        return
    
    print("=" * 50)
    print("✅ Deployment completed!")
    print("🌐 Your site should be available at: https://pentora.fly.dev")
    print("🔍 Test static files at: https://pentora.fly.dev/test-static/")
    print("")
    print("📋 Check these files after deployment:")
    print("- CSS: https://pentora.fly.dev/static/css/enhanced-ui.css")
    print("- JS: https://pentora.fly.dev/static/js/app.js")
    print("- Service Worker: https://pentora.fly.dev/static/sw.js")

if __name__ == "__main__":
    main() 