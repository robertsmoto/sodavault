from django.contrib import admin
import contactapp.models


@admin.register(contactapp.models.LocationCategory)
class LocationCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'keywords']
    exclude = ['group_type']
    prepopulated_fields = {"slug": ("name",)}

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(LocationCategoryAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="LOCACAT")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "LOCACAT"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.LocationTag)
class LocationTagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['group_type']
    prepopulated_fields = {"slug": ("name",)}

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(LocationTagAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="LOCATAG")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "LOCATAG"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.PersonCategory)
class PersonCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['group_type']
    prepopulated_fields = {"slug": ("name",)}

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PersonCategoryAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="PERSCAT")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "PERSCAT"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.PersonTag)
class PersonTagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ['group_type']
    prepopulated_fields = {"slug": ("name",)}

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PersonTagAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="PERSTAG")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "PERSTAG"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.Location)
class LocationAdmin(admin.ModelAdmin):
    fields = [
            'location_type',
            ('name', 'phone'),
            ('domain', 'website'),
            'address_01',
            'address_02',
            ('city', 'state', 'zipcode'),
            'ship_address_01',
            'ship_address_02',
            ('ship_city', 'ship_state', 'ship_zipcode'),
            ('categories', 'tags')
            ]
    list_display = ['location_type', 'name', 'domain', 'city']
    list_filter = ['location_type']
    search_fields = ['name']
    autocomplete_fields = ['categories', 'tags']
    INDEX = {
            'companies': "COMP",
            'suppliers': "SUPP",
            'stores': "STOR",
            'warehouses': "WARE",
            'websites': "WEBS"
            }

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(LocationAdmin, self).get_search_results(
            request, queryset, search_term
        )
        field_name = request.GET.get('field_name')
        print(field_name, request)
        self.field_name = field_name
        if field_name:
            queryset = queryset.filter(location_type=self.INDEX[field_name])
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        print("in save_model method")
        print("request", request)
        super().save_model(request, obj, form, change)

#     def get_model_perms(self, request):
        # """
        # Return empty perms dict thus hiding the model from admin index.
        # """
#         return {}


@admin.register(contactapp.models.Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['categories', 'tags']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['categories', 'tags']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.Store)
class StoreAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['categories', 'tags']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['categories', 'tags']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(contactapp.models.Website)
class WebsiteAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['categories', 'tags']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


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
            ('categories', 'tags')
            ]
    autocomplete_fields = ['companies', 'categories', 'tags']


@admin.register(contactapp.models.Contact)
class ContactAdmin(admin.ModelAdmin):
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
            ('stores', 'warehouses', 'websites'),
            ('categories', 'tags')
            ]
    autocomplete_fields = [
        'suppliers', 'stores', 'warehouses', 'websites',
        'categories', 'tags'
        ]
