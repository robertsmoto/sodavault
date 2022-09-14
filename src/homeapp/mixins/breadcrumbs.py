from django.urls import reverse, resolve
from django.views.generic.base import ContextMixin
import os


def breadcrumb_processor(self, *args, **kwargs) -> str:
    """Creates the breadcrumbs string."""

    # maps to readable name that will render in the breadcrumb
    urlname_index = {
            'blogapp-article-list': {
                'hrn': 'articles',
                'gobackto': 'home',
                'gobackto_kwargs': {}
                },
            'blogapp-article-detail': {
                'hrn': 'metadata',
                'gobackto': 'article-list',
                'gobackto_kwargs': {}
                },
            'blogapp-doc-list': {
                'hrn': 'docs',
                'gobackto': 'home',
                'gobackto_kwargs': {}
                },
            'blogapp-doc-detail': {
                'hrn': 'metadata',
                'gobackto': 'blogapp-doc-list',
                'gobackto_kwargs': {}
                },
            'blogapp-page-list': {
                'hrn': 'pages',
                'gobackto': 'home',
                'gobackto_kwargs': {}
                },
            'blogapp-page-detail': {
                'hrn': 'metadata',
                'gobackto': 'blogapp-page-list',
                'gobackto_kwargs': {}
                },
            'blogapp-category-list': {
                'hrn': 'topics',
                'gobackto': 'home',
                'gobackto_kwargs': {}
                },
            'blogapp-tag-list': {
                'hrn': 'interests',
                'gobackto': 'home',
                'gobackto_kwargs': {}
                },

            'blogapp-search': {
                'hrn': 'search',
                'gobackto': 'home',
                'gobackto_kwargs': {}
                },

            'home': {
                'hrn': 'home',
                'gobackto': 'home',
                'gobackto_kwargs': {}
                },

            }

    brdcrm_list = []

    def brdcrm_recursion(url_name=None, kwargs=None):

        urlname_dict = urlname_index.get(url_name, {})
        if not urlname_dict:
            print("##not url name")
            return brdcrm_list

        hrn = urlname_dict.get('hrn', '')
        url = reverse(url_name, kwargs=kwargs)

        brdcrm_dict = {}
        brdcrm_dict['hrn'] = hrn
        brdcrm_dict['url'] = url

        brdcrm_list.insert(0, brdcrm_dict)

        if 'home' in url_name:
            return brdcrm_list

        gobackto = urlname_dict.get('gobackto', '')
        gobackto_kwargs = urlname_dict.get('gobackto_kwargs', '')

        for k, v in gobackto_kwargs.items():
            gobackto_kwargs[k] = kwargs.get(k, '')

        print("###goback", gobackto)
        print("###goback_kwargs", gobackto_kwargs)

        return brdcrm_recursion(url_name=gobackto, kwargs=gobackto_kwargs)

    url_name = resolve(self.request.path_info).url_name

    return brdcrm_recursion(url_name=url_name, kwargs=self.kwargs)


class BrCrumb(ContextMixin):

    def get_context_data(self, **kwargs):
        breadcrumbs = breadcrumb_processor(self=self)
        context = super().get_context_data()
        context['breadcrumbs'] = breadcrumbs
        context['breadcrumb_bg_color'] = os.getenv('BREADCRUMB_BG_COLOR', '')
        return context
