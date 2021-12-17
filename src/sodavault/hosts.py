from django_hosts import patterns, host
from decouple import config

DEBUG = config('ENV_DEBUG', default=False, cast=bool)

API_HOST = config('ENV_API_HOST')

host_patterns = patterns(
        '',
        host(r'', 'sodavault.urls', name='default-host'),
        host(r'%s', 'graphqlapp.urls', name='api') % (API_HOST),
        host(r'blog', 'blogapp.urls', name='blog'),
        host(r'auth', 'registration.auth_urls', name='auth'),
        host(
            r'accounts',
            'registration.backends.default.urls',
            name='accounts'),
)
