from blogapp.models import Page, Doc
from django.views.generic.base import ContextMixin


class Navigation(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(Navigation, self).get_context_data(**kwargs)
        context["navigation"] = {}
        navigation = context["navigation"]
        pages_q = Page.objects \
            .filter(
                    websites__domain="sodavault.com",
                    status="PUBLI",
                    is_primary=True
                    ) \
            .only('title', 'slug')
        navigation["pages"] = pages_q

        docs_q = Doc.objects \
            .filter(
                    websites__domain="sodavault.com",
                    status="PUBLI",
                    is_primary=True
                    ) \
            .only('title', 'slug')
        navigation["docs"] = docs_q
        return context
