from django import template
from admin_panel.models import SiteSettings

register = template.Library()


@register.simple_tag
def get_site_logo():
    """Get the site logo URL or None if not set"""
    try:
        settings = SiteSettings.get_settings()
        return settings.site_logo.url if settings.site_logo else None
    except:
        return None


@register.simple_tag
def get_site_favicon():
    """Get the site favicon URL or None if not set"""
    try:
        settings = SiteSettings.get_settings()
        return settings.site_favicon.url if settings.site_favicon else None
    except:
        return None


@register.simple_tag
def get_hero_banner():
    """Get the hero banner URL or None if not set"""
    try:
        settings = SiteSettings.get_settings()
        return settings.hero_banner.url if settings.hero_banner else None
    except:
        return None


@register.simple_tag
def get_site_name():
    """Get the site name"""
    try:
        settings = SiteSettings.get_settings()
        return settings.site_name
    except:
        return "Pentora Learning Platform"


@register.simple_tag
def get_site_description():
    """Get the site description"""
    try:
        settings = SiteSettings.get_settings()
        return settings.site_description
    except:
        return "Empowering underprivileged learners through quality education"



