from advertisingapp.models import Campaign, Banner, Assett
from productapp.models import Product
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProductSerializer
from .serializers import CampaignSerializer, CampaignBannersSerializer
from .serializers import CampaignAssettsSerializer, CampaignProductsSerializer
from django.db.models import Q
from django.utils import timezone


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


# class CampaignViewSet(viewsets.ModelViewSet):
    # """
    # API endpoint that allows campaign to be viewed or edited.
    # """
    # queryset = Campaign.objects.filter(
        # Q(date_expires__isnull=True) |
        # Q(date_expires__gte=timezone.now())
    # ).order_by('-date_added')
    # serializer_class = CampaignSerializer
#     permission_classes = [permissions.IsAuthenticated]

"""
router.register(r'campaign_products', views.CampaignProductsViewSet)
router.register(r'campaign_banners', views.CampaignBannersViewSet)
router.register(r'campaign_assetts', views.CampaignAssettsViewSet)
"""

class CampaignViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bannner to be viewed or edited.
    """
    queryset = Campaign.objects.filter(
        Q(date_expires__isnull=True) |
        Q(date_expires__gte=timezone.now())
    ).prefetch_related('products', 'banners', 'assetts')
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

# class CampaignProductsViewSet(viewsets.ModelViewSet):
    # """
    # API endpoint that allows campaign-products to be viewed or edited.
    # """
    # queryset = Campaign.objects.filter(
        # products__isnull=False
    # ).prefetch_related(
        # 'products'
    # ).exclude(
        # date_expires__lte=timezone.now()
    # ).distinct('id').order_by('id')
    # serializer_class = CampaignProductsSerializer
    # permission_classes = [permissions.IsAuthenticated]

class CampaignBannersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bannner to be viewed or edited.
    """
    queryset = Campaign.objects.filter(
        banners__isnull=False
    ).prefetch_related(
        'banners'
    ).exclude(
        date_expires__lte=timezone.now()
    ).distinct('id').order_by('id')
    serializer_class = CampaignBannersSerializer
    permission_classes = [permissions.IsAuthenticated]


class CampaignAssettsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bannner to be viewed or edited.
    """
    queryset = Campaign.objects.filter(
        assetts__isnull=False
    ).prefetch_related(
        'assetts'
    ).exclude(
        date_expires__lte=timezone.now()
    ).distinct('id').order_by('id')
    serializer_class = CampaignAssettsSerializer
    permission_classes = [permissions.IsAuthenticated]

