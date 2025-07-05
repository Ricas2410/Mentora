"""
Management command to test storage configuration
"""
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import tempfile
import os


class Command(BaseCommand):
    help = 'Test storage configuration and connectivity'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing storage configuration...")
        
        # Check storage backend
        self.stdout.write(f"📦 Storage backend: {settings.DEFAULT_FILE_STORAGE}")
        self.stdout.write(f"🌐 Media URL: {settings.MEDIA_URL}")
        
        # Check S3 settings
        if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
            self.stdout.write(f"🔑 AWS Access Key: {'✅ Set' if settings.AWS_ACCESS_KEY_ID else '❌ Not set'}")
            self.stdout.write(f"🪣 Bucket: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set')}")
            self.stdout.write(f"🌍 Region: {getattr(settings, 'AWS_S3_REGION_NAME', 'Not set')}")
            self.stdout.write(f"🔗 Endpoint: {getattr(settings, 'AWS_S3_ENDPOINT_URL', 'Default')}")
            self.stdout.write(f"🌐 Custom Domain: {getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', 'Not set')}")
        
        # Test file upload
        try:
            self.stdout.write("\n📤 Testing file upload...")
            
            # Create a test file
            test_content = "This is a test file for storage configuration."
            test_file = ContentFile(test_content.encode('utf-8'))
            
            # Upload the file
            file_path = default_storage.save('test/storage_test.txt', test_file)
            self.stdout.write(f"✅ File uploaded successfully: {file_path}")
            
            # Get the URL
            file_url = default_storage.url(file_path)
            self.stdout.write(f"🔗 File URL: {file_url}")
            
            # Check if file exists
            if default_storage.exists(file_path):
                self.stdout.write("✅ File exists in storage")
                
                # Clean up - delete the test file
                default_storage.delete(file_path)
                self.stdout.write("🗑️  Test file cleaned up")
            else:
                self.stdout.write("❌ File not found in storage")
                
        except Exception as e:
            self.stdout.write(f"❌ Storage test failed: {str(e)}")
            self.stdout.write("💡 Check your storage configuration and credentials")
            
        self.stdout.write("\n✅ Storage test completed!")
