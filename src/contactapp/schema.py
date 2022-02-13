from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import configapp.models
import graphene


# class LocationNode(DjangoObjectType):
    # class Meta:
        # model = configapp.models.Location
        # filter_fields = [
                # 'domain',
                # 'name',
                # ]
        # interfaces = (relay.Node, )


# class CompanyNode(DjangoObjectType):
    # class Meta:
        # model = configapp.models.Company
        # filter_fields = [
                # 'domain',
                # 'name',
                # ]
        # interfaces = (relay.Node, )


# class StoreNode(DjangoObjectType):
    # class Meta:
        # model = configapp.models.Store
        # filter_fields = [
                # 'domain',
                # 'name',
                # ]
        # interfaces = (relay.Node, )


# class WarehouseNode(DjangoObjectType):
    # class Meta:
        # model = configapp.models.Warehouse
        # filter_fields = [
                # 'domain',
                # 'name',
                # ]
        # interfaces = (relay.Node, )


# class WebsiteNode(DjangoObjectType):
    # class Meta:
        # model = configapp.models.Website
        # filter_fields = [
                # 'domain',
                # 'name',
                # ]
#         interfaces = (relay.Node, )


# class Query(graphene.ObjectType):
    # location = relay.Node.Field(LocationNode)
    # all_locations = DjangoFilterConnectionField(LocationNode)
#     company = relay.Node.Field(CompanyNode)
    # all_companies = DjangoFilterConnectionField(CompanyNode)
    # store = relay.Node.Field(StoreNode)
    # all_stores = DjangoFilterConnectionField(StoreNode)
    # warehouse = relay.Node.Field(WarehouseNode)
    # all_warehouses = DjangoFilterConnectionField(WarehouseNode)
    # website = relay.Node.Field(WebsiteNode)
    # all_websites = DjangoFilterConnectionField(WebsiteNode)
