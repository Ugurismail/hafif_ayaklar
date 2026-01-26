
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / '.env')


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-4m3!p5t!fy=$22i7m==v!z$d#4-yq33=*1u_^e^=@cot@+9q))')

IS_HOSTED = os.environ.get('HOME', '').startswith('/home/')

# Default DEBUG to False everywhere (so error pages render locally too).
# To enable debug explicitly, set `DJANGO_DEBUG=True` (or `DEBUG=True` for backwards-compat).
_debug_env = os.environ.get('DJANGO_DEBUG', os.environ.get('DEBUG'))
if _debug_env is None:
    DEBUG = False
else:
    DEBUG = str(_debug_env).lower() in ('1', 'true', 'yes', 'on')

# Static asset cache-busting version (keep stable so browser caching works).
# Bump this (or set env var) when you deploy new static files.
STATIC_ASSET_VERSION = os.environ.get('STATIC_ASSET_VERSION', '1')

# Hardcoded ALLOWED_HOSTS to ensure all domains are always included
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'uia1.pythonanywhere.com',
    'ha-uia1.pythonanywhere.com',
    'hafifayaklar.com',
    'www.hafifayaklar.com'
]

# CSRF Trusted Origins (for production)
csrf_origins_str = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if csrf_origins_str:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins_str.split(',') if origin.strip()]

# Production security settings
# These should be enabled in production (hosted + DEBUG=False).
if IS_HOSTED and not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'core.apps.CoreConfig',
    'markdownify',
    'crispy_forms',
    'crispy_bootstrap5',
]

SITE_ID = 1

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MARKDOWNIFY = {
    "default": {
        "BLEACH": True,
        "NL2BR": True,
        "WHITELIST_TAGS": [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
            'em', 'i', 'li', 'ol', 'strong', 'ul', 'p', 'mark',
            'pre', 'img', 'br',
        ],
        "WHITELIST_ATTRS": ['href', 'src', 'alt'],
        "WHITELIST_PROTOCOLS": ['http', 'https'],
        "MARKDOWN_EXTENSIONS": {
            'markdown.extensions.extra': {},
            'markdown.extensions.nl2br': {},
        },
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.LastSeenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.CustomErrorPagesMiddleware',
]

ROOT_URLCONF = 'hafifayaklar.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.static_asset_version',
                'core.context_processors.unread_message_count',
                'core.context_processors.unread_notification_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'hafifayaklar.wsgi.application'

DATABASE_URL = os.environ.get('DATABASE_URL')

# if DATABASE_URL:
#     DATABASES = {
#         'default': dj_database_url.config(default=DATABASE_URL)
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
import os
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'tr'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'  # This should match the name of your login URL pattern
LOGIN_REDIRECT_URL = 'user_homepage'  # Optional: Redirect after successful login
LOGOUT_REDIRECT_URL = 'login'  # Optional: Redirect after logout

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Maximum upload size (5MB for images)
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB in bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB in bytes

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_errors.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file', 'error_file'],
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
