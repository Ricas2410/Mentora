from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class UserProgress(models.Model):
    """
    Model to track user progress through class levels
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='progress')
    class_level = models.ForeignKey('subjects.ClassLevel', on_delete=models.CASCADE, related_name='user_progress')

    # Progress tracking
    is_started = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Performance metrics
    topics_completed = models.PositiveIntegerField(default=0)
    total_topics = models.PositiveIntegerField(default=0)
    quizzes_taken = models.PositiveIntegerField(default=0)
    tests_taken = models.PositiveIntegerField(default=0)

    # Final assessment
    final_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    passed = models.BooleanField(default=False)

    # Time tracking
    total_study_time = models.PositiveIntegerField(default=0, help_text="Total study time in minutes")

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_progress'
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progress'
        unique_together = ['user', 'class_level']
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.class_level.name}"

    @property
    def completion_percentage(self):
        """Calculate completion percentage"""
        if self.total_topics == 0:
            return 0
        return (self.topics_completed / self.total_topics) * 100

    def update_progress(self):
        """Update progress based on completed topics"""
        from subjects.models import Topic

        # Get all topics for this class level
        all_topics = Topic.objects.filter(class_level=self.class_level, is_active=True)
        self.total_topics = all_topics.count()

        # Count completed topics
        completed_topics = 0
        for topic in all_topics:
            if TopicProgress.objects.filter(
                user=self.user,
                topic=topic,
                is_completed=True
            ).exists():
                completed_topics += 1

        self.topics_completed = completed_topics

        # Check if level is completed
        if self.topics_completed == self.total_topics and self.total_topics > 0:
            self.is_completed = True
            if not self.completed_at:
                self.completed_at = timezone.now()

        self.save()


class TopicProgress(models.Model):
    """
    Model to track user progress through individual topics
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey('subjects.Topic', on_delete=models.CASCADE, related_name='user_progress')

    # Progress tracking
    is_started = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Study tracking
    notes_read = models.BooleanField(default=False)
    quiz_completed = models.BooleanField(default=False)
    test_completed = models.BooleanField(default=False)

    # Performance
    best_quiz_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    best_test_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # Time tracking
    study_time = models.PositiveIntegerField(default=0, help_text="Study time in minutes")

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'topic_progress'
        verbose_name = 'Topic Progress'
        verbose_name_plural = 'Topic Progress'
        unique_together = ['user', 'topic']
        ordering = ['topic__order']

    def __str__(self):
        return f"{self.user.full_name} - {self.topic.title}"

    @property
    def completion_percentage(self):
        """Calculate completion percentage based on completed activities"""
        total_activities = 3  # notes, quiz, test
        completed_activities = 0

        if self.notes_read:
            completed_activities += 1
        if self.quiz_completed:
            completed_activities += 1
        if self.test_completed:
            completed_activities += 1

        return (completed_activities / total_activities) * 100

    def mark_notes_read(self):
        """Mark notes as read and start topic if not started"""
        self.notes_read = True
        if not self.is_started:
            self.is_started = True
            self.started_at = timezone.now()
        self.save()

    def update_quiz_score(self, score):
        """Update best quiz score and check completion"""
        from admin_panel.utils import get_quiz_settings

        if score > self.best_quiz_score:
            self.best_quiz_score = score
        self.quiz_completed = True

        # Get passing score from settings
        quiz_settings = get_quiz_settings()
        passing_score = quiz_settings['minimum_pass_percentage']

        # For now, complete topic if quiz is passed (simplified completion)
        # In future, this can be expanded to require notes + quiz + test
        if self.best_quiz_score >= passing_score:
            self.is_completed = True
            if not self.completed_at:
                self.completed_at = timezone.now()

        # Mark as started if not already
        if not self.is_started:
            self.is_started = True
            self.started_at = timezone.now()

        self.save()

        # Update class level progress
        try:
            class_progress = UserProgress.objects.get(
                user=self.user,
                class_level=self.topic.class_level
            )
            class_progress.update_progress()
        except UserProgress.DoesNotExist:
            # Create class progress if it doesn't exist
            UserProgress.objects.create(
                user=self.user,
                class_level=self.topic.class_level,
                is_started=True,
                started_at=timezone.now()
            )

    def update_test_score(self, score):
        """Update best test score and check completion"""
        if score > self.best_test_score:
            self.best_test_score = score
        self.test_completed = True

        # Check if topic is completed (notes read, quiz and test completed with passing scores)
        passing_score = 60  # Minimum 60% to pass

        if (self.notes_read and
            self.quiz_completed and
            self.test_completed and
            self.best_quiz_score >= passing_score and
            self.best_test_score >= passing_score):

            self.is_completed = True
            if not self.completed_at:
                self.completed_at = timezone.now()

        self.save()

        # Update class level progress
        try:
            class_progress = UserProgress.objects.get(
                user=self.user,
                class_level=self.topic.class_level
            )
            class_progress.update_progress()
        except UserProgress.DoesNotExist:
            # Create class progress if it doesn't exist
            UserProgress.objects.create(
                user=self.user,
                class_level=self.topic.class_level,
                is_started=True,
                started_at=timezone.now()
            )

    def check_completion_requirements(self):
        """Check if all requirements are met for topic completion"""
        passing_score = 60

        requirements = {
            'notes_read': self.notes_read,
            'quiz_completed': self.quiz_completed and self.best_quiz_score >= passing_score,
            'test_completed': self.test_completed and self.best_test_score >= passing_score,
        }

        return requirements


