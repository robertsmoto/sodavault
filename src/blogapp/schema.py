import blogapp.models
from decouple import config
from graphene import relay, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import graphene
import os


class PostCategoryNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Category
        interfaces = (relay.Node, )


class PostTagNode(DjangoObjectType):
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


class PostNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Post
        filter_fields = {
                'categories__id': ['exact'],
                'categories__slug': ['exact'],
                'tags__id': ['exact'],
                'tags__slug': ['exact'],
                # 'websites__domain': ['exact'],
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
    posts = relay.Node.Field(PostNode)
    all_posts = DjangoFilterConnectionField(PostNode)
