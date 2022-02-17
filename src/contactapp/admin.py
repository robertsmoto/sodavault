from django.contrib import admin
import contactapp.models


class ContactInline(admin.TabularInline):

    model = contactapp.models.Person
    extra = 0
    fields = [
            'firstname', 'lastname', 'phone', 'email',
            ]


@admin.register(contactapp.models.Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(LocationAdmin, self).get_search_results(
            request, queryset, search_term
        )
        INDEX = {
                'companies': "COMP",
                'suppliers': "SUPP",
                'stores': "STOR",
                'warehouses': "WARE",
                'websites': "WEBS"
                }
        field_name = request.GET.get('field_name')
        print('field_name', field_name)
        if field_name:
            queryset = queryset.filter(location_type=INDEX[field_name])
        return queryset, use_distinct

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['location_type']


@admin.register(contactapp.models.Store)
class StoreAdmin(admin.ModelAdmin):
    fields = [
            ('name', 'phone'),
            ('domain', 'website'),
            'address_01',
            'address_02',
            ('city', 'state', 'zipcode'),
            'ship_address_01',
            'ship_address_02',
            ('ship_city', 'ship_state', 'ship_zipcode'),
            ]
    search_fields = ['name']
    exclude = ['location_type']
    # inlines = [ContactInline]


@admin.register(contactapp.models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['location_type']


@admin.register(contactapp.models.Website)
class WebsiteAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['location_type']


@admin.register(contactapp.models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    fields = [
            ('firstname', 'lastname', 'nickname'),
            ('phone', 'mobile'),
            ('email', 'website'),
            'address_01',
            'address_02',
            ('city', 'state', 'zipcode'),
            'ship_address_01',
            'ship_address_02',
            ('ship_city', 'ship_state', 'ship_zipcode'),
            'companies'
            ]
    exclude = ['person_type']
    autocomplete_fields = ['companies']


@admin.register(contactapp.models.Contact)
class ContactAdmin(admin.ModelAdmin):
    # form = ContactForm
    fields = [
            ('firstname', 'lastname', 'nickname'),
            ('phone', 'mobile'),
            ('email', 'website'),
            'address_01',
            'address_02',
            ('city', 'state', 'zipcode'),
            'ship_address_01',
            'ship_address_02',
            ('ship_city', 'ship_state', 'ship_zipcode'),
            'suppliers',
            ('stores', 'warehouses', 'websites')
            ]
    exclude = ['person_type']
    autocomplete_fields = ['suppliers', 'stores', 'warehouses', 'websites']
