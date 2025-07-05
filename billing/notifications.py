from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .models import BillingSettings, BillingEvent
import logging

logger = logging.getLogger(__name__)


class BillingNotificationService:
    """Service for sending billing-related email notifications"""
    
    def __init__(self):
        self.billing_settings = BillingSettings.get_settings()
    
    def should_send_email(self):
        """Check if billing emails are enabled"""
        return self.billing_settings.send_billing_emails
    
    def get_from_email(self):
        """Get the from email address for billing notifications"""
        return self.billing_settings.billing_email_from or settings.DEFAULT_FROM_EMAIL
    
    def send_subscription_created(self, subscription):
        """Send email when subscription is created"""
        if not self.should_send_email():
            return False
        
        try:
            subject = f"Welcome to {subscription.plan.name}!"
            
            context = {
                'user': subscription.user,
                'subscription': subscription,
                'plan': subscription.plan,
                'billing_settings': self.billing_settings,
            }
            
            # Render email templates
            html_message = render_to_string('billing/emails/subscription_created.html', context)
            text_message = render_to_string('billing/emails/subscription_created.txt', context)
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email=self.get_from_email(),
                recipient_list=[subscription.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Log the event
            BillingEvent.objects.create(
                user=subscription.user,
                subscription=subscription,
                event_type='subscription_created',
                description=f"Welcome email sent for {subscription.plan.name}",
                metadata={'email_sent': True}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send subscription created email to {subscription.user.email}: {e}")
            return False
    
    def send_subscription_canceled(self, subscription):
        """Send email when subscription is canceled"""
        if not self.should_send_email():
            return False
        
        try:
            subject = "Your subscription has been canceled"
            
            context = {
                'user': subscription.user,
                'subscription': subscription,
                'plan': subscription.plan,
                'billing_settings': self.billing_settings,
            }
            
            html_message = render_to_string('billing/emails/subscription_canceled.html', context)
            text_message = render_to_string('billing/emails/subscription_canceled.txt', context)
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email=self.get_from_email(),
                recipient_list=[subscription.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send subscription canceled email to {subscription.user.email}: {e}")
            return False
    
    def send_payment_failed(self, payment):
        """Send email when payment fails"""
        if not self.should_send_email():
            return False
        
        try:
            subject = "Payment failed - Action required"
            
            context = {
                'user': payment.user,
                'payment': payment,
                'subscription': payment.subscription,
                'billing_settings': self.billing_settings,
            }
            
            html_message = render_to_string('billing/emails/payment_failed.html', context)
            text_message = render_to_string('billing/emails/payment_failed.txt', context)
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email=self.get_from_email(),
                recipient_list=[payment.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send payment failed email to {payment.user.email}: {e}")
            return False
    
    def send_trial_ending_reminder(self, subscription, days_left):
        """Send email reminder when trial is ending"""
        if not self.should_send_email():
            return False
        
        try:
            subject = f"Your free trial ends in {days_left} day{'s' if days_left != 1 else ''}"
            
            context = {
                'user': subscription.user,
                'subscription': subscription,
                'plan': subscription.plan,
                'days_left': days_left,
                'billing_settings': self.billing_settings,
            }
            
            html_message = render_to_string('billing/emails/trial_ending.html', context)
            text_message = render_to_string('billing/emails/trial_ending.txt', context)
            
            send_mail(
                subject=subject,
                message=text_message,
                from_email=self.get_from_email(),
                recipient_list=[subscription.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send trial ending email to {subscription.user.email}: {e}")
            return False
    
    def send_billing_activation_announcement(self, users_queryset):
        """Send email to all users announcing billing activation"""
        if not self.should_send_email():
            return 0
        
        sent_count = 0
        
        for user in users_queryset:
            try:
                subject = "Important Update: Subscription Plans Now Available"
                
                context = {
                    'user': user,
                    'billing_settings': self.billing_settings,
                }
                
                html_message = render_to_string('billing/emails/billing_activation.html', context)
                text_message = render_to_string('billing/emails/billing_activation.txt', context)
                
                send_mail(
                    subject=subject,
                    message=text_message,
                    from_email=self.get_from_email(),
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                sent_count += 1
                
            except Exception as e:
                logger.error(f"Failed to send billing activation email to {user.email}: {e}")
        
        return sent_count


# Convenience functions
def send_subscription_created_email(subscription):
    """Send subscription created email"""
    service = BillingNotificationService()
    return service.send_subscription_created(subscription)


def send_subscription_canceled_email(subscription):
    """Send subscription canceled email"""
    service = BillingNotificationService()
    return service.send_subscription_canceled(subscription)


def send_payment_failed_email(payment):
    """Send payment failed email"""
    service = BillingNotificationService()
    return service.send_payment_failed(payment)


def send_trial_ending_reminder(subscription, days_left):
    """Send trial ending reminder email"""
    service = BillingNotificationService()
    return service.send_trial_ending_reminder(subscription, days_left)


def send_billing_activation_announcement(users_queryset):
    """Send billing activation announcement to users"""
    service = BillingNotificationService()
    return service.send_billing_activation_announcement(users_queryset)
