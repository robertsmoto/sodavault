from decouple import config, Csv
from pathlib import Path
from storages.backends.s3boto3 import S3Boto3Storage


##### ENVIRONMENT
DEBUG = config('ENV_DEBUG', default=False, cast=bool)
SECRET_KEY = config('ENV_SECRET_KEY')
INTERNAL_IPS = config('ENV_INTERNAL_IPS', cast=Csv())
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
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party packages
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'debug_toolbar',
    'django_filters',
    'django_hosts',
    # 'django_registration',
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

# APPEND_SLASH = False

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = config('ENV_STATIC_ROOT')
STATIC_URL = config('ENV_STATIC_URL')
STATICFILES_DIRS = config('ENV_STATICFILES_DIRS', cast=Csv())
MEDIA_ROOT = config('ENV_MEDIA_ROOT')
MEDIA_URL = config('ENV_MEDIA_URL')







##### STORAGE
class MediaStorage(S3Boto3Storage):
    bucket_name = config('ENV_BUCKET_NAME')
    location = 'media'

class StaticStorage(S3Boto3Storage):
    bucket_name = config('ENV_BUCKET_NAME')
    location = 'static'



AWS_ACCESS_KEY_ID = 'YDI52ZS4AW2NDEABYWBS'
AWS_SECRET_ACCESS_KEY = '0vGYAUN5uKmga8d4kjXGsMNoCeyPEi3NW6nf0IS8YeE'
AWS_STORAGE_BUCKET_NAME = 'sodavault'
AWS_S3_CUSTOM_DOMAIN = 'cdn.sodavault.com'
AWS_S3_REGION_NAME = 'nyc3'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
    'ACL': 'public-read',
}

STATICFILES_STORAGE = 'sodavault.components.custom_storage.StaticStorage'
DEFAULT_FILE_STORAGE = 'sodavault.components.custom_storage.MediaStorage'


"""
Default: None
The absolute path to the directory where collectstatic will collect static files for deployment."""
ENV_STATIC_ROOT = "static/"
"""
Default: None
URL to use when referring to static files located in STATIC_ROOT.
"""
ENV_STATIC_URL = "https://cdn.sodavault.com/static/"
"""
This setting defines the additional locations the staticfiles app will traverse if the FileSystemFinder finder is enabled, e.g. if you use the collectstatic or findstatic management command or use the static file serving view.
"""
ENV_STATICFILES_DIRS = [
    '/home/robertsmoto/sodavault/src/templates/',
    '/home/robertsmoto/sodavault/src/static_dir/',
]

"""
Default: '' (Empty string)
Absolute filesystem path to the directory that will hold user-uploaded files.
Example: "/var/www/example.com/media/"
"""
ENV_MEDIA_ROOT = "media/"
"""
Default: '' (Empty string)
URL that handles the media served from MEDIA_ROOT, used for managing stored files. It must end in a slash if set to a non-empty value. You will need to configure these files to be served in both development and production environments.
If you want to use {{ MEDIA_URL }} in your templates, add 'django.template.context_processors.media' in the 'context_processors' option of TEMPLATES.
Example: "http://media.example.com/"
"""
ENV_MEDIA_URL = "https://cdn.sodavault.com/src/media/"



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



