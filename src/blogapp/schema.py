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
        filter_fields = {
                'id': ['exact'],
                'slug': ['exact'],
                'name': ['exact'],
                'order': ['exact'],
                'is_primary': ['exact'],
                'is_secondary': ['exact'],
                'is_tertiary': ['exact'],
                'article__websites__domain': ['exact'],
                'doc__websites__domain': ['exact'],
                'page__websites__domain': ['exact'],
                'parent': ['isnull'],
                }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.order_by('order', 'id').distinct('order', 'id')


class TagNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Tag
        interfaces = (relay.Node, )
        filter_fields = {
                'id': ['exact'],
                'slug': ['exact'],
                'name': ['exact'],
                'is_primary': ['exact'],
                'is_secondary': ['exact'],
                'is_tertiary': ['exact'],
                'article__websites__domain': ['exact'],
                'doc__websites__domain': ['exact'],
                'page__websites__domain': ['exact'],
                'parent': ['isnull'],
                }

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.order_by('order', 'id').distinct('order', 'id')


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

    def resolve_lg_11(self):
        if not self.lg_11:
            return ""
        return self.lg_11.url

    def resolve_md_11(self, info):
        if not self.md_11:
            return ""
        return os.path.join(config('ENV_MEDIA_URL'), self.md_11)

    def resolve_sm_11(self, info):
        if not self.sm_11:
            return ""
        return os.path.join(config('ENV_MEDIA_URL'), self.sm_11)

    def resolve_lg_21(self, info):
        if not self.lg_21:
            return ""
        return self.lg_21.url

    def resolve_md_21(self, info):
        if not self.md_21:
            return ""
        return os.path.join(config('ENV_MEDIA_URL'), self.md_21)

    def resolve_sm_21(self, info):
        if not self.sm_21:
            return ""
        return os.path.join(config('ENV_MEDIA_URL'), self.sm_21)

    def resolve_lg_191(self, info):
        if not self.lg_191:
            return ""
        return self.lg_191.url

    def resolve_custom(self, info):
        if not self.custom:
            return ""
        return self.custom.url

    lg_11 = graphene.Field(String, resolver=resolve_lg_11)
    sm_11 = graphene.Field(String, resolver=resolve_sm_11)
    lg_21 = graphene.Field(String, resolver=resolve_lg_21)
    md_21 = graphene.Field(String, resolver=resolve_md_21)
    sm_21 = graphene.Field(String, resolver=resolve_sm_21)
    lg_191 = graphene.Field(String, resolver=resolve_lg_191)
    custom = graphene.Field(String, resolver=resolve_custom)


class ArticleNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Article
        interfaces = (relay.Node, )
        filter_fields = {
                'websites__domain': ['exact'],
                'categories__slug': ['exact'],
                'categories__id': ['exact'],
                'tags__slug': ['exact'],
                'tags__id': ['exact'],
                'is_primary': ['exact'],
                'is_secondary': ['exact'],
                'is_tertiary': ['exact'],
                'is_featured': ['exact'],
                'slug': ['exact'],
                'status': ['exact'],
                'body': ['icontains'],
                'parent': ['isnull'],
                }

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


class DocNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Doc
        interfaces = (relay.Node, )
        filter_fields = [
                'websites__domain',
                'categories__slug',
                'categories__id',
                'tags__slug',
                'tags__id',
                'is_primary',
                'is_secondary',
                'is_tertiary',
                'is_featured',
                'slug',
                'status',
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


class PageNode(DjangoObjectType):
    class Meta:
        model = blogapp.models.Page
        interfaces = (relay.Node, )
        filter_fields = {
                'websites__domain': ['exact'],
                'categories__slug': ['exact'],
                'categories__id': ['exact'],
                'tags__slug': ['exact'],
                'tags__id': ['exact'],
                'is_primary': ['exact'],
                'is_secondary': ['exact'],
                'is_tertiary': ['exact'],
                'is_featured': ['exact'],
                'slug': ['exact'],
                'status': ['exact'],
                'parent': ['isnull']
                }

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
    article = relay.Node.Field(ArticleNode)
    all_articles = DjangoFilterConnectionField(ArticleNode)
    doc = relay.Node.Field(DocNode)
    all_docs = DjangoFilterConnectionField(DocNode)
    page = relay.Node.Field(PageNode)
    all_pages = DjangoFilterConnectionField(PageNode)
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)
    tag = relay.Node.Field(TagNode)
    all_tags = DjangoFilterConnectionField(TagNode)
