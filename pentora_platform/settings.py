
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

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,pentora.fly.dev,*.fly.dev,pentora.deigratiams.edu.gh,*.deigratiams.edu.gh', cast=lambda v: [s.strip() for s in v.split(',')])

# CSRF and CORS settings for production
CSRF_TRUSTED_ORIGINS = [
    'https://pentora.fly.dev',
    'https://*.fly.dev',
    'https://pentora.deigratiams.edu.gh',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Additional CSRF settings for better compatibility
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access to CSRF cookie
CSRF_USE_SESSIONS = False  # Use cookies instead of sessions for CSRF
CSRF_COOKIE_SAMESITE = 'Lax'  # Allow cross-site requests with CSRF protection
CSRF_COOKIE_DOMAIN = None  # Let Django auto-detect the domain
CSRF_FAILURE_VIEW = 'core.views.csrf_failure'  # Custom CSRF failure view

# Temporary CSRF debugging settings (remove after fixing)
if not DEBUG:
    # Production CSRF settings
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
else:
    # Development CSRF settings
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False

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
    'cloudinary_storage',
    'cloudinary',

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
if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    # Production: Use WhiteNoise for static file serving
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# WhiteNoise Configuration for production
if not DEBUG:
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = False  # Set to False in production
    WHITENOISE_MAX_AGE = 31536000  # 1 year
    WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br']
    WHITENOISE_INDEX_FILE = True  # Serve index.html for directory requests
    WHITENOISE_ROOT = BASE_DIR / 'staticfiles'  # Ensure WhiteNoise serves from the correct directory

# Static files finders configuration
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media Storage Configuration
if DEBUG:
    # Development: Use local file storage
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    # Production: Use Cloudinary for media storage
    # Production: Use Cloudinary
    CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default='')
    CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default='')
    CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET', default='')

    # Configure Cloudinary storage
    if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
        import cloudinary

        # Cloudinary configuration
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True
        )

        # Use Cloudinary for media files
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

        # Cloudinary storage settings
        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
            'API_KEY': CLOUDINARY_API_KEY,
            'API_SECRET': CLOUDINARY_API_SECRET,
            'SECURE': True,
            'MEDIA_TAG': 'media',
            'INVALID_VIDEO_ERROR_MESSAGE': 'Please upload a valid video file.',
            'EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS': (),
            'STATIC_TAG': 'static',
            'STATICFILES_MANIFEST_ROOT': BASE_DIR / 'staticfiles',
        }

        # Override MEDIA_URL to use Cloudinary's base URL
        MEDIA_URL = f'https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/image/upload/'

        MEDIA_URL = f'https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/image/upload/'

    else:
        # Fallback to local storage
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
        MEDIA_URL = '/media/'
        MEDIA_ROOT = BASE_DIR / 'media'

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
if DEBUG:
    # Development settings
    SITE_DOMAIN = config('SITE_DOMAIN', default='localhost:8000')
    SITE_PROTOCOL = config('SITE_PROTOCOL', default='http')
else:
    # Production settings - prioritize .edu.gh domain for better educational credibility
    SITE_DOMAIN = config('SITE_DOMAIN', default='pentora.deigratiams.edu.gh')
    SITE_PROTOCOL = config('SITE_PROTOCOL', default='https')

# WWW Redirect Configuration
PREPEND_WWW = config('PREPEND_WWW', default=False, cast=bool)
APPEND_SLASH = True

# SEO and Performance Settings
USE_ETAGS = True
USE_L10N = True
USE_TZ = True

# SEO Configuration
SITE_NAME = config('SITE_NAME', default='Pentora - Ghana\'s Leading Online Education Platform')
if DEBUG:
    SITE_URL = config('SITE_URL', default=f'{SITE_PROTOCOL}://{SITE_DOMAIN}')
else:
    SITE_URL = config('SITE_URL', default=f'{SITE_PROTOCOL}://{SITE_DOMAIN}')

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

    # Static file compression is handled by WhiteNoise in production
    # No additional configuration needed here

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
