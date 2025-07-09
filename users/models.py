from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid
import re


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""

    def generate_username_from_email(self, email):
        """Generate a unique username from email address"""
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
        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
            # Ensure we don't exceed 30 characters
            if len(username) > 30:
                base_username = base_username[:26-len(str(counter))]
                username = f"{base_username}_{counter}"

        return username

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)

        # Auto-generate username from email if not provided and username is required
        if 'username' not in extra_fields or extra_fields.get('username') is None:
            # For superusers or when explicitly needed, generate username
            if extra_fields.get('is_superuser') or extra_fields.get('is_staff'):
                extra_fields['username'] = self.generate_username_from_email(email)
            else:
                # For regular users, set username to None (optional)
                extra_fields['username'] = None

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Auto-generate username from email if not provided
        if 'username' not in extra_fields:
            extra_fields['username'] = self.generate_username_from_email(email)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]

    COUNTRY_CHOICES = [
        ('GH', 'Ghana'),
        ('NG', 'Nigeria'),
        ('KE', 'Kenya'),
        ('ZA', 'South Africa'),
        ('EG', 'Egypt'),
        ('MA', 'Morocco'),
        ('TZ', 'Tanzania'),
        ('UG', 'Uganda'),
        ('ZW', 'Zimbabwe'),
        ('BW', 'Botswana'),
        ('US', 'United States'),
        ('GB', 'United Kingdom'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('IN', 'India'),
        ('CN', 'China'),
        ('JP', 'Japan'),
        ('BR', 'Brazil'),
        ('OTHER', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True,
                               help_text="Optional username for easy login. If not set, email will be used.",
                               db_index=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Personal information
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        help_text="Gender identity"
    )
    country = models.CharField(
        max_length=10,
        choices=COUNTRY_CHOICES,
        blank=True,
        null=True,
        help_text="Country of residence"
    )

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

    objects = UserManager()

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
        return User.objects.generate_username_from_email(email)

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
        """Create a new email verification token and invalidate old ones"""
        import secrets

        # Invalidate all existing verification tokens for this user
        cls.objects.filter(user=user, is_used=False).update(is_used=True)

        # Create new token
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
