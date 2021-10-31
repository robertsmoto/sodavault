from django.views.generic import TemplateView
from homeapp.mixins import Navigation # , MetaData
from django.contrib.auth.mixins import LoginRequiredMixin

# LoginRequiredMixin, 
class CoreView(LoginRequiredMixin, Navigation, TemplateView):
    template_name = "coreapp/core.html"

    def get_context_data(self, **kwargs):
        context = super(CoreView, self).get_context_data(**kwargs)
        context["context"] = context
        return context

