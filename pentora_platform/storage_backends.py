"""
Custom storage backends for Pentora platform
"""
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class SupabaseMediaStorage(S3Boto3Storage):
    """
    Custom storage backend for Supabase storage
    """
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    addressing_style = 'path'  # Required for Supabase

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Supabase-specific settings
        self.default_acl = 'public-read'
        self.querystring_auth = False
        self.use_ssl = True
        self.addressing_style = 'path'

    def url(self, name):
        """
        Return the URL for accessing the file via Supabase public URL
        """
        if self.custom_domain:
            # Clean up the name to ensure proper URL format
            clean_name = name.lstrip('/')
            return f"https://{self.custom_domain}/{clean_name}"
        return super().url(name)

    def _save(self, name, content):
        """
        Override save to ensure proper file handling with Supabase
        """
        # Clean the name to avoid double slashes
        cleaned_name = name.lstrip('/')
        return super()._save(cleaned_name, content)


class SupabaseStaticStorage(S3Boto3Storage):
    """
    Custom storage backend for Supabase static files
    """
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = True
    custom_domain = getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    
    def url(self, name):
        """
        Return the URL for accessing static files
        """
        if self.custom_domain:
            return f"https://{self.custom_domain}/static/{name}"
        return super().url(name)
