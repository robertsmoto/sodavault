from django.views.generic import DetailView
# from homeapp.mixins.breadcrumbs import BrCrumb
from homeapp.mixins.metadata import MetaData
# from homeapp.mixins.navigation import Navigation
from svapi_py.api import SvApi
from django.conf import settings


CONF = settings.CONF


class HomeView(MetaData, DetailView):
    template_name = "homeapp/index.html"
    extra_context = {
        'title': 'Welcome',
        'breadcrumbs': [
            {'name': 'dashboard', 'namespce': ''}
        ],
    }

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
        # this needs to be connected to a document
        # result = SvApi(self.url, self.headers).getOne('document', {})
        result = {
            'body': "Connect this to a SV document ...",
            'pages': [
                    {'urlNamesapce': 'dashboard', 'urlName': 'dashbord'},
                    {'urlNamesapce': 'dashboard', 'urlName': 'dashbord'},
                    {'urlNamesapce': 'dashboard', 'urlName': 'dashbord'},
            ],
        }
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SVDocView(MetaData, DetailView):
    """Used for viewing sodavault superuser docs."""
    template_name = "homeapp/page_detail.html"

    def setup(self, request, *args, **kwargs):
        self.doc_type = kwargs.get('doc_type', '')
        self.doc_ID = kwargs.get('doc_id', '')
        headers = {
            'Aid': CONF.get('svapi', {}).get('aid', ''),
            'Auth': CONF.get('svapi', {}).get('auth', ''),
            'Prefix': CONF.get('svapi', {}).get('prefix', ''),
            'Content-Type': 'application/json'
        }
        self.svapi = SvApi(request=request, headers=headers)
        params = {'ID': self.doc_ID}
        result, err = self.svapi.getOne('document', params=params)
        self.obj = result
        return super().setup(request, *args, **kwargs)

    def get_template_names(self):
        temp_index = {
            'article': 'homeapp/document_article.html',
            'tech_doc': 'homeapp/document_techdoc.html',
            'page': 'homeapp/document_page.html'
        }
        return temp_index.get(self.doc_type, 'homeapp/article.html')

    def get_object(self):
        return self.obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
