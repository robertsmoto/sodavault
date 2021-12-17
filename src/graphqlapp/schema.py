from django.db.models import Q
from datetime import datetime
import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from itemsapp.models import Measurement, Promotion, Marketing
import blogapp.models
from itemsapp.models import DigitalOption, Bundle, ProductAttributeJoin
from itemsapp.models import Product, Identifier, Category, Tag 
from advertisingapp.models import Campaign, Assett, Banner
from django.contrib.auth.mixins import LoginRequiredMixin


# Products
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        fields = ["product", "name", "slug", "parent"]
        filter_fields = []
        interfaces = (relay.Node, )


class TagNode(DjangoObjectType):
    class Meta:
        model = Category
        fields = ["product", "name", "slug"]
        filter_fields = []
        interfaces = (relay.Node, )


class IdentifierNode(DjangoObjectType):
    class Meta:
        model = Identifier
        fields = ["product", "pid_i", "pid_c", "gtin", "isbn"]
        interfaces = (relay.Node, )


class MeasurementNode(DjangoObjectType):
    class Meta:
        model = Measurement
        fields = ["product", "weight", "length", "width", "height"]
        filter_fields = []
        interfaces = (relay.Node, )


class BundleOptionNode(DjangoObjectType):
    class Meta:
        model = Bundle
        fields = [
                "product", "subproduct", "quantity_min", "quantity_max",
                "is_optional"]
        filter_fields = []
        interfaces = (relay.Node, )


class DigitalOptionNode(DjangoObjectType):
    class Meta:
        model = DigitalOption
        fields = ["product", "name"]
        filter_fields = []
        interfaces = (relay.Node, )


class PromotionNode(DjangoObjectType):
    class Meta:
        model = Promotion
        fields = [
                "product", "promotion_override", "name", "slug", "begins",
                "ends", "percentage", "fixed", "price", "is_free_shipping",
                "bogx"]
        filter_fields = []
        interfaces = (relay.Node, )


# blog and pages
class BlogLocationNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Location
        fields = ["domain", "name", "description"]
        filter_fields = ["domain"]
        interfaces = (relay.Node, )


class BlogCategoryNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Category
        fields = ["name", "description", "image"]
        filter_fields = ["name"]
        interfaces = (relay.Node, )


class BlogTagNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Tag
        fields = ["name"]
        filter_fields = ["name"]
        interfaces = (relay.Node, )


class BlogPostNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Post
        fields = [
                "locations", "categories", "tags", "author", "menu_order",
                "parent", "primary_menu", "post_type", "title", "excerpt",
                "body", "slug", "status", "featured", "date_published",
                "date_modified", "keyword_list", "featured_image",
                "thumbnail_image", "image_title" "image_caption", "footer"]
        filter_fields = [
                "locations", "categories", "tags", "author", "menu_order",
                "parent", "primary_menu", "post_type", "title", "excerpt",
                "body", "slug", "status", "featured", "date_published",
                "date_modified", "keyword_list", "featured_image",
                "thumbnail_image", "image_title" "image_caption", "footer"]

        interfaces = (relay.Node, )


class MarketingNode(DjangoObjectType):
    class Meta:
        model = Marketing
        fields = [
                "product", "description_sm", "description_md",
                "description_lg", "img_1x1_lg", "img_1x1_md", "img_1x1_sm",
                "img_2x1_lg", "img_2x1_md", "img_2x1_sm", "img_1x2_lg",
                "img_1x2_md", "img_1x2_sm", "img_16x9", "img_191x1"]

        filter_fields = []
        interfaces = (relay.Node, )

    def resolve_img_1x1_lg(self, info):
        return self.img_1x1_lg.url

    def resolve_img_1x1_md(self, info):
        return self.image_xl.url

    def resolve_img_1x1_sm(self, info):
        return self.img_1x1_sm.url

    def resolve_img_2x1_lg(self, info):
        return self.img_2x1_lg.url

    def resolve_img_2x1_md(self, info):
        return self.img_2x1_md.url

    def resolve_img_2x1_sm(self, info):
        return self.img_2x1_sm.url

    def resolve_img_1x2_lg(self, info):
        return self.img_1x2_lg.url

    def resolve_img_1x2_md(self, info):
        return self.img_1x2_md.url

    def resolve_img_1x2_sm(self, info):
        return self.img_1x2_sm.url

    def resolve_img_16x9(self, info):
        return self.img_16x9.url

    def resolve_img_191x1(self, info):
        return self.img_191x1.url


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        fields = [
                "name", "sku", "cost", "price", "categories", "tags",
                "identifiers", "measurements", "digital_options", "promotions",
                "marketing"]
        filter_fields = ["name"]
        interfaces = (relay.Node, )


class CampaignNode(DjangoObjectType):

    class Meta:
        model = Campaign

        fields = [
                "name", "date_added", "date_expires", "site_name", "site_url",
                "url_analyticscode", "banners", "assetts"]
        filter_fields = {
            'name': ['iexact', 'icontains', 'istartswith'],
            'date_expires': ['isnull']}
        interfaces = (relay.Node, )


class AssettNode(DjangoObjectType):
    class Meta:
        model = Assett
        fields = [
                "campaign", "product", "name", "excerpt", "url_name",
                "url_link", "img_1x1"]
        filter_fields = []
        interfaces = (relay.Node, )

    def resolve_img_1x1(self, info):
        return self.img_1x1.url


class BannerNode(DjangoObjectType):
    class Meta:
        model = Banner
        fields = [
                "campaign", "image_xl", "image_lg", "image_md", "image_sm",
                "image_skyscraper"]
        filter_fields = ['campaign']
        interfaces = (relay.Node, )

    def resolve_image_xl(self, info):
        return self.image_xl.url

    def resolve_image_lg(self, info):
        return self.image_lg.url

    def resolve_image_md(self, info):
        return self.image_md.url

    def resolve_image_sm(self, info):
        return self.image_sm.url

    def resolve_image_skyscraper(self, info):
        return self.image_skyscraper.url

#     # blog and pages
    # posts_and_pages = relay.Node.Field(BlogPostNode)
#     all_posts_and_pages = DjangoFilterConnectionField(BlogPostNode)


class Query(graphene.ObjectType):
    # products
    products = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    tag = relay.Node.Field(TagNode)
    all_tags = DjangoFilterConnectionField(TagNode)

    # ads
    campaign = relay.Node.Field(CampaignNode)
    all_campaigns = DjangoFilterConnectionField(CampaignNode)

    banner = relay.Node.Field(BannerNode)
    all_banners = DjangoFilterConnectionField(BannerNode)

    assett = relay.Node.Field(AssettNode)
    all_assetts = DjangoFilterConnectionField(AssettNode)


schema = graphene.Schema(query=Query)
