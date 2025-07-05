from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import BillingSettings, UserSubscription


class BillingMiddleware:
    """
    Middleware to check subscription status and restrict access when billing is enabled.
    Only applies when billing is globally enabled.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that are always accessible (even with expired subscription)
        self.public_urls = [
            '/',
            '/login/',
            '/register/',
            '/logout/',
            '/about/',
            '/contact/',
            '/help/',
            '/privacy/',
            '/terms/',
            '/billing/',
            '/billing/plans/',
            '/billing/subscribe/',
            '/billing/payment/',
            '/billing/success/',
            '/billing/cancel/',
            '/billing/webhook/',
            '/admin/',
        ]
        
        # URL patterns that require active subscription
        self.subscription_required_patterns = [
            '/dashboard/',
            '/subjects/',
            '/quiz/',
            '/study/',
            '/progress/',
            '/exam/',
            '/take/',
            '/result/',
        ]
    
    def __call__(self, request):
        # Skip middleware if billing is not enabled
        billing_settings = BillingSettings.get_settings()
        if not billing_settings.billing_enabled:
            return self.get_response(request)
        
        # Skip for unauthenticated users on public URLs
        if not request.user.is_authenticated:
            if self.is_public_url(request.path):
                return self.get_response(request)
            else:
                return self.redirect_to_login(request)
        
        # Skip for superusers and staff
        if request.user.is_superuser or request.user.is_staff:
            return self.get_response(request)
        
        # Skip for public URLs
        if self.is_public_url(request.path):
            return self.get_response(request)
        
        # Check subscription status for protected URLs
        if self.requires_subscription(request.path):
            subscription = self.get_user_subscription(request.user)
            
            if not subscription:
                return self.redirect_to_billing(request, "Please choose a subscription plan to continue.")
            
            if not subscription.is_active:
                if subscription.status == 'past_due':
                    return self.redirect_to_billing(request, "Your subscription payment is past due. Please update your payment method.")
                elif subscription.status == 'canceled':
                    return self.redirect_to_billing(request, "Your subscription has been canceled. Please subscribe to continue.")
                else:
                    return self.redirect_to_billing(request, "Your subscription is not active. Please check your billing status.")
        
        return self.get_response(request)
    
    def is_public_url(self, path):
        """Check if URL is publicly accessible"""
        return any(path.startswith(url) for url in self.public_urls)
    
    def requires_subscription(self, path):
        """Check if URL requires active subscription"""
        return any(path.startswith(pattern) for pattern in self.subscription_required_patterns)
    
    def get_user_subscription(self, user):
        """Get user's subscription"""
        try:
            return user.subscription
        except UserSubscription.DoesNotExist:
            return None
    
    def redirect_to_login(self, request):
        """Redirect to login page"""
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Authentication required',
                'login_url': reverse('users:login')
            }, status=401)
        
        messages.info(request, "Please sign in to continue.")
        return redirect('users:login')
    
    def redirect_to_billing(self, request, message):
        """Redirect to billing page with message"""
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Subscription required',
                'message': message,
                'billing_url': reverse('billing:plans')
            }, status=402)  # Payment Required
        
        messages.warning(request, message)
        return redirect('billing:plans')


class UsageLimitMiddleware:
    """
    Middleware to track and enforce usage limits based on subscription plan.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that count towards usage limits
        self.usage_tracked_patterns = [
            '/quiz/take/',
            '/exam/take/',
        ]
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only track for authenticated users when billing is enabled
        billing_settings = BillingSettings.get_settings()
        if not billing_settings.billing_enabled or not request.user.is_authenticated:
            return response
        
        # Skip for superusers and staff
        if request.user.is_superuser or request.user.is_staff:
            return response
        
        # Track usage for specific endpoints
        if self.should_track_usage(request.path, request.method):
            self.track_usage(request.user, request.path)
        
        return response
    
    def should_track_usage(self, path, method):
        """Check if this request should count towards usage limits"""
        if method != 'POST':  # Only track actual quiz/exam submissions
            return False
        
        return any(path.startswith(pattern) for pattern in self.usage_tracked_patterns)
    
    def track_usage(self, user, path):
        """Track usage for the user"""
        try:
            subscription = user.subscription
            limits = subscription.get_usage_limits()
            
            # Track daily quiz usage
            if '/quiz/take/' in path and limits['max_quizzes_per_day']:
                from .models import BillingEvent
                today = timezone.now().date()
                
                # Count today's quiz attempts
                daily_quizzes = BillingEvent.objects.filter(
                    user=user,
                    event_type='quiz_attempt',
                    created_at__date=today
                ).count()
                
                # Log the attempt
                BillingEvent.objects.create(
                    user=user,
                    event_type='quiz_attempt',
                    description=f"Quiz attempt on {path}",
                    metadata={'path': path, 'daily_count': daily_quizzes + 1}
                )
                
        except UserSubscription.DoesNotExist:
            pass  # No subscription, no limits to track
