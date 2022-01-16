from decouple import config
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import advertisingapp.models
import graphene
import os


class CampaignNode(DjangoObjectType):

    class Meta:
        model = advertisingapp.models.Campaign
        filter_fields = {
            'name': ['iexact', 'icontains', 'istartswith'],
            'date_expires': ['isnull']}
        interfaces = (relay.Node, )


class BannerNode(DjangoObjectType):
    class Meta:
        model = advertisingapp.models.Banner
        filter_fields = ["name"]
        interfaces = (relay.Node, )

    def resolve_ban_square(self, info):
        return self.ban_square.url

    def resolve_ban_lg_square(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.ban_lg_square)

    def resolve_ban_md_square(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.ban_md_square)

    def resolve_ban_sm_square(self, info):
        return os.path.join(config('ENV_MEDIA_URL'), self.ban_sm_square)

    def resolve_ban_leaderboard(self, info):
        return self.ban_leaderboard.url

    def resolve_ban_lg_leaderboard(self, info):
        return self.ban_lg_leaderboard.url

    def resolve_ban_inline_rectangle(self, info):
        return self.ban_inline_rectangle.url

    def resolve_ban_lg_rectangle(self, info):
        return self.ban_lg_rectangle.url

    def resolve_ban_skyscraper(self, info):
        return self.ban_skyscraper.url


class Query(graphene.ObjectType):
    campaign = relay.Node.Field(CampaignNode)
    all_campaigns = DjangoFilterConnectionField(CampaignNode)

    banner = relay.Node.Field(BannerNode)
    all_banners = DjangoFilterConnectionField(BannerNode)
