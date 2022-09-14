from pathlib import Path
import os
import json

# LOAD THE ENVIRONMENT VARIABLES
def load_env(fpath: str) -> None:
    env_data = json.loads(open(fpath, "r").read())
    for key, value in env_data.items():
        os.environ[key] = value
CONFPATH = os.getenv('CONFPATH')
if not CONFPATH:
    CONFPATH="/etc/sv/conf-sv-development.json"
load_env(CONFPATH)

# ENVIRONMENT
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
SECRET_KEY = os.getenv('SECRET_KEY', '')
INTERNAL_IPS = os.getenv('INTERNAL_IPS', '').split(',')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# COMMON SETTINGS
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': os.getenv('LOG_LEVEL', 'ERROR'),
            'class': 'logging.FileHandler',
            'filename': os.getenv('LOG_FILE', ''),
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
    'debug_toolbar',
    'django_filters',
    'django_hosts',
    'django_registration',
    'imagekit',
    'nested_admin',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',

    'advertisingapp',
    'blogapp',
    'configapp',
    'contactapp',
    'homeapp',
    'itemsapp',
    'ledgerapp',
    'peopleapp',
    'transactionsapp',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware'
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
            ],
        },
    },
]

WSGI_APPLICATION = 'sodavault.wsgi.application'

AUTH_USER_MODEL = 'configapp.CustomUser'

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

# REST_FRAMEWORK = {
    # # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # # 'PAGE_SIZE': 10,
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
    # ),
    # 'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    # )
# }

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': os.getenv('PGDB_ENGINE'),
        'NAME': os.getenv('PGDB_NAME'),
        'USER': os.getenv('PGDB_USER'),
        'PASSWORD': os.getenv('PGDB_PASSWORD'),
        'HOST': os.getenv('PGDB_HOST'),
        'PORT': os.getenv('PGDB_PORT'),
    }
}

# TIMEZONE, LANGUAGE, ENCODING
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE')
USE_TZ = os.getenv('USE_TZ')
TIME_ZONE = os.getenv('TIME_ZONE')
USE_I18N = os.getenv('USE_I18N')
USE_L10N = os.getenv('USE_L10N')

GRAPHENE = {'SCHEMA': 'graphqlapp.schema.schema', }

# STORAGE
STATICFILES_DIRS = os.getenv('STATICFILES_DIRS', '').split(',')
STATIC_URL = os.getenv('STATIC_URL')
MEDIA_URL = os.getenv('MEDIA_URL')

if (os.getenv('AWS_USE_SPACES', 'False') == 'True'):
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
    AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
        'ACL': 'public-read',
    }

    STATICFILES_STORAGE = 'sodavault.custom_storage.StaticStorage'
    DEFAULT_FILE_STORAGE = 'sodavault.custom_storage.MediaStorage'
else:
    STATIC_ROOT = os.getenv('STATIC_ROOT')
    MEDIA_ROOT = os.getenv('MEDIA_ROOT')

# EMAIL
SERVER_EMAIL = os.getenv('SERVER_EMAIL')
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_USE_TLS = (os.getenv('EMAIL_USE_TLS', 'False') == 'True')
EMAIL_PORT = (os.getenv('EMAIL_PORT', 'False') == 'True')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# registration settings
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window
LOGIN_REDIRECT_URL = '/core/'

# crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

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
        # 'toolbar': 'Basic',
        'skin': 'moonocolor',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
#         'toolbar_CustomConfig': [
            # # custom toolbar os.getenv here
        # ],
        # 'toolbar': 'CustomConfig', # <-- use custom os.getenv
        'height': 100,
        'tabSpaces': 4,
        'removePlugins': 'stylesheetparser',
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    },
    'blog': {
        'skin': 'moonocolor',
        'toolbar_Basic': [
            ['Source', ],
            {
                'name': 'styles',
                'items': [
                    'Format', ]  # 'Styles', 'Font', 'FontSize']
            },

            # ['-', 'Bold', 'Italic',],
            {
                'name': 'basicstyles',
                'items': [
                    'Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                    'Superscript', '-', 'RemoveFormat']
            },
            {'name': 'styles', 'items': ['Styles', ]},
            ['CodeSnippet', 'Code'],
            {
                'name': 'links',
                'items': ['Link', 'Unlink', 'Anchor']
            },
            {
                'name': 'insert',
                'items': [
                     'Image', 'Table', 'HorizontalRule', 'SpecialChar',
                     'PageBreak', 'Iframe', 'UploadImage', ]
            },
            {
                'name': 'codesnippet',
                'items': ['code', 'codeblock', ]
            },
            '/',
            {
                'name': 'paragraph',
                'items': [
                    'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
                    '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft',
                    'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-',
                    'BidiLtr', 'BidiRtl', 'Language']
            },
            {
                'name': 'clipboard',
                'items': [
                    'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-',
                    'Undo', 'Redo']
            },

        ],
        'toolbar': 'Basic',  # <-- use custom os.getenv
        'codeSnippet_theme': 'groovebox',
        'height': 300,
        'tabSpaces': 4,
        # "removePlugins": "stylesheetparser",
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'codesnippet',
            'wordcount',
            # 'spreadsheet',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    },
}
