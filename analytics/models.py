from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import json

User = get_user_model()


class PageVisit(models.Model):
    """Track page visits and user activity"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    page_url = models.URLField()
    page_title = models.CharField(max_length=200, blank=True)
    referrer = models.URLField(blank=True, null=True)

    # Geographic data
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)

    # Timing
    timestamp = models.DateTimeField(default=timezone.now)
    time_on_page = models.PositiveIntegerField(null=True, blank=True, help_text="Time spent on page in seconds")

    # Device info
    device_type = models.CharField(max_length=20, choices=[
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('bot', 'Bot'),
    ], default='desktop')

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.page_url} - {self.timestamp}"


class SystemMetrics(models.Model):
    """Track system performance metrics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default=timezone.now)

    # Server metrics
    cpu_usage = models.FloatField(help_text="CPU usage percentage")
    memory_usage = models.FloatField(help_text="Memory usage percentage")
    memory_total = models.BigIntegerField(help_text="Total memory in bytes")
    memory_used = models.BigIntegerField(help_text="Used memory in bytes")

    # Database metrics
    db_connections = models.PositiveIntegerField(default=0)
    db_size = models.BigIntegerField(help_text="Database size in bytes", null=True, blank=True)

    # Storage metrics
    disk_usage = models.FloatField(help_text="Disk usage percentage")
    disk_total = models.BigIntegerField(help_text="Total disk space in bytes")
    disk_used = models.BigIntegerField(help_text="Used disk space in bytes")

    # Application metrics
    active_users = models.PositiveIntegerField(default=0)
    total_users = models.PositiveIntegerField(default=0)
    page_views_last_hour = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"System Metrics - {self.timestamp}"


class UserActivity(models.Model):
    """Track detailed user activity"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=[
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('quiz_start', 'Quiz Started'),
        ('quiz_complete', 'Quiz Completed'),
        ('lesson_view', 'Lesson Viewed'),
        ('profile_update', 'Profile Updated'),
        ('subscription_change', 'Subscription Changed'),
    ])
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['activity_type', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.activity_type} - {self.timestamp}"


class ErrorLog(models.Model):
    """Track application errors"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    error_type = models.CharField(max_length=100)
    error_message = models.TextField()
    stack_trace = models.TextField(blank=True)
    request_url = models.URLField(blank=True)
    request_method = models.CharField(max_length=10, blank=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['error_type', 'timestamp']),
            models.Index(fields=['resolved', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.error_type} - {self.timestamp}"


class ConversionFunnel(models.Model):
    """Track user conversion through different stages"""
    FUNNEL_STAGES = [
        ('visitor', 'Visitor'),
        ('signup', 'Sign Up'),
        ('first_quiz', 'First Quiz'),
        ('first_lesson', 'First Lesson'),
        ('active_learner', 'Active Learner'),
        ('subscriber', 'Subscriber'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    stage = models.CharField(max_length=20, choices=FUNNEL_STAGES)
    timestamp = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['stage', 'timestamp']),
            models.Index(fields=['user', 'stage']),
        ]

    def __str__(self):
        return f"{self.stage} - {self.timestamp}"


class ABTestVariant(models.Model):
    """A/B test variants"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_name = models.CharField(max_length=100)
    variant_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    traffic_percentage = models.PositiveIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['test_name', 'variant_name']

    def __str__(self):
        return f"{self.test_name} - {self.variant_name}"


class ABTestAssignment(models.Model):
    """Track user assignments to A/B test variants"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    variant = models.ForeignKey(ABTestVariant, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['variant', 'assigned_at']),
            models.Index(fields=['user', 'variant']),
        ]

    def __str__(self):
        return f"{self.variant.test_name} - {self.variant.variant_name}"


class UserEngagementMetrics(models.Model):
    """Daily user engagement metrics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    # Time metrics
    total_time_spent = models.PositiveIntegerField(default=0, help_text="Total time in seconds")
    session_count = models.PositiveIntegerField(default=0)
    avg_session_duration = models.PositiveIntegerField(default=0, help_text="Average session duration in seconds")

    # Activity metrics
    pages_viewed = models.PositiveIntegerField(default=0)
    quizzes_taken = models.PositiveIntegerField(default=0)
    lessons_completed = models.PositiveIntegerField(default=0)

    # Performance metrics
    quiz_success_rate = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['user', 'date']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.date}"


class SystemPerformanceMetrics(models.Model):
    """System performance metrics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default=timezone.now)

    # Response time metrics
    avg_response_time = models.FloatField(help_text="Average response time in seconds")
    max_response_time = models.FloatField(help_text="Maximum response time in seconds")
    min_response_time = models.FloatField(help_text="Minimum response time in seconds")

    # Database metrics
    avg_query_time = models.FloatField(help_text="Average database query time in seconds")
    total_queries = models.PositiveIntegerField()
    slow_queries = models.PositiveIntegerField(default=0)

    # Memory and CPU
    memory_usage_mb = models.PositiveIntegerField(help_text="Memory usage in MB")
    cpu_usage_percent = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    # Request metrics
    total_requests = models.PositiveIntegerField()
    error_rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"Performance - {self.timestamp}"
