from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid

User = get_user_model()


class BillingSettings(models.Model):
    """Global billing configuration - singleton model"""

    # Billing activation
    billing_enabled = models.BooleanField(
        default=False,
        help_text="Enable billing system globally"
    )
    free_trial_days = models.PositiveIntegerField(
        default=30,
        help_text="Number of free trial days for new users"
    )
    grace_period_days = models.PositiveIntegerField(
        default=7,
        help_text="Grace period after subscription expires"
    )

    # Payment providers
    stripe_enabled = models.BooleanField(default=False)
    stripe_public_key = models.CharField(max_length=200, blank=True)
    stripe_secret_key = models.CharField(max_length=200, blank=True)
    stripe_webhook_secret = models.CharField(max_length=200, blank=True)

    paypal_enabled = models.BooleanField(default=False)
    paypal_client_id = models.CharField(max_length=200, blank=True)
    paypal_client_secret = models.CharField(max_length=200, blank=True)
    paypal_sandbox = models.BooleanField(default=True)

    # Paystack configuration
    paystack_enabled = models.BooleanField(default=True, help_text="Enable Paystack payments")
    paystack_public_key = models.CharField(max_length=200, blank=True, help_text="Paystack public key")
    paystack_secret_key = models.CharField(max_length=200, blank=True, help_text="Paystack secret key")
    paystack_test_mode = models.BooleanField(default=True, help_text="Use Paystack test mode")

    # Currency settings
    base_currency = models.CharField(
        max_length=3,
        default='GHS',
        choices=[
            ('GHS', 'Ghana Cedi'),
            ('USD', 'US Dollar'),
            ('EUR', 'Euro'),
            ('GBP', 'British Pound'),
        ],
        help_text="Base currency for pricing"
    )
    usd_to_ghs_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal('12.0000'),
        help_text="Exchange rate from USD to GHS (manual override)"
    )
    auto_currency_conversion = models.BooleanField(
        default=False,
        help_text="Automatically fetch exchange rates (requires API)"
    )
    last_rate_update = models.DateTimeField(null=True, blank=True, help_text="Last exchange rate update")

    # Announcement tracking
    announcement_sent = models.BooleanField(default=False, help_text="Whether billing activation announcement has been sent")

    # Notifications
    send_billing_emails = models.BooleanField(
        default=True,
        help_text="Send billing-related emails to users"
    )
    billing_email_from = models.EmailField(
        default='billing@Pentora.com',
        help_text="From email for billing notifications"
    )

    # Announcements
    show_billing_announcement = models.BooleanField(
        default=False,
        help_text="Show billing announcement banner"
    )
    announcement_title = models.CharField(max_length=200, blank=True)
    announcement_message = models.TextField(blank=True)
    announcement_type = models.CharField(
        max_length=20,
        choices=[
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('success', 'Success'),
            ('error', 'Error'),
        ],
        default='info'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Billing Settings"
        verbose_name_plural = "Billing Settings"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and BillingSettings.objects.exists():
            raise ValueError("Only one BillingSettings instance is allowed")
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create billing settings"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    def __str__(self):
        return f"Billing Settings ({'Enabled' if self.billing_enabled else 'Disabled'})"


class SubscriptionPlan(models.Model):
    """Subscription plans available to users"""

    BILLING_CYCLES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('lifetime', 'Lifetime'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Pricing
    monthly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Monthly subscription price in USD"
    )
    yearly_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True, blank=True,
        help_text="Yearly subscription price in USD (leave blank to disable yearly option)"
    )

    # GHS Pricing (for Paystack)
    monthly_price_ghs = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True, blank=True,
        help_text="Monthly subscription price in GHS (auto-calculated if not set)"
    )
    yearly_price_ghs = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True, blank=True,
        help_text="Yearly subscription price in GHS (auto-calculated if not set)"
    )

    # Legacy field for backward compatibility
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Legacy price field - will be deprecated"
    )
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLES, default='monthly')

    # Class/Subject Access
    allowed_subjects = models.ManyToManyField(
        'subjects.Subject',
        blank=True,
        help_text="Specific subjects/classes this plan can access. Leave empty for unlimited access."
    )
    max_subjects = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Maximum subjects user can access (null = unlimited, overridden by allowed_subjects if set)"
    )

    # Features
    max_quizzes_per_day = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Maximum quizzes per day (null = unlimited)"
    )
    priority_support = models.BooleanField(default=False)
    advanced_analytics = models.BooleanField(default=False)
    offline_access = models.BooleanField(default=False)

    # Plan management
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    # Payment provider IDs
    stripe_price_id = models.CharField(max_length=100, blank=True)
    paypal_plan_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'price']
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"

    def __str__(self):
        return f"{self.name} - ${self.monthly_price}/month"

    @property
    def is_free(self):
        return self.monthly_price == 0

    @property
    def has_yearly_option(self):
        """Check if this plan offers yearly subscription"""
        return self.yearly_price is not None and self.yearly_price > 0

    def get_monthly_price_ghs(self):
        """Get monthly price in GHS"""
        if self.monthly_price_ghs:
            return self.monthly_price_ghs

        # Auto-convert from USD
        settings = BillingSettings.get_settings()
        return self.monthly_price * settings.usd_to_ghs_rate

    def get_yearly_price_ghs(self):
        """Get yearly price in GHS"""
        if self.yearly_price_ghs:
            return self.yearly_price_ghs

        if not self.yearly_price:
            return None

        # Auto-convert from USD
        settings = BillingSettings.get_settings()
        return self.yearly_price * settings.usd_to_ghs_rate

    def get_price_display(self, currency='USD', billing_cycle='monthly'):
        """Get formatted price display"""
        if currency == 'GHS':
            if billing_cycle == 'yearly' and self.has_yearly_option:
                price = self.get_yearly_price_ghs()
                return f"GH₵{price:.2f}/year" if price else None
            else:
                price = self.get_monthly_price_ghs()
                return f"GH₵{price:.2f}/month"
        else:  # USD
            if billing_cycle == 'yearly' and self.has_yearly_option:
                return f"${self.yearly_price:.2f}/year"
            else:
                return f"${self.monthly_price:.2f}/month"

    def get_paystack_amount(self, billing_cycle='monthly'):
        """Get amount in kobo (Paystack's smallest unit for GHS)"""
        if billing_cycle == 'yearly' and self.has_yearly_option:
            price_ghs = self.get_yearly_price_ghs()
        else:
            price_ghs = self.get_monthly_price_ghs()

        # Convert to pesewas (100 pesewas = 1 GHS)
        return int(price_ghs * 100)

    @property
    def yearly_discount_percentage(self):
        """Calculate yearly discount percentage"""
        if not self.has_yearly_option or self.monthly_price == 0:
            return 0
        monthly_yearly_total = self.monthly_price * 12
        if monthly_yearly_total == 0:
            return 0
        discount = ((monthly_yearly_total - self.yearly_price) / monthly_yearly_total) * 100
        return round(discount)

    def get_price_for_cycle(self, cycle='monthly'):
        """Get price for specific billing cycle"""
        if cycle == 'yearly' and self.has_yearly_option:
            return self.yearly_price
        return self.monthly_price

    def get_allowed_subjects(self):
        """Get subjects this plan can access"""
        if self.allowed_subjects.exists():
            return self.allowed_subjects.all()
        # If no specific subjects set, return all subjects (unlimited)
        from subjects.models import Subject
        return Subject.objects.filter(is_active=True)

    def can_access_subject(self, subject):
        """Check if this plan can access a specific subject"""
        if not self.allowed_subjects.exists():
            return True  # Unlimited access
        return self.allowed_subjects.filter(id=subject.id).exists()

    @property
    def subject_count_display(self):
        """Display string for subject access"""
        if not self.allowed_subjects.exists():
            return "All subjects"
        count = self.allowed_subjects.count()
        return f"{count} subject{'s' if count != 1 else ''}"


