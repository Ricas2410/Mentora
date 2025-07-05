import requests
import json
import hashlib
import hmac
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from .models import BillingSettings, Payment, UserSubscription
import logging

logger = logging.getLogger(__name__)


class PaystackService:
    """Service class for Paystack payment integration"""
    
    def __init__(self):
        self.billing_settings = BillingSettings.get_settings()
        self.secret_key = self.billing_settings.paystack_secret_key
        self.public_key = self.billing_settings.paystack_public_key
        self.test_mode = self.billing_settings.paystack_test_mode
        
        # Paystack API endpoints
        if self.test_mode:
            self.base_url = "https://api.paystack.co"
        else:
            self.base_url = "https://api.paystack.co"
    
    def get_headers(self):
        """Get headers for Paystack API requests"""
        return {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }
    
    def initialize_payment(self, user, plan, billing_cycle='monthly', callback_url=None):
        """Initialize a payment transaction"""
        try:
            amount = plan.get_paystack_amount(billing_cycle)
            
            # Create payment record
            payment = Payment.objects.create(
                user=user,
                amount=plan.get_monthly_price_ghs() if billing_cycle == 'monthly' else plan.get_yearly_price_ghs(),
                currency='GHS',
                status='pending',
                payment_method='paystack',
                metadata={
                    'plan_id': str(plan.id),
                    'billing_cycle': billing_cycle,
                    'amount_pesewas': amount,
                }
            )
            
            # Prepare Paystack payload
            payload = {
                'email': user.email,
                'amount': amount,  # Amount in pesewas
                'currency': 'GHS',
                'reference': f"Pentora_{payment.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}",
                'callback_url': callback_url or f"{settings.SITE_URL}/billing/paystack/callback/",
                'metadata': {
                    'payment_id': str(payment.id),
                    'user_id': str(user.id),
                    'plan_id': str(plan.id),
                    'billing_cycle': billing_cycle,
                    'custom_fields': [
                        {
                            'display_name': 'Plan',
                            'variable_name': 'plan',
                            'value': plan.name
                        },
                        {
                            'display_name': 'Billing Cycle',
                            'variable_name': 'billing_cycle',
                            'value': billing_cycle.title()
                        }
                    ]
                }
            }
            
            # Make API request to Paystack
            response = requests.post(
                f"{self.base_url}/transaction/initialize",
                headers=self.get_headers(),
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['status']:
                    # Update payment with Paystack reference
                    payment.provider_transaction_id = data['data']['reference']
                    payment.metadata.update({
                        'paystack_access_code': data['data']['access_code'],
                        'authorization_url': data['data']['authorization_url']
                    })
                    payment.save()
                    
                    return {
                        'success': True,
                        'payment_id': payment.id,
                        'authorization_url': data['data']['authorization_url'],
                        'access_code': data['data']['access_code'],
                        'reference': data['data']['reference']
                    }
                else:
                    logger.error(f"Paystack initialization failed: {data['message']}")
                    payment.status = 'failed'
                    payment.save()
                    return {'success': False, 'error': data['message']}
            else:
                logger.error(f"Paystack API error: {response.status_code} - {response.text}")
                payment.status = 'failed'
                payment.save()
                return {'success': False, 'error': 'Payment initialization failed'}
                
        except Exception as e:
            logger.error(f"Paystack initialization error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def verify_payment(self, reference):
        """Verify a payment transaction"""
        try:
            response = requests.get(
                f"{self.base_url}/transaction/verify/{reference}",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['status']:
                    return {
                        'success': True,
                        'data': data['data']
                    }
                else:
                    return {'success': False, 'error': data['message']}
            else:
                return {'success': False, 'error': 'Verification failed'}
                
        except Exception as e:
            logger.error(f"Paystack verification error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def process_webhook(self, payload, signature):
        """Process Paystack webhook"""
        try:
            # Verify webhook signature
            if not self.verify_webhook_signature(payload, signature):
                return {'success': False, 'error': 'Invalid signature'}
            
            event_data = json.loads(payload)
            event_type = event_data.get('event')
            
            if event_type == 'charge.success':
                return self.handle_successful_payment(event_data['data'])
            elif event_type == 'charge.failed':
                return self.handle_failed_payment(event_data['data'])
            else:
                logger.info(f"Unhandled webhook event: {event_type}")
                return {'success': True, 'message': 'Event not handled'}
                
        except Exception as e:
            logger.error(f"Webhook processing error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def verify_webhook_signature(self, payload, signature):
        """Verify Paystack webhook signature"""
        try:
            computed_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha512
            ).hexdigest()
            return hmac.compare_digest(computed_signature, signature)
        except Exception:
            return False
    
    def handle_successful_payment(self, payment_data):
        """Handle successful payment"""
        try:
            reference = payment_data['reference']
            metadata = payment_data.get('metadata', {})
            payment_id = metadata.get('payment_id')
            
            if not payment_id:
                logger.error(f"No payment_id in metadata for reference: {reference}")
                return {'success': False, 'error': 'Payment ID not found'}
            
            # Update payment record
            payment = Payment.objects.get(id=payment_id)
            payment.status = 'completed'
            payment.provider_transaction_id = reference
            payment.completed_at = timezone.now()
            payment.metadata.update({
                'paystack_response': payment_data
            })
            payment.save()
            
            # Create or update subscription
            plan_id = metadata.get('plan_id')
            billing_cycle = metadata.get('billing_cycle', 'monthly')
            
            if plan_id:
                from .models import SubscriptionPlan
                plan = SubscriptionPlan.objects.get(id=plan_id)
                
                # Calculate subscription period
                if billing_cycle == 'yearly':
                    from dateutil.relativedelta import relativedelta
                    end_date = timezone.now() + relativedelta(years=1)
                else:
                    from dateutil.relativedelta import relativedelta
                    end_date = timezone.now() + relativedelta(months=1)
                
                # Create or update subscription
                subscription, created = UserSubscription.objects.get_or_create(
                    user=payment.user,
                    defaults={
                        'plan': plan,
                        'status': 'active',
                        'current_period_start': timezone.now(),
                        'current_period_end': end_date,
                        'billing_cycle': billing_cycle,
                    }
                )
                
                if not created:
                    # Update existing subscription
                    subscription.plan = plan
                    subscription.status = 'active'
                    subscription.current_period_start = timezone.now()
                    subscription.current_period_end = end_date
                    subscription.billing_cycle = billing_cycle
                    subscription.save()
                
                logger.info(f"Subscription {'created' if created else 'updated'} for user {payment.user.email}")
            
            return {'success': True, 'message': 'Payment processed successfully'}
            
        except Exception as e:
            logger.error(f"Error handling successful payment: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def handle_failed_payment(self, payment_data):
        """Handle failed payment"""
        try:
            reference = payment_data['reference']
            metadata = payment_data.get('metadata', {})
            payment_id = metadata.get('payment_id')
            
            if payment_id:
                payment = Payment.objects.get(id=payment_id)
                payment.status = 'failed'
                payment.metadata.update({
                    'paystack_response': payment_data,
                    'failure_reason': payment_data.get('gateway_response', 'Payment failed')
                })
                payment.save()
                
                logger.info(f"Payment failed for reference: {reference}")
            
            return {'success': True, 'message': 'Failed payment processed'}
            
        except Exception as e:
            logger.error(f"Error handling failed payment: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_exchange_rate(self):
        """Get current USD to GHS exchange rate (placeholder for future API integration)"""
        # This could be integrated with a currency API like exchangerate-api.com
        # For now, return the manual rate from settings
        return self.billing_settings.usd_to_ghs_rate
