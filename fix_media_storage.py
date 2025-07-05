#!/usr/bin/env python3
"""
Fix media storage configuration for Supabase
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pentora_platform.settings')
django.setup()

def check_and_fix_media_storage():
    """Check and fix media storage configuration"""
    print("🔍 Checking Media Storage Configuration...")
    print("=" * 50)
    
    # Check current settings
    print(f"Current DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"Current MEDIA_URL: {settings.MEDIA_URL}")
    
    # Check if Supabase credentials are properly loaded
    aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
    aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
    aws_bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', '')
    aws_endpoint = getattr(settings, 'AWS_S3_ENDPOINT_URL', '')
    aws_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', '')
    
    print(f"\nSupabase Configuration:")
    print(f"  AWS_ACCESS_KEY_ID: {'✅ Set' if aws_access_key else '❌ Not set'}")
    print(f"  AWS_SECRET_ACCESS_KEY: {'✅ Set' if aws_secret_key else '❌ Not set'}")
    print(f"  AWS_STORAGE_BUCKET_NAME: {aws_bucket}")
    print(f"  AWS_S3_ENDPOINT_URL: {aws_endpoint}")
    print(f"  AWS_S3_CUSTOM_DOMAIN: {aws_domain}")
    
    # Check if the issue is with the settings logic
    if aws_access_key and aws_secret_key:
        print("\n✅ Supabase credentials are present")
        print("The issue might be in the settings logic or environment variables")
        
        # Test the storage backend directly
        try:
            from pentora_platform.storage_backends import SupabaseMediaStorage
            storage = SupabaseMediaStorage()
            print(f"✅ SupabaseMediaStorage can be instantiated")
            
            # Test a simple operation
            from django.core.files.base import ContentFile
            test_content = b"Test content"
            test_filename = "test_supabase_storage.txt"
            
            saved_path = storage.save(test_filename, ContentFile(test_content))
            print(f"✅ Test file saved: {saved_path}")
            
            if storage.exists(saved_path):
                print(f"✅ File exists in Supabase storage")
                file_url = storage.url(saved_path)
                print(f"✅ File URL: {file_url}")
                
                # Clean up
                storage.delete(saved_path)
                print(f"✅ Test file cleaned up")
            else:
                print(f"❌ File does not exist in storage")
                
        except Exception as e:
            print(f"❌ Error testing Supabase storage: {e}")
    else:
        print("\n❌ Supabase credentials are missing")
        print("Please set the following environment variables:")
        print("  AWS_ACCESS_KEY_ID")
        print("  AWS_SECRET_ACCESS_KEY")
        print("  AWS_STORAGE_BUCKET_NAME")
        print("  AWS_S3_ENDPOINT_URL")
        print("  AWS_S3_CUSTOM_DOMAIN")

def main():
    """Main function"""
    print("🚀 Media Storage Configuration Check")
    print("=" * 60)
    
    check_and_fix_media_storage()
    
    print("\n" + "=" * 60)
    print("📋 Next Steps:")
    print("1. If Supabase credentials are missing, set them via Fly.io secrets")
    print("2. If credentials are present but not working, check the endpoint URL")
    print("3. Deploy again after fixing any issues")

if __name__ == "__main__":
    main() 