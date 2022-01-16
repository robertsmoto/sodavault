from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import blogapp.models
import graphene


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

        """
        fields = [
                "locations", "categories", "tags", "author",
                "menu_order", "parent", "is_primary_menu",
                "is_secondary_menu", "is_footer_menu",
                "post_type", "title", "excerpt", "body", "slug", "status",
                "featured", "date_published", "date_modified", "kwd_list",
                "image_featured", "image_thumb", "image_191", "image_21",
                "image_title", "image_caption", "footer", "featured_lg",
                "featured_md", "featured_sm", "thumb_lg", "thumb_md",
                "thumb_sm",
                ]

        filter_fields = [
                'id', 'author__username', 'categories__name',
                'date_modified', 'date_published', 'featured', 'kwd_list',
                'locations__domain', 'post_type', 'slug', 'status',
                'tags__name', 'icontains', 'istartswith', 'is_primary_menu',
                'is_secondary_menu', 'is_footer_menu',
                ]
        """


class BlogPostNode(DjangoObjectType):
    custom_string = graphene.String()

    class Meta:
        model = blogapp.models.Post
        filter_fields = [
                'is_footer_menu',
                'is_primary_menu',
                'is_secondary_menu',
                'locations__domain',
                'featured',
                'slug',
                'status',
                ]

        interfaces = (relay.Node, )

        # 'id': ['iexact', ],
        # 'author__username': ['iexact', ],
        # 'categories__name': ['iexact', 'icontains', 'istartswith'],
        # 'date_modified': ['isnull', 'iexact', 'icontains'],
        # 'date_published': ['isnull', 'iexact', 'icontains'],
        # 'featured': ['iexact'],
        # 'kwd_list': ['icontains'],
        # 'locations__domain': ['iexact'],
        # 'post_type': ['iexact'],
        # 'slug': ['iexact'],
        # 'status': ['iexact'],
        # 'tags__name': ['iexact', 'icontains', 'istartswith'],
        # 'is_primary_menu': [],


#     def resolve_image_featured(self, info):
        # return self.image_featured.url

    # def resolve_featured_lg(self, info):
        # return os.path.join(config('ENV_MEDIA_URL'), self.featured_lg)

    # def resolve_featured_md(self, info):
        # return os.path.join(config('ENV_MEDIA_URL'), self.featured_md)

    # def resolve_featured_sm(self, info):
        # return os.path.join(config('ENV_MEDIA_URL'), self.featured_sm)

    # def resolve_image_thumb(self, info):
        # return self.image_thumb.url

    # def resolve_thumb_lg(self, info):
        # return os.path.join(config('ENV_MEDIA_URL'), self.thumb_lg)

    # def resolve_thumb_md(self, info):
        # return os.path.join(config('ENV_MEDIA_URL'), self.thumb_md)

    # def resolve_thumb_sm(self, info):
        # return os.path.join(config('ENV_MEDIA_URL'), self.thumb_sm)

    # def resolve_pub_year(self, info):
        # return self.date_published.strftime("%Y")

    # def resolve_pub_month(self, info):
        # return self.date_published.strftime("%m")

    # def resolve_pub_day(self, info):
        # return self.date_published.strftime("%d")

    # def resolve_pub_us(self, info):
        # return self.date_published.strftime("%b %d, %Y")

    # def resolve_mod_us(self, info):
        # return self.date_modified.strftime("%b %d, %Y")

    # def resolve_reading_time(self, info):
        # text = ""
        # if len(self.body) > 0 or len(self.excerpt) > 0:
            # text = self.body + self.excerpt
        # time = round((len(text.split()) / 250))
        # timestr = ""
        # if time > 1:
            # timestr = f"{time} minutes"
        # else:
            # timestr = "1 minute"
        # return timestr

    # pub_year = graphene.Field(String, resolver=resolve_pub_year)
    # pub_month = graphene.Field(String, resolver=resolve_pub_month)
    # pub_day = graphene.Field(String, resolver=resolve_pub_day)
    # pub_us = graphene.Field(String, resolver=resolve_pub_us)
    # mod_us = graphene.Field(String, resolver=resolve_mod_us)
    # reading_time = graphene.Field(String, resolver=resolve_reading_time)


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
