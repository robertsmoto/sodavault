"""sodavault URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
import itemsapp.views as views
# from .views import AttrAutocomplete, AttrTermAutocomplete
# from .views import VarAttrAutocomplete, VarTermAutocomplete


urlpatterns = [
    path(
        '',
        views.ProductHomeView.as_view(
            extra_context={
                'doc_slug': 'product-home',
            }
        ),
        name='product-home',
    ),
#     path('attr-autocomplete', AttrAutocomplete.as_view(), name='attr-autocomplete'), 
    # path('attr-term-autocomplete', AttrTermAutocomplete.as_view(), name='attr-term-autocomplete'), 
    # path('var-attr-autocomplete', VarAttrAutocomplete.as_view(), name='var-attr-autocomplete'), 
#     path('var-term-autocomplete', VarTermAutocomplete.as_view(), name='var-term-autocomplete'), 
    # path(
        # 'product-list/',
        # views.ProductListView.as_view(
            # extra_context={'doc_slug': 'product-list', }),
        # name='product-list',
    # ),
#     path(
        # 'product-create/',
        # views.ProductCreateView.as_view(
            # extra_context={'doc_slug': 'product-create', }),
        # name='product-create',
    # ),
    # path(
        # '<pk>/product-update/',
        # views.ProductUpdateView.as_view(
            # extra_context={'doc_slug': 'product-update', }),
        # name='product-update',
    # ),
    # path(
        # '<pk>/product-delete/',
        # views.ProductDeleteView.as_view(
            # extra_context={'doc_slug': 'product-delete', }),
        # name='product-delete',
#     ),

]
