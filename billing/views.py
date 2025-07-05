from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from .models import (
    BillingSettings, SubscriptionPlan, UserSubscription,
    PaymentMethod, Payment, BillingEvent
)
import json
import logging
from .paystack import PaystackService

logger = logging.getLogger(__name__)


class BillingPlansView(TemplateView):
    """Display available subscription plans"""
    template_name = 'billing/plans.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        billing_settings = BillingSettings.get_settings()

        context.update({
            'billing_enabled': billing_settings.billing_enabled,
            'plans': SubscriptionPlan.objects.filter(is_active=True).order_by('sort_order', 'price'),
            'current_subscription': self.get_current_subscription(),
            'billing_settings': billing_settings,
        })
        return context

    def get_current_subscription(self):
        """Get current user's subscription if authenticated"""
        if self.request.user.is_authenticated:
            try:
                return self.request.user.subscription
            except UserSubscription.DoesNotExist:
                return None
        return None


class BillingDashboardView(LoginRequiredMixin, TemplateView):
    """User billing dashboard"""
    template_name = 'billing/dashboard.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get subscription
        try:
            subscription = user.subscription
        except UserSubscription.DoesNotExist:
            subscription = None

        # Get payment history
        payments = Payment.objects.filter(user=user).order_by('-created_at')[:10]

        # Get payment methods
        payment_methods = PaymentMethod.objects.filter(user=user, is_active=True)

        context.update({
            'subscription': subscription,
            'payments': payments,
            'payment_methods': payment_methods,
            'billing_settings': BillingSettings.get_settings(),
        })
        return context


class SubscribeView(LoginRequiredMixin, View):
    """Handle subscription creation"""
    login_url = '/login/'

    def get(self, request, plan_id):
        """Show subscription confirmation page"""
        plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
        billing_cycle = request.GET.get('cycle', 'monthly')

        # Validate billing cycle
        if billing_cycle == 'yearly' and not plan.has_yearly_option:
            billing_cycle = 'monthly'

        # Check if user already has a subscription
        try:
            current_subscription = request.user.subscription
            if current_subscription.is_active:
                messages.info(request, "You already have an active subscription.")
                return redirect('billing:dashboard')
        except UserSubscription.DoesNotExist:
            current_subscription = None

        context = {
            'plan': plan,
            'billing_cycle': billing_cycle,
            'selected_price': plan.get_price_for_cycle(billing_cycle),
            'current_subscription': current_subscription,
            'billing_settings': BillingSettings.get_settings(),
        }
        return render(request, 'billing/subscribe.html', context)

    def post(self, request, plan_id):
        """Process subscription"""
        plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
        billing_settings = BillingSettings.get_settings()
        billing_cycle = request.POST.get('billing_cycle', 'monthly')

        # Validate billing cycle
        if billing_cycle == 'yearly' and not plan.has_yearly_option:
            billing_cycle = 'monthly'

        if not billing_settings.billing_enabled:
            messages.error(request, "Billing is currently disabled.")
            return redirect('billing:plans')

        try:
            with transaction.atomic():
                # Create or update subscription
                subscription, created = UserSubscription.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'plan': plan,
                        'status': 'trialing' if billing_settings.free_trial_days > 0 else 'active',
                        'trial_start': timezone.now() if billing_settings.free_trial_days > 0 else None,
                        'trial_end': timezone.now() + timezone.timedelta(days=billing_settings.free_trial_days) if billing_settings.free_trial_days > 0 else None,
                        'current_period_start': timezone.now(),
                        'current_period_end': self.calculate_period_end(plan, billing_cycle),
                    }
                )

                if not created:
                    # Update existing subscription
                    subscription.plan = plan
                    subscription.status = 'active'
                    subscription.current_period_start = timezone.now()
                    subscription.current_period_end = self.calculate_period_end(plan, billing_cycle)
                    subscription.save()

                # Log event
                BillingEvent.objects.create(
                    user=request.user,
                    subscription=subscription,
                    event_type='subscription_created' if created else 'subscription_updated',
                    description=f"Subscribed to {plan.name} ({billing_cycle})",
                    metadata={
                        'plan_id': str(plan.id),
                        'plan_name': plan.name,
                        'billing_cycle': billing_cycle,
                        'price': str(plan.get_price_for_cycle(billing_cycle))
                    }
                )

                messages.success(request, f"Successfully subscribed to {plan.name} ({billing_cycle})!")
                return redirect('billing:dashboard')

        except Exception as e:
            logger.error(f"Subscription error for user {request.user.id}: {e}")
            messages.error(request, "An error occurred while processing your subscription. Please try again.")
            return redirect('billing:plans')

    def calculate_period_end(self, plan, billing_cycle='monthly'):
        """Calculate subscription period end date"""
        now = timezone.now()
        if billing_cycle == 'monthly':
            return now + timezone.timedelta(days=30)
        elif billing_cycle == 'quarterly':
            return now + timezone.timedelta(days=90)
        elif billing_cycle == 'yearly':
            return now + timezone.timedelta(days=365)
        elif billing_cycle == 'lifetime':
            return now + timezone.timedelta(days=36500)  # 100 years
        return now + timezone.timedelta(days=30)


