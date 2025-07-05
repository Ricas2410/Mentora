from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from billing.models import BillingSettings

User = get_user_model()


class Command(BaseCommand):
    help = 'Send billing activation announcement to all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be sent without actually sending emails',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Limit number of emails to send (for testing)',
        )

    def handle(self, *args, **options):
        billing_settings = BillingSettings.get_settings()
        
        if not billing_settings.is_enabled:
            self.stdout.write(
                self.style.ERROR('Billing is not enabled. Enable billing first.')
            )
            return
        
        # Get all active users
        users = User.objects.filter(is_active=True, is_email_verified=True)
        
        if options['limit']:
            users = users[:options['limit']]
            
        total_users = users.count()
        
        if options['dry_run']:
            self.stdout.write(f'DRY RUN: Would send announcement emails to {total_users} users')
            for user in users[:5]:  # Show first 5 users
                self.stdout.write(f'  - {user.email} ({user.get_full_name()})')
            if total_users > 5:
                self.stdout.write(f'  ... and {total_users - 5} more users')
            return
        
        self.stdout.write(f'Sending billing announcement to {total_users} users...')
        
        # Prepare email data
        subject = '🎉 Exciting News: Premium Subscription Plans Are Now Available!'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        messages = []
        for user in users:
            # Render email content
            html_content = render_to_string('billing/emails/announcement.html', {
                'user': user,
                'billing_settings': billing_settings,
                'site_url': settings.SITE_URL,
            })
            
            text_content = render_to_string('billing/emails/announcement.txt', {
                'user': user,
                'billing_settings': billing_settings,
                'site_url': settings.SITE_URL,
            })
            
            messages.append((
                subject,
                text_content,
                from_email,
                [user.email]
            ))
        
        # Send emails in batches
        try:
            send_mass_mail(messages, fail_silently=False)
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully sent {len(messages)} announcement emails!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error sending emails: {str(e)}')
            )
        
        # Update billing settings to mark announcement as sent
        billing_settings.announcement_sent = True
        billing_settings.save()
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('📧 Billing announcement campaign complete!'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Monitor user signups and subscriptions')
        self.stdout.write('2. Check analytics dashboard for engagement')
        self.stdout.write('3. Follow up with users who haven\'t subscribed')
        self.stdout.write(f'\nAnnouncement page: {settings.SITE_URL}/billing/announcement/')
