import blogapp.models
from decouple import config
from graphene import relay, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import graphene
import os


MEDIA_URL = config('ENV_MEDIA_URL')


class CategoryNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Category
        interfaces = (relay.Node, )
        filter_fields = [
                'id',
                'name',
                'is_primary',
                'is_secondary',
                'is_tertiary',
                'post__post_type',
                ]


class TagNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Tag
        interfaces = (relay.Node, )


class OpeningHoursNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.OpeningHours
        interfaces = (relay.Node, )


class ReviewNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Review
        interfaces = (relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Ingredient
        interfaces = (relay.Node, )


class RecipeNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Recipe
        interfaces = (relay.Node, )


class ReviewBookNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Book
        interfaces = (relay.Node, )


class ReviewBusinessNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.LocalBusiness
        interfaces = (relay.Node, )


class ReviewMovieNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Movie
        interfaces = (relay.Node, )


class ImageNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Image
        interfaces = (relay.Node, )
        filter_fields = [
                'featured',
                'order',
                ]

    def resolve_lg_11(self, info):
        return self.lg_11.url

    def resolve_md_11(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.md_11)

    def resolve_sm_11(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.sm_11)

    def resolve_lg_21(self, info):
        return self.lg_21.url

    def resolve_md_21(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.md_21)

    def resolve_sm_21(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.sm_21)

    def resolve_lg_191(self, info):
        return self.lg_191.url

    def resolve_custom(self, info):
        return self.lg_custom.url

    lg_11 = graphene.Field(String, resolver=resolve_lg_11)
    sm_11 = graphene.Field(String, resolver=resolve_sm_11)
    lg_21 = graphene.Field(String, resolver=resolve_lg_21)
    md_21 = graphene.Field(String, resolver=resolve_md_21)
    sm_21 = graphene.Field(String, resolver=resolve_sm_21)
    lg_191 = graphene.Field(String, resolver=resolve_lg_191)
    custom = graphene.Field(String, resolver=resolve_custom)


class PostNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Post
        interfaces = (relay.Node, )
        filter_fields = [
                'websites__domain',
                'categories',
                'tags',
                'is_primary',
                'is_secondary',
                'is_tertiary',
                'is_featured',
                'slug',
                'status',
                'post_type'
                ]

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
    posts = relay.Node.Field(PostNode)
    all_posts = DjangoFilterConnectionField(PostNode)
    post_categories = relay.Node.Field(CategoryNode)
    all_post_categories = DjangoFilterConnectionField(CategoryNode)
    # post_tags = relay.Node.Field(TagNode)
    # all_post_tags = DjangoFilterConnectionField(TagNode)
