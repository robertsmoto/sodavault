from django import forms
from django.contrib import admin
from django.urls import resolve
from django.utils.translation import gettext_lazy as _
from ledgerapp.models import Entry
import configapp.models
import itemsapp.models


class SubDepartmentInline(admin.TabularInline):
    model = configapp.models.Group
    exclude = ['cat_type']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Department"
    verbose_name_plural = "Sub-Departments"


@admin.register(itemsapp.models.ItemDepartment)
class ItemDepartmentAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name']
    exclude = ['group_type']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [SubDepartmentInline, ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ItemDepartmentAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="ITEMDEP")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "ITEMDEP"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}



class SubCategoryInline(admin.TabularInline):
    model = configapp.models.Group
    exclude = ['cat_type']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Category"
    verbose_name_plural = "Sub-Categories"


@admin.register(itemsapp.models.ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
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

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ItemCategoryAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="ITEMCAT")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "ITEMCAT"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}



class SubTagInline(admin.TabularInline):
    model = configapp.models.Group
    exclude = ['cat_type']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Tag"
    verbose_name_plural = "Sub-Tags"


@admin.register(itemsapp.models.ItemTag)
class ItemTagAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name']
    exclude = ['cat_type', ]
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubTagInline, ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ItemTagAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="ITEMTAG")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "ITEMTAG"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class SubAttributeInline(admin.TabularInline):
    model = itemsapp.models.ItemAttribute
    # exclude = ['group_type']
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Term"
    verbose_name_plural = "Attribute Terms"
    # autocomplete_fields = ['stores', 'warehouses']


