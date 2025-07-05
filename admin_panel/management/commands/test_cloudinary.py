"""
Management command to test Cloudinary storage connectivity
"""
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import cloudinary
import cloudinary.uploader


class Command(BaseCommand):
    help = 'Test Cloudinary storage connectivity and upload'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing Cloudinary connectivity...")

        try:
            # Check Cloudinary configuration
            self.stdout.write(f"☁️  Cloud Name: {settings.CLOUDINARY_CLOUD_NAME}")
            self.stdout.write(f"🔑 API Key: {settings.CLOUDINARY_API_KEY[:8]}...")
            self.stdout.write(f"🌐 Media URL: {settings.MEDIA_URL}")
            self.stdout.write(f"📦 Storage Backend: {settings.DEFAULT_FILE_STORAGE}")

            # Test file upload using Django storage
            self.stdout.write("\n📤 Testing file upload via Django storage...")
            test_content = "Test file for Cloudinary storage"
            test_file = ContentFile(test_content.encode('utf-8'))

            try:
                # Upload file
                file_path = default_storage.save('test/cloudinary_test.txt', test_file)
                file_url = default_storage.url(file_path)

                self.stdout.write(f"✅ File uploaded successfully: {file_path}")
                self.stdout.write(f"🔗 File URL: {file_url}")

                # Test if file exists
                if default_storage.exists(file_path):
                    self.stdout.write("✅ File exists in storage")
                else:
                    self.stdout.write("❌ File does not exist in storage")

                # Clean up test file
                default_storage.delete(file_path)
                self.stdout.write("🗑️  Test file cleaned up")

            except Exception as upload_error:
                self.stdout.write(f"❌ Django storage upload failed: {str(upload_error)}")
                import traceback
                self.stdout.write(f"📋 Traceback: {traceback.format_exc()}")
            
            # Test direct Cloudinary upload
            self.stdout.write("\n📤 Testing direct Cloudinary upload...")
            result = cloudinary.uploader.upload(
                "data:text/plain;base64,VGVzdCBmaWxlIGZvciBDbG91ZGluYXJ5",
                public_id="test/direct_upload_test",
                resource_type="raw"
            )
            
            self.stdout.write(f"✅ Direct upload successful: {result['public_id']}")
            self.stdout.write(f"🔗 Direct upload URL: {result['secure_url']}")
            
            # Clean up direct upload
            cloudinary.uploader.destroy("test/direct_upload_test", resource_type="raw")
            self.stdout.write("🗑️  Direct upload test file cleaned up")
            
        except Exception as e:
            self.stdout.write(f"❌ Cloudinary test failed: {str(e)}")
            self.stdout.write("💡 Check your Cloudinary credentials")
            
        self.stdout.write("\n✅ Cloudinary test completed!")
