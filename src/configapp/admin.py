from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile
from rest_framework.authtoken.models import Token, TokenProxy
from rest_framework.authtoken.admin import TokenAdmin
from django.forms import models 


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
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, TokenInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# This changes the default user admin to this admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
