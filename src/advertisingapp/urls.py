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
from .views import CampaignAutocomplete
from .views import CampaignListView, CampaignCreateView, CampaignUpdateView, CampaignDeleteView
from .views import AdvertisingView, AssettView, BannerView

urlpatterns = [
    # using the blogapp to serve the homepage
    path(
        '', 
        AdvertisingView.as_view(
            extra_context={
                'doc_slug': 'ad-home',
            }
        ), 
        name='ad-home',
    ),
    path(
        'assett/', 
        AssettView.as_view(
            extra_context={
                'doc_slug': 'ad-assett',
            }
        ), 
        name='ad-assett',
    ),
    path(
        'banner/', 
        BannerView.as_view(
            extra_context={
                'doc_slug': 'ad-banner',
            }
        ), 
        name='ad-banner',
    ),
    path(
        'assett/', 
        AssettView.as_view(extra_context={'doc_slug': 'ad-assett',}), 
        name='ad-assett',
    ),
    path(
        'campaign-autocomplete/', 
        CampaignAutocomplete.as_view(), 
        name='campaign-autocomplete',
    ),
    path(
        'campaign-list/', 
        CampaignListView.as_view(extra_context={'doc_slug': 'campaign-list',}), 
        name='campaign-list',
    ),
    path(
        'campaign-create/', 
        CampaignCreateView.as_view(extra_context={'doc_slug': 'campaign-create',}), 
        name='campaign-create',
    ),
    path(
        '<pk>/campaign-update/', 
        CampaignUpdateView.as_view(extra_context={'doc_slug': 'campaign-update',}), 
        name='campaign-update',
    ),
    path(
        '<pk>/campaign-delete/', 
        CampaignDeleteView.as_view(extra_context={'doc_slug': 'campaign-delete',}), 
        name='campaign-delete',
    ),

]
