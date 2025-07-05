from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    BillingSettings, SubscriptionPlan, UserSubscription,
    PaymentMethod, Payment, BillingEvent
)


@admin.register(BillingSettings)
class BillingSettingsAdmin(admin.ModelAdmin):
    list_display = ['billing_enabled', 'free_trial_days', 'stripe_enabled', 'paypal_enabled']

    fieldsets = (
        ('Billing Activation', {
            'fields': ('billing_enabled', 'free_trial_days', 'grace_period_days'),
            'classes': ('wide',),
        }),
        ('Stripe Configuration', {
            'fields': ('stripe_enabled', 'stripe_public_key', 'stripe_secret_key', 'stripe_webhook_secret'),
            'classes': ('collapse',),
        }),
        ('PayPal Configuration', {
            'fields': ('paypal_enabled', 'paypal_client_id', 'paypal_client_secret', 'paypal_sandbox'),
            'classes': ('collapse',),
        }),
        ('Email Settings', {
            'fields': ('send_billing_emails', 'billing_email_from'),
            'classes': ('wide',),
        }),
        ('Announcements', {
            'fields': ('show_billing_announcement', 'announcement_title', 'announcement_message', 'announcement_type'),
            'classes': ('wide',),
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not BillingSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'monthly_price', 'yearly_price', 'yearly_discount_display', 'subject_count_display', 'is_active', 'is_featured', 'sort_order']
    list_filter = ['is_active', 'is_featured', 'priority_support', 'advanced_analytics', 'offline_access']
    list_editable = ['is_active', 'is_featured', 'sort_order']
    search_fields = ['name', 'description']
    ordering = ['sort_order', 'monthly_price']
    filter_horizontal = ['allowed_subjects']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description'),
        }),
        ('Pricing', {
            'fields': ('monthly_price', 'yearly_price'),
            'description': 'Set monthly price (required) and yearly price (optional). Leave yearly price blank to disable yearly subscription option.',
        }),
        ('Subject/Class Access', {
            'fields': ('allowed_subjects', 'max_subjects'),
            'description': 'Select specific subjects this plan can access, or leave empty for unlimited access. Max subjects setting is ignored if specific subjects are selected.',
        }),
        ('Features', {
            'fields': ('max_quizzes_per_day', 'priority_support', 'advanced_analytics', 'offline_access'),
        }),
        ('Plan Management', {
            'fields': ('is_active', 'is_featured', 'sort_order'),
        }),
        ('Legacy Fields', {
            'fields': ('price', 'billing_cycle'),
            'classes': ('collapse',),
            'description': 'Legacy fields for backward compatibility. Will be deprecated.',
        }),
        ('Payment Provider IDs', {
            'fields': ('stripe_price_id', 'paypal_plan_id'),
            'classes': ('collapse',),
        }),
    )

    def yearly_discount_display(self, obj):
        if obj.has_yearly_option:
            discount = obj.yearly_discount_percentage
            return f"{discount}% off" if discount > 0 else "No discount"
        return "No yearly option"
    yearly_discount_display.short_description = 'Yearly Discount'

    def save_model(self, request, obj, form, change):
        # Auto-update legacy price field for backward compatibility
        obj.price = obj.monthly_price
        super().save_model(request, obj, form, change)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'plan_name', 'status', 'current_period_end', 'auto_renew']
    list_filter = ['status', 'plan', 'auto_renew', 'cancel_at_period_end']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at', 'stripe_subscription_id', 'paypal_subscription_id']

    fieldsets = (
        ('Subscription Details', {
            'fields': ('user', 'plan', 'status'),
        }),
        ('Dates', {
            'fields': ('trial_start', 'trial_end', 'current_period_start',
                      'current_period_end', 'canceled_at', 'ended_at'),
        }),
        ('Billing Settings', {
            'fields': ('auto_renew', 'cancel_at_period_end'),
        }),
        ('Provider Data', {
            'fields': ('stripe_subscription_id', 'paypal_subscription_id'),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def plan_name(self, obj):
        return obj.plan.name
    plan_name.short_description = 'Plan'


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'payment_type', 'card_display', 'is_default', 'is_active']
    list_filter = ['payment_type', 'is_default', 'is_active', 'card_brand']
    search_fields = ['user__email', 'card_last_four']
    readonly_fields = ['created_at', 'updated_at']

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def card_display(self, obj):
        if obj.payment_type == 'card':
            return f"{obj.card_brand} ****{obj.card_last_four}"
        return obj.get_payment_type_display()
    card_display.short_description = 'Payment Method'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'amount', 'currency', 'status', 'payment_type', 'provider', 'created_at']
    list_filter = ['status', 'payment_type', 'provider', 'currency']
    search_fields = ['user__email', 'provider_payment_id', 'description']
    readonly_fields = ['created_at', 'processed_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Payment Details', {
            'fields': ('user', 'subscription', 'amount', 'currency', 'status', 'payment_type'),
        }),
        ('Provider Information', {
            'fields': ('provider', 'provider_payment_id', 'provider_fee', 'receipt_url'),
        }),
        ('Additional Information', {
            'fields': ('description', 'failure_reason'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at'),
        }),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'


@admin.register(BillingEvent)
class BillingEventAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'event_type', 'description_short', 'created_at']
    list_filter = ['event_type', 'created_at']
    search_fields = ['user__email', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
