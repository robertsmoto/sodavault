# from blogapp.models import Page
from django.views.generic import TemplateView
from homeapp.mixins.breadcrumbs import BrCrumb
from homeapp.mixins.metadata import MetaData
from homeapp.mixins.navigation import Navigation
from repo.svapi import SVApiRequest


class HomeView(MetaData, BrCrumb, Navigation, TemplateView):
    template_name = "homeapp/index.html"

    def dispatch(self, request, *args, **kwargs):
        qstr = '''
        {
        collections(type: "priceClass") {
            edges {
                node {
                    id
                    document
                }
            }
        }
        }'''
        r = SVApiRequest(qstr).query()
        self.queryset = r.decode_base('collections')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.queryset
        return context
