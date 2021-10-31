from django.views.generic.detail import DetailView
from docsapp.models import Doc
from docsapp.utils import breadcrumb_processor
from django.views.generic.base import ContextMixin
from os import environ


class DocDetailView(DetailView):

    model = Doc

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['context'] = context
        return context

class BrCrumb(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(BrCrumb, self).get_context_data(**kwargs)
        if 'doc_slug' in context:
            doc_slug = context['doc_slug']
        else:
            doc_slug = 'missing'
        context['breadcrumbs'] = breadcrumb_processor(self, doc_slug, context)
        context['breadcrumb_bg_color'] = environ['BREADCRUMB_BG_COLOR']
        return context
