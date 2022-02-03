from blogapp.models import Post
from django.views.generic.base import ContextMixin


class Navigation(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(Navigation, self).get_context_data(**kwargs)
        context["navigation"] = {}
        navigation = context["navigation"]
        pages_q = Post.objects.filter(
            locations__domain="sodavault.com",
            status="PUBLI",
            post_type="PAGE",
            is_primary_menu=True
        ).values_list('title', 'post_type', 'slug')
        navigation["pages"] = pages_q
        return context
