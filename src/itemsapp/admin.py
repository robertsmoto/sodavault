# from django import forms
from django.contrib import admin
import itemsapp.models

GROUP_FIELDS = [
        ('name', 'slug'),
        ('description', 'kwd_list'),
        ('order', 'is_primary', 'is_secondary', 'is_tertiary'),
        ]
GROUP_LIST_DISPLAY = [
        'slug', 'name', 'description', 'is_primary', 'is_secondary',
        'is_tertiary', 'order'
        ]
GROUP_LIST_DISPLAY_LINKS = ['slug']


class SubDepartmentInline(admin.TabularInline):
    model = itemsapp.models.Department
    fields = GROUP_FIELDS
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Department"
    verbose_name_plural = "Sub-Departments"


@admin.register(itemsapp.models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    fields = GROUP_FIELDS
    list_display = GROUP_LIST_DISPLAY
    list_display_links = GROUP_LIST_DISPLAY_LINKS
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [SubDepartmentInline, ]


class SubBrandInline(admin.TabularInline):
    model = itemsapp.models.Brand
    fields = GROUP_FIELDS
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Brand"
    verbose_name_plural = "Sub-Brands"


@admin.register(itemsapp.models.Brand)
class BrandAdmin(admin.ModelAdmin):
    fields = GROUP_FIELDS
    list_display = GROUP_LIST_DISPLAY
    list_display_links = GROUP_LIST_DISPLAY_LINKS
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [SubBrandInline, ]


class SubCategoryInline(admin.TabularInline):
    model = itemsapp.models.Category
    fields = GROUP_FIELDS
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Category"
    verbose_name_plural = "Sub-Categories"


@admin.register(itemsapp.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = GROUP_FIELDS
    list_display = GROUP_LIST_DISPLAY
    list_display_links = GROUP_LIST_DISPLAY_LINKS
    search_fields = ['name']
    exclude = ['cat_type', ]
    prepopulated_fields = {'slug': ('name', )}
    inlines = [SubCategoryInline, ]


class SubTagInline(admin.TabularInline):
    model = itemsapp.models.Tag
    fields = GROUP_FIELDS
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Sub-Tag"
    verbose_name_plural = "Sub-Tags"


@admin.register(itemsapp.models.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = GROUP_FIELDS
    list_display = GROUP_LIST_DISPLAY
    list_display_links = GROUP_LIST_DISPLAY_LINKS
    search_fields = ['name']
    exclude = ['cat_type', ]
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubTagInline, ]


class SubAttributeInline(admin.TabularInline):
    model = itemsapp.models.Attribute
    fields = GROUP_FIELDS
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = "Term"
    verbose_name_plural = "Attribute Terms"
    # autocomplete_fields = ['stores', 'warehouses']


@admin.register(itemsapp.models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    fields = GROUP_FIELDS
    readonly_fields = ['terms_display']
    list_display = [
        'slug', 'name', 'terms_display', 'is_primary', 'is_secondary',
        'is_tertiary', 'order'
        ]

    list_display_links = GROUP_LIST_DISPLAY_LINKS
    search_fields = ['name', 'id']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubAttributeInline, ]

    def get_search_results(self, request, queryset, search_term):
        field_name = request.GET.get('field_name', 'attribute')

        if field_name == "term" or field_name == "terms":
            queryset = queryset.filter(parent__isnull=False)
        elif field_name == "attribute":
            queryset = queryset.filter(parent__isnull=True)

        return super().get_search_results(request, queryset, search_term)

    def terms_display(self, obj):
        terms = obj.subgroups.all()
        terms_str = 'none'
        if terms:
            terms_str = ", ".join([term.name for term in terms])
        return terms_str

    terms_display.short_description = "Terms"


class NoteInline(admin.TabularInline):
    model = itemsapp.models.Note
    extra = 0
    classes = ['collapse']
    verbose_name = "note"
    verbose_name_plural = "notes"

    def get_exclude(self, request, obj):
        if obj.__class__.__name__ == "Component":
            return ['part', 'product']
        if obj.__class__.__name__ == "Part":
            return ['component', 'product']
        if obj.__class__.__name__ == "Product":
            return ['component', 'part']
        return


class BidInline(admin.TabularInline):
    model = itemsapp.models.Bid
    extra = 0
    classes = ['collapse']
    verbose_name = "bid"
    verbose_name_plural = "bids"
    # autocomplete_fields = ['supplier', 'unit']

    def get_exclude(self, request, obj):
        if obj.__class__.__name__ == "Component":
            return ['part', 'product']
        if obj.__class__.__name__ == "Part":
            return ['component', 'product']
        if obj.__class__.__name__ == "Product":
            return ['component', 'part']
        return


class IdentifierInline(admin.TabularInline):

    model = itemsapp.models.Identifier
    fields = [
        ('gtin', 'isbn'),
        ('pid_i', 'pid_c')
    ]
    classes = ['collapse']
    verbose_name = "identifiers"
    verbose_name_plural = "identifiers"


class MeasurementInline(admin.TabularInline):

    model = itemsapp.models.Measurement
    fields = [
        'weight',
        ('length', 'width', 'height')
    ]
    classes = ['collapse']
    verbose_name = "measurements"


class MarketingOptionInline(admin.StackedInline):

    model = itemsapp.models.Marketing
    classes = ['collapse']
    verbose_name = "marketing options"
    fields = [
        'description_sm',
        'description_md',
        'description_lg',
    ]
    verbose_name = "marketing options"
    verbose_name_plural = "marketing options"


class ImageInline(admin.StackedInline):

    model = itemsapp.models.Image
    classes = ['collapse']
    verbose_name = "marketing options"
    fields = [
        ('title', 'caption'),
        ('featured', 'order'),
        ('lg_11', 'md_11', 'sm_11'),
        ('lg_21', 'md_21', 'sm_21'),
        'lg_191',
        'custom',
    ]
    readonly_fields = ['md_11', 'sm_11', 'md_21', 'sm_21']
    verbose_name = "image"
    verbose_name_plural = "images"
    extra = 0


class DigitalInline(admin.StackedInline):
    model = itemsapp.models.Digital
    verbose_name = "Digital Option"
    verbose_name_plural = "Digital Options"
    classes = ['collapse']

    def get_exclude(self, request, obj):
        if obj.__class__.__name__ == "Part":
            return ['product']
        if obj.__class__.__name__ == "Product":
            return ['part']
        return


class AssemblyInline(admin.TabularInline):
    """Item cost assembly."""

    model = itemsapp.models.Item.assembly.through
    fk_name = 'item'
    fields = ['assembly', 'assembly_ecpu', 'quantity', 'is_unlimited' ,'use_all']
    # autocomplete_fields = ['assembly']
    readonly_fields = ['assembly_ecpu']
    extra = 0
    classes = ['collapse']
    verbose_name = 'Assembly'
    verbose_name_plural = 'Assembled Items'

    def assembly_ecpu(self, model):
        return model.assembly.ecpu


class AttributeInline(admin.TabularInline):

    model = itemsapp.models.Product.attributes.through
    extra = 0
    classes = ['collapse']
    ordering = ['order', ]
    verbose_name = "Attribute"
    verbose_name_plural = "Attributes"
    autocomplete_fields = ['attribute', 'terms']


class VariationInline(admin.TabularInline):

    model = itemsapp.models.Product.variations.through
    fk_name = 'item'
    extra = 0
    classes = ['collapse']
    verbose_name = "Variation"
    verbose_name_plural = "Variations"
    # autocomplete_fields = ['variation', 'attribute', 'term']


class CollectionInline(admin.TabularInline):
    """Item collection."""

    model = itemsapp.models.Item.collections.through
    fk_name = 'item'
    autocomplete_fields = ['collection']
    extra = 0
    classes = ['collapse']
    verbose_name = 'Item'
    verbose_name_plural = 'Collection'


@admin.register(itemsapp.models.Unit)
class UnitInventoryAdmin(admin.ModelAdmin):
    search_fields = ['inv_singular', 'dis_singular']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    pass


ITEM_FIELDS = [
        ('name', 'sku'),
        ('description', 'keywords'),
        ('categories', 'tags'),
        ('cost', 'cost_shipping', 'cost_quantity', 'unit'),
        'ecpu_display',
        'inv_display',
        ]
ITEM_READONLY_FIELDS = ['ecpu_display', 'inv_display']
ITEM_AUTOCOMPLETE_FIELDS = ['categories', 'tags', 'unit']
ITEM_PREPOPULATED_FIELDS = {'sku': ('name',), }
ITEM_LIST_DISPLAY = [
        'sku',
        'name',
        'ecpu'
        ]
ITEM_LIST_FILTER = [
        'categories',
        'tags'
        ]
ITEM_LIST_DISPLAY_LINKS = [
        'sku',
        'name'
        ]
ITEM_SEARCH_FIELDS = [
        'sku',
        'name'
        ]
ITEM_ORDERING = ['sku']


@admin.register(itemsapp.models.Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['sku', 'name']

    def save_related(self, request, form, formsets, change):
        print("change", change)
        super().save_related(request, form, formsets, change)

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


@admin.register(itemsapp.models.Component)
class ComponentAdmin(admin.ModelAdmin):
    fields = ITEM_FIELDS
    readonly_fields = ITEM_READONLY_FIELDS
    autocomplete_fields = ITEM_AUTOCOMPLETE_FIELDS
    prepopulated_fields = ITEM_PREPOPULATED_FIELDS
    list_display = ITEM_LIST_DISPLAY
    list_filter = ITEM_LIST_FILTER
    list_display_links = ITEM_LIST_DISPLAY_LINKS
    search_fields = ITEM_SEARCH_FIELDS
    ordering = ITEM_ORDERING

    def get_inlines(self, request, obj):
        return [BidInline, NoteInline]

    def unit_inv(self, obj):
        return f"{obj.unit.inv_singular} ({obj.unit.inv_plural})"


@admin.register(itemsapp.models.Part)
class PartAdmin(admin.ModelAdmin):
    fields = ITEM_FIELDS
    readonly_fields = ITEM_READONLY_FIELDS
    autocomplete_fields = ITEM_AUTOCOMPLETE_FIELDS
    prepopulated_fields = ITEM_PREPOPULATED_FIELDS
    list_display = ITEM_LIST_DISPLAY
    list_filter = ITEM_LIST_FILTER
    list_display_links = ITEM_LIST_DISPLAY_LINKS
    search_fields = ITEM_SEARCH_FIELDS
    ordering = ITEM_ORDERING

    def get_inlines(self, request, obj):
        return [BidInline, AssemblyInline, NoteInline]


@admin.register(itemsapp.models.Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ITEM_FIELDS
    readonly_fields = ITEM_READONLY_FIELDS
    autocomplete_fields = ITEM_AUTOCOMPLETE_FIELDS
    prepopulated_fields = ITEM_PREPOPULATED_FIELDS
    list_display = ITEM_LIST_DISPLAY
    list_filter = ITEM_LIST_FILTER
    list_display_links = ITEM_LIST_DISPLAY_LINKS
    search_fields = ITEM_SEARCH_FIELDS
    ordering = ITEM_ORDERING

    def get_inlines(self, request, obj):
        return [
                BidInline,
                AssemblyInline,
                NoteInline,
                AttributeInline,
                VariationInline,
                CollectionInline,
                DigitalInline,
                IdentifierInline,
                MeasurementInline,
                MarketingOptionInline,
                ImageInline,
                ]


@admin.register(itemsapp.models.Ledger)
class LedgerAdmin(admin.ModelAdmin):

    list_display = [
        'date',
        'account',
        'item_sku',
        'location',
        'lot',
        'debit_quantity',
        'debit_amount',
        'credit_quantity',
        'credit_amount',
        'note',
    ]
    readonly_fields = ['item_sku']
    autocomplete_fields = ['location', 'item']

    def item_sku(self, obj):
        return obj.item.sku if obj.item else "hello"
