from decouple import config
from django.contrib.auth.models import User
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import configapp.models
import graphene
import os


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
                # 'group_type',
                'id',
                'is_primary',
                'is_secondary',
                'is_tertiary',
                'websites__domain',
                'name',
                'order',
                'slug',
                ]
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    group = relay.Node.Field(GroupNode)
    all_groups = DjangoFilterConnectionField(GroupNode)
