from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from homeapp.models import Profile, APICredentials

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class APIInline(admin.StackedInline):
    model = APICredentials
    verbose_name_plural = 'API Credentials'
    fk_name = 'user'
    fields = ['aid', 'auth', 'prefix', 'is_current']
    readonly_fields = ['prefix', 'aid']

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, APIInline)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Changes the default user admin to this admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
