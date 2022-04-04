from decouple import config
from graphene import relay, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import advertisingapp.models
import graphene
import os


class CampaignNode(DjangoObjectType):

    class Meta:
        model = advertisingapp.models.Campaign
        filter_fields = [
            'name',
            'date_expires',
            ]
        interfaces = (relay.Node, )


class BannerNode(DjangoObjectType):
    class Meta:
        model = advertisingapp.models.Banner
        filter_fields = [
                "name",
                "campaign__name",
                ]
        interfaces = (relay.Node, )

    def resolve_lg_11(self, info):
        return self.lg_11.url

    def resolve_md_11(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.md_11)

    def resolve_sm_11(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.sm_11)

    def resolve_lg_leaderboard(self, info):
        return self.lg_leaderboard.url

    def resolve_md_leaderboard(self, info):
        return self.md_leaderboard.url

    def resolve_sm_leaderboard(self, info):
        return self.sm_leaderboard.url

    def resolve_md_rectangle(self, info):
        return self.md_rectangle.url

    def resolve_sm_rectangle(self, info):
        if not self.sm_rectangle:
            return ""
        return self.sm_rectangle.url

    def resolve_skyscraper(self, info):
        return self.skyscraper.url

    lg_11 = graphene.Field(String, resolver=resolve_lg_11)
    md_11 = graphene.Field(String, resolver=resolve_md_11)
    sm_11 = graphene.Field(String, resolver=resolve_sm_11)
    lg_leaderboard = graphene.Field(String, resolver=resolve_lg_leaderboard)
    md_leaderboard = graphene.Field(String, resolver=resolve_md_leaderboard)
    sm_leaderboard = graphene.Field(String, resolver=resolve_sm_leaderboard)
    md_rectangle = graphene.Field(String, resolver=resolve_md_rectangle)
    sm_rectangle = graphene.Field(String, resolver=resolve_sm_rectangle)
    skyscraper = graphene.Field(String, resolver=resolve_skyscraper)


class Query(graphene.ObjectType):
    campaign = relay.Node.Field(CampaignNode)
    all_campaigns = DjangoFilterConnectionField(CampaignNode)

    banner = relay.Node.Field(BannerNode)
    all_banners = DjangoFilterConnectionField(BannerNode)
