from os.path import exists
from pathlib import Path
import json
import os
import yaml
from django.urls import reverse_lazy

"""Switch beween servers using:
    $ SERVER=development python manage.py runserver """

BASE_DIR = Path(__file__).resolve().parent.parent
SERVER = os.getenv('SERVER', 'development').lower()
CONFIG_DIR = os.path.join('/etc/sv/', SERVER)

# read the ini.yaml file into CONF{} then dict is available at: settings.CONF
file_exists = exists(os.path.join(CONFIG_DIR, 'ini.yaml'))
if not file_exists:
    raise Exception("Can't find ini.yaml file.")

file_exists = exists(os.path.join(CONFIG_DIR, 'settings.yaml'))
if not file_exists:
    raise Exception("Can't find settings.yaml file.")

ini_dict = {}
set_dict = {}

with open(os.path.join(CONFIG_DIR, 'ini.yaml'), "r") as stream:
    try:
        ini_dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(os.path.join(CONFIG_DIR, 'settings.yaml'), "r") as stream:
    try:
        set_dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

CONF = {**ini_dict, **set_dict}

# ################################################
pretty = json.dumps(CONF, indent=2)
# print("CONF", pretty)
# ################################################

# ENVIRONMENT
DEBUG = CONF.get('django', {}).get('debug', False)
SECRET_KEY = CONF.get('django', {}).get('secret_key', '')
INTERNAL_IPS = CONF.get('django', {}).get('internal_ips', '').split(',')
ALLOWED_HOSTS = CONF.get('django', {}).get('allowed_hosts', '').split(',')

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': CONF.get('log', {}).get('level', 'ERROR'),
            'class': 'logging.FileHandler',
            'filename': CONF.get('log', {}).get('file', ''),
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Admins
ADMINS = [
    ('Scott', 'roberts.moto@gmail.com'),
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    # third party packages
    'debug_toolbar',
    'django_bootstrap5',
    'django_editorjs_fields',
    'django_registration',
    'django_select2',
    'storages',

    # apps
    'cmsapp',
    'homeapp',
]

# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
# CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sodavault.urls'

# # django_hosts settings
# ROOT_HOSTCONF = 'sodavault.hosts'
# DEFAULT_HOST = 'default-host'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # custom processors
                'homeapp.cntx.processors.navigation',
                'homeapp.mixins.context_processors.colors',
            ],
        },
    },
]

WSGI_APPLICATION = 'sodavault.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': CONF.get('postgres', {}).get('engine', ''),
        'NAME': CONF.get('postgres', {}).get('name', ''),
        'USER': CONF.get('postgres', {}).get('user', ''),
        'PASSWORD': CONF.get('postgres', {}).get('pass', ''),
        'HOST': CONF.get('postgres', {}).get('host', ''),
        'PORT': CONF.get('postgres', {}).get('port', ''),
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# CACHE (FOR SESSION CACHING)
RPASS = CONF.get('redis', {}).get('pass', '')
RHOST = CONF.get('redis', {}).get('host', '')
RPORT = CONF.get('redis', {}).get('port', '')
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://:{RPASS}@{RHOST}:{RPORT}/3',
        'TIMEOUT': 60 * 60 * 6,  # <-- 6 hours
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        'LOCATION': f'redis://:{RPASS}@{RHOST}:{RPORT}/4',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SELECT2_CACHE_BACKEND = "select2"
SELECT2_THEME = 'bootstrap-5'

# TIMEZONE, LANGUAGE, ENCODING
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = CONF.get('django', {}).get('language_code', '')
USE_TZ = CONF.get('django', {}).get('use_tz', '')
TIME_ZONE = CONF.get('django', {}).get('time_zone')
USE_I18N = CONF.get('django', {}).get('use_I18N', '')
USE_L10N = CONF.get('django', {}).get('use_L10N', '')

GRAPHENE = {'SCHEMA': 'graphqlapp.schema.schema', }

# STORAGE
STATICFILES_DIRS = CONF.get('dirs', {}).get('staticfiles_dirs', '').split(',')
MEDIA_ROOT = CONF.get('dirs', {}).get('media_root', '')
MEDIA_URL = CONF.get('dirs', {}).get('media_url', '')

