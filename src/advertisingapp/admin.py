from django.contrib import admin
from .models import Banner, Campaign


class BannersInline(admin.StackedInline):
    model = Banner
    extra = 0
    exclude = ['user', 'ban_lg_square', 'ban_md_square', 'ban_sm_square']
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
        BannersInline
    ]
    # filter_horizontal = ['products']
    verbose_name = 'campaign'
    verbose_name_plural = 'campaigns'

    def save_formset(self, request, form, formset, change):
        """This method ensures that there is a user saved in the Image
        model before the image file paths are updated."""
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Banner):
                instance.user = request.user
                instance.save()
        formset.save()
