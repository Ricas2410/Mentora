from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import User, EmailVerification
from users.views import RegisterView


class Command(BaseCommand):
    help = 'Test email verification system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to test with',
            default='test@example.com'
        )
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Clean up test user after testing',
        )

    def handle(self, *args, **options):
        email = options['email']
        cleanup = options['cleanup']
        
        self.stdout.write(
            self.style.SUCCESS(f'🧪 Testing email verification system with: {email}')
        )
        
        # Check email backend
        self.stdout.write(f"📧 Email Backend: {settings.EMAIL_BACKEND}")
        
        if 'console' in settings.EMAIL_BACKEND.lower():
            self.stdout.write(
                self.style.WARNING("⚠️  Using console backend - emails will appear in terminal")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("✅ Using SMTP backend - emails will be sent")
            )
        
        try:
            # Clean up existing test user if requested
            if cleanup:
                try:
                    existing_user = User.objects.get(email=email)
                    existing_user.delete()
                    self.stdout.write(f"🗑️  Cleaned up existing user: {email}")
                except User.DoesNotExist:
                    pass
            
            # Create test user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': User.generate_username_from_email(email),
                    'first_name': 'Test',
                    'last_name': 'User',
                    'is_email_verified': False
                }
            )
            
            if created:
                user.set_password('testpassword123')
                user.save()
                self.stdout.write(f"👤 Created test user: {email}")
            else:
                self.stdout.write(f"👤 Using existing user: {email}")
            
            # Create verification token
            verification = EmailVerification.create_verification(user)
            self.stdout.write(f"🔑 Created verification token: {verification.token}")
            
            # Test sending verification email
            register_view = RegisterView()
            email_sent = register_view.send_verification_email(user, verification)
            
            if email_sent:
                self.stdout.write(
                    self.style.SUCCESS("✅ Verification email sent successfully!")
                )
                
                # Show verification URL
                verification_url = f"http://localhost:8000/auth/verify-email/{verification.token}/"
                self.stdout.write(f"🔗 Verification URL: {verification_url}")
                
                if 'console' in settings.EMAIL_BACKEND.lower():
                    self.stdout.write(
                        self.style.WARNING("📺 Check the console output above for the email content")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"📬 Email sent to: {email}")
                    )
                
                # Test verification process
                self.stdout.write("\n🔍 Testing verification process...")
                
                # Verify the token works
                if not verification.is_expired() and not verification.is_used:
                    self.stdout.write("✅ Verification token is valid")
                    
                    # You can manually verify by visiting the URL
                    self.stdout.write(
                        f"🌐 Visit this URL to complete verification: {verification_url}"
                    )
                else:
                    self.stdout.write("❌ Verification token is invalid or expired")
                
            else:
                self.stdout.write(
                    self.style.ERROR("❌ Failed to send verification email")
                )
            
            # Show user status
            user.refresh_from_db()
            self.stdout.write(f"\n👤 User Status:")
            self.stdout.write(f"   Email: {user.email}")
            self.stdout.write(f"   Verified: {user.is_email_verified}")
            self.stdout.write(f"   Created: {user.date_joined}")
            
            # Cleanup if requested
            if cleanup and created:
                user.delete()
                self.stdout.write(f"🗑️  Cleaned up test user: {email}")
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error during testing: {e}")
            )
            
        self.stdout.write(
            self.style.SUCCESS("\n🎉 Email verification test completed!")
        )
