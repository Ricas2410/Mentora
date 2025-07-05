"""
Management command to clear broken image references
"""
from django.core.management.base import BaseCommand
from admin_panel.models import SiteSettings


class Command(BaseCommand):
    help = 'Clear broken image references from site settings'

    def handle(self, *args, **options):
        self.stdout.write("🧹 Clearing broken image references...")
        
        try:
            settings = SiteSettings.objects.first()
            if not settings:
                self.stdout.write("❌ No site settings found")
                return
            
            # Clear the broken image fields
            settings.site_logo = None
            settings.hero_banner = None
            settings.site_favicon = None
            settings.save()
            
            self.stdout.write("✅ Cleared broken image references")
            self.stdout.write("ℹ️  You can now upload new images through the admin interface")
            
        except Exception as e:
            self.stdout.write(f"❌ Failed to clear images: {str(e)}")
            
        self.stdout.write("✅ Cleanup completed!")
