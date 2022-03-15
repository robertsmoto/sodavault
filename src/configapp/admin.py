from rest_framework.authtoken.models import Token
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
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


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, TokenInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)  # Changes the default user admin to this admin
admin.site.register(User, CustomUserAdmin)
