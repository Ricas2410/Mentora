#!/usr/bin/env python
"""
Test real email sending with the SMTP settings
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_settings():
    """Test current email settings"""
    print("🔧 CURRENT EMAIL SETTINGS:")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Not set'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")

def test_real_email():
    """Test sending a real email"""
    print("\n📧 TESTING REAL EMAIL SENDING...")

    try:
        # Test with a real email address
        test_email = input("Enter your email address to test: ").strip()
        if not test_email:
            test_email = "skillnetservices@gmail.com"  # Send to self for testing

        print(f"Sending test email to: {test_email}")

        # Use Django's send_mail with custom connection
        from django.core.mail import get_connection, EmailMessage

        # Create custom connection
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='smtp.gmail.com',
            port=587,
            username='skillnetservices@gmail.com',
            password='tdms ckdk tmgo fado',
            use_tls=True,
            fail_silently=False,
        )

        # Create and send email
        email = EmailMessage(
            subject='🎓 Mentora Email Test - Success!',
            body='''Hello!

This is a test email from your Mentora Learning Platform.

✅ Email configuration is working correctly!
✅ SMTP connection successful
✅ Authentication successful

Your email verification system is now ready to send real emails to users.

Best regards,
The Mentora Team

---
This email was sent from: skillnetservices@gmail.com
Platform: Mentora Learning Platform
''',
            from_email='Mentora <skillnetservices@gmail.com>',
            to=[test_email],
            connection=connection,
        )

        email.send()

        print("✅ EMAIL SENT SUCCESSFULLY!")
        print(f"📬 Check the inbox for: {test_email}")
        print("🎉 Your email system is working!")

        return True

    except Exception as e:
        print(f"❌ FAILED TO SEND EMAIL: {e}")
        print("\n🔍 TROUBLESHOOTING:")
        print("1. Check your internet connection")
        print("2. Verify Gmail credentials are correct")
        print("3. Make sure 2FA is enabled and you're using an App Password")
        print("4. Check if Gmail is blocking the connection")

        return False

def update_env_file():
    """Update .env file to force SMTP backend"""
    print("\n📝 UPDATING .ENV FILE...")
    
    try:
        # Read current .env file
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update EMAIL_BACKEND line
        updated_lines = []
        for line in lines:
            if line.startswith('EMAIL_BACKEND='):
                updated_lines.append('EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend\n')
                print("✅ Updated EMAIL_BACKEND to smtp.EmailBackend")
            else:
                updated_lines.append(line)
        
        # Write back to .env file
        with open('.env', 'w') as f:
            f.writelines(updated_lines)
        
        print("✅ .env file updated successfully!")
        print("🔄 Please restart your Django server to apply changes")
        
    except Exception as e:
        print(f"❌ Failed to update .env file: {e}")

def main():
    """Main function"""
    print("🎯 MENTORA EMAIL SYSTEM TEST")
    print("=" * 50)
    
    # Show current settings
    test_email_settings()
    
    # Update .env file
    update_env_file()
    
    # Test real email sending
    if test_real_email():
        print("\n🎉 SUCCESS! Your email system is ready!")
        print("Users will now receive real verification emails when they register.")
    else:
        print("\n❌ EMAIL SYSTEM NEEDS ATTENTION")
        print("Please check the troubleshooting steps above.")

if __name__ == '__main__':
    main()
