from django_hosts import patterns, host

host_patterns = patterns(
        '',
        host(r'', 'sodavault.urls', name='default-host'),
        host(r'api|api-stage', 'graphqlapp.urls', name='api'),
        host(r'blog', 'blogapp.urls', name='blog'),
        host(r'auth', 'registration.auth_urls', name='auth'),
        host(
            r'accounts',
            'registration.backends.default.urls',
            name='accounts'),
)
