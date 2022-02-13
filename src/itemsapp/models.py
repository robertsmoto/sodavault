from ckeditor.fields import RichTextField
from configapp.models import Group
from django.db import models
from django.db.models import Sum
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import configapp.models
import contactapp.models
import utilities.utils as utils
import uuid

# comment

class DepartmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='DEP')


class Department(Group):
    """Is a proxy model of Group."""
    objects = DepartmentManager()

    class Meta:
        proxy = True
        verbose_name_plural = "04. Departments"

    def save(self, *args, **kwargs):
        self.group_type = 'ITEMDEP'
        super(Department, self).save(*args, **kwargs)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='ITEMCAT')


class Category(Group):
    """Is a proxy model of Group."""
    objects = CategoryManager()

    class Meta:
        proxy = True
        verbose_name_plural = "05. Categories"

    def save(self, *args, **kwargs):
        self.group_type = 'ITEMCAT'
        super(Category, self).save(*args, **kwargs)


class TagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='ITEMTAG')


class Tag(Group):
    """Is a proxy model of Group."""
    objects = TagManager()

    class Meta:
        proxy = True
        verbose_name_plural = "06. Tags"

    def save(self, *args, **kwargs):
        self.group_type = 'ITEMTAG'
        super(Tag, self).save(*args, **kwargs)


class AttributeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group_type='ITEMATT')


class Attribute(Group):
    """Is a proxy model of Group."""
    objects = AttributeManager()

    class Meta:
        proxy = True
        verbose_name_plural = "07. Attributes"

    def save(self, *args, **kwargs):
        self.group_type = 'ITEMATT'
        super(Attribute, self).save(*args, **kwargs)



"""
kit: collection of items
    can be price separately, or a summation of items

bundle: collection of items, individual items may have sep configs
    can be price separately, or summation of items
    plus product can be incremented individually with thresholds
    the increment is handled in the transaction, need a bool to tell to swich
    on or off the increment.

kit is same as bundle, can call them a collection
"""

"""
variation: collection of items
with special attribute filters
variation is a collection but uses variations to filter the subitems
attr: need to know if a specific attr is_variation and display_order
collection, but need to know which attributes are used for filtering sub-items
parent
    attr1 [list] used for variations, order 0
    attr2 [list] used for variations, order 1
    (check if certain attr are used or unused)
    attr3 [list] not used for fitering
"""


class AttributeItemJoin(models.Model):
    # attributes = models.ForeignKey(
    #         Attribute, blank=True, on_delete=models.CASCADE)
    # this should filter based on the attribute selection
    terms = models.CharField(max_length=200, blank=True)
    is_variation = models.BooleanField(default=False)
    display_order = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.attribute.name}"


class CostMultiplier(models.Model):
    MULTIPLIER_CHOICES = [
            ('FL', 'Flat Rate'),
            ('GM', 'Gross Margin'),
            ('MU', 'Markup'),
    ]
    multiplier_type = models.CharField(
            max_length=4,
            blank=True,
            choices=MULTIPLIER_CHOICES,
    )
    amount = models.DecimalField(decimal_places=2, max_digits=11, blank=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.multiplier_type}"

    class Meta:
        ordering = ['multiplier_type', 'amount']


class UnitInventoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(unit_type="INV")


class UnitInventory(configapp.models.Unit):
    """Is a proxy model of configapp.Unit"""

    class Meta:
        proxy = True
        # verbose_name_plural = "05. Categories"

    def save(self, *args, **kwargs):
        self.unit_type = "INV"
        super(UnitInventory, self).save(*args, **kwargs)


class UnitDisplayManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(unit_type="DIS")


class UnitDisplay(configapp.models.Unit):
    """Is a proxy model of configapp.Unit"""

    class Meta:
        proxy = True
        # verbose_name_plural = "05. Categories"

    def save(self, *args, **kwargs):
        self.unit_type = "DIS"
        super(UnitInventory, self).save(*args, **kwargs)


