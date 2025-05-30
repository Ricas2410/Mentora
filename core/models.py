from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import uuid


class SystemSettings(models.Model):
    """
    Model for system-wide settings and configurations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'system_settings'
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'
        ordering = ['key']

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"

    @classmethod
    def get_setting(cls, key, default=None):
        """Get a setting value by key"""
        try:
            setting = cls.objects.get(key=key, is_active=True)
            return setting.value
        except cls.DoesNotExist:
            return default

    @classmethod
    def set_setting(cls, key, value, description="", user=None):
        """Set a setting value"""
        setting, created = cls.objects.get_or_create(
            key=key,
            defaults={
                'value': value,
                'description': description,
                'updated_by': user
            }
        )
        if not created:
            setting.value = value
            setting.description = description
            setting.updated_by = user
            setting.save()
        return setting


class Notification(models.Model):
    """
    Model for system notifications
    """
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('achievement', 'Achievement'),
        ('reminder', 'Reminder'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')

    # Status
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.title}"

    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class CSVImportLog(models.Model):
    """
    Model to track CSV import operations
    """
    IMPORT_TYPES = [
        ('questions', 'Questions'),
        ('study_notes', 'Study Notes'),
        ('users', 'Users'),
        ('subjects', 'Subjects'),
        ('topics', 'Topics'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('partial', 'Partially Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    import_type = models.CharField(max_length=20, choices=IMPORT_TYPES)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500, blank=True)

    # Import details
    total_rows = models.PositiveIntegerField(default=0)
    successful_rows = models.PositiveIntegerField(default=0)
    failed_rows = models.PositiveIntegerField(default=0)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_log = models.TextField(blank=True)

    # Metadata
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    imported_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'csv_import_logs'
        verbose_name = 'CSV Import Log'
        verbose_name_plural = 'CSV Import Logs'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.import_type} - {self.file_name} ({self.status})"

    @property
    def success_rate(self):
        """Calculate success rate percentage"""
        if self.total_rows == 0:
            return 0
        return (self.successful_rows / self.total_rows) * 100

    def mark_completed(self, status='completed'):
        """Mark import as completed"""
        self.status = status
        self.completed_at = timezone.now()
        self.save()

    def add_error(self, error_message):
        """Add error to the error log"""
        if self.error_log:
            self.error_log += f"\n{error_message}"
        else:
            self.error_log = error_message
        self.save()

    def add_info(self, info_message):
        """Add info message to the error log (used for general logging)"""
        if self.error_log:
            self.error_log += f"\nINFO: {info_message}"
        else:
            self.error_log = f"INFO: {info_message}"
        self.save()


class HeroSection(models.Model):
    """
    Model for managing the hero section content on the home page
    """
    title = models.CharField(max_length=200, default="An Easy Way to Learn and Grow")
    subtitle = models.CharField(max_length=200, default="No matter your background")
    description = models.TextField(
        default="Quality education for everyone. Start your learning journey today with our comprehensive, mobile-friendly platform designed specifically for Ghanaian learners."
    )
    hero_image = models.ImageField(
        upload_to='hero_images/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Upload a high-quality image for the hero section (recommended: 1920x1080px)"
    )
    cta_text = models.CharField(max_length=50, default="Get Started Free")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"
        ordering = ['-created_at']

    def __str__(self):
        return f"Hero Section: {self.title}"

    def save(self, *args, **kwargs):
        # Ensure only one active hero section at a time
        if self.is_active:
            HeroSection.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class SiteStatistic(models.Model):
    """
    Model for managing site statistics displayed on the home page
    """
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    icon = models.CharField(
        max_length=50,
        help_text="FontAwesome icon class (e.g., 'fas fa-users')",
        default="fas fa-chart-line"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Site Statistic"
        verbose_name_plural = "Site Statistics"

    def __str__(self):
        return f"{self.label}: {self.value}"