class CancelSubscriptionView(LoginRequiredMixin, View):
    """Handle subscription cancellation"""
    login_url = '/login/'

    def post(self, request):
        """Cancel user's subscription"""
        try:
            subscription = request.user.subscription

            if not subscription.is_active:
                messages.error(request, "No active subscription to cancel.")
                return redirect('billing:dashboard')

            # Cancel subscription
            subscription.status = 'canceled'
            subscription.canceled_at = timezone.now()
            subscription.auto_renew = False
            subscription.save()

            # Log event
            BillingEvent.objects.create(
                user=request.user,
                subscription=subscription,
                event_type='subscription_canceled',
                description="Subscription canceled by user",
                metadata={'canceled_at': subscription.canceled_at.isoformat()}
            )

            messages.success(request, "Your subscription has been canceled.")
            return redirect('billing:dashboard')

        except UserSubscription.DoesNotExist:
            messages.error(request, "No subscription found.")
            return redirect('billing:plans')


class ReactivateSubscriptionView(LoginRequiredMixin, View):
    """Handle subscription reactivation"""
    login_url = '/login/'

    def post(self, request):
        """Reactivate user's subscription"""
        try:
            subscription = request.user.subscription

            if subscription.status != 'canceled':
                messages.error(request, "Subscription is not canceled.")
                return redirect('billing:dashboard')

            # Reactivate subscription
            subscription.status = 'active'
            subscription.canceled_at = None
            subscription.auto_renew = True
            subscription.current_period_start = timezone.now()
            subscription.current_period_end = self.calculate_period_end(subscription.plan)
            subscription.save()

            # Log event
            BillingEvent.objects.create(
                user=request.user,
                subscription=subscription,
                event_type='subscription_updated',
                description="Subscription reactivated by user",
                metadata={'reactivated_at': timezone.now().isoformat()}
            )

            messages.success(request, "Your subscription has been reactivated.")
            return redirect('billing:dashboard')

        except UserSubscription.DoesNotExist:
            messages.error(request, "No subscription found.")
            return redirect('billing:plans')

    def calculate_period_end(self, plan):
        """Calculate subscription period end date"""
        now = timezone.now()
        if plan.billing_cycle == 'monthly':
            return now + timezone.timedelta(days=30)
        elif plan.billing_cycle == 'quarterly':
            return now + timezone.timedelta(days=90)
        elif plan.billing_cycle == 'yearly':
            return now + timezone.timedelta(days=365)
        elif plan.billing_cycle == 'lifetime':
            return now + timezone.timedelta(days=36500)
        return now + timezone.timedelta(days=30)


class BillingWebhookView(View):
    """Handle payment provider webhooks"""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        """Process webhook from payment provider"""
        try:
            payload = request.body
            provider = request.GET.get('provider', 'stripe')

            if provider == 'stripe':
                return self.handle_stripe_webhook(payload, request)
            elif provider == 'paypal':
                return self.handle_paypal_webhook(payload, request)
            else:
                return HttpResponse(status=400)

        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return HttpResponse(status=500)

    def handle_stripe_webhook(self, payload, request):
        """Handle Stripe webhook"""
        # This would integrate with Stripe's webhook handling
        # For now, return success
        return HttpResponse(status=200)

    def handle_paypal_webhook(self, payload, request):
        """Handle PayPal webhook"""
        # This would integrate with PayPal's webhook handling
        # For now, return success
        return HttpResponse(status=200)


