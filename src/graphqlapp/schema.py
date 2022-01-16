from decouple import config
from graphene import relay, String, Boolean
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from configapp.models import Profile
import advertisingapp.models
import blogapp.models
import graphene
import itemsapp.models
import os
from django.contrib.auth.models import User


# Users
class UserProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        interfaces = (relay.Node, )

    def resolve_avatar(self, info):
        return self.avatar.url


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = [
                "id", "username", "first_name", "last_name", "email",
                "profile"]
        filter_fields = {
                'id': ['iexact'],
                'username': ['iexact'],
                }
        interfaces = (relay.Node, )


# Products
class CategoryNode(DjangoObjectType):
    class Meta:
        model = itemsapp.models.Category
        fields = ["product", "name", "slug", "parent"]
        filter_fields = []
        interfaces = (relay.Node, )


class TagNode(DjangoObjectType):
    class Meta:
        model = itemsapp.models.Category
        fields = ["product", "name", "slug"]
        filter_fields = []
        interfaces = (relay.Node, )


class IdentifierNode(DjangoObjectType):
    class Meta:
        model = itemsapp.models.Identifier
        fields = ["product", "pid_i", "pid_c", "gtin", "isbn"]
        interfaces = (relay.Node, )


class MeasurementNode(DjangoObjectType):
    class Meta:
        model = itemsapp.models.Measurement
        fields = ["product", "weight", "length", "width", "height"]
        filter_fields = []
        interfaces = (relay.Node, )


class BundleOptionNode(DjangoObjectType):
    class Meta:
        model = itemsapp.models.Bundle
        fields = [
                "product", "subproduct", "quantity_min", "quantity_max",
                "is_optional"]
        filter_fields = []
        interfaces = (relay.Node, )


class DigitalOptionNode(DjangoObjectType):
    class Meta:
        model = itemsapp.models.DigitalOption
        fields = ["product", "name"]
        filter_fields = []
        interfaces = (relay.Node, )


class PromotionNode(DjangoObjectType):
    class Meta:
        model = itemsapp.models.Promotion
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
        # fields = ["domain", "name", "description"]
        filter_fields = {
                'domain': ['iexact'],
                }
        interfaces = (relay.Node, )


class BlogCategoryNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Category
        fields = [
                "id", "name", "description", "kwd_list", "image",
                "image_191", "image_21"
                ]
        filter_fields = {
                'id': ['iexact'],
                'name': ['iexact'],
                }
        interfaces = (relay.Node, )


class BlogTagNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Tag
        fields = [
                "id", "name", "description", "kwd_list", "image",
                "image_191", "image_21"
                ]
        filter_fields = {
                'id': ['iexact'],
                'name': ['iexact'],
                }
        interfaces = (relay.Node, )


class BlogPostNode(DjangoObjectType):
    custom_string = graphene.String()

    class Meta:
        model = blogapp.models.Post

        fields = [
                "id", "locations", "categories", "tags", "author",
                "menu_order", "parent", "is_primary_menu",
                "is_secondary_menu", "is_footer_menu",
                "post_type", "title", "excerpt", "body", "slug", "status",
                "featured", "date_published", "date_modified", "kwd_list",
                "image_featured", "image_thumb", "image_191", "image_21",
                "image_title", "image_caption", "footer", "featured_lg",
                "featured_md", "featured_sm", "thumb_lg", "thumb_md",
                "thumb_sm",
                ]
        filter_fields = {
                'id': ['iexact', ],
                'author__username': ['iexact', ],
                'categories__name': ['iexact', 'icontains', 'istartswith'],
                'date_modified': ['isnull', 'iexact', 'icontains'],
                'date_published': ['isnull', 'iexact', 'icontains'],
                'featured': ['iexact'],
                'kwd_list': ['icontains'],
                'locations__domain': ['iexact'],
                'post_type': ['iexact'],
                'slug': ['iexact'],
                'status': ['iexact'],
                'tags__name': ['iexact', 'icontains', 'istartswith'],
                'is_primary_menu': ['iexact'],
                'is_secondary_menu': [],
                'is_footer_menu': ['iexact'],
                }

        interfaces = (relay.Node, )

    def resolve_is_primary_menu(self, info):
        return self.is_primary_menu

    def resolve_is_secondary_menu(self, info):
        return self.is_secondary_menu

    def resolve_is_footer_menu(self, info):
        return self.is_secondary_menu

    def resolve_image_featured(self, info):
        return self.image_featured.url

    def resolve_featured_lg(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.featured_lg)

    def resolve_featured_md(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.featured_md)

    def resolve_featured_sm(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.featured_sm)

    def resolve_image_thumb(self, info):
        return self.image_thumb.url

    def resolve_thumb_lg(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.thumb_lg)

    def resolve_thumb_md(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.thumb_md)

    def resolve_thumb_sm(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.thumb_sm)

    def resolve_pub_year(self, info):
        return self.date_published.strftime("%Y")

    def resolve_pub_month(self, info):
        return self.date_published.strftime("%m")

    def resolve_pub_day(self, info):
        return self.date_published.strftime("%d")

    def resolve_pub_us(self, info):
        return self.date_published.strftime("%b %d, %Y")

    def resolve_mod_us(self, info):
        return self.date_modified.strftime("%b %d, %Y")

    def resolve_reading_time(self, info):
        text = ""
        if len(self.body) > 0 or len(self.excerpt) > 0:
            text = self.body + self.excerpt
        time = round((len(text.split()) / 250))
        timestr = ""
        if time > 1:
            timestr = f"{time} minutes"
        else:
            timestr = "1 minute"
        return timestr

    pub_year = graphene.Field(String, resolver=resolve_pub_year)
    pub_month = graphene.Field(String, resolver=resolve_pub_month)
    pub_day = graphene.Field(String, resolver=resolve_pub_day)
    pub_us = graphene.Field(String, resolver=resolve_pub_us)
    mod_us = graphene.Field(String, resolver=resolve_mod_us)
    reading_time = graphene.Field(String, resolver=resolve_reading_time)
    is_primary_menu = graphene.Field(Boolean, resolver=resolve_is_primary_menu)
    is_secondary_menu = graphene.Field(Boolean, resolver=resolve_is_secondary_menu)
    is_footer_menu = graphene.Field(Boolean, resolver=resolve_is_footer_menu)


