from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid
import re


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Email verification
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)

    # Learning preferences
    preferred_language = models.CharField(max_length=10, default='en')
    learning_goals = models.TextField(blank=True, help_text="Personal learning goals")
    CLASS_LEVEL_CHOICES = [
        # Elementary School (Grades 1-6)
        (1, 'Grade 1'),
        (2, 'Grade 2'),
        (3, 'Grade 3'),
        (4, 'Grade 4'),
        (5, 'Grade 5'),
        (6, 'Grade 6'),
        # Middle School (Grades 7-9)
        (7, 'Grade 7'),
        (8, 'Grade 8'),
        (9, 'Grade 9'),
        # High School (Grades 10-12)
        (10, 'Grade 10'),
        (11, 'Grade 11'),
        (12, 'Grade 12'),
    ]

    current_class_level = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="User's current class level",
        choices=CLASS_LEVEL_CHOICES
    )

    # Profile information
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @staticmethod
    def generate_username_from_email(email):
        """
        Generate a unique username from email address
        """
        # Extract the part before @ from email
        base_username = email.split('@')[0]

        # Clean the username - remove special characters except underscore
        base_username = re.sub(r'[^a-zA-Z0-9_]', '', base_username)

        # Ensure it starts with a letter
        if not base_username or not base_username[0].isalpha():
            base_username = 'user_' + base_username

        # Limit length to 30 characters (Django's default max_length for username)
        base_username = base_username[:26]  # Leave room for numbers

        # Check if username exists, if so, add numbers
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
            # Ensure we don't exceed 30 characters
            if len(username) > 30:
                base_username = base_username[:26-len(str(counter))]
                username = f"{base_username}_{counter}"

        return username

    def get_current_level(self):
        """Get user's current learning level"""
        from progress.models import UserProgress
        try:
            latest_progress = UserProgress.objects.filter(
                user=self
            ).order_by('-created_at').first()
            return latest_progress.class_level if latest_progress else None
        except:
            return None


class EmailVerification(models.Model):
    """
    Model to handle email verification tokens
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'email_verifications'
        verbose_name = 'Email Verification'
        verbose_name_plural = 'Email Verifications'

    def __str__(self):
        return f"Verification for {self.user.email}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def create_verification(cls, user):
        """Create a new email verification token"""
        import secrets
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timezone.timedelta(hours=24)

        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )


class PasswordReset(models.Model):
    """
    Model to handle password reset tokens
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'password_resets'
        verbose_name = 'Password Reset'
        verbose_name_plural = 'Password Resets'

    def __str__(self):
        return f"Password reset for {self.user.email}"

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def create_reset(cls, user, ip_address=None):
        """Create a new password reset token"""
        import secrets

        # Deactivate old unused resets
        cls.objects.filter(user=user, is_used=False).update(is_used=True)

        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timezone.timedelta(hours=1)  # 1 hour expiry

        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at,
            ip_address=ip_address
        )
