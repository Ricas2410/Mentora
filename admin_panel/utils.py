"""
Utility functions for admin panel
"""
import os
from django.conf import settings
from django.templatetags.static import static
from .models import SiteSettings


def get_default_user_avatar():
    """
    Get the default user avatar image URL.
    Returns the admin-configured default or system fallback.
    """
    try:
        site_settings = SiteSettings.get_settings()
        if site_settings.default_user_avatar:
            return site_settings.default_user_avatar.url
    except:
        pass

    # System fallback
    return static('images/defaults/default-avatar.svg')


def get_default_subject_icon():
    """
    Get the default subject icon image URL.
    Returns the admin-configured default or system fallback.
    """
    try:
        site_settings = SiteSettings.get_settings()
        if site_settings.default_subject_icon:
            return site_settings.default_subject_icon.url
    except:
        pass

    # System fallback
    return static('images/defaults/default-subject.svg')


def get_default_hero_image():
    """
    Get the default hero image URL.
    Returns the admin-configured default or system fallback.
    """
    try:
        site_settings = SiteSettings.get_settings()
        if site_settings.default_hero_image:
            return site_settings.default_hero_image.url
    except:
        pass

    # System fallback
    return static('images/defaults/default-hero.svg')


def get_file_upload_settings():
    """
    Get file upload settings from admin configuration.
    Returns a dictionary with upload settings.
    """
    try:
        site_settings = SiteSettings.get_settings()
        return {
            'allow_uploads': site_settings.allow_file_uploads,
            'max_size_mb': site_settings.max_file_size_mb,
            'allowed_types': [ext.strip() for ext in site_settings.allowed_file_types.split(',')],
            'auto_approve': site_settings.auto_approve_uploads,
        }
    except:
        # Fallback settings
        return {
            'allow_uploads': True,
            'max_size_mb': 10,
            'allowed_types': ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif'],
            'auto_approve': False,
        }


def validate_file_upload(uploaded_file):
    """
    Validate uploaded file against admin settings.
    Returns (is_valid, error_message).
    """
    upload_settings = get_file_upload_settings()

    if not upload_settings['allow_uploads']:
        return False, "File uploads are currently disabled."

    # Check file size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > upload_settings['max_size_mb']:
        return False, f"File size ({file_size_mb:.1f}MB) exceeds maximum allowed size ({upload_settings['max_size_mb']}MB)."

    # Check file extension
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension not in upload_settings['allowed_types']:
        return False, f"File type '{file_extension}' is not allowed. Allowed types: {', '.join(upload_settings['allowed_types'])}"

    return True, None


def get_security_settings():
    """
    Get security settings from admin configuration.
    """
    try:
        site_settings = SiteSettings.get_settings()
        return {
            'enable_user_registration': site_settings.enable_user_registration,
            'require_strong_passwords': site_settings.require_strong_passwords,
            'session_timeout_minutes': site_settings.session_timeout_minutes,
            'max_login_attempts': site_settings.max_login_attempts,
            'email_verification_required': site_settings.email_verification_required,
        }
    except:
        # Fallback settings
        return {
            'enable_user_registration': True,
            'require_strong_passwords': True,
            'session_timeout_minutes': 60,
            'max_login_attempts': 5,
            'email_verification_required': True,
        }


def get_learning_settings():
    """
    Get learning feature settings from admin configuration.
    """
    try:
        site_settings = SiteSettings.get_settings()
        return {
            'enable_offline_mode': site_settings.enable_offline_mode,
            'enable_progress_tracking': site_settings.enable_progress_tracking,
            'enable_achievements': site_settings.enable_achievements,
            'enable_leaderboards': site_settings.enable_leaderboards,
            'require_all_subjects_completion': site_settings.require_all_subjects_completion,
            'allow_retakes': site_settings.allow_retakes,
            'max_retake_attempts': site_settings.max_retake_attempts,
        }
    except:
        # Fallback settings
        return {
            'enable_offline_mode': True,
            'enable_progress_tracking': True,
            'enable_achievements': True,
            'enable_leaderboards': False,
            'require_all_subjects_completion': True,
            'allow_retakes': True,
            'max_retake_attempts': 3,
        }


def get_notification_settings():
    """
    Get notification settings from admin configuration.
    """
    try:
        site_settings = SiteSettings.get_settings()
        return {
            'enable_email_notifications': site_settings.enable_email_notifications,
            'enable_push_notifications': site_settings.enable_push_notifications,
            'enable_sms_notifications': site_settings.enable_sms_notifications,
            'daily_reminder_time': site_settings.daily_reminder_time,
        }
    except:
        # Fallback settings
        from datetime import time
        return {
            'enable_email_notifications': True,
            'enable_push_notifications': True,
            'enable_sms_notifications': False,
            'daily_reminder_time': time(18, 0),
        }


def get_quiz_settings():
    """
    Get quiz settings from admin configuration.
    """
    try:
        site_settings = SiteSettings.get_settings()
        return {
            'quiz_time_limit': site_settings.quiz_time_limit,
            'quiz_questions_per_topic': site_settings.quiz_questions_per_topic,
            'question_time_limit': site_settings.question_time_limit,
            'minimum_pass_percentage': site_settings.minimum_pass_percentage,
            'show_correct_answers': site_settings.show_correct_answers,
            'shuffle_questions': site_settings.shuffle_questions,
            'shuffle_answers': site_settings.shuffle_answers,
            'allow_question_skip': site_settings.allow_question_skip,
            'show_progress_bar': site_settings.show_progress_bar,
        }
    except:
        # Fallback settings
        return {
            'quiz_time_limit': 300,
            'quiz_questions_per_topic': 10,
            'question_time_limit': 45,
            'minimum_pass_percentage': 60,
            'show_correct_answers': True,
            'shuffle_questions': True,
            'shuffle_answers': True,
            'allow_question_skip': False,
            'show_progress_bar': True,
        }


def is_maintenance_mode():
    """
    Check if the site is in maintenance mode.
    """
    try:
        site_settings = SiteSettings.get_settings()
        return site_settings.maintenance_mode
    except:
        return False


def get_maintenance_message():
    """
    Get the maintenance mode message.
    """
    try:
        site_settings = SiteSettings.get_settings()
        return site_settings.maintenance_message
    except:
        return "The site is currently under maintenance. Please check back later."


def get_site_info():
    """
    Get basic site information.
    """
    try:
        site_settings = SiteSettings.get_settings()
        return {
            'site_name': site_settings.site_name,
            'site_description': site_settings.site_description,
            'contact_email': site_settings.contact_email,
            'contact_phone': site_settings.contact_phone,
            'contact_address': site_settings.contact_address,
            'site_logo': site_settings.site_logo.url if site_settings.site_logo else None,
            'site_favicon': site_settings.site_favicon.url if site_settings.site_favicon else None,
        }
    except:
        # Fallback settings
        return {
            'site_name': 'Mentora Learning Platform',
            'site_description': 'Empowering underprivileged learners through quality education',
            'contact_email': 'info@mentora.edu.gh',
            'contact_phone': '',
            'contact_address': '',
            'site_logo': None,
            'site_favicon': None,
        }
