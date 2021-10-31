from django.urls import include, path
from rest_framework import routers
from restapp import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'campaigns', views.CampaignViewSet)
# router.register(r'campaign_products', views.CampaignProductsViewSet)
router.register(r'campaign_banners', views.CampaignBannersViewSet)
router.register(r'campaign_assetts', views.CampaignAssettsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
