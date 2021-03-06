"""
WSGI config for sodavault project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'sodavault.settings'
# os.environ['DJANGO_ENV'] = 'production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
