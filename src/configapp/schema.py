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


class LocationNode(DjangoObjectType):
    class Meta:
        model = configapp.models.Location
        filter_fields = [
                'domain',
                'name',
                ]
        interfaces = (relay.Node, )


class GroupNode(DjangoObjectType):
    class Meta:
        model = configapp.models.Group
        filter_fields = [
                'id',
                'slug',
                'name',
                'is_primary_menu',
                'is_secondary_menu',
                'is_footer_menu',
                'locations__domain',
                ]
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    location = relay.Node.Field(LocationNode)
    all_locations = DjangoFilterConnectionField(LocationNode)

    group = relay.Node.Field(GroupNode)
    all_groups = DjangoFilterConnectionField(GroupNode)
