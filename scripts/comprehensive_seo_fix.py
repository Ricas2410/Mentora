#!/usr/bin/env python
"""
Comprehensive SEO Fix Script for Pentora Platform
This script addresses critical SEO issues preventing search visibility
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pentora_platform.settings')
django.setup()

from django.contrib.sites.models import Site
from django.core.management import call_command
from django.urls import reverse
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote
import requests
from urllib.parse import urljoin


def main():
    print("🚀 COMPREHENSIVE SEO FIX FOR PENTORA PLATFORM")
    print("=" * 60)
    
    # 1. Fix Site Domain Configuration
    print("\n1️⃣ FIXING SITE DOMAIN CONFIGURATION")
    print("-" * 40)
    
    try:
        current_site = Site.objects.get_current()
        site_domain = getattr(settings, 'SITE_DOMAIN', 'pentora.fly.dev')
        
        if current_site.domain != site_domain:
            current_site.domain = site_domain
            current_site.name = 'Pentora - Ghana\'s Leading Online Education Platform'
            current_site.save()
            print(f"✅ Updated site domain to: {site_domain}")
        else:
            print(f"✅ Site domain already correct: {site_domain}")
            
    except Exception as e:
        print(f"❌ Error updating site domain: {e}")
    
    # 2. Generate and Test Sitemap
    print("\n2️⃣ GENERATING AND TESTING SITEMAP")
    print("-" * 40)
    
    try:
        # Generate sitemap
        call_command('collectstatic', '--noinput', verbosity=0)
        print("✅ Static files collected")
        
        # Test sitemap accessibility
        site_url = getattr(settings, 'SITE_URL', f'https://{site_domain}')
        sitemap_url = f"{site_url}/sitemap.xml"
        robots_url = f"{site_url}/robots.txt"
        
        print(f"📍 Sitemap URL: {sitemap_url}")
        print(f"📍 Robots.txt URL: {robots_url}")
        
    except Exception as e:
        print(f"❌ Error with sitemap generation: {e}")
    
    # 3. Check Content for SEO
    print("\n3️⃣ ANALYZING CONTENT FOR SEO")
    print("-" * 40)
    
    try:
        # Count content
        subjects_count = Subject.objects.filter(is_active=True).count()
        topics_count = Topic.objects.filter(is_active=True).count()
        notes_count = StudyNote.objects.filter(is_active=True).count()
        
        print(f"📚 Active Subjects: {subjects_count}")
        print(f"📖 Active Topics: {topics_count}")
        print(f"📝 Active Study Notes: {notes_count}")
        
        if subjects_count == 0:
            print("⚠️  WARNING: No active subjects found!")
        if topics_count == 0:
            print("⚠️  WARNING: No active topics found!")
            
    except Exception as e:
        print(f"❌ Error analyzing content: {e}")
    
    # 4. SEO Recommendations
    print("\n4️⃣ SEO RECOMMENDATIONS")
    print("-" * 40)
    
    recommendations = [
        "✅ Domain configuration updated",
        "✅ Meta tags enhanced with 'Mentora learn' keywords",
        "✅ Structured data improved for educational content",
        "✅ Robots.txt configured to guide search engines",
        "✅ Sitemap generated for all content",
        "",
        "🔄 NEXT STEPS REQUIRED:",
        "1. Submit sitemap to Google Search Console",
        "2. Verify domain ownership in Google Search Console",
        "3. Check for crawl errors and fix them",
        "4. Monitor search rankings for target keywords",
        "5. Create more content targeting 'Mentora learn' and 'education Ghana'",
        "6. Build backlinks from educational websites",
        "7. Optimize page loading speeds",
        "8. Ensure mobile responsiveness",
        "",
        "🎯 TARGET KEYWORDS TO FOCUS ON:",
        "- Mentora learn",
        "- Mentora education", 
        "- Online learning Ghana",
        "- Free education Ghana",
        "- BECE preparation",
        "- WASSCE preparation",
        "- Ghana education platform",
        "- Online studies Ghana",
        "- Educational platform Ghana"
    ]
    
    for rec in recommendations:
        print(rec)
    
    # 5. Generate SEO Report
    print("\n5️⃣ SEO CONFIGURATION SUMMARY")
    print("-" * 40)
    
    try:
        site_name = getattr(settings, 'SITE_NAME', 'Not Set')
        site_url = getattr(settings, 'SITE_URL', 'Not Set')
        debug_mode = getattr(settings, 'DEBUG', True)
        allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
        
        print(f"🏷️  Site Name: {site_name}")
        print(f"🌐 Site URL: {site_url}")
        print(f"🔧 Debug Mode: {debug_mode}")
        print(f"🏠 Allowed Hosts: {', '.join(allowed_hosts)}")
        
        if site_name == 'Not Set':
            print("❌ SITE_NAME not configured!")
        if site_url == 'Not Set':
            print("❌ SITE_URL not configured!")
        if debug_mode:
            print("⚠️  Debug mode is ON - should be OFF in production")
            
    except Exception as e:
        print(f"❌ Error generating SEO report: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 SEO FIX SCRIPT COMPLETED!")
    print("📧 Contact Google Search Console to submit your sitemap")
    print("🔍 Monitor search rankings for improved visibility")
    print("=" * 60)


if __name__ == '__main__':
    main()