@admin.register(itemsapp.models.ItemAttribute)
class ItemAttributeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]
    search_fields = ['name']
    exclude = ['group_type', 'subgroup']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubAttributeInline, ]

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ItemAttributeAdmin, self).get_search_results(
            request, queryset, search_term
        )
        queryset = queryset.filter(group_type="ITEMATT")
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.group_type = "ITEMATT"
        super().save_model(request, obj, form, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class ProductInventoryInline(admin.TabularInline):

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


class PartInventoryInline(admin.TabularInline):

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


class NoteInline(admin.TabularInline):
    model = itemsapp.models.Note
    extra = 0
    classes = ['collapse']
    verbose_name = "note"
    verbose_name_plural = "notes"
    # exclude = ['pos', 'asns']


class BidComponentInline(admin.TabularInline):
    model = itemsapp.models.Bid
    exclude = ['part', 'product']
    extra = 0
    classes = ['collapse']
    verbose_name = "bid"
    verbose_name_plural = "bids"
    # autocomplete_fields = ['unit_inventory', 'supplier']


class BidPartInline(admin.TabularInline):
    model = itemsapp.models.Bid
    exclude = ['component', 'product']
    extra = 0
    classes = ['collapse']
    verbose_name = "bid"
    verbose_name_plural = "bids"
    # autocomplete_fields = ['unit_inventory', 'supplier']


class BidProductInline(admin.TabularInline):
    model = itemsapp.models.Bid
    exclude = ['component', 'part']
    extra = 0
    classes = ['collapse']
    verbose_name = "bid"
    verbose_name_plural = "bids"


class IdentifierInline(admin.TabularInline):

    model = itemsapp.models.Identifier
    fields = [
        ('gtin', 'isbn'),
        ('pid_i', 'pid_c')
    ]
    extra = 0
    classes = ['collapse']
    verbose_name = "identifier"
    verbose_name_plural = "identifiers"


class MeasurementInline(admin.TabularInline):

    model = itemsapp.models.Measurement
    fields = [
        'weight',
        ('length', 'width', 'height')
    ]
    extra = 0
    classes = ['collapse']
    verbose_name = "measurements"


class MarketingOptionInline(admin.StackedInline):

    model = itemsapp.models.Marketing
    extra = 0
    classes = ['collapse']
    verbose_name = "marketing options"
    fields = [
        'description_sm',
        'description_md',
        'description_lg',
    ]
    verbose_name = "option"
    verbose_name_plural = "marketing options"


class ImageInline(admin.StackedInline):

    model = itemsapp.models.Image
    extra = 0
    classes = ['collapse']
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


class ComponentInlineForm(forms.ModelForm):

    to_item = forms.ModelChoiceField(
            queryset=itemsapp.models.Item.objects
            .filter(item_type="COMP"),
            empty_label="-----")


class ComponentInline(admin.TabularInline):
    """Component is an Item with item_type='COMP'."""

    model = itemsapp.models.Item.components.through
    form = ComponentInlineForm
    fk_name = 'from_item'
    extra = 0
    classes = ['collapse']
    verbose_name = 'Component'
    verbose_name_plural = 'Components'
    # autocomplete_fields = ['categories', 'tags', 'unit_inventory']


class PartInlineForm(forms.ModelForm):

    to_item = forms.ModelChoiceField(
            queryset=itemsapp.models.Item.objects
            .filter(item_type="PART"),
            empty_label="-----")


class PartInline(admin.TabularInline):
    """Component, part is an Item with item_type='PART'."""

    model = itemsapp.models.Item.components.through
    form = PartInlineForm
    fk_name = 'from_item'
    extra = 0
    classes = ['collapse']
    verbose_name = 'Part'
    verbose_name_plural = 'Parts'
    # autocomplete_fields = ['categories', 'tags', 'unit_inventory']


@admin.register(itemsapp.models.UnitInventory)
class UnitInventoryAdmin(admin.ModelAdmin):
    search_fields = ['singular']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(itemsapp.models.UnitDisplay)
class UnitDisplayAdmin(admin.ModelAdmin):
    search_fields = ['singular']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(itemsapp.models.Component)
class ComponentAdmin(admin.ModelAdmin):

    fields = [
            ('name', 'sku'),
            ('description', 'keywords'),
            ('categories', 'tags'),
            ('cost', 'cost_shipping', 'cost_quantity', 'unit_inventory'),
            # 'ecpu',
    ]
    prepopulated_fields = {'sku': ('name',), }
    readonly_fields = ['ecpu']
    list_display = (
        'sku',
        'name',
    )
    list_display_links = (
        'sku',
        'name',
    )
    search_fields = (
        'sku',
        'name',
    )
    # autocomplete_fields = ['categories', 'tags', 'unit_inventory']
    ordering = ['sku']

    inlines = [
        BidComponentInline,
        NoteInline,
    ]

    def get_queryset(self, request):
        """Use custom model manager."""
        qs = self.model.objects.components()
        return qs


@admin.register(itemsapp.models.Part)
class PartAdmin(admin.ModelAdmin):

    fields = [
            ('name', 'sku'),
            ('description', 'keywords'),
            ('categories', 'tags'),
            ('cost', 'cost_shipping', 'cost_quantity', 'unit_inventory'),
            # 'new_field'
            # 'ecpu',
    ]
    prepopulated_fields = {'sku': ('name',), }
    readonly_fields = ['ecpu']
    list_display = (
        'sku',
        'name',
    )
    list_display_links = (
        'sku',
        'name',
    )
    search_fields = (
        'sku',
        'name',
    )
    # autocomplete_fields = ['categories', 'tags', 'unit_inventory']
    ordering = ['sku']

    inlines = [
        BidPartInline,
        ComponentInline,
        NoteInline,
    ]

    def get_queryset(self, request):
        """Use custom model manager."""
        qs = self.model.objects.parts()
        return qs


def calc_ecpu(main: dict) -> dict:
    """Recursive function that calculates the estimated cost per unit.
    Begin with 'start_ids' key as a list of one or more obj.ids
    formatted: main = {'start_ids': [17]}"""

    main['ecpu'] = 0 if 'ecpu' not in main else main['ecpu']
    main['ecpu_fcnt'] = 0 if 'ecpu_fcnt' not in main else main['ecpu_fcnt']

    def check_for_list(main: dict) -> (int, int, dict):
        item_id = None
        qnty_multby = 1
        if main['start_ids']:
            item_id = main['start_ids'].pop()
        if isinstance(item_id, list):
            if item_id:
                hold_ids = item_id
                item_id = hold_ids.pop()
                if hold_ids:
                    main['start_ids'].append(hold_ids)
            else:
                check_for_list(main)
        if isinstance(item_id, tuple):
            qnty_multby = item_id[0]
            item_id = item_id[1]

        return qnty_multby, item_id, main

    qnty_multby, item_id, main = check_for_list(main)

    if not item_id:
        return main

    item = itemsapp.models.Item.objects \
        .prefetch_related(
                'bid_components',
                'bid_parts',
                'bid_products',
                ) \
        .get(id=item_id)

    # bid queries
    bids = (
            item.bid_components.filter(is_winning_bid=True) |
            item.bid_parts.filter(is_winning_bid=True) |
            item.bid_products.filter(is_winning_bid=True)
            )

    # component queries
    new_ids = itemsapp.models.ComponentJoin.objects \
        .values_list('quantity', 'to_item_id') \
        .filter(from_item_id=item_id)

    # check override
    if item.cost + item.cost_shipping > 0:
        main['ecpu'] = main['ecpu'] + (
                qnty_multby
                * ((item.cost + item.cost_shipping) / item.cost_quantity)
                )
        main['ecpu_fcnt'] = 1 if main['ecpu_fcnt'] == 0 else main['ecpu_fcnt']

    # check winning bid
    elif len(bids) > 0:
        bid = bids[0]
        main['ecpu'] = main['ecpu'] + (
                qnty_multby
                * ((bid.cost + bid.cost_shipping) / bid.cost_quantity)
                )

        main['ecpu_fcnt'] = 2 if main['ecpu_fcnt'] == 0 else main['ecpu_fcnt']

    # check components
    elif new_ids:
        main['start_ids'].append(list(new_ids))

    # return condition
    print("main @ end",  main)
    if len(main['start_ids']) > 0:
        main['ecpu_fcnt'] += 1
        return calc_ecpu(main=main)
    else:
        print("this is the end")
        if main['ecpu_fcnt'] == 1:
            main['ecpu_from'] = "cost override"
        elif main['ecpu_fcnt'] == 2:
            main['ecpu_from'] = "winning bid"
        else:
            main['ecpu_from'] = "component costs"

        main.pop('start_ids')
        main.pop('ecpu_fcnt')
        return main


class ProductForm(forms.ModelForm):

    class Meta:
        model = itemsapp.models.Product
        fields = '__all__'

    ecpu = forms.CharField(
            max_length=200,
            disabled=True,
            widget=forms.TextInput(
                attrs={
                    'style': 'width: 350px;'}
                )
            )

    def __init__(self, *args, **kwargs):
        """Return the initial data to use for forms on this view."""
        super(ProductForm, self).__init__(*args, **kwargs)
        object_ids = []
        obj = self.instance
        object_ids.append(obj.id)
        main_dict = {'start_ids': object_ids}
        main = calc_ecpu(main=main_dict)
        print(main)
        self.fields['ecpu'].initial = main


@admin.register(itemsapp.models.Product)
class ProductAdmin(admin.ModelAdmin):

    form = ProductForm
    fields = [
            ('name', 'sku'),
            ('description', 'keywords'),
            ('categories', 'tags'),
            ('cost', 'cost_shipping', 'cost_quantity', 'unit_inventory'),
            'ecpu'
    ]

    prepopulated_fields = {'sku': ('name',), }

    list_display = (
        'sku',
        'name',
        # 'ecpu',
        'price',
    )
    list_filter = (
        ProductTypesFilter,
    )
    list_display_links = (
        'name',
    )
    search_fields = (
        'sku',
        'name',
    )
    # autocomplete_fields = ['departments', 'categories', 'tags']

    inlines = (
        # ProductPartJoinInline,
        # ProductInventoryInline,
        BidProductInline,
        PartInline,
        IdentifierInline,
        MeasurementInline,
        MarketingOptionInline,
        ImageInline,
        # ProdAttrJoinInline,  # <-- trouble here
        # DigitalOptionInline,
        # BundleInline,
        # VariationInline,
    )

    def get_queryset(self, request):
        """Use custom model manager."""
        qs = self.model.objects.products()
        return qs
