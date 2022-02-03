from django.views.generic import TemplateView
from homeapp.mixins import Navigation
from blogapp.models import Post


class HomeView(Navigation, TemplateView):
    template_name = "blogapp/page_detail.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["context"] = context
        slug = 'home'
        try:
            post_q = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            post_q = None
        context["post"] = post_q
        return context
