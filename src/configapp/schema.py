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

    def resolve_category_posts__websites__domain(self, info):
        return self.category_posts__websites__domain.distinct('name')


class Query(graphene.ObjectType):
    group = relay.Node.Field(GroupNode)
    all_groups = DjangoFilterConnectionField(GroupNode)
