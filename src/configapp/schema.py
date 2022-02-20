from django.contrib.auth.models import User
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import configapp.models
import graphene


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = [
                'username',
                ]
        interfaces = (relay.Node, )


class UserProfileNode(DjangoObjectType):
    class Meta:
        model = configapp.models.Profile
        interfaces = (relay.Node, )

    def resolve_avatar(self, info):
        return self.avatar.url


class CategoryPostsNode(DjangoObjectType):
    class Meta:
        model = configapp.models.Group
        interfaces = (relay.Node, )


class GroupNode(DjangoObjectType):
    class Meta:
        model = configapp.models.Group
        filter_fields = [
                'category_posts__websites__domain',
                'tag_posts__websites__domain',
                'group_type',
                'id',
                'is_primary',
                'is_secondary',
                'is_tertiary',
                'name',
                'order',
                'slug',
                ]
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    group = relay.Node.Field(GroupNode)
    all_groups = DjangoFilterConnectionField(GroupNode)

    category_post = relay.Node.Field(CategoryPostsNode)
    category_posts = DjangoFilterConnectionField(CategoryPostsNode)

    def resolve_category_post(self, info):
        return configapp.models.Group.filter(group_type="POSTTAG")
