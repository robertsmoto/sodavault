from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token, TokenProxy
import configapp.models


@admin.register(configapp.models.Image)
class ImageAdmin(admin.ModelAdmin):
    exclude = ['user']
    readonly_fields = ['img_md_21', 'img_sm_21', 'img_md_11', 'img_sm_11']
    print("in admin")

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(ImageAdmin, self).save_model(request, obj, form, change)


class SubgroupInline(admin.StackedInline):

    model = configapp.models.Group
    fields = [
            'parent',
            ('name', 'slug'),
            ('description', 'kwd_list'),
            ('order', 'is_primary', 'is_secondary', 'is_tertiary'),
            ('image_thumb', 'image_21', 'image_191'),
            ('image_sm_square', 'image_md_square', 'image_lg_square'),
            ]
    prepopulated_fields = {"slug": ("name", )}
    can_delete = False
    verbose_name_plural = 'Subgroups'
    extra = 0


@admin.register(configapp.models.Group)
class GroupAdmin(admin.ModelAdmin):
    # form = GroupForm
    fields = [
            'group_type',
            ('name', 'slug'),
            ('description', 'kwd_list'),
            ('order', 'is_primary', 'is_secondary', 'is_tertiary'),
            ('image_thumb', 'image_21', 'image_191'),
            ('image_sm_square', 'image_md_square', 'image_lg_square'),
            ]
    list_display = [
            'group_type', 'name', 'get_subgroups', 'is_primary',
            'is_secondary', 'is_tertiary', 'order'
            ]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ['group_type']
    search_fields = ['group_type', 'name', 'description']
    inlines = [SubgroupInline, ]

    @admin.display(
            ordering='subgroups__name',
            description='Subgroups',
            empty_value='-')
    def get_subgroups(self, obj):
        if obj.subgroups:
            sglist = []
            for sg in obj.subgroups.all():
                sglist.append(sg.name)
            return sglist

    def get_queryset(self, request):
        queryset = super(GroupAdmin, self).get_queryset(request)
        queryset = queryset.exclude(parent__isnull=False)
        return queryset


class TokenInline(admin.StackedInline):
    model = Token
    raw_id_fields = ['user']
    # need to post username and password

    def __init__(self, *args, **kwargs):
        super(TokenInline, self).__init__(*args, **kwargs)
        self.can_delete = False
        self.show_change_link = True


# # unregisters the 'standard' admin
# admin.site.unregister(TokenProxy)

class ProfileInline(admin.StackedInline):
    model = configapp.models.Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ['cdn_dir']


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, TokenInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# This changes the default user admin to this admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
