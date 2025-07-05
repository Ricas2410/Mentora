from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from users.models import User, EmailVerification


class Command(BaseCommand):
    help = 'Test email functionality'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email address to send test to')

    def handle(self, *args, **options):
        email = options.get('email')
        if not email:
            self.stdout.write(self.style.ERROR('Please provide an email address with --email'))
            return

        try:
            # Test basic email
            send_mail(
                'Test Email from Pentora',
                'This is a test email to verify the email configuration is working.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Test email sent successfully to {email}'))

            # Test verification email template
            from django.template.loader import render_to_string
            from django.core.mail import EmailMultiAlternatives
            
            # Create a dummy verification for testing
            context = {
                'user': {'first_name': 'Test', 'email': email},
                'verification_url': 'http://localhost:8000/auth/verify-email/test-token/',
                'site_name': 'Pentora',
            }
            
            subject = 'Test Verification Email - Pentora'
            text_content = render_to_string('emails/verification_email.txt', context)
            html_content = render_to_string('emails/verification_email.html', context)
            
            email_msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()
            
            self.stdout.write(self.style.SUCCESS(f'Verification email template test sent to {email}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))