class UserSubscription(models.Model):
    """User's subscription to a plan"""

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('trialing', 'Trial'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('unpaid', 'Unpaid'),
        ('incomplete', 'Incomplete'),
        ('incomplete_expired', 'Incomplete Expired'),
        ('paused', 'Paused'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)

    # Subscription status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trialing')

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    trial_start = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    # Payment provider data
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    paypal_subscription_id = models.CharField(max_length=100, blank=True)

    # Billing
    auto_renew = models.BooleanField(default=True)
    cancel_at_period_end = models.BooleanField(default=False)

    # Metadata
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Subscription"
        verbose_name_plural = "User Subscriptions"

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"

    @property
    def is_active(self):
        """Check if subscription is currently active"""
        if not BillingSettings.get_settings().billing_enabled:
            return True  # Always active when billing is disabled

        return self.status in ['active', 'trialing']

    @property
    def is_trial(self):
        """Check if user is in trial period"""
        return self.status == 'trialing'

    @property
    def days_until_expiry(self):
        """Days until subscription expires"""
        if not self.current_period_end:
            return None

        delta = self.current_period_end - timezone.now()
        return delta.days if delta.days > 0 else 0

    @property
    def is_past_due(self):
        """Check if subscription is past due"""
        return self.status == 'past_due'

    def can_access_feature(self, feature):
        """Check if user can access a specific feature"""
        if not BillingSettings.get_settings().billing_enabled:
            return True

        if not self.is_active:
            return False

        # Check plan features
        if feature == 'priority_support':
            return self.plan.priority_support
        elif feature == 'advanced_analytics':
            return self.plan.advanced_analytics
        elif feature == 'offline_access':
            return self.plan.offline_access

        return True

    def get_usage_limits(self):
        """Get usage limits for the current plan"""
        if not BillingSettings.get_settings().billing_enabled:
            return {
                'max_subjects': None,
                'max_quizzes_per_day': None,
            }

        return {
            'max_subjects': self.plan.max_subjects,
            'max_quizzes_per_day': self.plan.max_quizzes_per_day,
        }


class PaymentMethod(models.Model):
    """User's saved payment methods"""

    PAYMENT_TYPES = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')

    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Card details (masked)
    card_last_four = models.CharField(max_length=4, blank=True)
    card_brand = models.CharField(max_length=20, blank=True)  # visa, mastercard, etc.
    card_exp_month = models.PositiveIntegerField(null=True, blank=True)
    card_exp_year = models.PositiveIntegerField(null=True, blank=True)

    # Payment provider IDs
    stripe_payment_method_id = models.CharField(max_length=100, blank=True)
    paypal_payment_method_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        if self.payment_type == 'card':
            return f"{self.card_brand} ****{self.card_last_four}"
        return f"{self.get_payment_type_display()}"


class Payment(models.Model):
    """Payment transactions"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]

    PAYMENT_TYPES = [
        ('subscription', 'Subscription'),
        ('one_time', 'One-time Payment'),
        ('upgrade', 'Plan Upgrade'),
        ('refund', 'Refund'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='payments'
    )

    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='subscription')

    # Payment provider data
    provider = models.CharField(max_length=20, blank=True)  # stripe, paypal, etc.
    provider_payment_id = models.CharField(max_length=100, blank=True)
    provider_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Metadata
    description = models.TextField(blank=True)
    failure_reason = models.TextField(blank=True)
    receipt_url = models.URLField(blank=True)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"${self.amount} - {self.user.email} ({self.status})"


class BillingEvent(models.Model):
    """Log of billing-related events"""

    EVENT_TYPES = [
        ('subscription_created', 'Subscription Created'),
        ('subscription_updated', 'Subscription Updated'),
        ('subscription_canceled', 'Subscription Canceled'),
        ('payment_succeeded', 'Payment Succeeded'),
        ('payment_failed', 'Payment Failed'),
        ('trial_started', 'Trial Started'),
        ('trial_ending', 'Trial Ending'),
        ('invoice_created', 'Invoice Created'),
        ('refund_created', 'Refund Created'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billing_events')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)

    # Related objects
    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # Event data
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Billing Event"
        verbose_name_plural = "Billing Events"

    def __str__(self):
        return f"{self.get_event_type_display()} - {self.user.email}"
