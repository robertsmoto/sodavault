from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token
import configapp.models


@admin.register(configapp.models.Image)
class ImageAdmin(admin.ModelAdmin):
    exclude = ['user']
    readonly_fields = ['md_21', 'sm_21', 'md_11', 'sm_11']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(ImageAdmin, self).save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

# @admin.register(configapp.models.CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
    # exclude = ['user']
    # readonly_fields = ['md_21', 'sm_21', 'md_11', 'sm_11']

    # def save_model(self, request, obj, form, change):
        # obj.user = request.user
        # return super(ImageAdmin, self).save_model(request, obj, form, change)

    # def get_model_perms(self, request):
        # """
        # Return empty perms dict thus hiding the model from admin index.
        # """
        # return {}

class TokenInline(admin.StackedInline):
    model = Token
    raw_id_fields = ['user']
    # need to post username and password

    def __init__(self, *args, **kwargs):
        super(TokenInline, self).__init__(*args, **kwargs)
        self.can_delete = False
        self.show_change_link = True

class ProfileInline(admin.StackedInline):
    model = configapp.models.Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ['cdn_dir']

# class APICredentialsForm(forms.ModelForm):
        # class Meta:
            # model = configapp.models.APICredentials
            # fields = ['auth', 'prefix']
        # def __init__(self, *args, **kwargs):
            # super(APICredentialsForm, self).__init__(*args, **kwargs) 
            # kwargs['aid'] = self.instance.user_id

class APIInline(admin.StackedInline):
    model = configapp.models.APICredentials
    verbose_name_plural = 'API Credentials'
    fk_name = 'user'
    readonly_fields = ['prefix', 'user_id']
    # can_delete = False
    # def __init__(self, *args, **kwargs):
        # super(APIInline, self).__init__(*args, **kwargs)
        # print("## form -->", kwargs.get('aid'))
        # print("## model -->", self.model.user_id)

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, TokenInline, APIInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# # Changes the default user admin to this admin
# admin.site.unregister(configapp.models.CustomUser)
admin.site.register(configapp.models.CustomUser, CustomUserAdmin)
