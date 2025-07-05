from .models import BillingSettings


def billing_context(request):
    """
    Add billing-related context to all templates.
    This allows billing announcements and status to be shown globally.
    """
    billing_settings = BillingSettings.get_settings()
    
    context = {
        'billing_enabled': billing_settings.billing_enabled,
        'show_billing_announcement': billing_settings.show_billing_announcement,
        'billing_announcement': {
            'title': billing_settings.announcement_title,
            'message': billing_settings.announcement_message,
            'type': billing_settings.announcement_type,
        } if billing_settings.show_billing_announcement else None,
    }
    
    # Add user subscription status if authenticated
    if request.user.is_authenticated:
        try:
            subscription = request.user.subscription
            context.update({
                'user_subscription': subscription,
                'user_subscription_active': subscription.is_active,
                'user_subscription_trial': subscription.is_trial,
                'user_subscription_expires_soon': subscription.days_until_expiry is not None and subscription.days_until_expiry <= 7,
            })
        except:
            context.update({
                'user_subscription': None,
                'user_subscription_active': not billing_settings.billing_enabled,  # Active if billing disabled
                'user_subscription_trial': False,
                'user_subscription_expires_soon': False,
            })
    
    return context
