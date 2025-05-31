#!/usr/bin/env python
"""
Setup and Test Email System
Configure email settings and test email verification functionality
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from users.models import User, EmailVerification

def check_email_configuration():
    """Check current email configuration"""
    print("🔧 CHECKING EMAIL CONFIGURATION")
    print("=" * 50)
    
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'Not set'}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Check if using console backend
    if 'console' in settings.EMAIL_BACKEND.lower():
        print("\n⚠️  WARNING: Using console email backend!")
        print("Emails will be printed to console, not sent to recipients.")
        print("To send real emails, update your .env file with:")
        print("EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
        print("EMAIL_HOST_USER=your-email@gmail.com")
        print("EMAIL_HOST_PASSWORD=your-app-password")
        return False
    
    # Check if credentials are set
    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
        print("\n❌ ERROR: Email credentials not configured!")
        print("Please set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in your .env file")
        return False
    
    print("\n✅ Email configuration looks good!")
    return True

def test_basic_email(recipient_email):
    """Test sending a basic email"""
    print(f"\n📧 TESTING BASIC EMAIL TO: {recipient_email}")
    print("=" * 50)
    
    try:
        send_mail(
            subject='Test Email from Mentora',
            message='This is a test email to verify your email configuration is working correctly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        print("✅ Basic email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send basic email: {e}")
        return False

def test_verification_email(recipient_email):
    """Test sending a verification email"""
    print(f"\n🔐 TESTING VERIFICATION EMAIL TO: {recipient_email}")
    print("=" * 50)
    
    try:
        # Create a test user if doesn't exist
        user, created = User.objects.get_or_create(
            email=recipient_email,
            defaults={
                'username': User.generate_username_from_email(recipient_email),
                'first_name': 'Test',
                'last_name': 'User',
                'is_email_verified': False
            }
        )
        
        if created:
            print(f"Created test user: {user.email}")
        else:
            print(f"Using existing user: {user.email}")
        
        # Create verification token
        verification = EmailVerification.create_verification(user)
        print(f"Created verification token: {verification.token}")
        
        # Send verification email
        from users.views import RegisterView
        register_view = RegisterView()
        register_view.send_verification_email(user, verification)
        
        print("✅ Verification email sent successfully!")
        print(f"🔗 Verification URL: http://localhost:8000/auth/verify-email/{verification.token}/")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send verification email: {e}")
        return False

def create_env_template():
    """Create .env template with email configuration"""
    print("\n📝 CREATING EMAIL CONFIGURATION TEMPLATE")
    print("=" * 50)
    
    env_content = """
# ===========================================
# EMAIL CONFIGURATION FOR MENTORA
# ===========================================

# For Development (emails printed to console)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# For Production (real emails via Gmail)
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# DEFAULT_FROM_EMAIL=Mentora <noreply@mentora.com>

# ===========================================
# HOW TO SET UP GMAIL FOR SENDING EMAILS
# ===========================================
# 1. Go to your Google Account settings
# 2. Enable 2-Factor Authentication
# 3. Generate an "App Password" for Mentora
# 4. Use your Gmail address as EMAIL_HOST_USER
# 5. Use the App Password as EMAIL_HOST_PASSWORD
# 6. Update EMAIL_BACKEND to smtp.EmailBackend
# ===========================================
"""
    
    try:
        with open('.env.email.example', 'w') as f:
            f.write(env_content.strip())
        print("✅ Created .env.email.example file")
        print("📋 Copy the settings to your .env file and update with your credentials")
    except Exception as e:
        print(f"❌ Failed to create template: {e}")

def provide_setup_instructions():
    """Provide detailed setup instructions"""
    print("\n📚 EMAIL SETUP INSTRUCTIONS")
    print("=" * 50)
    
    instructions = """
🔧 FOR DEVELOPMENT (Console Emails):
   Add to your .env file:
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   
   Emails will be printed to the console where you run the server.

📧 FOR PRODUCTION (Real Emails via Gmail):
   
   Step 1: Set up Gmail App Password
   • Go to https://myaccount.google.com/
   • Security → 2-Step Verification (enable if not already)
   • Security → App passwords → Generate password for "Mentora"
   
   Step 2: Update your .env file:
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-character-app-password
   DEFAULT_FROM_EMAIL=Mentora <noreply@mentora.com>
   
   Step 3: Restart your Django server
   
🌐 FOR PYTHONANYWHERE:
   • Update your .env file on PythonAnywhere with the same settings
   • Restart your web app
   • Test with a real email address

⚠️  SECURITY NOTES:
   • Never commit your .env file to Git
   • Use App Passwords, not your regular Gmail password
   • Keep your email credentials secure
"""
    
    print(instructions)

def main():
    """Main function to setup and test email system"""
    print("🎯 MENTORA EMAIL SYSTEM SETUP & TEST")
    print("=" * 60)
    
    # Check current configuration
    config_ok = check_email_configuration()
    
    # Create template
    create_env_template()
    
    # Provide instructions
    provide_setup_instructions()
    
    # Test emails if configuration is ready
    if config_ok:
        test_email = input("\n📧 Enter an email address to test with (or press Enter to skip): ").strip()
        if test_email:
            print(f"\nTesting emails with: {test_email}")
            
            # Test basic email
            basic_ok = test_basic_email(test_email)
            
            # Test verification email
            if basic_ok:
                verification_ok = test_verification_email(test_email)
                
                if verification_ok:
                    print("\n🎉 EMAIL SYSTEM IS WORKING!")
                    print("Users will now receive verification emails when they register.")
            else:
                print("\n❌ EMAIL SYSTEM NEEDS CONFIGURATION")
                print("Please check your email settings and try again.")
    else:
        print("\n⚙️  CONFIGURE EMAIL SETTINGS FIRST")
        print("Follow the instructions above to set up email sending.")

if __name__ == '__main__':
    main()
