from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.db.models import Sum, Q
from django.utils import timezone
import configapp.models
import contactapp.models
import datetime
import itemsapp.utils.stats


class Attribute(configapp.models.GroupABC):
    class Meta(configapp.models.GroupABC.Meta):
        verbose_name_plural = '_ attributes'


class Department(configapp.models.GroupABC):
    class Meta(configapp.models.GroupABC.Meta):
        verbose_name_plural = '_ departments'


class Brand(configapp.models.GroupABC):
    class Meta(configapp.models.GroupABC.Meta):
        verbose_name_plural = '_ brands'


class Category(configapp.models.GroupABC):
    class Meta(configapp.models.GroupABC.Meta):
        verbose_name_plural = '__ categories'


class Tag(configapp.models.GroupABC):
    class Meta(configapp.models.GroupABC.Meta):
        verbose_name_plural = '__ tags'


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
    amount = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.multiplier_type}"

    class Meta:
        ordering = ['multiplier_type', 'amount']


class Unit(models.Model):
    """Used to describe Item units for inventory and for the front-end."""

    inv_singular = models.CharField(max_length=100, default="centimeter")
    inv_plural = models.CharField(max_length=100, default="centimeters")
    dis_singular = models.CharField(max_length=100, default="meter")
    dis_plural = models.CharField(max_length=100, default="meters")
    unit_base = models.IntegerField(
            default=1,
            help_text="eg. 100 if inventory = 120 cm, display = 1.2 meters")

    def __str__(self):
        return (
                f"{self.inv_singular} ({self.inv_plural}) | "
                f"{self.dis_singular} ({self.dis_plural}) | "
                f"{self.unit_base}"
                )


