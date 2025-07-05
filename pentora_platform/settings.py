
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-p%50(al(pq=t*ta4hstizqnm%mk3zjb6v(hk=)py9a2=4a4^&4')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,pentora.fly.dev,*.fly.dev', cast=lambda v: [s.strip() for s in v.split(',')])

# CSRF and CORS settings for production
CSRF_TRUSTED_ORIGINS = [
    'https://pentora.fly.dev',
    'https://*.fly.dev',
    'https://pentora.deigratiams.edu.gh',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    # Third party apps
    'rest_framework',

    # Local apps
    'users',
    'subjects',
    'content',
    'progress',
    'admin_panel',
    'core',
    'billing',
    'analytics',
]

# Optional third-party apps (only add if installed)
OPTIONAL_APPS = [
    'drf_spectacular',
    'corsheaders',
    'django_ratelimit',
    'compressor',
    'imagekit',
    'haystack',
    'import_export',
    'storages',  # For S3 media storage
]

# Add optional apps if they're available
for app in OPTIONAL_APPS:
    try:
        __import__(app)
        INSTALLED_APPS.append(app)
    except ImportError:
        pass

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For serving static files in production
    'core.middleware.IPCanonicalizationMiddleware',  # SEO: Redirect IP to domain
    'core.middleware.WWWRedirectMiddleware',  # SEO: Handle WWW redirects
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_panel.middleware.MaintenanceModeMiddleware',
    'billing.middleware.BillingMiddleware',  # Check subscription status
    'billing.middleware.UsageLimitMiddleware',  # Track usage limits
    'analytics.middleware.AnalyticsMiddleware',  # Track page visits and user activity
    'core.middleware.SecurityHeadersMiddleware',  # SEO: Add security and cache headers
    'core.middleware.PerformanceMiddleware',  # Performance monitoring
]

# Add optional middleware if packages are available
if 'corsheaders' in INSTALLED_APPS:
    MIDDLEWARE.insert(2, 'corsheaders.middleware.CorsMiddleware')

ROOT_URLCONF = 'pentora_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'billing.context_processors.billing_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'pentora_platform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if DEBUG:
    # Development: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Production: Use PostgreSQL (Neon)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Static files storage for production
STATICFILES_STORAGE = config('STATICFILES_STORAGE', default='django.contrib.staticfiles.storage.StaticFilesStorage')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Supabase Storage Configuration (S3-compatible)
# Enable for both development and production when credentials are available
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='pentora-media-storage')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')

# Supabase Storage Configuration
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    # Supabase S3-compatible endpoint configuration
    AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default='')
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default='')
    AWS_DEFAULT_ACL = config('AWS_DEFAULT_ACL', default='public-read')

    # Supabase-specific S3 settings
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_VERIFY = True
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_USE_SSL = True
    AWS_S3_ADDRESSING_STYLE = 'path'  # Required for Supabase

    # Use custom Supabase storage backend
    DEFAULT_FILE_STORAGE = 'pentora_platform.storage_backends.SupabaseMediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

    print(f"✅ Supabase Storage configured: {MEDIA_URL}")
    print(f"📡 Endpoint: {AWS_S3_ENDPOINT_URL}")
    print(f"🪣 Bucket: {AWS_STORAGE_BUCKET_NAME}")
else:
    print("⚠️  Supabase credentials not found, using local storage")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Sites framework
SITE_ID = 1

# Site Domain Configuration
SITE_DOMAIN = config('SITE_DOMAIN', default='localhost:8000')
SITE_PROTOCOL = config('SITE_PROTOCOL', default='http')  # http or https

# WWW Redirect Configuration
PREPEND_WWW = config('PREPEND_WWW', default=False, cast=bool)
APPEND_SLASH = True

# SEO and Performance Settings
USE_ETAGS = True
USE_L10N = True
USE_TZ = True

# Custom Error Pages
HANDLER404 = 'core.views.custom_404_view'
HANDLER500 = 'core.views.custom_500_view'

