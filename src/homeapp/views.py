from django.views.generic import DetailView
from homeapp.mixins.breadcrumbs import BrCrumb
from homeapp.mixins.metadata import MetaData
from homeapp.mixins.navigation import Navigation
from svapi_py.api import SvApi
from django.conf import settings


"""

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
"""
CONF = settings.CONF

class HomeView(MetaData, BrCrumb, Navigation, DetailView):
    template_name = "homeapp/index.html"

    def setup(self, request, *args, **kwargs):
        # this is information related to SV account
        # self.node_id = kwargs.get('id', '') 
        # self.type_arg = kwargs.get('typeArg', '')
        self.url = CONF.get('svapi', {}).get('host', '')
        self.headers = {
                'Aid': CONF.get('svapi', {}).get('aid', ''),
                'Auth': CONF.get('svapi', {}).get('auth', ''),
                'Prefix': CONF.get('svapi', {}).get('prefix', ''),
                'Content-Type': 'application/json'
                }
        return super().setup(request, *args, **kwargs)

    def get_object(self):
        ## this needs to be connected to a document
        result = SvApi(self.url, self.headers).getOne('document', {})
        result = {
                'title': 'Welcome',
                'body': '''
                Connect this to a SV document ... <br>
                <a href={% url 'common'%}>link name</a>
                '''}
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PageView(MetaData, BrCrumb, Navigation, DetailView):
    template_name = "homeapp/page_detail.html"

    def setup(self, request, *args, **kwargs):
        self.node_id = kwargs.get('id', '') 
        self.type_arg = kwargs.get('typeArg', '')
        return super().setup(request, *args, **kwargs)

    def get_object(self):
        page_id = 'fc9430a7-11f1-45e3-a0d6-58f2b57a1914'
        qlist = [QueryData(alias='page', ID=page_id)]
        return list(Query(f'sv:home:{page_id}', qlist).queryset())[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
