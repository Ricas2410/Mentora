#!/usr/bin/env python3
"""
Script to fix email verification URLs for production deployment
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from django.contrib.sites.models import Site
from django.conf import settings


def main():
    print("🔧 FIXING EMAIL VERIFICATION URLS")
    print("=" * 50)
    
    # Get current configuration
    try:
        current_site = Site.objects.get_current()
        print(f"Current site domain: {current_site.domain}")
        print(f"Current site name: {current_site.name}")
    except Exception as e:
        print(f"Error getting current site: {e}")
        return
    
    # Check settings
    site_domain = getattr(settings, 'SITE_DOMAIN', 'localhost:8000')
    site_protocol = getattr(settings, 'SITE_PROTOCOL', 'http')
    
    print(f"Settings SITE_DOMAIN: {site_domain}")
    print(f"Settings SITE_PROTOCOL: {site_protocol}")
    
    # Detect if we need to update
    if current_site.domain == 'localhost:8000' and 'pythonanywhere.com' in site_domain:
        print("\n⚠️  DOMAIN MISMATCH DETECTED!")
        print("The Sites framework still has localhost:8000 but your settings have a production domain.")
        print("Updating Sites framework to match settings...")
        
        # Update the site
        current_site.domain = site_domain
        current_site.name = f'Mentora ({site_domain})'
        current_site.save()
        
        print(f"✅ Updated site domain to: {site_domain}")
        
    elif current_site.domain == site_domain:
        print("✅ Site domain is correctly configured!")
        
    else:
        print(f"\n❓ Manual check needed:")
        print(f"   Sites framework domain: {current_site.domain}")
        print(f"   Settings domain: {site_domain}")
        
        response = input("\nUpdate Sites framework to match settings? (y/n): ")
        if response.lower() == 'y':
            current_site.domain = site_domain
            current_site.name = f'Mentora ({site_domain})'
            current_site.save()
            print(f"✅ Updated site domain to: {site_domain}")
    
    # Test URL generation
    print(f"\n🔗 Email verification URLs will now use:")
    print(f"   {site_protocol}://{site_domain}/auth/verify-email/[token]/")
    
    print("\n📧 NEXT STEPS:")
    print("1. Make sure your .env file has the correct SITE_DOMAIN and SITE_PROTOCOL")
    print("2. Restart your web application")
    print("3. Test email verification with a new user registration")
    
    print("\n✅ Email verification fix complete!")


if __name__ == '__main__':
    main()
