from django.contrib import admin
import contactapp.models


@admin.register(contactapp.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

    # def get_model_perms(self, request):
        # """
        # Return empty perms dict thus hiding the model from admin index.
        # """
    #     return {}


@admin.register(contactapp.models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']

    # def get_model_perms(self, request):
        # """
        # Return empty perms dict thus hiding the model from admin index.
        # """
    #     return {}


LOCATION_FIELDS = [
        ('name', 'phone'),
        ('domain', 'website'),
        'address_01',
        'address_02',
        ('city', 'state', 'zipcode'),
        'ship_address_01',
        'ship_address_02',
        ('ship_city', 'ship_state', 'ship_zipcode'),
        ('categories', 'tags'),
        ]
LOCATION_LIST_DISPLAY = ['name', 'domain', 'city']
LOCATION_SEARCH_FIELDS = ['name']
LOCATION_AUTOCOMPLETE_FIELDS = ['categories', 'tags']


@admin.register(contactapp.models.Location)
class LocationAdmin(admin.ModelAdmin):
    fields = LOCATION_FIELDS
    list_display = LOCATION_LIST_DISPLAY
    search_fields = LOCATION_SEARCH_FIELDS
    autocomplete_fields = LOCATION_AUTOCOMPLETE_FIELDS

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.Store)
class StoreAdmin(admin.ModelAdmin):
    fields = LOCATION_FIELDS
    list_display = LOCATION_LIST_DISPLAY
    search_fields = LOCATION_SEARCH_FIELDS
    autocomplete_fields = LOCATION_AUTOCOMPLETE_FIELDS


@admin.register(contactapp.models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    fields = LOCATION_FIELDS
    list_display = LOCATION_LIST_DISPLAY
    search_fields = LOCATION_SEARCH_FIELDS
    autocomplete_fields = LOCATION_AUTOCOMPLETE_FIELDS


@admin.register(contactapp.models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    fields = LOCATION_FIELDS
    list_display = LOCATION_LIST_DISPLAY
    search_fields = LOCATION_SEARCH_FIELDS
    autocomplete_fields = LOCATION_AUTOCOMPLETE_FIELDS


@admin.register(contactapp.models.Website)
class WebsiteAdmin(admin.ModelAdmin):
    fields = LOCATION_FIELDS
    list_display = LOCATION_LIST_DISPLAY
    search_fields = LOCATION_SEARCH_FIELDS
    autocomplete_fields = LOCATION_AUTOCOMPLETE_FIELDS


PERSON_FIELDS = [
        ('firstname', 'lastname', 'nickname'),
        ('phone', 'mobile'),
        ('email', 'website'),
        'address_01',
        'address_02',
        ('city', 'state', 'zipcode'),
        'ship_address_01',
        'ship_address_02',
        ('ship_city', 'ship_state', 'ship_zipcode'),
        ('categories', 'tags')
        ]
PERSON_AUTOCOMPLETE_FIELDS = ['categories', 'tags']


@admin.register(contactapp.models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = PERSON_FIELDS
    autocomplete_fields = PERSON_AUTOCOMPLETE_FIELDS


@admin.register(contactapp.models.Contact)
class ContactAdmin(admin.ModelAdmin):
    fields = PERSON_FIELDS
    autocomplete_fields = PERSON_AUTOCOMPLETE_FIELDS