class CampaignNode(DjangoObjectType):

    class Meta:
        model = advertisingapp.models.Campaign

        fields = [
                "name", "date_added", "date_expires", "site_name", "site_url",
                "url_analyticscode", "banners", "assetts"]
        filter_fields = {
            'name': ['iexact', 'icontains', 'istartswith'],
            'date_expires': ['isnull']}
        interfaces = (relay.Node, )


class BannerNode(DjangoObjectType):
    class Meta:
        model = advertisingapp.models.Banner
        fields = [
                "name", "excerpt", "url_name", "url_link",
                "ban_square", "ban_lg_square", "ban_md_square",
                "ban_sm_square", "ban_leaderboard", "ban_lg_leaderboard",
                "ban_inline_rectangle", "ban_lg_rectangle", "ban_skyscraper"]

        filter_fields = ["name"]
        interfaces = (relay.Node, )

    def resolve_ban_square(self, info):
        return self.ban_square.url

    def resolve_ban_lg_square(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.ban_lg_square)

    def resolve_ban_md_square(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.ban_md_square)

    def resolve_ban_sm_square(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.ban_sm_square)

    def resolve_ban_leaderboard(self, info):
        return self.ban_leaderboard.url

    def resolve_ban_lg_leaderboard(self, info):
        return self.ban_lg_leaderboard.url

    def resolve_ban_inline_rectangle(self, info):
        return self.ban_inline_rectangle.url

    def resolve_ban_lg_rectangle(self, info):
        return self.ban_lg_rectangle.url

    def resolve_ban_skyscraper(self, info):
        return self.ban_skyscraper.url


class Query(graphene.ObjectType):
    # products
    # products = relay.Node.Field(ProductNode)
    # all_products = DjangoFilterConnectionField(ProductNode)

    # category = relay.Node.Field(CategoryNode)
    # all_categories = DjangoFilterConnectionField(CategoryNode)

    # tag = relay.Node.Field(TagNode)
    # all_tags = DjangoFilterConnectionField(TagNode)

    # users
    all_users = relay.Node.Field(UserType)
    all_users = DjangoFilterConnectionField(UserType)

    # blog by locations
    all_locations = relay.Node.Field(BlogLocationNode)
    all_location = DjangoFilterConnectionField(BlogLocationNode)

    # blog and pages
    posts_and_pages = relay.Node.Field(BlogPostNode)
    all_posts_and_pages = DjangoFilterConnectionField(BlogPostNode)
    post_categories = relay.Node.Field(BlogCategoryNode)
    all_post_categories = DjangoFilterConnectionField(BlogCategoryNode)
    post_tags = relay.Node.Field(BlogTagNode)
    all_post_tags = DjangoFilterConnectionField(BlogTagNode)

    # ads
    campaign = relay.Node.Field(CampaignNode)
    all_campaigns = DjangoFilterConnectionField(CampaignNode)

    banner = relay.Node.Field(BannerNode)
    all_banners = DjangoFilterConnectionField(BannerNode)


schema = graphene.Schema(query=Query)
