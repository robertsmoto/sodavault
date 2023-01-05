from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from homeapp.models import Profile, APICredentials

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'profile'
    fk_name = 'user'

class APIInline(admin.StackedInline):
    model = APICredentials
    verbose_name = 'api credentials'
    fk_name = 'user'
    fields = ['aid', 'auth', 'prefix', 'is_current']
    readonly_fields = ['prefix', 'aid']

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, APIInline,)

# Changes the default user admin to this admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