class Item(models.Model):
    departments = models.ManyToManyField(
            Department,
            related_name='item_departments',
            blank=True)
    categories = models.ManyToManyField(
            Category,
            related_name='item_categories',
            blank=True)
    tags = models.ManyToManyField(
            Tag,
            related_name='item_tags',
            blank=True)
    attributes = models.ManyToManyField(
            AttributeItemJoin,
            blank=True)

    #  parent_id is available
    #  query parents --> Item.objects.filter(subitems__isnull=True)
    parent = models.ForeignKey(
            'self',
            null=True,
            on_delete=models.CASCADE,
            related_name="subitems")

    ITEM_TYPE_CHOICES = [
            ('PART', 'Part'),
            ('PROD', 'Product'),
    ]
    item_type = models.CharField(
            max_length=4,
            blank=True,
            choices=ITEM_TYPE_CHOICES,
    )
    sku = models.CharField(
            max_length=100,
            unique=True,
            default=f"SKU-{str(uuid.uuid4())[0:23]}"
            )
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(
            max_length=200,
            blank=True,
            help_text="For internal and purchasing use.")
    keywords = models.CharField(
            max_length=200,
            blank=True,
            help_text="comma, separated, list")
    # from this calculate ecpu
    cost = models.BigIntegerField(default=0)
    cost_shipping = models.BigIntegerField(default=0)
    cost_quantity = models.IntegerField(default=1)
    unit_inventory = models.ForeignKey(
            UnitInventory,
            related_name="unit_inventory",
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    unit_display = models.ForeignKey(
            UnitDisplay,
            related_name="unit_display",
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    unit_base = models.IntegerField(
            default=1,
            help_text="eg. 100 if inventory = 120 cm, display = 1.2 meters")

    # used for parts
    cost_multiplier = models.ForeignKey(
            CostMultiplier,
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    price = models.BigIntegerField(blank=True, null=True)
    order_min = models.IntegerField(
            blank=True,
            null=True,
            help_text="Use to require minium order quantity.")
    order_max = models.IntegerField(
            blank=True,
            null=True,
            help_text="Use to limit order quantity.")
    collection_quantity = models.IntegerField(
            blank=True,
            null=True,
            help_text="How many items are included in the collection.")

    @property
    def ecpu(self):
        winning_bids = self.bid_parts.filter(is_winning_bid=True)
        secpu = self.subitems.annotate(
                item_ecpu=(Sum('cost') + Sum('cost_shipping'))
                / Sum('cost_quantity')).aggregate(Sum('item_ecpu'))
        # priority 1 item cost override
        if (self.cost + self.cost_shipping) / self.cost_quantity is not None:
            print("in priority 1")
            return {
                    'ecpu': (
                        self.cost + self.cost_shipping) / self.cost_quantity,
                    'ecpu_display': '',
                    'ecpu_from': 'item cost override'}
        # priority 2 winning bid
        elif winning_bids:
            return {
                    'ecpu': winning_bids[0].ecpu,
                    'ecpu_display': '',
                    'ecpu_from': 'item winning bid'}
        # priority 3 subitems ecpu
        elif secpu['item_ecpu__sum'] > 0:
            return {
                    'ecpu': secpu['item_ecpu__sum'],
                    'ecpu_display': '',
                    'ecpu_from': 'sub subitem ecpu'}
        else:
            return {'ecpu': 0, 'ecpu_from': 'not calculated'}

    class Meta:
        indexes = [
            models.Index(fields=['sku', ]),
        ]

    def __str__(self):
        return f"{self.sku} {self.name}"  # .format(self.sku, self.name)


class PartManager(models.Manager):
    def get_queryset(self):
        return Item.objects.filter(item_type="PART")


class Part(Item):
    """Is a proxy model of Item."""
    objects = PartManager()

    class Meta:
        proxy = True
        verbose_name_plural = "01. Parts"

    def save(self, *args, **kwargs):
        self.item_type = "PART"
        super(Part, self).save(*args, **kwargs)


class ProductManager(models.Manager):
    def get_queryset(self):
        qs = Item.objects.filter(parent_id__isnull=True, item_type="PROD")
        return qs


class Product(Item):
    """Is a proxy model of Item."""
    objects = ProductManager()

    class Meta:
        proxy = True
        verbose_name_plural = "02a. Products"

    def save(self, *args, **kwargs):
        self.item_type = "PROD"
        super(Product, self).save(*args, **kwargs)


class Bid(models.Model):
    part = models.ForeignKey(
            Part,
            related_name="bid_parts",
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    product = models.ForeignKey(
            Product,
            related_name="bid_products",
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    supplier = models.ForeignKey(
            contactapp.models.Supplier,
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    date_requested = models.DateField(
            blank=True,
            null=True)
    date_submitted = models.DateField(
        blank=True,
        null=True)
    cost = models.BigIntegerField(default=0)
    cost_shipping = models.BigIntegerField(default=0)
    cost_quantity = models.IntegerField(
            default=1,
            help_text="Divides total cost by this number to return ecpu."
            )
    unit_inventory = models.ForeignKey(
            UnitInventory,
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    is_winning_bid = models.BooleanField(default=False)

    @property
    def ecpu(self):
        return (self.cost + self.cost_shipping) / self.cost_quantity

    def __str__(self):
        if self.part:
            return "{} {}".format(self.supplier, self.part)
        else:
            return "{} {}".format(self.supplier, self.product)



# do I need to do this, or just add a related digital items relation?
class DigitalProduct(Item):
    """Is a multi-table inheritance model of Item."""
    # put additional digital-related fields here
    test_field = models.CharField(max_length=200, blank=True)

    # objects = DigitalProductManager()
    class Meta:
        # proxy = True
        verbose_name_plural = "02b. Digital Products"

    def save(self, *args, **kwargs):
        self.item_type = "PROD"
        super(Product, self).save(*args, **kwargs)


class Identifier(models.Model):
    item = models.OneToOneField(
        Item,
        related_name='identifiers',
        null=True,
        on_delete=models.CASCADE)
    pid_i = models.BigIntegerField(null=True, blank=True)
    pid_c = models.CharField(max_length=100, blank=True)
    gtin = models.BigIntegerField(null=True, blank=True)
    isbn = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.item.name)


class Measurement(models.Model):
    item = models.OneToOneField(
        Item,
        related_name='measurements',
        null=True,
        on_delete=models.CASCADE,)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        return '{}'.format(self.item.name)


# class ProductAttributeJoin(models.Model):
    # """Used for product attributes."""
    # items = models.ForeignKey(
        # Item,
        # related_name='product_att_join',
        # null=True,
        # blank=True,
        # on_delete=models.CASCADE)
    # attribute = models.ForeignKey(
        # Attribute,
        # null=True,
        # blank=True,
        # on_delete=models.CASCADE)
    # # ManyToMany for product-attributes
    # term = models.ManyToManyField(
        # Term,
        # blank=True)

    # def __str__(self):
        # return '{}'.format(self.attribute.name)


# class Variation(models.Model):
    # parent = models.ForeignKey(
        # Item,
        # related_name='variation_parents',
        # null=True,
        # blank=True,
        # on_delete=models.CASCADE)
    # items = models.ForeignKey(
        # Item,
        # related_name='variation_products',
        # null=True,
        # on_delete=models.CASCADE)

    # def __str__(self):
        # return '{} : {}'.format(self.parent.sku, self.parent.name)


# class VariationAttribute(models.Model):
    # items = models.ForeignKey(
        # Item,
        # null=True,
        # blank=True,
        # on_delete=models.CASCADE)
    # variations = models.ForeignKey(
        # Variation,
        # related_name='variation_attributes',
        # null=True,
        # blank=True,
        # on_delete=models.CASCADE)
    # attributes = models.ForeignKey(
        # Attribute,
        # null=True,
        # blank=True,
        # on_delete=models.CASCADE)
    # terms = models.ForeignKey(
        # Term,
        # null=True,
        # blank=True,
        # on_delete=models.CASCADE)

    # def __str__(self):
        # return '{}'.format(self.variations.product.sku)


# class Bundle(models.Model):
    # parent = models.ForeignKey(
        # Item,
        # related_name='bundle_parents',
        # on_delete=models.CASCADE)
    # items = models.ForeignKey(
        # Item,
        # related_name='bundle_products',
        # null=True,
        # on_delete=models.CASCADE)
    # quantity_min = models.PositiveSmallIntegerField(default=1)
    # quantity_max = models.PositiveSmallIntegerField(blank=True, null=True)
    # is_optional = models.BooleanField(default=False)

    # def __str__(self):
#         return '{} : {}'.format(self.parent.sku, self.parent.name)


# class DigitalOption(models.Model):
    # item = models.OneToOneField(
        # Item,
        # related_name='digital_options',
        # null=True,
        # on_delete=models.CASCADE)
    # name = models.CharField(max_length=200, blank=True)
    # # other things like a download key, file, expiration date etc ...

    # def __str__(self):
        # return '{}'.format(self.item.name)


class Promotion(models.Model):
    items = models.ManyToManyField(
        Item,
        related_name='promotions')
    promotion_override = models.ForeignKey(
        'self',
        related_name='overrides',
        null=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=50)
    begins = models.DateField(null=True)
    ends = models.DateField(null=True)
    percentage = models.DecimalField(
        max_digits=4, decimal_places=2, null=True,
        help_text="Percentage discount eg. 25% off")
    fixed = models.DecimalField(
        max_digits=8, decimal_places=2, null=True,
        help_text="Fixed discount eg. $5.00 off")
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True,
        help_text="Fixed price eg. Sale Price $25.00")
    is_free_shipping = models.BooleanField(default=False)
    bogx = models.PositiveSmallIntegerField(
        null=True,
        help_text="Buy One Get x Free")

    def __str__(self):
        return '{}'.format(self.name)


class Marketing(models.Model):
    item = models.OneToOneField(
        Item,
        related_name='marketing_options',
        null=True,
        on_delete=models.CASCADE)
    description_sm = RichTextField(
            blank=True,
            null=True,
            max_length=500, help_text="500 characters max.")
    description_md = RichTextField(
            blank=True,
            null=True,
            max_length=1000, help_text="1000 characters max.")
    description_lg = RichTextField(
            blank=True,
            null=True,
            max_length=1000, help_text="1000 characters max.")

    def __str__(self):
        return '{}'.format(self.item.name)


class Image(models.Model):
    item = models.ForeignKey(
        Item,
        related_name='images',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    # possibly make this a calculated field as well as gross margin?
    order = models.IntegerField(
        blank=True, null=True,
        help_text='integer used to order images')
    # images client-determined size
    img_lg = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="converts to WebP format")
    img_md = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="converts to WebP format")
    img_sm = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="converts to WebP format")
    # images square 1:1
    img_1x1_lg = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(1000, 1000)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="1000px x 1000px")
    img_1x1_md = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(500, 500)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="500px x 500px")
    img_1x1_sm = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(250, 250)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="250px x 250px")
    # images 2:1
    img_2x1_lg = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(1000, 500)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="1000px x 500px")
    img_2x1_md = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(500, 250)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="500px x 250px")
    img_2x1_sm = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(250, 125)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="250px x 125px")
    # images 1:2
    img_1x2_lg = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(500, 1000)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="500px x 1000px")
    img_1x2_md = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(250, 500)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="250px x 500px")
    img_1x2_sm = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(125, 250)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="125px x 250px")
    # 16_9
    img_16x9 = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(1200, 675)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="16:9 1200px x 675px")
    # 191_1
    img_191x1 = ProcessedImageField(
            upload_to='product_images/%Y/%m/%d',
            processors=[ResizeToFill(1200, 628)],
            format='WebP',
            options={'quality': 80},
            blank=True,
            null=True,
            help_text="1.91:1 1200px x 628px")

    class Meta:
        ordering = ('order', )

    def __str__(self):
        return '{}'.format(self.name)


