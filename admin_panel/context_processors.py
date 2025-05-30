"""
Context processors for admin panel
"""
from .utils import (
    get_default_user_avatar,
    get_default_subject_icon,
    get_default_hero_image,
    get_file_upload_settings,
    get_security_settings,
    get_learning_settings,
    get_notification_settings,
    get_quiz_settings,
    is_maintenance_mode,
    get_maintenance_message,
    get_site_info
)


def admin_settings(request):
    """
    Add admin settings to template context
    """
    return {
        'admin_settings': {
            'default_user_avatar': get_default_user_avatar(),
            'default_subject_icon': get_default_subject_icon(),
            'default_hero_image': get_default_hero_image(),
            'file_upload': get_file_upload_settings(),
            'security': get_security_settings(),
            'learning': get_learning_settings(),
            'notifications': get_notification_settings(),
            'quiz': get_quiz_settings(),
            'maintenance_mode': is_maintenance_mode(),
            'maintenance_message': get_maintenance_message(),
            'site_info': get_site_info(),
        }
    }
