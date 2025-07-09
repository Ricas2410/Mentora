from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User, EmailVerification


class Command(BaseCommand):
    help = 'Fix email verification issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to fix verification for',
        )
        parser.add_argument(
            '--verify',
            action='store_true',
            help='Mark user as verified',
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean up old verification tokens',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List verification status for all users',
        )

    def handle(self, *args, **options):
        email = options.get('email')
        verify = options.get('verify')
        clean = options.get('clean')
        list_users = options.get('list')

        if list_users:
            self.list_verification_status()
            return

        if not email:
            self.stdout.write(self.style.ERROR('Please provide an email address with --email'))
            return

        try:
            user = User.objects.get(email=email)
            self.stdout.write(f"Found user: {user.email}")
            self.stdout.write(f"Current verification status: {'✅ Verified' if user.is_email_verified else '❌ Not verified'}")

            # Show verification tokens
            verifications = EmailVerification.objects.filter(user=user).order_by('-created_at')
            self.stdout.write(f"\nVerification tokens for {user.email}:")
            for i, v in enumerate(verifications[:5]):  # Show last 5
                status = "✅ Valid" if not v.is_used and not v.is_expired() else "❌ Invalid"
                expired = "⏰ Expired" if v.is_expired() else "✅ Active"
                used = "🔒 Used" if v.is_used else "🔓 Unused"
                self.stdout.write(f"  {i+1}. {v.token[:20]}... - {status} - {expired} - {used}")

            if verify:
                user.is_email_verified = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Marked {user.email} as verified'))

            if clean:
                # Mark old tokens as used
                old_count = EmailVerification.objects.filter(user=user, is_used=False).update(is_used=True)
                self.stdout.write(self.style.SUCCESS(f'🧹 Cleaned up {old_count} old verification tokens'))

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with email {email} not found'))

    def list_verification_status(self):
        """List verification status for all users"""
        users = User.objects.all().order_by('-date_joined')
        
        self.stdout.write("\n📊 Email Verification Status:")
        self.stdout.write("-" * 80)
        
        verified_count = 0
        unverified_count = 0
        
        for user in users:
            status = "✅ Verified" if user.is_email_verified else "❌ Not verified"
            pending_tokens = EmailVerification.objects.filter(
                user=user, 
                is_used=False, 
                expires_at__gt=timezone.now()
            ).count()
            
            token_info = f"({pending_tokens} pending tokens)" if pending_tokens > 0 else ""
            
            self.stdout.write(f"{user.email:<40} {status} {token_info}")
            
            if user.is_email_verified:
                verified_count += 1
            else:
                unverified_count += 1
        
        self.stdout.write("-" * 80)
        self.stdout.write(f"Total: {verified_count} verified, {unverified_count} unverified")
