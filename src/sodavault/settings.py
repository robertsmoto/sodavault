from os.path import exists
from pathlib import Path
import json
import os
import yaml

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
print("CONF", pretty)
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
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'crispy_bootstrap5',
    'debug_toolbar',
    # 'django_hosts',
    'django_registration',
    # 'imagekit',
    'storages',

    'cmsapp',
    'homeapp',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

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

# django_hosts settings
ROOT_HOSTCONF = 'sodavault.hosts'
DEFAULT_HOST = 'default-host'

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
RURI = f'redis://:{RPASS}@{RHOST}:{RPORT}/3'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': RURI,
        'TIMEOUT': 60 * 60 * 6,  # <-- 6 hours
    },
}

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
STATIC_URL = CONF.get('dirs', {}).get('static_url', '')
MEDIA_URL = CONF.get('dirs', {}).get('media_url', '')

if CONF.get('aws', {}).get('use_spaces', False):
    AWS_ACCESS_KEY_ID = CONF.get('aws', {}).get('access_key_id', '')
    AWS_SECRET_ACCESS_KEY = CONF.get('aws', {}).get('secret_access_key', '')
    AWS_STORAGE_BUCKET_NAME = CONF.get(
        'aws', {}).get(
        'storage_bucket_name', '')
    AWS_S3_CUSTOM_DOMAIN = CONF.get('aws', {}).get('custom_domain', '')
    AWS_S3_REGION_NAME = CONF.get('aws', {}).get('s3_region_name', '')
    AWS_S3_ENDPOINT_URL = CONF.get('aws', {}).get('s3_endpoint_url', '')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
        'ACL': 'public-read',
    }

    STATICFILES_STORAGE = 'sodavault.custom_storage.StaticStorage'
    DEFAULT_FILE_STORAGE = 'sodavault.custom_storage.MediaStorage'
else:
    STATIC_ROOT = CONF.get('dirs', {}).get('static_root', '')
    MEDIA_ROOT = CONF.get('dirs', {}).get('media_root', '')

if DEBUG:
    STATIC_URL = CONF.get('dirs', {}).get('static_url_debug', '')
    STATIC_ROOT = CONF.get('dirs', {}).get('static_root_debug', '')
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    MEDIA_URL = CONF.get('dirs', {}).get('media_url_debug', '')
    MEDIA_ROOT = CONF.get('dirs', {}).get('media_root_debug', '')

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

# ck editor
"""
The django-ckeditor documentation is not complete on this issue,
so I am documenting it here.
In order for the ckeditor to render correctly in development environment
(DEBUG=True) all the static files must be available in the
/env/lib/site-packages/ directory. In this project case it is:
~/dev/envs/sodavault/lib/python3.8/site-packages/ckeditor/static/ckeditor/
Specifically the plugin:wordcount and the skin:moonocolor must be installed
in the corresponding directories /static and /plugins. After these packages
are installed, the ckeditor will render correctly in the
development environment.
"""

CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
AWS_QUERYSTRING_AUTH = False
# the wordcount pluging os.getenv is in the ckeditor/os.getenv.js file
CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
        'skin': 'moonocolor',
        'toolbar': 'Basic',
    },
    'sv': {
        'width': 'auto',
        'height': 'auto',
        'autogrow_bottomSpace': 250,
        'uiColor': '#d9d9d9',
        'skin': 'moonocolor',
        'disableNativeSpellChecker': 'false',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Source'],
            # ['Format'],
            ['Format', 'Font', 'FontSize', 'Styles'],
            # ['Styles'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                'Superscript', '-', 'RemoveFormat'],
            ['Link', 'Unlink', 'Anchor'],
            ['CodeSnippet'],
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar',
                'PageBreak', 'Iframe', 'UploadImage'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
                '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft',
                'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-',
                'BidiLtr', 'BidiRtl', 'Language'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-',
                'Undo', 'Redo']
        ],
        'codeSnippet_theme': 'github',
        'tabSpaces': 4,
        'removePlugins': ','.join(['stylesheetparser, exportpdf']),
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            'div',
            'autolink',
            'autoembed',
            'autogrow',
            'codesnippet',
            'embedsemantic',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'wordcount'
        ]),
        'contentsCss': os.path.join(
            STATIC_URL,
            'ckeditor/ckeditor/contents_custom.css'),
    },
}
