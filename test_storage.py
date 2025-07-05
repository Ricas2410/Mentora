#!/usr/bin/env python3
"""
Comprehensive storage test script for Pentora Platform
Tests both static files and media storage configuration
"""
import os
import sys
import django
from pathlib import Path
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pentora_platform.settings')
django.setup()

def test_static_files_configuration():
    """Test static files configuration"""
    print("🔍 Testing Static Files Configuration...")
    print("=" * 50)
    
    # Check basic settings
    print(f"✅ STATIC_URL: {settings.STATIC_URL}")
    print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"✅ STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    print(f"✅ DEBUG Mode: {settings.DEBUG}")
    
    # Check if static files directory exists
    static_root = Path(settings.STATIC_ROOT)
    if static_root.exists():
        print(f"✅ Static files directory exists: {static_root}")
        
        # Check key static files
        key_files = [
            'css/enhanced-ui.css',
            'js/app.js',
            'js/progress-bar-cleanup.js',
            'js/ux-enhancements.js',
            'js/mobile-navigation.js',
            'js/performance-optimizer.js',
            'js/ui-interactions.js',
            'js/page-specific-enhancements.js',
            'sw.js',
            'manifest.json'
        ]
        
        print("\n📁 Checking key static files:")
        for file_path in key_files:
            full_path = static_root / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                print(f"   ✅ {file_path} ({size} bytes)")
            else:
                print(f"   ❌ {file_path} - MISSING")
    else:
        print(f"❌ Static files directory does not exist: {static_root}")
    
    # Check WhiteNoise configuration
    if hasattr(settings, 'WHITENOISE_USE_FINDERS'):
        print(f"✅ WHITENOISE_USE_FINDERS: {settings.WHITENOISE_USE_FINDERS}")
    if hasattr(settings, 'WHITENOISE_ROOT'):
        print(f"✅ WHITENOISE_ROOT: {settings.WHITENOISE_ROOT}")
    
    print()

def test_media_storage_configuration():
    """Test media storage configuration"""
    print("🔍 Testing Media Storage Configuration...")
    print("=" * 50)
    
    # Check basic settings
    print(f"✅ MEDIA_URL: {settings.MEDIA_URL}")
    print(f"✅ MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"✅ DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    # Check Supabase configuration
    if hasattr(settings, 'AWS_ACCESS_KEY_ID') and settings.AWS_ACCESS_KEY_ID:
        print("✅ Supabase credentials found")
        print(f"   AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
        print(f"   AWS_S3_ENDPOINT_URL: {settings.AWS_S3_ENDPOINT_URL}")
        print(f"   AWS_S3_CUSTOM_DOMAIN: {settings.AWS_S3_CUSTOM_DOMAIN}")
    else:
        print("⚠️  Supabase credentials not found - using local storage")
    
    # Test storage backend
    try:
        storage_class = default_storage.__class__.__name__
        print(f"✅ Current storage backend: {storage_class}")
        
        # Test if we can write a test file
        test_content = b"Test file content for storage verification"
        test_filename = "test_storage_verification.txt"
        
        print(f"\n🧪 Testing file upload to storage...")
        saved_path = default_storage.save(test_filename, ContentFile(test_content))
        print(f"   ✅ File saved as: {saved_path}")
        
        # Test if we can read the file back
        if default_storage.exists(saved_path):
            print(f"   ✅ File exists in storage")
            
            # Get the URL
            try:
                file_url = default_storage.url(saved_path)
                print(f"   ✅ File URL: {file_url}")
                
                # Test if URL is accessible (for Supabase)
                if file_url.startswith('http'):
                    try:
                        response = requests.head(file_url, timeout=10)
                        if response.status_code == 200:
                            print(f"   ✅ File is accessible via URL")
                        else:
                            print(f"   ⚠️  File URL returned status: {response.status_code}")
                    except Exception as e:
                        print(f"   ⚠️  Could not access file URL: {e}")
                
            except Exception as e:
                print(f"   ⚠️  Could not generate file URL: {e}")
        else:
            print(f"   ❌ File does not exist in storage")
        
        # Clean up test file
        try:
            default_storage.delete(saved_path)
            print(f"   ✅ Test file cleaned up")
        except Exception as e:
            print(f"   ⚠️  Could not clean up test file: {e}")
            
    except Exception as e:
        print(f"❌ Storage test failed: {e}")
    
    print()

def test_supabase_connection():
    """Test Supabase connection if configured"""
    print("🔍 Testing Supabase Connection...")
    print("=" * 50)
    
    if not hasattr(settings, 'AWS_ACCESS_KEY_ID') or not settings.AWS_ACCESS_KEY_ID:
        print("⚠️  Supabase not configured - skipping connection test")
        return
    
    try:
        endpoint = settings.AWS_S3_ENDPOINT_URL
        if not endpoint:
            print("❌ No Supabase endpoint URL configured")
            return
        
        # Test the endpoint
        test_url = endpoint.replace('/storage/v1/s3', '')
        print(f"Testing endpoint: {test_url}")
        
        response = requests.head(test_url, timeout=10)
        if response.status_code == 200:
            print("✅ Supabase endpoint is reachable")
        else:
            print(f"⚠️  Endpoint returned status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Supabase connection test failed: {e}")
    
    print()

def test_static_files_serving():
    """Test if static files can be served"""
    print("🔍 Testing Static Files Serving...")
    print("=" * 50)
    
    # Test URLs for key static files
    base_url = "https://pentora.fly.dev"
    test_files = [
        '/static/css/enhanced-ui.css',
        '/static/js/app.js',
        '/static/js/progress-bar-cleanup.js',
        '/static/sw.js',
        '/static/manifest.json'
    ]
    
    print("🌐 Testing static files via HTTP...")
    for file_path in test_files:
        url = base_url + file_path
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', 'unknown')
                print(f"   ✅ {file_path} - {response.status_code} ({content_type})")
            else:
                print(f"   ❌ {file_path} - {response.status_code}")
        except Exception as e:
            print(f"   ❌ {file_path} - Error: {e}")
    
    print()

def main():
    """Run all storage tests"""
    print("🚀 Pentora Platform - Storage Configuration Test")
    print("=" * 60)
    
    # Test static files configuration
    test_static_files_configuration()
    
    # Test media storage configuration
    test_media_storage_configuration()
    
    # Test Supabase connection
    test_supabase_connection()
    
    # Test static files serving
    test_static_files_serving()
    
    print("=" * 60)
    print("✅ Storage test completed!")
    print("\n📋 Summary:")
    print("- Static files should be served by WhiteNoise in production")
    print("- Media files should upload to Supabase (if configured) or local storage")
    print("- Check the test results above for any issues")

if __name__ == "__main__":
    main() 