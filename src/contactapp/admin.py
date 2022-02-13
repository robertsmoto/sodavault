from django.contrib import admin
import contactapp.models


class PersonInline(admin.StackedInline):
    model = contactapp.models.Person
    extra = 0
    verbose_name = "people"


@admin.register(contactapp.models.Company)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [PersonInline, ]
    verbose_name = "companies"


@admin.register(contactapp.models.Store)
class StoreAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(contactapp.models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(contactapp.models.Website)
class WebsiteAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(contactapp.models.Person)
class PersonAdmin(admin.ModelAdmin):
    verbose_name = "people"
