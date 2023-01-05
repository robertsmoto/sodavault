from django.conf import settings

CONF = settings.CONF

def colors(request):
    ctx = {}
    colors = {}
    colors['breadcrum_bg_color'] = CONF.get(
            'colors', {}).get('breadcrumb_bg_color', '')
    ctx['colors'] = colors
    return ctx