@login_required
def billing_status_api(request):
    """API endpoint to check user's billing status"""
    try:
        subscription = request.user.subscription
        data = {
            'has_subscription': True,
            'is_active': subscription.is_active,
            'status': subscription.status,
            'plan_name': subscription.plan.name,
            'current_period_end': subscription.current_period_end.isoformat() if subscription.current_period_end else None,
            'days_until_expiry': subscription.days_until_expiry,
            'usage_limits': subscription.get_usage_limits(),
        }
    except UserSubscription.DoesNotExist:
        data = {
            'has_subscription': False,
            'is_active': not BillingSettings.get_settings().billing_enabled,  # Active if billing disabled
            'status': 'none',
            'plan_name': None,
            'current_period_end': None,
            'days_until_expiry': None,
            'usage_limits': {'max_subjects': None, 'max_quizzes_per_day': None},
        }

    return JsonResponse(data)


class PaystackPaymentView(LoginRequiredMixin, View):
    """Initialize Paystack payment"""

    def post(self, request):
        try:
            data = json.loads(request.body)
            plan_id = data.get('plan_id')
            billing_cycle = data.get('billing_cycle', 'monthly')

            if not plan_id:
                return JsonResponse({'success': False, 'error': 'Plan ID required'})

            plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)

            # Initialize Paystack payment
            paystack = PaystackService()
            callback_url = request.build_absolute_uri('/billing/paystack/callback/')

            result = paystack.initialize_payment(
                user=request.user,
                plan=plan,
                billing_cycle=billing_cycle,
                callback_url=callback_url
            )

            if result['success']:
                return JsonResponse({
                    'success': True,
                    'authorization_url': result['authorization_url'],
                    'reference': result['reference']
                })
            else:
                return JsonResponse({'success': False, 'error': result['error']})

        except Exception as e:
            logger.error(f"Paystack payment initialization error: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Payment initialization failed'})


class PaystackCallbackView(LoginRequiredMixin, View):
    """Handle Paystack payment callback"""

    def get(self, request):
        reference = request.GET.get('reference')

        if not reference:
            messages.error(request, 'Invalid payment reference')
            return redirect('billing:plans')

        # Verify payment with Paystack
        paystack = PaystackService()
        result = paystack.verify_payment(reference)

        if result['success']:
            payment_data = result['data']

            if payment_data['status'] == 'success':
                # Payment successful
                messages.success(request, 'Payment successful! Your subscription has been activated.')
                return redirect('billing:dashboard')
            else:
                # Payment failed
                messages.error(request, f"Payment failed: {payment_data.get('gateway_response', 'Unknown error')}")
                return redirect('billing:plans')
        else:
            messages.error(request, 'Payment verification failed')
            return redirect('billing:plans')


@method_decorator(csrf_exempt, name='dispatch')
class PaystackWebhookView(View):
    """Handle Paystack webhooks"""

    def post(self, request):
        try:
            payload = request.body.decode('utf-8')
            signature = request.META.get('HTTP_X_PAYSTACK_SIGNATURE', '')

            paystack = PaystackService()
            result = paystack.process_webhook(payload, signature)

            if result['success']:
                return HttpResponse('OK', status=200)
            else:
                logger.error(f"Webhook processing failed: {result['error']}")
                return HttpResponse('Error', status=400)

        except Exception as e:
            logger.error(f"Webhook error: {str(e)}")
            return HttpResponse('Error', status=500)


class CurrencyConversionView(LoginRequiredMixin, View):
    """Handle currency conversion for pricing display"""

    def get(self, request):
        try:
            plans = SubscriptionPlan.objects.filter(is_active=True).order_by('sort_order')
            currency = request.GET.get('currency', 'USD')

            plans_data = []
            for plan in plans:
                if currency == 'GHS':
                    monthly_price = plan.get_monthly_price_ghs()
                    yearly_price = plan.get_yearly_price_ghs()
                    currency_symbol = 'GH₵'
                else:
                    monthly_price = plan.monthly_price
                    yearly_price = plan.yearly_price
                    currency_symbol = '$'

                plans_data.append({
                    'id': str(plan.id),
                    'name': plan.name,
                    'monthly_price': float(monthly_price),
                    'yearly_price': float(yearly_price) if yearly_price else None,
                    'monthly_display': f"{currency_symbol}{monthly_price:.2f}",
                    'yearly_display': f"{currency_symbol}{yearly_price:.2f}" if yearly_price else None,
                    'currency': currency,
                })

            return JsonResponse({
                'success': True,
                'plans': plans_data,
                'exchange_rate': float(BillingSettings.get_settings().usd_to_ghs_rate)
            })

        except Exception as e:
            logger.error(f"Currency conversion error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})


class ActivationAnnouncementView(TemplateView):
    """Announcement page for when billing is first activated"""
    template_name = 'billing/activation_announcement.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['billing_settings'] = BillingSettings.get_settings()
        return context
