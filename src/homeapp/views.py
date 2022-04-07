from blogapp.models import Page
from django.views.generic import TemplateView
from homeapp.mixins.breadcrumbs import BrCrumb
from homeapp.mixins.metadata import MetaData
from homeapp.mixins.navigation import Navigation


class HomeView(MetaData, BrCrumb, Navigation, TemplateView):
    template_name = "blogapp/page_detail.html"
    queryset = Page.objects.get(slug='home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset, created = Page.objects.get_or_create(slug='home')
        if created:
            print("###created new Page with slug 'home'")
        context['object'] = queryset
        return context