if CONF.get('aws', {}).get('use_spaces', False):
    AWS_ACCESS_KEY_ID = CONF.get('aws', {}).get('access_key_id', '')
    AWS_SECRET_ACCESS_KEY = CONF.get('aws', {}).get('secret_access_key', '')
    AWS_STORAGE_BUCKET_NAME = CONF.get(
        'aws', {}).get(
        'storage_bucket_name', '')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
        'ACL': 'public-read',
    }
    AWS_S3_REGION_NAME = CONF.get('aws', {}).get('region_name', '')
    AWS_S3_ENDPOINT_URL = CONF.get('aws', {}).get('endpoint_url', '')
    AWS_S3_CUSTOM_DOMAIN = CONF.get('aws', {}).get('custom_domain', '')
    AWS_DEFAULT_ACL = 'public-read'
    # AWS_S3_ADDRESSING_STYLE = 'path'

    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    AWS_LOCATION = 'static'
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/"
    EDITORJS_STORAGE_BACKEND = 'sodavault.custom_storage.S3MediaStorage'

else:
    STATIC_URL = CONF.get('dirs', {}).get('static_url', '')
    STATIC_ROOT = CONF.get('dirs', {}).get('static_root', '')
    # EDITORJS_STORAGE_BACKEND = 'storages.backends.s3boto3.S3Boto3Storage'

# EMAIL
SERVER_EMAIL = CONF.get('email', {}).get('server_email', '')
EMAIL_BACKEND = CONF.get('email', {}).get('email_backend', '')
EMAIL_HOST = CONF.get('email', {}).get('email_host', '')
EMAIL_USE_TLS = CONF.get('email', {}).get('email_use_tls', False)
EMAIL_PORT = CONF.get('email', {}).get('email_port', 587)
EMAIL_HOST_USER = CONF.get('email', {}).get('email_host_user', '')
EMAIL_HOST_PASSWORD = CONF.get('email', {}).get('email_host_password', '')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# registration settings
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window
LOGIN_REDIRECT_URL = '/cms/dashboard/'

# editor_js settings
EDITORJS_IMAGE_UPLOAD_PATH = ''  # path set in cmsapp.views.S3ImageUploadView
EDITORJS_EMBED_HOSTNAME_ALLOWED = (
    'player.vimeo.com',
    'www.youtube.com',
    'coub.com',
    'vine.co',
    'imgur.com',
    'gfycat.com',
    'player.twitch.tv',
    'player.twitch.tv',
    'music.yandex.ru',
    'codepen.io',
    'www.instagram.com',
    'twitframe.com',
    'assets.pinterest.com',
    'www.facebook.com',
    'www.aparat.com'
)

EDITORJS_VERSION = 'latest'

EDITORJS_DEFAULT_CONFIG_TOOLS = {
    'Image': {
        'class': 'ImageTool',
        'inlineToolbar': True,
        "config": {
            "endpoints": {
                "byFile": reverse_lazy('editorjs_image_upload'),
                "byUrl": reverse_lazy('editorjs_image_by_url')
            }
        },
    },
    'Header': {
        'class': 'Header',
        'config': {
            'placeholder': 'Enter a header',
            'levels': [1, 2, 3, 4],
            'defaultLevel': 1,
        },
    },
    'Checklist': {'class': 'Checklist', 'inlineToolbar': True},
    'List': {'class': 'List', 'inlineToolbar': True},
    'Quote': {'class': 'Quote', 'inlineToolbar': True},
    'Raw': {'class': 'RawTool'},
    'Code': {'class': 'CodeTool'},
    'Embed': {'class': 'Embed'},
    'InlineCode': {'class': 'InlineCode'},
    'Delimiter': {'class': 'Delimiter'},
    'Warning': {'class': 'Warning', 'inlineToolbar': True},
    'LinkTool': {
        'class': 'LinkTool',
        'config': {
            # Backend endpoint for url data fetching
            'endpoint': reverse_lazy('editorjs_linktool'),
        }
    },
    'Marker': {'class': 'Marker', 'inlineToolbar': True},
    'Table': {'class': 'Table', 'inlineToolbar': True},
}
