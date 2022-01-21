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
        # interfaces = (relay.Node, )

    def resolve_avatar(self, info):
        return self.avatar.url


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = [
                'username',
                ]
        # interfaces = (relay.Node, )


class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        filter_fields = {
                'domain': ['iexact'],
                }
        # interfaces = (relay.Node, )


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = {
                'id': ['iexact'],
                'name': ['iexact'],
                }
        # interfaces = (relay.Node, )


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        filter_fields = {
                'id': ['iexact'],
                'name': ['iexact'],
                }
        # interfaces = (relay.Node, )


class PostType(DjangoObjectType):
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

    # interfaces = (relay.Node, )

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
    all_locations = graphene.List(LocationType)

    def resolve_all_locations(self, info):
        return Location.objects.all().order_by('id')

    all_pages = graphene.List(PostType)

    def resolve_all_pages(self, info):
        return Post.objects.filter(
                post_type="PAGE").order_by('-date_published')

    all_articles = graphene.List(PostType)

    def resolve_all_articles(self, info):
        return Post.objects.filter(
                post_type="ARTICLE").order_by('-date_published')

    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info):
        return Category.objects.all().order_by('name')

    all_tags = graphene.List(TagType)

    def resolve_all_tags(self, info):
        return Tag.objects.all().order_by('name')

    # primary menu
    p_menu_cat = graphene.List(CategoryType)

    def resolve_p_menu_cat(self, info):
        query = (
                Category.objects
                .filter(is_primary_menu=True)
                .order_by('menu_order')
                )
        return query

    p_menu_page = graphene.List(PostType)

    def resolve_p_menu_page(self, info):
        query = (
                Post.objects
                .filter(is_primary_menu=True, post_type="PAGE")
                .order_by('menu_order')
                )
        return query
