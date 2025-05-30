import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import time


class SiteSettings(models.Model):
    """
    Model to store site-wide settings that can be managed by admin
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Site Information
    site_name = models.CharField(max_length=100, default="Mentora Learning Platform")
    site_description = models.TextField(default="Empowering underprivileged learners through quality education")
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    site_favicon = models.ImageField(upload_to='site/', blank=True, null=True)

    # Contact Information
    contact_email = models.EmailField(default="info@mentora.edu.gh")
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)

    # Learning Platform Settings
    minimum_pass_percentage = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Minimum percentage required to pass quizzes and tests"
    )

    # Quiz Settings
    quiz_questions_per_topic = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Default number of questions per quiz"
    )
    quiz_time_limit = models.PositiveIntegerField(
        default=300,
        validators=[MinValueValidator(60), MaxValueValidator(3600)],
        help_text="Default quiz time limit in seconds"
    )
    question_time_limit = models.PositiveIntegerField(
        default=45,
        validators=[MinValueValidator(10), MaxValueValidator(300)],
        help_text="Default time limit per question in seconds"
    )
    explanation_display_time = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        help_text="Time to display explanation after each question in seconds"
    )

    # Test Settings
    test_questions_per_topic = models.PositiveIntegerField(
        default=20,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Default number of questions per test"
    )
    test_time_limit = models.PositiveIntegerField(
        default=1800,
        validators=[MinValueValidator(300), MaxValueValidator(7200)],
        help_text="Default test time limit in seconds"
    )

    # Exam Settings
    exam_questions_per_level = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(200)],
        help_text="Default number of questions per level exam"
    )
    exam_time_limit = models.PositiveIntegerField(
        default=3600,
        validators=[MinValueValidator(600), MaxValueValidator(14400)],
        help_text="Default exam time limit in seconds"
    )

    # Progression Settings
    require_all_subjects_completion = models.BooleanField(
        default=True,
        help_text="Require completion of all subjects in a level before promotion"
    )
    allow_retakes = models.BooleanField(
        default=True,
        help_text="Allow users to retake quizzes and tests"
    )
    max_retake_attempts = models.PositiveIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Maximum number of retake attempts allowed"
    )

    # Email Settings
    enable_email_notifications = models.BooleanField(
        default=True,
        help_text="Enable email notifications for users"
    )
    email_verification_required = models.BooleanField(
        default=True,
        help_text="Require email verification for new users"
    )

    # Content Settings
    allow_file_uploads = models.BooleanField(
        default=True,
        help_text="Allow file uploads for study materials"
    )
    max_file_size_mb = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Maximum file size for uploads in MB"
    )
    allowed_file_types = models.TextField(
        default="pdf,doc,docx,txt,jpg,jpeg,png,gif,mp4,mp3,webp",
        help_text="Comma-separated list of allowed file extensions"
    )

    # Default Images/Fallbacks
    default_user_avatar = models.ImageField(
        upload_to='defaults/',
        null=True,
        blank=True,
        help_text="Default avatar image for users without profile pictures"
    )
    default_subject_icon = models.ImageField(
        upload_to='defaults/',
        null=True,
        blank=True,
        help_text="Default icon for subjects without custom icons"
    )
    default_hero_image = models.ImageField(
        upload_to='defaults/',
        null=True,
        blank=True,
        help_text="Default hero image when no custom hero is set"
    )

    # Security Settings
    enable_user_registration = models.BooleanField(
        default=True,
        help_text="Allow new users to register accounts"
    )
    require_strong_passwords = models.BooleanField(
        default=True,
        help_text="Enforce strong password requirements"
    )
    session_timeout_minutes = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(5), MaxValueValidator(480)],
        help_text="User session timeout in minutes"
    )
    max_login_attempts = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(3), MaxValueValidator(20)],
        help_text="Maximum failed login attempts before account lockout"
    )

    # Learning Settings
    enable_offline_mode = models.BooleanField(
        default=True,
        help_text="Allow users to download content for offline learning"
    )
    enable_progress_tracking = models.BooleanField(
        default=True,
        help_text="Track and display user learning progress"
    )
    enable_achievements = models.BooleanField(
        default=True,
        help_text="Enable achievement badges and rewards system"
    )
    enable_leaderboards = models.BooleanField(
        default=False,
        help_text="Show leaderboards and competitive features"
    )

    # Notification Settings
    enable_push_notifications = models.BooleanField(
        default=True,
        help_text="Enable browser push notifications"
    )
    enable_sms_notifications = models.BooleanField(
        default=False,
        help_text="Enable SMS notifications (requires SMS service setup)"
    )
    daily_reminder_time = models.TimeField(
        default=time(18, 0),
        help_text="Default time for daily learning reminders"
    )

    # Content Moderation
    enable_content_moderation = models.BooleanField(
        default=True,
        help_text="Enable automatic content moderation"
    )
    auto_approve_uploads = models.BooleanField(
        default=False,
        help_text="Automatically approve user file uploads"
    )

    # Maintenance
    maintenance_mode = models.BooleanField(
        default=False,
        help_text="Enable maintenance mode to restrict access"
    )
    maintenance_message = models.TextField(
        default="The site is currently under maintenance. Please check back later.",
        help_text="Message to display during maintenance"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='settings_updates'
    )

    class Meta:
        db_table = 'site_settings'
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return f"Site Settings - {self.site_name}"

    @classmethod
    def get_settings(cls):
        """Get the current site settings, create default if none exist"""
        settings, created = cls.objects.get_or_create(
            pk=cls.objects.first().pk if cls.objects.exists() else uuid.uuid4()
        )
        return settings

    def save(self, *args, **kwargs):
        # Ensure only one settings instance exists
        if not self.pk and SiteSettings.objects.exists():
            self.pk = SiteSettings.objects.first().pk
        super().save(*args, **kwargs)


class AdminActivity(models.Model):
    """
    Model to track admin activities for audit purposes
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='admin_activities')
    action = models.CharField(max_length=100)
    description = models.TextField()
    model_name = models.CharField(max_length=50, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_activities'
        verbose_name = 'Admin Activity'
        verbose_name_plural = 'Admin Activities'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.admin_user.full_name} - {self.action} - {self.timestamp}"


# CSVImportLog is already defined in core.models, so we'll use that one