class Item(models.Model):
    categories = models.ManyToManyField(
            Category,
            blank=True)
    tags = models.ManyToManyField(
            Tag,
            blank=True)
    cost_multiplier = models.ForeignKey(
            CostMultiplier,
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    assembly = models.ManyToManyField(
            'self',
            through='ItemAssemblyJoin',
            through_fields=('item', 'assembly'),
            blank=True)
    collections = models.ManyToManyField(
            'self',
            through='ItemCollectionJoin',
            through_fields=('item', 'collection'),
            blank=True)
    attributes = models.ManyToManyField(
            Attribute,
            through='ItemAttributeJoin',
            through_fields=('item', 'attribute'),
            blank=True)
    variations = models.ManyToManyField(
            'self',
            through='ItemVariationJoin',
            through_fields=('item', 'variation'),
            blank=True)
    departments = models.ManyToManyField(
            Department,
            blank=True)
    brands = models.ManyToManyField(
            Brand,
            blank=True)
    categories = models.ManyToManyField(
            Category,
            blank=True)
    tags = models.ManyToManyField(
            Tag,
            blank=True)
    unit = models.ForeignKey(
            Unit,
            blank=True,
            null=True,
            on_delete=models.CASCADE)

    ITEM_TYPE_CHOICES = [
            ("COMP", "Component"),
            ("PART", "Part"),
            ("PROD", "Product"),
            ]
    item_type = models.CharField(
            max_length=4,
            choices=ITEM_TYPE_CHOICES
            )
    sku = models.CharField(
            max_length=100,
            unique=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(
            max_length=200,
            blank=True,
            help_text="For internal and purchasing use.")
    keywords = models.CharField(
            max_length=200,
            blank=True,
            help_text="comma, separated, list")

    cost = models.BigIntegerField(default=0)
    cost_shipping = models.BigIntegerField(default=0)
    cost_quantity = models.IntegerField(default=1)
    ecpu = models.BigIntegerField(default=0)
    ecpu_from = models.CharField(max_length=20, blank=True)

    price = models.BigIntegerField(blank=True, null=True)

    @property
    def ecpu_display(self):
        return itemsapp.utils.stats.calc_ecpu(obj=self)

    @property
    def inv_display(self):
        return itemsapp.utils.stats.calc_inv(obj=self)

    class Meta:
        ordering = ['sku']
        indexes = [
            models.Index(fields=['sku', ]),
        ]

    def save(self, **kwargs):
        super().save(**kwargs)
        self.ecpu = self.ecpu_display['ecpu']
        self.ecpu_from = self.ecpu_display['ecpu_from']
        return super().save(**kwargs)

    def __str__(self):
        return f"{self.sku} {self.name}"  # .format(self.sku, self.name)


class ComponentManager(models.Manager):

    def get_queryset(self):
        return super(ComponentManager, self).get_queryset().filter(
                item_type="COMP")


class Component(Item):
    objects = ComponentManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.item_type = "COMP"
        return super().save(**kwargs)


class PartManager(models.Manager):

    def get_queryset(self):
        return super(PartManager, self).get_queryset().filter(
                item_type="PART")


class Part(Item):
    objects = PartManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.item_type = "PART"
        return super().save(**kwargs)


class ProductManager(models.Manager):

    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(
                item_type="PROD")


class Product(Item):
    objects = ProductManager()

    class Meta:
        proxy = True

    def save(self, **kwargs):
        self.item_type = "PROD"
        return super().save(**kwargs)


class ItemAssemblyJoin(models.Model):
    item = models.ForeignKey(
            Item,
            related_name="item_assemb_join",
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    assembly = models.ForeignKey(
            Item,
            related_name="assembly_assemb_join",
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    quantity = models.IntegerField(
            default=1,
            help_text="How many items are included in the cost."
            )
    is_unlimited = models.BooleanField(
            default=False,
            help_text="Is not limited by inventory eg. skilled labor.")
    use_all = models.BooleanField(
            default=False,
            help_text="Use the entire quantity when creating a parent item. "
            "eg. labels")

    def save(self, **kwargs):
        super().save(**kwargs)
        item = self.item
        item.save()


class ItemAttributeJoin(models.Model):
    item = models.ForeignKey(
            Item,
            related_name='item_attr_join',
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    attribute = models.ForeignKey(
            Attribute,
            related_name='attr_attr_join',
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    terms = models.ManyToManyField(
            Attribute,
            related_name='term_attr_join',
            blank=True)
    is_variation = models.BooleanField(default=False)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.attribute:
            return f"{self.attribute.name}"
        else:
            return "----"


class ItemCollectionJoin(models.Model):
    item = models.ForeignKey(
            Item,
            related_name='item_coll_join',
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    collection = models.ForeignKey(
            Item,
            related_name='coll_coll_join',
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    order_min = models.IntegerField(
            default=0,
            help_text="Use to require minium order quantity.")
    order_max = models.IntegerField(
            default=0,
            help_text="Use to limit order quantity.")
    discount = models.IntegerField(
            default=0,
            help_text="Discount (5.0%) for purchase in collection.")

    def __str__(self):
        if self.included_products:
            return f"{self.included_products.name}"
        else:
            return "----"


class ItemVariationJoin(models.Model):
    item = models.ForeignKey(
            Item,
            related_name='item_var_join',
            null=True,
            on_delete=models.CASCADE)
    variation = models.OneToOneField(
            Item,
            related_name='var_var_join',
            null=True,
            on_delete=models.CASCADE)
    attribute = models.OneToOneField(
            Attribute,
            related_name='attr_var_join',
            null=True,
            on_delete=models.CASCADE)
    term = models.ForeignKey(
            Attribute,
            related_name='term_var_join',
            null=True,
            on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product}"


class Bid(models.Model):
    item = models.ForeignKey(
            Item,
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
    unit = models.ForeignKey(
            Unit,
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    is_winning_bid = models.BooleanField(default=False)

    def save(self, **kwargs):
        super().save(**kwargs)
        item = self.item
        item.save()

    def __str__(self):
        if self.item:
            return "{} {}".format(self.supplier, self.item)


class Digital(models.Model):
    item = models.OneToOneField(
            Item,
            null=True,
            on_delete=models.CASCADE)
    new_int_field = models.BigIntegerField(null=True, blank=True)
    new_char_tield = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return '{}'.format(self.item.name)


class Identifier(models.Model):
    item = models.OneToOneField(
            Item,
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
            null=True,
            on_delete=models.CASCADE,)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    def __str__(self):
        return '{}'.format(self.item.name)


class Promotion(models.Model):
    item = models.ManyToManyField(
            Item,
            blank=True)
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=50)
    begins = models.DateField(null=True)
    ends = models.DateField(null=True)
    percentage = models.BigIntegerField(
            blank=True,
            null=True,
            help_text="Percentage discount eg. 25% off")
    fixed = models.BigIntegerField(
            blank=True,
            null=True,
            help_text="Fixed discount eg. $5.00 off")
    price = models.BigIntegerField(
            blank=True,
            null=True,
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


class Image(configapp.models.ImageABC):
    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='item_user_images',
            blank=True,
            null=True)
    category = models.OneToOneField(
            Category,
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    tag = models.OneToOneField(
            Tag,
            on_delete=models.CASCADE,
            blank=True,
            null=True)
    item = models.OneToOneField(
            Item,
            blank=True,
            null=True,
            on_delete=models.CASCADE)


class Note(configapp.models.NoteABC):
    item = models.ForeignKey(
            Item,
            blank=True,
            null=True,
            on_delete=models.CASCADE)


class InventoryQuerySet(models.query.QuerySet):
    """
    Can use like this:
    myq = Entry.inventory.products(pid=9)
    myq = Entry.inventory.products(pid=9).with_counts()
    """

    def parts(self, iid=None):
        return self.filter(account='IRAW', item_id=iid)

    def products(self, iid=None):
        return self.filter(account='IMER', item_id=iid).order_by('-date')

    def all_items(self, iid=None):
        return self \
            .filter(item_id=iid) \
            .filter(Q(account='IRAW') | Q(account='IMER')) \
            .order_by('-date')

    def by_location(self, lid=None):
        return self.filter(locations_id=lid)

    def agg_counts(self):
        return self.aggregate(
            dquan=Sum("debit_quantity"),
            cquan=Sum("credit_quantity"),
            damou=Sum("debit_amount"),
            camou=Sum("credit_amount"))

    def with_counts(self):
        return self.annotate(
            dquan=Sum("debit_quantity"),
            cquan=Sum("credit_quantity"),
            damou=Sum("debit_amount"),
            camou=Sum("credit_amount"))


class InventoryManager(models.Manager):
    def get_queryset(self):
        return InventoryQuerySet(self.model, using=self._db)


class Ledger(configapp.models.Timestamps, models.Model):
    location = models.ForeignKey(
        contactapp.models.Location,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item,
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    ACCOUNT_CHOICES = [
        ('APAY', 'Accounts Payable'),
        ('COGM', 'Cost of Goods Manufactured'),
        ('COGS', 'Cost of Goods Sold'),
        ('CASH', 'Cash Account'),
        ('IRAW', 'Inventory Raw Materials'),
        ('IMER', 'Inventory Merchandise'),
        ('ILOS', 'Inventory Loss'),  # expense account for inventory write-off
        ('OWEQ', 'Owner Equity')]

    account = models.CharField(
        choices=ACCOUNT_CHOICES,
        max_length=4)
    date = models.DateField(default=datetime.date.today)
    lot = models.DateTimeField(default=timezone.now)
    debit_quantity = models.BigIntegerField(blank=True, null=True)
    debit_amount = models.BigIntegerField(blank=True, null=True)
    credit_quantity = models.BigIntegerField(blank=True, null=True)
    credit_amount = models.BigIntegerField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True)

    objects = models.Manager()
    inventory = InventoryManager.from_queryset(InventoryQuerySet)()

    @property
    def item_sku(self):
        return self.item.sku if self.item else "---"

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return self.date.isoformat()
