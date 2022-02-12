# from transactionsapp.models import Note, Bid
from django.contrib import admin
import configapp.models
import nested_admin
import itemsapp.models
from dal import autocomplete
from django import forms
from dal import forward
from django.utils.translation import gettext_lazy as _
from ledgerapp.models import Entry
from django.urls import resolve
from django.db.models import Sum, Count, F


# @admin.register(models.Price)
# class PriceAdmin(admin.ModelAdmin):
    # model = models.Price
    # list_display = ['name', 'is_margin', 'is_markup', 'is_flat']
#     list_filter = ['is_margin', 'is_markup', 'is_flat']


class SubDepartmentInline(nested_admin.NestedTabularInline):
    model = configapp.models.Group
    exclude = ['cat_type']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Department"
    verbose_name_plural = "Sub-Departments"


@admin.register(itemsapp.models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name']
    exclude = ['group_type']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [SubDepartmentInline, ]

    def get_queryset(self, request):
        qs = super(DepartmentAdmin, self).get_queryset(request)
        return qs.filter(group_type="ITEMDEP")


class SubCategoryInline(nested_admin.NestedTabularInline):
    model = configapp.models.Group
    exclude = ['cat_type']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Category"
    verbose_name_plural = "Sub-Categories"


@admin.register(itemsapp.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    list_display_links = [
        'name',
    ]
    search_fields = ['name']
    exclude = ['cat_type', ]
    prepopulated_fields = {'slug': ('name', )}
    inlines = [SubCategoryInline, ]


class SubTagInline(nested_admin.NestedTabularInline):
    model = configapp.models.Group
    exclude = ['cat_type']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Tag"
    verbose_name_plural = "Sub-Tags"


@admin.register(itemsapp.models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name']
    exclude = ['cat_type', ]
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubTagInline, ]


class SubAttributeInline(nested_admin.NestedTabularInline):
    model = itemsapp.models.Attribute
    exclude = ['group_type']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Term"
    verbose_name_plural = "Attribute Terms"
    autocomplete_fields = ['locations']


@admin.register(itemsapp.models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name']
    exclude = ['group_type', 'subgroup']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubAttributeInline, ]
    autocomplete_fields = ['locations']

    def get_queryset(self, request):
        qs = super(AttributeAdmin, self).get_queryset(request)
        return qs.filter(subgroup_id__isnull=True)


class ProductInventoryInline(nested_admin.NestedTabularInline):

    model = Entry

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        pid = None
        if resolved.kwargs:
            pid = resolved.kwargs['object_id']
        return pid

    def get_queryset(self, request):
        pid = self.get_parent_object_from_request(request)
        return Entry.inventory.products(pid=pid)

    extra = 0
    verbose_name = "Inventory"
    verbose_name_plural = "Inventory"
    exclude = ['parts']


class PartInventoryInline(nested_admin.NestedTabularInline):

    model = Entry

    def get_parent_object_from_request(self, request):
        """
        Returns the parent object from the request or None.

        Note that this only works for Inlines, because the `parent_model`
        is not available in the regular admin.ModelAdmin as an attribute.
        """
        resolved = resolve(request.path_info)
        pid = None
        if resolved.kwargs:
            pid = resolved.kwargs['object_id']
            # print("\n--> PID", pid)
        return pid

    def get_queryset(self, request):
        pid = self.get_parent_object_from_request(request)
        return Entry.inventory.parts(pid=pid)

    extra = 0
    verbose_name = "Inventory"
    verbose_name_plural = "Inventory"
    exclude = ['lots', 'products', 'account']  # , 'note'


# class NotePartInline(nested_admin.NestedTabularInline):
    # model = Note
    # extra = 0
    # verbose_name = "note"
    # verbose_name_plural = "notes"
    # exclude = ['pos', 'asns']


# class BidPartInline(nested_admin.NestedTabularInline):
    # model = Bid
    # exclude = ['products', ]
    # extra = 0
    # verbose_name = "bid"
    # verbose_name_plural = "bids"


# class BidProductInline(nested_admin.NestedTabularInline):
    # model = Bid
    # exclude = ['parts', ]
    # extra = 0
    # verbose_name = "bid"
    # verbose_name_plural = "bids"


class IdentifierInline(nested_admin.NestedTabularInline):

    model = itemsapp.models.Identifier
    fields = [
        ('gtin', 'isbn'),
        ('pid_i', 'pid_c')
    ]
    extra = 0
    verbose_name = "identifier"
    verbose_name_plural = "identifiers"


class MeasurementInline(nested_admin.NestedTabularInline):

    model = itemsapp.models.Measurement
    fields = [
        'weight',
        ('length', 'width', 'height')
    ]
    extra = 0
    verbose_name = "measurements"


class MarketingOptionInline(nested_admin.NestedStackedInline):

    model = itemsapp.models.Marketing
    extra = 0
    verbose_name = "marketing options"
    fields = [
        'description_sm',
        'description_md',
        'description_lg',
    ]
    verbose_name = "option"
    verbose_name_plural = "marketing options"


class ImageInline(nested_admin.NestedStackedInline):

    model = itemsapp.models.Image
    extra = 0
    verbose_name = "marketing options"
    fields = [
        ('name', 'order'),
        ('img_lg', 'img_md', 'img_sm'),
        ('img_1x1_lg', 'img_1x1_md', 'img_1x1_sm'),
        ('img_2x1_lg', 'img_2x1_md', 'img_2x1_sm'),
        ('img_1x2_lg', 'img_1x2_md', 'img_1x2_sm'),
        ('img_16x9', 'img_191x1')
    ]
    verbose_name = "image"
    verbose_name_plural = "images"

# class DigitalOptionInline(nested_admin.NestedTabularInline):
    # model = DigitalOption
    # extra = 0
    # verbose_name = "option"
#     verbose_name_plural = "digital options"


# class BundleInline(nested_admin.NestedTabularInline):
    # model = Bundle
    # fk_name = 'parent'
    # extra = 0
    # verbose_name = "bundle"
    # verbose_name_plural = "bundles"

# # used in Attribute admin
# class TermInline(admin.TabularInline):
    # model = Term
    # fields = ['name', 'slug', 'img']
    # extra = 0
    # verbose_name = "term"
    # verbose_name_plural = "terms"
    # prepopulated_fields = {'slug': ('name',)}


#### PRODUCT-ATTRIBUTES ####
# I'm putting this form directly in Admin rather than in forms.py
# since this is where it is used
# class ProdAttrJoinForm(forms.ModelForm):
    # class Meta:
        # model = ProductAttributeJoin
        # fields = ('attribute', 'term')
        # widgets = {
            # 'attribute': autocomplete.ModelSelect2(
                # url='attr-autocomplete',
                # forward=('product',),
                # attrs={
                    # 'data-placeholder': 'Autocomplete ...',
                # },
            # ),
            # 'term': autocomplete.ModelSelect2Multiple(
                # url='attr-term-autocomplete',
                # forward=('attribute', forward.Self(),),
                # attrs={
                    # 'data-placeholder': 'Autocomplete ...',
                # },
            # ),
        # }

# class ProdAttrJoinInline(nested_admin.NestedTabularInline):
    # form = ProdAttrJoinForm
    # model = ProductAttributeJoin
    # # fields = [
        # # 'attribute',
        # # 'term',
    # # ]
    # extra = 0
    # verbose_name = "attribute"
    # verbose_name_plural = "attributes"

# @admin.register(Attribute)
# class AttributeAdmin(admin.ModelAdmin):
    # list_display = [
        # 'name',
        # 'slug',
    # ]
    # list_display_links = [
        # 'name'
    # ]
    # search_fields = ['name',]
    # fields = [
        # ('name', 'slug'),
    # ]
    # prepopulated_fields = {'slug': ('name',)}
    # # inlines = [TermInline,]



#### PRODUCT-VARIATIONS
# I'm putting this form directly in Admin rather than in forms.py
# since this is where we are going to us it

# class VarAttrForm(forms.ModelForm):
    # class Meta:
        # model = VariationAttribute
        # fields = ('attributes', 'terms')
        # widgets = {
            # 'attributes': autocomplete.ModelSelect2(
                # url='var-attr-autocomplete',
                # forward=('variation',),
                # attrs={
                    # 'data-placeholder': 'Autocomplete ...',
                # },
            # ),
            # 'terms': autocomplete.ModelSelect2(
                # url='var-term-autocomplete',
                # forward=('variation', 'attributes',),
                # attrs={
                    # 'data-placeholder': 'Autocomplete ...',
                # },
            # ),
#         }

# class VarAttrInline(nested_admin.NestedTabularInline):
    # form = VarAttrForm
    # model = VariationAttribute
    # extra = 0
    # fk_name='variations'
    # verbose_name = "variation attribute"
    # verbose_name_plural = "variation attributes"

# class VariationInline(nested_admin.NestedTabularInline):
    # model = Variation
    # extra = 0
    # fk_name = 'parent'
    # verbose_name = "variation"
    # verbose_name_plural = "variations"
#     inlines = [VarAttrInline]


class ProductTypesFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('product types')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            # ('simp', _('is_simple')),
            ('digi', _('is_digital')),
            ('bund', _('is_bundle')),
            ('vari', _('is_variable')),
            # ('bund', _('is_bundle')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
#         if self.value() == 'simp':
#             return queryset.all()
        if self.value() == 'digi':
            return queryset.filter(digital_options__isnull=False).distinct()

        if self.value() == 'bund':
            return queryset.filter(bundle_parents__isnull=False).distinct()

        if self.value() == 'vari':
            return queryset.filter(variation_parents__isnull=False).distinct()


class ComponentInline(nested_admin.NestedStackedInline):
    """Component is a Part subitem."""
    model = itemsapp.models.Item
    fields = [
            'sku',
            'name',
            'description',
            ('categories', 'tags'),
            ('cost', 'cost_shipping', 'cost_other', 'unit_inventory'),
    ]

    extra = 0
    verbose_name = 'Component'
    verbose_name_plural = 'Components'
    autocomplete_fields = ['categories', 'tags', 'unit_inventory']


@admin.register(itemsapp.models.UnitInventory)
class UnitInventoryAdmin(admin.ModelAdmin):
    search_fields = ['singular']
    pass


# @admin.register(itemsapp.models.UnitDisplay)
# class UnitDisplayAdmin(admin.ModelAdmin):
    # search_fields = ['singular']
#     pass


@admin.register(itemsapp.models.Part)
class PartAdmin(nested_admin.NestedModelAdmin):

    fields = [
            'sku',
            'name',
            'description',
            ('categories', 'tags'),
            ('cost', 'cost_shipping', 'cost_other', 'unit_inventory'),
            'sum_component_cost',
    ]
    readonly_fields = (
            'sum_component_cost',
            )
    list_display = (
        'sku',
        'name',
        # should put final inventory avail, cost here not details
        # 'sum_component_cost'
    )
    list_display_links = (
        'sku',
        'name',
    )
    search_fields = (
        'sku',
        'name',
    )
    autocomplete_fields = [
        'categories',
        'tags',
        'unit_inventory',
    ]
    ordering = ['sku']

    inlines = [
        ComponentInline,
        # BidPartInline,
        # NotePartInline,
    ]

    def sum_component_cost(self, obj):
        return {
                'cost': obj.sum_subitems_cost,
                'cost_shipping': obj.sum_subitems_cost_shipping,
                'cost_other': obj.sum_subitems_cost_other
                }

    # def save_related(self, request, form, formsets, change):
        # super().save_related(request, form, formsets, change)
    #     form.instance.save()


@admin.register(itemsapp.models.Product)
class ProductAdmin(nested_admin.NestedModelAdmin):

    fields = (
        ('sku', 'name'),
        'description',
        'keywords',
        ('departments', 'categories', 'tags'),
        'price',
        ('unit', 'unit_plural', 'unit_base'),
        ('order_min', 'order_max')
    )
    # readonly_fields = (
        # 'ecpu',
        # 'unit',
        # 'ecpu_calc_from',
        # 'available_inventory',
        # 'max_new_inventory',
        # 'price',
        # 'price_calc_from',
        # 'is_digital',
        # 'is_variable',
        # 'is_bundle',
    # )
    list_display = (
        'sku',
        'name',
    #     'ecpu',
    #     'available_inventory',
        'price',
        # 'price_calc_from',
    )
    list_filter = (
        ProductTypesFilter,
    )
    list_display_links = (
        'sku',
        'name',
    )
    search_fields = (
        'sku',
        'name',
    )
    autocomplete_fields = [
        'departments',
        'categories',
        'tags',
    ]
    ordering = ['sku']

    inlines = (
        # ProductPartJoinInline,
        # ProductInventoryInline,
        # BidProductInline,
        IdentifierInline,
        MeasurementInline,
        MarketingOptionInline,
        ImageInline,
        # ProdAttrJoinInline,  # <-- trouble here
        # DigitalOptionInline,
        # BundleInline,
        # VariationInline,
    )

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.save()


@admin.register(itemsapp.models.DigitalProduct)
class DigitalProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    # autocomplete_fields = [
        # 'departments',
        # 'categories',
        # 'tags',
    # ]
    search_fields = ['name']
    # prepopulated_fields = {'slug': ('sku', 'name', )}
