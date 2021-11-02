from decouple import config, Csv
from pathlib import Path

##### ENVIRONMENT
DEBUG = config('ENV_DEBUG', default=False, cast=bool)
SECRET_KEY = config('ENV_SECRET_KEY')
INTERNAL_IPS = config('ENV_INTERNAL_IPS', default='', cast=Csv())
ALLOWED_HOSTS = config('ENV_ALLOWED_HOSTS', cast=Csv())

##### COMMON SETTINGS
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition
INSTALLED_APPS = [
    # django autocomplete light
    'dal',
    'dal_select2',
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
    'graphene_django',
    'imagekit',
    'nested_admin',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'advertisingapp',
    'blogapp',
    'configapp',
    'contactapp',
    'coreapp',
    'docsapp',
    'graphqlapp',
    'homeapp',
    'itemsapp',
    'ledgerapp',
    'peopleapp',
    'restapp',
    'shippingapp',
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
        'DIRS': [BASE_DIR / 'templates'],
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

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

##### DATABASE
DATABASES = {
    'default': {
        'ENGINE': config('ENV_DB_ENGINE'),
        'NAME': config('ENV_DB_NAME'),
        'USER': config('ENV_DB_USER'),
        'PASSWORD': config('ENV_DB_PASSWORD'),
        'HOST': config('ENV_DB_HOST'),
        'PORT': config('ENV_DB_PORT'),
    }
}

##### TIMEZONE, LANGUAGE, ENCODING
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = config('ENV_LANGUAGE_CODE')
USE_TZ = config('ENV_USE_TZ')
TIME_ZONE = config('ENV_TIME_ZONE')
USE_I18N = config('ENV_USE_I18N')
USE_L10N = config('ENV_USE_L10N')

GRAPHENE = { 'SCHEMA': 'graphqlapp.schema.schema', }

##### STORAGE
STATIC_URL = config('ENV_STATIC_URL')
MEDIA_URL = config('ENV_MEDIA_URL')
STATICFILES_DIRS = config('ENV_STATICFILES_DIRS', cast=Csv())

if config('ENV_USE_SPCES', cast=bool):
    AWS_ACCESS_KEY_ID = config('ENV_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('ENV_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('ENV_AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = config('ENV_AWS_S3_CUSTOM_DOMAIN')
    AWS_S3_REGION_NAME = config('ENV_AWS_S3_REGION_NAME')
    AWS_S3_ENDPOINT_URL = config('ENV_AWS_S3_ENDPOINT_URL')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
        'ACL': 'public-read',
    }
    STATICFILES_STORAGE = 'sodavault.custom_storage.StaticStorage'
    DEFAULT_FILE_STORAGE = 'sodavault.custom_storage.MediaStorage'
else:
    STATIC_ROOT = config('ENV_STATIC_ROOT')
    MEDIA_ROOT = config('ENV_MEDIA_ROOT')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# registration settings
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window
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
CKEDITOR_IMAGE_BACKEND = "Pillow"
AWS_QUERYSTRING_AUTH = False
# the wordcount pluging config is in the ckeditor/config.js file
CKEDITOR_CONFIGS = {
    'default': {
        # 'toolbar': 'Basic',
        'skin': 'moonocolor',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
#         'toolbar_CustomConfig': [
            # # custom toolbar config here
        # ],
        # 'toolbar': 'CustomConfig', # <-- use custom config
        'height': 100,
        'tabSpaces': 4,
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
            ['Source',],
            {
                'name': 'styles', 
                'items': [
                    'Format',] # 'Styles', 'Font', 'FontSize']
            },

            # ['-', 'Bold', 'Italic',],
            {
                'name': 'basicstyles', 
                'items': [
                    'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 
                    'Superscript', '-', 'RemoveFormat']
            },
            {'name': 'styles', 'items': ['Styles',]},
            ['CodeSnippet', 'Code'],
            {
                'name': 'links', 
                'items': ['Link', 'Unlink', 'Anchor']
            },
            {
                'name': 'insert',
                 'items': [
                     'Image', 'Table', 'HorizontalRule', 'SpecialChar', 
                     'PageBreak', 'Iframe', 'UploadImage',]
            },
            {
                'name': 'codesnippet',
                'items': ['code', 'codeblock',]
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
        'toolbar': 'Basic', # <-- use custom config
        'codeSnippet_theme': 'groovebox',
        'height': 300,
        'tabSpaces': 4,
        # "removePlugins": "stylesheetparser",
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
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



