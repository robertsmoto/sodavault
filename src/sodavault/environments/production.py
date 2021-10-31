SECRET_KEY = 'django-insecure-m_3^_3++l6res3(6=^!_7*7)+625ttcq9c5_-8ko*wax(^ls)7'

DEBUG = False

ALLOWED_HOSTS = [
    '142.93.119.107',
    'localhost',
    '127.0.0.1',
    'sodavault.com', 
    '.sodavault.com',
]

SERVER_EMAIL = 'robertsmoto@localhost'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'roberts.moto@gmail.com'
EMAIL_HOST_PASSWORD = 'Iamth3bananam4n.'

ADMINS = [
    ('Scott', 'roberts.moto@gmail.com'),
]

DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
DB_NAME = 'sodavault'
DB_USER = 'sodavault_dbuser'
DB_PASSWORD = 'Swimmingisg00dforyou.'
DB_HOST = 'localhost'
DB_PORT = ''

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