class StudyNoteProgress(models.Model):
    """
    Model to track individual study note reading progress
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='note_progress')
    study_note = models.ForeignKey('content.StudyNote', on_delete=models.CASCADE, related_name='user_progress')

    # Progress tracking
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'study_note_progress'
        verbose_name = 'Study Note Progress'
        verbose_name_plural = 'Study Note Progress'
        unique_together = ['user', 'study_note']
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.study_note.title}"

    def mark_as_read(self):
        """Mark this study note as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

            # Check if all notes for this topic are read
            topic = self.study_note.topic
            all_notes = topic.get_study_notes()
            read_notes = StudyNoteProgress.objects.filter(
                user=self.user,
                study_note__topic=topic,
                is_read=True
            ).count()

            # If all notes are read, mark topic notes as read
            if read_notes >= all_notes.count() and all_notes.count() > 0:
                topic_progress, created = TopicProgress.objects.get_or_create(
                    user=self.user,
                    topic=topic,
                    defaults={
                        'is_started': True,
                        'started_at': timezone.now()
                    }
                )
                if not topic_progress.notes_read:
                    topic_progress.mark_notes_read()


class StudySession(models.Model):
    """
    Model to track individual study sessions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='study_sessions')
    topic = models.ForeignKey('subjects.Topic', on_delete=models.CASCADE, related_name='study_sessions')

    # Session details
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, help_text="Duration in minutes")

    # Activity tracking
    notes_viewed = models.BooleanField(default=False)
    quiz_taken = models.BooleanField(default=False)
    test_taken = models.BooleanField(default=False)

    class Meta:
        db_table = 'study_sessions'
        verbose_name = 'Study Session'
        verbose_name_plural = 'Study Sessions'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.topic.title} ({self.started_at.date()})"

    def end_session(self):
        """End the study session and calculate duration"""
        if not self.ended_at:
            self.ended_at = timezone.now()
            duration_seconds = (self.ended_at - self.started_at).total_seconds()
            self.duration = int(duration_seconds / 60)  # Convert to minutes
            self.save()

            # Update topic progress study time
            try:
                topic_progress = TopicProgress.objects.get(
                    user=self.user,
                    topic=self.topic
                )
                topic_progress.study_time += self.duration
                topic_progress.save()
            except TopicProgress.DoesNotExist:
                pass


class Achievement(models.Model):
    """
    Model for user achievements and badges
    """
    ACHIEVEMENT_TYPES = [
        ('first_quiz', 'First Quiz Completed'),
        ('first_test', 'First Test Completed'),
        ('level_complete', 'Level Completed'),
        ('perfect_score', 'Perfect Score'),
        ('study_streak', 'Study Streak'),
        ('fast_learner', 'Fast Learner'),
        ('persistent', 'Persistent Learner'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='achievements')
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)

    # Achievement data
    earned_at = models.DateTimeField(default=timezone.now)
    points = models.PositiveIntegerField(default=10)

    class Meta:
        db_table = 'achievements'
        verbose_name = 'Achievement'
        verbose_name_plural = 'Achievements'
        unique_together = ['user', 'achievement_type']
        ordering = ['-earned_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.title}"
