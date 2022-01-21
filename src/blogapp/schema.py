from decouple import config
from graphene import relay, String
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
import graphene
import os
from configapp.models import Profile
from django.contrib.auth.models import User
from blogapp.models import Category, Tag, Location, Post


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
        filter_fields = [
                'username',
                ]
        interfaces = (relay.Node, )


class BlogLocationNode(DjangoObjectType):
    class Meta:
        model = Location
        filter_fields = {
                'domain': ['iexact'],
                }
        interfaces = (relay.Node, )


class BlogCategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {
                'id': ['iexact'],
                'name': ['iexact'],
                }
        interfaces = (relay.Node, )


class BlogTagNode(DjangoObjectType):
    class Meta:
        model = Tag
        filter_fields = {
                'id': ['iexact'],
                'name': ['iexact'],
                }
        interfaces = (relay.Node, )


class BlogPostNode(DjangoObjectType):
    custom_string = graphene.String()

    class Meta:
        model = Post
        filter_fields = [
                'categories__id',
                'categories__slug',
                'tags__id',
                'tags__slug',
                'locations__domain',
                'is_footer_menu',
                'is_primary_menu',
                'is_secondary_menu',
                'featured',
                'post_type',
                'slug',
                'status',
                ]

    interfaces = (relay.Node, )

    def resolve_image_featured(self, info):
        return self.image_featured.url

    def resolve_featured_lg(self, info):
        if self.featured_lg:
            return os.path.join(config('ENV_MEDIA_URL'), self.featured_lg)
        return ''

    def resolve_featured_md(self, info):
        if self.featured_md:
            return os.path.join(config('ENV_MEDIA_URL'), self.featured_md)
        return ''

    def resolve_featured_sm(self, info):
        if self.featured_sm:
            return os.path.join(config('ENV_MEDIA_URL'), self.featured_sm)
        return ''

    def resolve_image_thumb(self, info):
        return self.image_thumb.url

    def resolve_thumb_lg(self, info):
        if self.thumb_lg:
            return os.path.join(config('ENV_MEDIA_URL'), self.thumb_lg)
        return ''

    def resolve_thumb_md(self, info):
        if self.thumb_md:
            return os.path.join(config('ENV_MEDIA_URL'), self.thumb_md)
        return ''

    def resolve_thumb_sm(self, info):
        if self.thumb_sm:
            return os.path.join(config('ENV_MEDIA_URL'), self.thumb_sm)
        return ''

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


class Query(graphene.ObjectType):
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

    # primary menu categories
    p_menu_cat = DjangoListField(BlogCategoryNode)

    def resolve_p_menu_cat(self, info):
        # Categories that have posts and ordered
        return Category.objects.filter(
                is_primary_menu=True).exclude(
                posts__id="").order_by('menu_order')
