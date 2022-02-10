from blogapp.models import Post  # Category, Tag,
# from configapp.models import Location
from blogapp.models import Ingredient, Recipe
from blogapp.models import LocalBusiness, Book, Movie
from blogapp.models import OpeningHours, Review
from configapp.models import Profile
from decouple import config
from django.contrib.auth.models import User
from graphene import relay, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import graphene
import os


class OpeningHoursNode(DjangoObjectType):
    class Meta:
        model = OpeningHours
        interfaces = (relay.Node, )


class ReviewNode(DjangoObjectType):
    class Meta:
        model = Review
        interfaces = (relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        interfaces = (relay.Node, )


class RecipeNode(DjangoObjectType):
    class Meta:
        model = Recipe
        interfaces = (relay.Node, )


class ReviewBookNode(DjangoObjectType):
    class Meta:
        model = Book
        interfaces = (relay.Node, )


class ReviewBusinessNode(DjangoObjectType):
    class Meta:
        model = LocalBusiness
        interfaces = (relay.Node, )


class ReviewMovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        interfaces = (relay.Node, )


class UserProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        interfaces = (relay.Node, )

    def resolve_avatar(self, info):
        return self.avatar.url


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = [
                'username',
                ]
        interfaces = (relay.Node, )


# class LocationNode(DjangoObjectType):
    # class Meta:
        # model = Location
        # filter_fields = [
                # 'domain',
                # 'name',
                # ]
        # interfaces = (relay.Node, )


# class CategoryNode(DjangoObjectType):
    # class Meta:
        # model = Category
        # filter_fields = [
                # 'id',
                # 'slug',
                # 'name',
                # 'is_primary_menu',
                # 'is_secondary_menu',
                # 'is_footer_menu',
                # # 'locations__domain',
                # ]

        # interfaces = (relay.Node, )


# class TagNode(DjangoObjectType):
    # class Meta:
        # model = Tag
        # filter_fields = [
                # 'id',
                # 'slug',
                # 'name',
                # # 'locations__domain',
                # ]
        # interfaces = (relay.Node, )


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = {
                # 'categories__id': ['exact'],
                # 'categories__slug': ['exact'],
                # 'tags__id': ['exact'],
                # 'tags__slug': ['exact'],
                # 'locations__domain': ['exact'],
                'is_footer_menu': ['exact'],
                'is_primary_menu': ['exact'],
                'is_secondary_menu': ['exact'],
                'is_featured': ['exact'],
                'post_type': ['exact'],
                'slug': ['exact'],
                'status': ['exact'],
                'title': ['icontains'],
                'excerpt': ['icontains'],
                'body': ['icontains'],
                }
        interfaces = (relay.Node, )

    def resolve_image_featured(self, info):
        return self.image_featured.url

    def resolve_image_191(self, info):
        return self.image_191.url

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
    # location = relay.Node.Field(LocationNode)
    # all_locations = DjangoFilterConnectionField(LocationNode)

    # category = relay.Node.Field(CategoryNode)
    # all_categories = DjangoFilterConnectionField(CategoryNode)

    # tag = relay.Node.Field(TagNode)
    # all_tags = DjangoFilterConnectionField(TagNode)

    posts = relay.Node.Field(PostNode)
    all_posts = DjangoFilterConnectionField(PostNode)
