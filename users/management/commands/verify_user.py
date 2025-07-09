from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import User, EmailVerification


class Command(BaseCommand):
    help = 'Manually verify a user\'s email address'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email address of the user to verify',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force verification even if already verified',
        )

    def handle(self, *args, **options):
        email = options['email'].strip().lower()
        force = options.get('force', False)

        try:
            user = User.objects.get(email=email)
            
            self.stdout.write(f"Found user: {user.email}")
            self.stdout.write(f"Current name: {user.get_full_name()}")
            self.stdout.write(f"Date joined: {user.date_joined}")
            self.stdout.write(f"Current verification status: {'✅ Verified' if user.is_email_verified else '❌ Not verified'}")

            if user.is_email_verified and not force:
                self.stdout.write(self.style.WARNING('User is already verified. Use --force to verify anyway.'))
                return

            # Verify the user with proper transaction handling
            with transaction.atomic():
                user.is_email_verified = True
                user.save(update_fields=['is_email_verified'])

                # Mark all verification tokens as used
                tokens_updated = EmailVerification.objects.filter(
                    user=user,
                    is_used=False
                ).update(is_used=True)

            self.stdout.write(self.style.SUCCESS(f'✅ Successfully verified {user.email}'))
            self.stdout.write(f'🧹 Marked {tokens_updated} verification tokens as used')

            # Show final status
            user.refresh_from_db()
            self.stdout.write(f"Final verification status: {'✅ Verified' if user.is_email_verified else '❌ Not verified'}")

        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ User with email {email} not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error verifying user: {str(e)}'))
