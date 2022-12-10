from django.views.generic.base import ContextMixin
from svapi_py.api import SvApi



class Navigation(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(Navigation, self).get_context_data(**kwargs)
        context["navigation"] = {}
        navigation = context["navigation"]
        # pqdata = QueryData(
                # alias='pages', typeArg='page',
                # docFilter="document->'menu'->>'isPrimary'",
                # docFilterValue='true'
                # )
        # pq = Query('sv:nav:pages', [pqdata]).queryset()
        # navigation["pages"] = pq

        # docs_q = Doc.objects \
            # .filter(
                    # websites__domain="sodavault.com",
                    # status="PUBLI",
                    # is_primary=True
                    # ) \
            # .only('title', 'slug')
        # navigation["docs"] = docs_q
        return context
