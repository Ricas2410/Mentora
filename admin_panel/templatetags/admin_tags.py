"""
Template tags for admin panel
"""
from django import template
from admin_panel.models import SiteSettings

register = template.Library()


@register.simple_tag
def get_maintenance_status():
    """
    Get current maintenance mode status
    """
    try:
        settings = SiteSettings.get_settings()
        return settings.maintenance_mode
    except:
        return False


@register.simple_tag
def get_site_setting(setting_name, default=None):
    """
    Get a specific site setting value
    """
    try:
        settings = SiteSettings.get_settings()
        return getattr(settings, setting_name, default)
    except:
        return default


@register.filter
def session_timeout_display(minutes):
    """
    Convert session timeout minutes to user-friendly display
    """
    if not minutes:
        return "1 hour (default)"
    
    if minutes == 30:
        return "30 minutes"
    elif minutes == 60:
        return "1 hour"
    elif minutes == 120:
        return "2 hours"
    elif minutes == 240:
        return "4 hours"
    elif minutes == 480:
        return "8 hours"
    else:
        return f"{minutes} minutes"


@register.filter
def quiz_time_display(seconds):
    """
    Convert quiz time seconds to user-friendly display
    """
    if not seconds:
        return "5 minutes (default)"
    
    if seconds >= 60:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        return f"{seconds} seconds"
