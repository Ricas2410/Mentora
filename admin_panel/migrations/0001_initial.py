# Generated by Django 5.2.1 on 2025-07-05 14:54

import datetime
import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminActivity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('model_name', models.CharField(blank=True, max_length=50)),
                ('object_id', models.CharField(blank=True, max_length=100)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Admin Activity',
                'verbose_name_plural': 'Admin Activities',
                'db_table': 'admin_activities',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('site_name', models.CharField(default='Pentora Learning Platform', max_length=100)),
                ('site_description', models.TextField(default='Empowering underprivileged learners through quality education')),
                ('site_logo', models.ImageField(blank=True, help_text='Main site logo (recommended: 200x60px)', null=True, upload_to='site/logos/')),
                ('site_favicon', models.ImageField(blank=True, help_text='Site favicon (recommended: 32x32px)', null=True, upload_to='site/favicons/')),
                ('hero_banner', models.ImageField(blank=True, help_text='Main hero banner for homepage (recommended: 1920x600px)', null=True, upload_to='site/banners/')),
                ('contact_email', models.EmailField(default='info@Pentora.edu.gh', max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=20)),
                ('contact_address', models.TextField(blank=True)),
                ('minimum_pass_percentage', models.PositiveIntegerField(default=60, help_text='Minimum percentage required to pass quizzes and tests', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('quiz_questions_per_topic', models.PositiveIntegerField(default=10, help_text='Default number of questions per quiz', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50)])),
                ('quiz_time_limit', models.PositiveIntegerField(default=300, help_text='Default quiz time limit in seconds', validators=[django.core.validators.MinValueValidator(60), django.core.validators.MaxValueValidator(3600)])),
                ('question_time_limit', models.PositiveIntegerField(default=45, help_text='Default time limit per question in seconds', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(300)])),
                ('explanation_display_time', models.PositiveIntegerField(default=5, help_text='Time to display explanation after each question in seconds', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
                ('test_questions_per_topic', models.PositiveIntegerField(default=20, help_text='Default number of questions per test', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('test_time_limit', models.PositiveIntegerField(default=1800, help_text='Default test time limit in seconds', validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(7200)])),
                ('exam_questions_per_level', models.PositiveIntegerField(default=30, help_text='Default number of questions per level exam', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(200)])),
                ('exam_time_limit', models.PositiveIntegerField(default=3600, help_text='Default exam time limit in seconds', validators=[django.core.validators.MinValueValidator(600), django.core.validators.MaxValueValidator(14400)])),
                ('require_all_subjects_completion', models.BooleanField(default=True, help_text='Require completion of all subjects in a level before promotion')),
                ('allow_retakes', models.BooleanField(default=True, help_text='Allow users to retake quizzes and tests')),
                ('max_retake_attempts', models.PositiveIntegerField(default=3, help_text='Maximum number of retake attempts allowed', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('enable_email_notifications', models.BooleanField(default=True, help_text='Enable email notifications for users')),
                ('email_verification_required', models.BooleanField(default=True, help_text='Require email verification for new users')),
                ('allow_file_uploads', models.BooleanField(default=True, help_text='Allow file uploads for study materials')),
                ('max_file_size_mb', models.PositiveIntegerField(default=10, help_text='Maximum file size for uploads in MB', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('allowed_file_types', models.TextField(default='pdf,doc,docx,txt,jpg,jpeg,png,gif,mp4,mp3,webp', help_text='Comma-separated list of allowed file extensions')),
                ('default_user_avatar', models.ImageField(blank=True, help_text='Default avatar image for users without profile pictures', null=True, upload_to='defaults/')),
                ('default_subject_icon', models.ImageField(blank=True, help_text='Default icon for subjects without custom icons', null=True, upload_to='defaults/')),
                ('default_hero_image', models.ImageField(blank=True, help_text='Default hero image when no custom hero is set', null=True, upload_to='defaults/')),
                ('enable_user_registration', models.BooleanField(default=True, help_text='Allow new users to register accounts')),
                ('require_strong_passwords', models.BooleanField(default=True, help_text='Enforce strong password requirements')),
                ('session_timeout_minutes', models.PositiveIntegerField(default=60, help_text='User session timeout in minutes', validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(480)])),
                ('max_login_attempts', models.PositiveIntegerField(default=5, help_text='Maximum failed login attempts before account lockout', validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(20)])),
                ('enable_offline_mode', models.BooleanField(default=True, help_text='Allow users to download content for offline learning')),
                ('enable_progress_tracking', models.BooleanField(default=True, help_text='Track and display user learning progress')),
                ('enable_achievements', models.BooleanField(default=True, help_text='Enable achievement badges and rewards system')),
                ('enable_leaderboards', models.BooleanField(default=False, help_text='Show leaderboards and competitive features')),
                ('enable_push_notifications', models.BooleanField(default=True, help_text='Enable browser push notifications')),
                ('enable_sms_notifications', models.BooleanField(default=False, help_text='Enable SMS notifications (requires SMS service setup)')),
                ('daily_reminder_time', models.TimeField(default=datetime.time(18, 0), help_text='Default time for daily learning reminders')),
                ('enable_content_moderation', models.BooleanField(default=True, help_text='Enable automatic content moderation')),
                ('auto_approve_uploads', models.BooleanField(default=False, help_text='Automatically approve user file uploads')),
                ('maintenance_mode', models.BooleanField(default=False, help_text='Enable maintenance mode to restrict access')),
                ('maintenance_message', models.TextField(default='The site is currently under maintenance. Please check back later.', help_text='Message to display during maintenance')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
                'db_table': 'site_settings',
            },
        ),
    ]