class ProductPartJoin(models.Model):
    parts = models.ForeignKey(
            Part,
            related_name='ppj_parts',
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    products = models.ForeignKey(
            Product,
            related_name='ppj_products',
            blank=True,
            null=True,
            on_delete=models.CASCADE)
#     simple_products = models.ForeignKey(
            # SimpleProduct,
            # related_name="ppj_simple_products",
            # blank=True,
            # null=True,
#             on_delete=models.CASCADE)
#     digital_products = models.ForeignKey(
            # DigitalProduct,
            # related_name="ppj_digital_products",
            # blank=True,
            # null=True,
#             on_delete=models.CASCADE)
    # bundle_products = models.ForeignKey(
            # BundleProduct,
            # related_name="ppj_bundle_products",
            # blank=True,
            # null=True,
            # on_delete=models.CASCADE)
    # variable_products = models.ForeignKey(
            # VariableProduct,
            # related_name="ppj_variable_products",
            # blank=True,
            # null=True,
    #         on_delete=models.CASCADE)
    quantity = models.IntegerField(
            default=1,
            help_text="How many parts per product?")
    is_unlimited = models.BooleanField(
            default=False,
            help_text="Denotes if a part should be considered unlimited.")
    use_all = models.BooleanField(
            default=False,
            help_text=(
                "Use all part inventory when the related product is "
                "brought into inventory."))

    @property
    def _ecpu(self):
        ecpu = self.parts.ecpu if self.parts.ecpu is not None else 0
        return round(ecpu, 4)

    @property
    def _unit(self):
        return self.parts._unit


class Note(models.Model):
    item = models.ForeignKey(
            Item,
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    date = models.DateField(
            blank=True,
            null=True)
    note = models.TextField(
            max_length=3000,
            blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.date.isoformat()


"""

class PartManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(item_type='PART')


class SimpleProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
                item_type="PROD", product_type="SIMP")


class DigitalProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
                item_type="PROD", product_type="DIGI")


class BundleProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
                item_type="PROD", product_type="BUND")


class VariableProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
                item_type="PROD", product_type="VARI")

class SimpleProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
                item_type="PROD", product_type="SIMP")



"""
