from advertisingapp.models import Campaign, Assett, Banner
from productapp.models import Category, Tag
from productapp.models import Product, Identifier
from productapp.models import Measurement, BundleOption, DigitalOption
from productapp.models import Promotion, Marketing
from rest_framework import serializers



# productapp.models
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent'] 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug'] 

class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        fields = ['pid_i', 'pid_c', 'gtin', 'isbn'] 

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['weight', 'length', 'width', 'height'] 
        
# need to fix images on model and add them here ...
class MarketingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketing
        fields = ['description_sm', 'description_md', 'description_lg', 'img_1x1_lg'] 
 
class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    identifiers = IdentifierSerializer(read_only=True)
    measurements = MeasurementSerializer(read_only=True)
    marketing_options = MarketingSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['name', 'sku', 'cost', 'price', 'categories', 'tags',
            'identifiers', 'measurements', 'marketing_options'] 

class AdAssettSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assett
        fields = ['name', 'excerpt', 'image_square', 'url_name', 'url_link']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['image_xl', 'image_skyscraper', 'campaign']
        # 'image_lg', 'image_md', 'image_sm', 

# advertisingapp.models
class CampaignSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    assetts = AdAssettSerializer(many=True, read_only=True)
    banners = BannerSerializer(many=True, read_only=True)
    class Meta:
        model = Campaign
        fields = ['name', 'site_name', 'site_url', 'url_analyticscode',
            'date_added', 'date_expires', 'products', 'banners', 'assetts']

class CampaignProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Campaign
        fields = ['name', 'site_name', 'site_url', 'url_analyticscode',
            'date_added', 'date_expires', 'products']

class CampaignAssettsSerializer(serializers.ModelSerializer):
    assetts = AdAssettSerializer(many=True, read_only=True)
    class Meta:
        model = Campaign
        fields = ['name', 'site_name', 'site_url', 'url_analyticscode',
            'date_added', 'date_expires', 'assetts']

class CampaignBannersSerializer(serializers.ModelSerializer):
    banners = BannerSerializer(many=True, read_only=True)
    class Meta:
        model = Campaign
        fields = ['name', 'site_name', 'site_url', 'url_analyticscode',
            'date_added', 'date_expires', 'banners']

