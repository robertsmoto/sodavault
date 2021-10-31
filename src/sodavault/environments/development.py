DEBUG = True
SECRET_KEY = 'django-insecure-m_3^_3++l6res3(6=^!_7*7)+625ttcq9c5_-8ko*wax(^ls)7'

INTERNAL_IPS = [ '127.0.0.1', '::1', '0.0.0.0' ]

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'www.sodavault.local',
    'api.sodavault.local',
    'accounts.sodavault.local',
    'auth.sodavault.local',
    'blog.sodavault.local',
]

DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
DB_NAME = 'sodavault'
DB_USER = 'sodavault_dbuser'
DB_PASSWORD = 'Swimmingisg00dforyou.'
DB_HOST = 'localhost'
DB_PORT = ''

"""
Default: None
The absolute path to the directory where collectstatic will collect static files for deployment."""
ENV_STATIC_ROOT = "/home/robertsmoto/dev/sodavault/src/collectstatic/"
"""
Default: None
URL to use when referring to static files located in STATIC_ROOT.
"""
ENV_STATIC_URL = "/static/"
"""
This setting defines the additional locations the staticfiles app will traverse if the FileSystemFinder finder is enabled, e.g. if you use the collectstatic or findstatic management command or use the static file serving view.
"""
ENV_STATICFILES_DIRS = [
    # not serving templates in development --> '/home/robertsmoto/dev/sodavault/templates/',
    '/home/robertsmoto/dev/sodavault/src/static_dir/',
    ]

"""
Default: '' (Empty string)
Absolute filesystem path to the directory that will hold user-uploaded files.
Example: "/var/www/example.com/media/"
"""
ENV_MEDIA_ROOT = "/home/robertsmoto/dev/sodavault/src/media/"
"""
Default: '' (Empty string)
URL that handles the media served from MEDIA_ROOT, used for managing stored files. It must end in a slash if set to a non-empty value. You will need to configure these files to be served in both development and production environments.
If you want to use {{ MEDIA_URL }} in your templates, add 'django.template.context_processors.media' in the 'context_processors' option of TEMPLATES.
Example: "http://media.example.com/"
"""
ENV_MEDIA_URL = "/media/"


