from django.conf import settings
from django.views.generic import ListView
from homeapp.mixins.breadcrumbs import BrCrumb
from homeapp.mixins.metadata import MetaData
from homeapp.mixins.navigation import Navigation
from svapi_py.api import SvApi
# from configapp.constants import COLLECTION

CONF = settings.CONF

class ArticleList(MetaData, BrCrumb, Navigation, ListView):

    template_name = 'creatorapp/article_list.html'

    def setup(self, request, *args, **kwargs):
        setup = super().setup(request, *args, **kwargs)
        # apiCred = request.user.apicredentials
        self.headers = {
                'Aid': request.user.id,
                'Auth': apiCred.auth,
                'Prefix': apiCred.prefix,
                'Content-Type': 'application/json'
                }
        return setup

    def get_queryset(self):
        svApiUrl = CONF.get('svapi', {}).get('host', '')
        results =  SvApi(svApiUrl, self.headers) \
                .getMany('set', params={
                    'ID': COLLECTION.get('article', ''),
                    'start': 0,
                    'end': -1
                    })
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
