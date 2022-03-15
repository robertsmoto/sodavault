from blogapp.models import Page
from django.views.generic.base import ContextMixin
import pickle


class Navigation(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(Navigation, self).get_context_data(**kwargs)
        context["navigation"] = {}
        navigation = context["navigation"]
        pages_q = Page.objects.filter(
            websites__domain="sodavault.com",
            status="PUBLI",
            is_primary=True
        ).values_list('title', 'slug')
        pages_q.query = pickle.loads(pickle.dumps(pages_q.query))
        navigation["pages"] = pages_q
        return context
