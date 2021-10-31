from django.contrib import admin
from .models import *


class AssettsInline(admin.StackedInline):
    model = Assett
#     fields = [
        # 'attribute',
        # 'term',
    # ]
    extra = 0
    verbose_name = "asset"
    verbose_name_plural = "assetts"


class BannersInline(admin.StackedInline):
    model = Banner
#     fields = [
        # 'attribute',
        # 'term',
    # ]
    extra = 0
    verbose_name = "bannner"
    verbose_name_plural = "banner"


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'site_name',
    ]
    list_display_links = [
        'name',
    ]
    fields = [
        'name',
        'site_name',
        'site_url',
        'url_analyticscode',
        'date_added',
        'date_expires',
        'notes',
    ]
    inlines = [
        AssettsInline,
        BannersInline
    ]
    # filter_horizontal = ['products']
    verbose_name = 'campaign'
    verbose_name_plural = 'campaigns'

