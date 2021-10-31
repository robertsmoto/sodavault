from django.contrib import admin
from django.conf import settings
from django_hosts import patterns, host


host_patterns = patterns('',
    host(r'', 'sodavault.urls', name='default-host'), 
    host(r'api', 'graphqlapp.urls', name='api'),
    host(r'blog', 'blogapp.urls', name='blog'),
    host(r'auth', 'registration.auth_urls', name='auth'),
    host(r'accounts', 'registration.backends.default.urls', name='accounts'),
)


"""
use auth.sodavault.com for authorization views
Another URLConf is also provided – at registration.auth_urls – which just handles the Django auth views, should you want to put those at a different location.




host_patterns = patterns('path.to',
            host(r'www', 'urls.default', name='default'),
            host(r'api', 'urls.api', name='api'),
            host(r'admin', 'urls.admin', name='admin', scheme='https://'),
        )
"""
