from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import configapp.models
import graphene


class LocationNode(DjangoObjectType):
    class Meta:
        model = configapp.models.Location
        filter_fields = [
                'domain',
                'name',
                ]
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    location = relay.Node.Field(LocationNode)
    all_locations = DjangoFilterConnectionField(LocationNode)