# Email Configuration - Use environment variables for security
# For development, use console backend to avoid SMTP issues
if DEBUG:
    EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
else:
    EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='skillnetservices@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='tdms ckdk tmgo fado')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Pentora <skillnetservices@gmail.com>')

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Login/Logout URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Session settings
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True

# Security settings (configurable via .env for production)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False, cast=bool)
SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)

# Learning Platform Settings
MINIMUM_PASS_PERCENTAGE = 70
QUIZ_QUESTIONS_PER_TOPIC = 10
TEST_QUESTIONS_PER_TOPIC = 20
EXAM_QUESTIONS_PER_LEVEL = 30

# ============================================================================
# PERFORMANCE AND OPTIMIZATION SETTINGS
# ============================================================================

# Free Tier Optimizations for Fly.io
# Reduce memory usage and CPU consumption
if not DEBUG:
    # Database connection pooling and optimization
    DATABASES['default']['CONN_MAX_AGE'] = config('DATABASE_CONN_MAX_AGE', default=600, cast=int)

    # Only add OPTIONS if using PostgreSQL and not already configured
    if 'postgresql' in DATABASES['default']['ENGINE'] and 'OPTIONS' not in DATABASES['default']:
        DATABASES['default']['OPTIONS'] = {
            'sslmode': 'require',
        }

    # Session optimization
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
    SESSION_CACHE_ALIAS = 'default'
    SESSION_COOKIE_AGE = 86400  # 24 hours

    # Cache optimization for free tier
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'pentora-cache',
            'TIMEOUT': config('DJANGO_CACHE_TIMEOUT', default=3600, cast=int),
            'OPTIONS': {
                'MAX_ENTRIES': 1000,  # Limit memory usage
                'CULL_FREQUENCY': 3,
            }
        }
    }

    # Static file compression (disabled for deployment stability)
    if config('STATIC_FILE_COMPRESSION', default=False, cast=bool):
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

    # Logging optimization - reduce I/O
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'WARNING',  # Only log warnings and errors
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
        },
    }

# Import performance settings for production (only if packages are available)
# Performance settings disabled for free tier deployment
# Redis-based performance settings require additional packages not included in free tier
# The local memory cache configuration above is sufficient for free tier deployment
if not DEBUG and config('ENABLE_REDIS_PERFORMANCE', default=False, cast=bool):
    try:
        # Only import performance settings if explicitly enabled and Redis is available
        from .performance_settings import *
    except ImportError:
        # Fallback to basic caching if performance packages aren't available
        pass

# API Documentation (only if drf_spectacular is installed)
if 'drf_spectacular' in INSTALLED_APPS:
    REST_FRAMEWORK.update({
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'DEFAULT_THROTTLE_CLASSES': [
            'rest_framework.throttling.AnonRateThrottle',
            'rest_framework.throttling.UserRateThrottle'
        ],
        'DEFAULT_THROTTLE_RATES': {
            'anon': '100/hour',
            'user': '1000/hour'
        }
    })

    SPECTACULAR_SETTINGS = {
        'TITLE': 'Pentora API',
        'DESCRIPTION': 'Educational Platform API',
        'VERSION': '1.0.0',
        'SERVE_INCLUDE_SCHEMA': False,
    }

# CORS Settings (only if corsheaders is installed)
if 'corsheaders' in INSTALLED_APPS:
    CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=lambda v: [s.strip() for s in v.split(',') if s.strip()])
    CORS_ALLOW_CREDENTIALS = True

# Basic caching for development
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Internationalization improvements
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

# Additional languages for future expansion
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
    ('es', 'Spanish'),
    ('pt', 'Portuguese'),
    ('ar', 'Arabic'),
]

# Search configuration (only if haystack is installed)
if 'haystack' in INSTALLED_APPS:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': BASE_DIR / 'whoosh_index',
        },
    }

# Create logs directory if it doesn't exist
import os
LOGS_DIR = BASE_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'Pentora.log',
            'formatter': 'verbose',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'Pentora': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}
