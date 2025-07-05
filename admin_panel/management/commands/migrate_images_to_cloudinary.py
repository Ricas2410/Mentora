"""
Management command to migrate existing images to Cloudinary
"""
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from admin_panel.models import SiteSettings
import os
import requests


class Command(BaseCommand):
    help = 'Migrate existing images from local storage to Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write("🔄 Migrating existing images to Cloudinary...")
        
        try:
            # Get site settings
            settings = SiteSettings.objects.first()
            if not settings:
                self.stdout.write("❌ No site settings found")
                return
            
            self.stdout.write("📋 Found site settings, checking images...")
            
            # Check each image field
            images_to_migrate = []
            
            if settings.site_logo:
                images_to_migrate.append(('logo', settings.site_logo))
            if settings.hero_banner:
                images_to_migrate.append(('banner', settings.hero_banner))
            if settings.site_favicon:
                images_to_migrate.append(('favicon', settings.site_favicon))
            
            if not images_to_migrate:
                self.stdout.write("ℹ️  No images found to migrate")
                return
            
            self.stdout.write(f"📸 Found {len(images_to_migrate)} images to migrate")
            
            for image_type, image_field in images_to_migrate:
                self.stdout.write(f"\n🔄 Processing {image_type}...")
                
                try:
                    # Get the current file path
                    current_path = image_field.name
                    self.stdout.write(f"📁 Current path: {current_path}")
                    
                    # Check if file exists locally
                    local_path = os.path.join('media', current_path)
                    if os.path.exists(local_path):
                        self.stdout.write(f"✅ Found local file: {local_path}")
                        
                        # Read the file
                        with open(local_path, 'rb') as f:
                            file_content = f.read()
                        
                        # Create a new file object
                        file_obj = ContentFile(file_content)
                        file_obj.name = os.path.basename(current_path)
                        
                        # Upload to Cloudinary via Django storage
                        new_path = default_storage.save(current_path, file_obj)
                        new_url = default_storage.url(new_path)
                        
                        self.stdout.write(f"✅ Uploaded to Cloudinary: {new_path}")
                        self.stdout.write(f"🔗 New URL: {new_url}")
                        
                        # Update the model field
                        if image_type == 'banner':
                            settings.hero_banner = new_path
                        else:
                            setattr(settings, f'site_{image_type}', new_path)
                        
                    else:
                        self.stdout.write(f"⚠️  Local file not found: {local_path}")
                        self.stdout.write("🔄 Trying to download from current URL...")
                        
                        # Try to download from current URL
                        try:
                            current_url = image_field.url
                            response = requests.get(current_url, timeout=10)
                            if response.status_code == 200:
                                file_content = response.content
                                file_obj = ContentFile(file_content)
                                file_obj.name = os.path.basename(current_path)
                                
                                # Upload to Cloudinary
                                new_path = default_storage.save(current_path, file_obj)
                                new_url = default_storage.url(new_path)
                                
                                self.stdout.write(f"✅ Downloaded and uploaded: {new_path}")
                                self.stdout.write(f"🔗 New URL: {new_url}")
                                
                                # Update the model field
                                if image_type == 'banner':
                                    settings.hero_banner = new_path
                                else:
                                    setattr(settings, f'site_{image_type}', new_path)
                            else:
                                self.stdout.write(f"❌ Failed to download: HTTP {response.status_code}")
                        except Exception as download_error:
                            self.stdout.write(f"❌ Download failed: {str(download_error)}")
                
                except Exception as e:
                    self.stdout.write(f"❌ Failed to migrate {image_type}: {str(e)}")
            
            # Save the updated settings
            settings.save()
            self.stdout.write("\n✅ Site settings updated!")
            
        except Exception as e:
            self.stdout.write(f"❌ Migration failed: {str(e)}")
            import traceback
            self.stdout.write(f"📋 Traceback: {traceback.format_exc()}")
            
        self.stdout.write("\n✅ Image migration completed!")
