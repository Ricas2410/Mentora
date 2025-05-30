from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid


class Subject(models.Model):
    """
    Model representing academic subjects (English, Mathematics, Science, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class or emoji")
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subjects'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_class_levels(self):
        """Get all class levels for this subject"""
        return self.classlevels.filter(is_active=True).order_by('level_number')

    def get_total_topics(self):
        """Get total number of topics across all levels"""
        return sum(level.get_topics_count() for level in self.get_class_levels())


class ClassLevel(models.Model):
    """
    Model representing class levels within subjects (Class 1, Class 2, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='classlevels')
    name = models.CharField(max_length=50)  # e.g., "Class 1", "Beginner Level"
    level_number = models.PositiveIntegerField()  # 1, 2, 3, etc.
    description = models.TextField(blank=True)

    # Prerequisites
    prerequisite_level = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Previous level required to unlock this level"
    )

    # Settings
    is_active = models.BooleanField(default=True)
    pass_percentage = models.PositiveIntegerField(
        default=60,
        help_text="Minimum percentage to pass this level"
    )

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'class_levels'
        verbose_name = 'Class Level'
        verbose_name_plural = 'Class Levels'
        unique_together = ['subject', 'level_number']
        ordering = ['subject', 'level_number']

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

    def get_topics(self):
        """Get all active topics for this class level"""
        return self.topics.filter(is_active=True).order_by('order')

    def get_topics_count(self):
        """Get count of active topics"""
        return self.topics.filter(is_active=True).count()

    def is_unlocked_for_user(self, user):
        """Check if this level is unlocked for a specific user"""
        if not self.prerequisite_level:
            return True

        from progress.models import UserProgress
        try:
            progress = UserProgress.objects.get(
                user=user,
                class_level=self.prerequisite_level
            )
            return progress.is_completed and progress.final_score >= self.prerequisite_level.pass_percentage
        except UserProgress.DoesNotExist:
            return False


class Topic(models.Model):
    """
    Model representing topics within class levels
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    description = models.TextField(blank=True)

    # Content organization
    order = models.PositiveIntegerField(default=0)
    estimated_duration = models.PositiveIntegerField(
        default=30,
        help_text="Estimated study time in minutes"
    )

    # Settings
    is_active = models.BooleanField(default=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'topics'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        unique_together = ['class_level', 'order']
        ordering = ['class_level', 'order']

    def __str__(self):
        return f"{self.class_level} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_study_notes(self):
        """Get all study notes for this topic"""
        from content.models import StudyNote
        return StudyNote.objects.filter(topic=self, is_active=True)

    def get_questions_count(self):
        """Get total number of questions for this topic"""
        from content.models import Question
        return Question.objects.filter(topic=self, is_active=True).count()

    def has_sufficient_questions(self):
        """Check if topic has enough questions for quizzes and tests"""
        from django.conf import settings
        min_questions = getattr(settings, 'TEST_QUESTIONS_PER_TOPIC', 10)
        return self.get_questions_count() >= min_questions


