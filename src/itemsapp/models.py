from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor.fields import RichTextField
from configapp.models import Price
from django.db.models import Sum
from django.db.models import Prefetch
import math
from sodavault.utils_logging import svlog_info


class Group(models.Model):

    CAT_TYPE_CHOICES = [
        ('CAT', 'Category'),
        ('TAG', 'Tag'),
        ('DEP', 'Department'),
    ]
    cat_type = models.CharField(
        max_length=3,
        blank=True,
        choices=CAT_TYPE_CHOICES,
    )

    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return '{}'.format(self.name)


class DepartmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(cat_type='DEP')


class Department(Group):
    objects = DepartmentManager()

    class Meta:
        proxy = True
        verbose_name_plural = "04. Departments"

    def save(self, *args, **kwargs):
        if self.cat_type == '':
            self.cat_type = 'DEP'
        super(Department, self).save(*args, **kwargs)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(cat_type='CAT')


class Category(Group):
    objects = CategoryManager()

    class Meta:
        proxy = True
        verbose_name_plural = "05. Categories"

    def save(self, *args, **kwargs):
        if self.cat_type == '':
            self.cat_type = 'CAT'
        super(Category, self).save(*args, **kwargs)


class TagManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(cat_type='TAG')


class Tag(Group):
    objects = TagManager()

    class Meta:
        proxy = True
        verbose_name_plural = "06. Tags"

    def save(self, *args, **kwargs):
        if self.cat_type == '':
            self.cat_type = 'TAG'
        super(Tag, self).save(*args, **kwargs)


class PartManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(item_type='PART')


class AllProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(item_type='PROD')


class SimpleProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(item_type="PROD", product_type="SIMP")


class DigitalProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(item_type="PROD", product_type="DIGI")


class BundleProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(item_type="PROD", product_type="BUND")


class VariableProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(item_type="PROD", product_type="VARI")


class Item(models.Model):
    price_class = models.ForeignKey(
        Price,
        related_name='price_items',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    departments = models.ManyToManyField(
        Department,
        related_name='department_items',
        blank=True)
    categories = models.ManyToManyField(
        Category,
        related_name='category_items',
        blank=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='tag_item',
        blank=True)
    ITEM_TYPE_CHOICES = [
        ('PART', 'Part'),
        ('PROD', 'Product'),
    ]
    item_type = models.CharField(
        max_length=4,
        blank=True,
        choices=ITEM_TYPE_CHOICES,
    )
    PRODUCT_TYPE_CHOICES = [
        ('SIMP', 'Simple'),
        ('DIGI', 'Digital'),
        ('BUND', 'Bundled'),
        ('VARI', 'Variable'),
    ]
    product_type = models.CharField(
        max_length=4,
        blank=True,
        choices=PRODUCT_TYPE_CHOICES,
    )
    sku = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(
        blank=True,
        help_text="For internal and purchasing use.")
    ecpu = models.DecimalField(
        max_digits=14, decimal_places=4, blank=True, null=True)
    ecpu_override = models.DecimalField(
        max_digits=14, decimal_places=4, blank=True, null=True)
    ecpu_calc_from = models.CharField(
            max_length=100,
            blank=True,
            help_text="how ecpu has been calculated")
    unit = models.CharField(
            max_length=100,
            blank=True,
            help_text="singlular unit")
    unit_override = models.CharField(
            max_length=100,
            blank=True,
            help_text="singlular unit")
    price = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True)
    price_override = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True)
    price_calc_from = models.CharField(
            max_length=100,
            blank=True,
            help_text="how price has been calculated")

    objects = models.Manager()
    parts = PartManager()
    all_products = AllProductManager()
    simple_products = SimpleProductManager()
    digital_products = DigitalProductManager()
    bundle_products = BundleProductManager()
    variable_products = VariableProductManager()

    def __str__(self):
        return "{} {}".format(self.sku, self.name)

    @property
    def is_digital(self):
        # raising an exception is the default behavior for one-to-one relationships
        try:
            self.digital_options
            return True
        except Exception as e:
            svlog_info(f"Digital options doe not exist: {e}")
            return False

    @property
    def is_bundle(self):
        return True if self.bundle_parents.exists() else False 

    @property
    def is_variable(self):
        return True if self.variation_parents.exists() else False 

    @property
    def inv_stats(self):

        _le_q = None
        if self.item_type == 'PART':
            _le_q = self.le_parts.filter(account='IRAW').aggregate(
                    Sum('debit_amount'),
                Sum('credit_amount'),
                Sum('debit_quantity'),
                Sum('credit_quantity'))

        if self.item_type == 'PROD':
            _le_q = self.le_products.filter(account='IMER').aggregate(
                Sum('debit_amount'),
                Sum('credit_amount'),
                Sum('debit_quantity'),
                Sum('credit_quantity'))

        """
        'debit_amount__sum': Decimal('3363.66'),
        'credit_amount__sum': None,
        'debit_quantity__sum': Decimal('10000.00'),
        'credit_quantity__sum': None
        """

        def check_for_zero(self, myvariable):
            return 0 if myvariable is None else myvariable

        _d_amount = 0
        _c_amount = 0
        _d_quantity = 0
        _c_quantity = 0

        if _le_q:
            _d_amount = check_for_zero(self, _le_q['debit_amount__sum'])
            _c_amount = check_for_zero(self, _le_q['credit_amount__sum'])
            _d_quantity = check_for_zero(self, _le_q['debit_quantity__sum'])
            _c_quantity = check_for_zero(self, _le_q['credit_quantity__sum'])

        _cost = _d_amount - _c_amount
        _quantity = _d_quantity - _c_quantity
        _avg_cpu = _cost / _quantity if _quantity > 0 else 0

        inv_stats_dict = {}

        if _quantity == 0:
            _cost = 0
            _quantity = 0
            _avg_cpu = 0

        else:
            inv_stats_dict['cost'] = _cost
            inv_stats_dict['quantity'] = _quantity
            inv_stats_dict['avg_cpu'] = _avg_cpu

        # print("inv_stats_dict", inv_stats_dict)
        return inv_stats_dict
        # inv_stats['cost'], inv_stats['quantity'], inv_stats['avg_cpu']

    @property
    def available_inventory(self):
        inv_stats = self.inv_stats
        # print("here inv_stas", inv_stats)
        if inv_stats:
            return "{} units available. {} total cost. {} avg cpu".format(
                int(inv_stats['quantity']),
                round(inv_stats['cost'], 2),
                round(inv_stats['avg_cpu'], 4)
            )
        else:
            return "No available inventory"

    @property
    def calc_max_new_inventory(self):

        # checks there is ecpu assigned to part
        if self.ecpu == 0:
            return """Before you can create new inventory, you must assign a cost. 
                You can assign costs by creating winning bids, assembling products
                from parts, or by entering an estimated cost override (ecpu override).
                """

        # for products assembed from parts, may be limited by parts inventory
        _pid = None
        _ppj_q = None
        _part_inv = []
        _part_dict = {}
        # query is_unlimted = False,
        # because an unlimited Part does not limit the creation of a Product
        if self.item_type == "PROD":
            _pid = self.id
            print("self.id, self.name", self.id, self.name)
            _ppj_q = ProductPartJoin.objects.filter(
                products_id=_pid, 
                is_unlimited=False
            ).prefetch_related(
                Prefetch('parts'))
        if _ppj_q:
            for ppj in _ppj_q:
                _part_dict = {}
                if ppj.parts.inv_stats:
                    _part_dict['id'] = ppj.parts.id
                    _part_dict['name'] = ppj.parts.name
                    _part_dict['total_quantity'] = math.floor(
                            ppj.parts.inv_stats['quantity'])
                    _part_dict['max_quantity'] = math.floor(
                            ppj.parts.inv_stats['quantity'] / ppj.quantity)
                else:
                    _part_dict['id'] = ppj.parts.id
                    _part_dict['name'] = ppj.parts.name
                    _part_dict['total_quantity'] = 0
                    _part_dict['max_quantity'] = 0 

                _part_inv.append(_part_dict)

            def by_max_quantity(p_list):
                return p_list['max_quantity']

            _part_inv.sort(key=by_max_quantity)

            print("_part_inv", _part_inv)

            # change the return to include meaningful information
            if len(_part_inv) > 0:
                _part_inv[0]['is_limited'] = True
                return """This product is assembled from parts. You can bring a maximum 
                    number of {} new pcs into inventory. New inventory is currently 
                    limted by {} which currently has {} pcs in stock.
                    """.format(
                        _part_inv[0]['max_quantity'],
                        _part_inv[0]['name'],
                        _part_inv[0]['total_quantity']
                    ), _part_inv[0]
            else:
                _part_inv.append(_part_dict)
                _part_inv[0]['is_limited'] = False
                _part_inv[0]['max_quantity'] = None
                return """This product is assembled from parts, however,
                    it is not limited by the inventory of those parts.""", _part_inv[0]

        # may create unlimited inventory
        else:
            _part_inv.append(_part_dict)
            _part_inv[0]['is_limited'] = False
            _part_inv[0]['max_quantity'] = None
            return "You may create unlimited new inventory for this item.", _part_inv[0]

    @property
    def max_new_inventory(self):
        return self.calc_max_new_inventory[0]

    @property
    def calc_ecpu(self):
        _ecpu = 0
        _unit = ""
        _designator = ""

        # check for estimated costs based on winning_bid
        _items_q = None
        _w_bid = None

        if self.item_type == 'PART':
            # print("made it to first PART")
            # query part winning_bid
            _w_bid = self.bid_parts.filter(is_winning_bid=True).first()

        if self.item_type == 'PROD':
            # print("made it to first PROD")
            # query product winning_bid
            _w_bid = self.bid_products.filter(is_winning_bid=True).first()

        # check for ecpu based on winning bid
        if _w_bid:
            # print("_w_bid", _w_bid)
            _cost = 0; _shipping = 0; _quantity = 0; _unit = ""
            _cost = _w_bid.cost if _w_bid.cost is not None else 0
            _shipping = _w_bid.shipping if _w_bid.shipping is not None else 0
            _quantity = _w_bid.quantity
            _unit = _w_bid.units
            _unit = _unit.rstrip('s') # rstrip only from the end of string
            _ecpu = (_cost + _shipping) / _quantity if _quantity > 0 else 0
            _designator = "ecpu based on winning bid"


        # check for ecpu based on assembled parts (for product)
        _items_q = None
        if self.item_type == 'PROD':
            _items_q = self.ppj_products.all().prefetch_related('parts')

        if _items_q:
            _total_ecpu = 0
            for it in _items_q:
                _quantity = it.quantity if it.quantity is not None else 0
                _ecpu = it.parts.ecpu if it.parts.ecpu is not None else 0
                _total_ecpu = _total_ecpu + (_quantity * _ecpu)

            _ecpu = round(_total_ecpu, 4)
            _unit = "pc"
            _designator = "ecpu based on assembled parts"

        # check ecpu based on overrides
        _ecpu = self.ecpu_override if self.ecpu_override is not None else _ecpu
        _unit = self.unit_override if self.unit_override != "" else _unit
        if self.ecpu_override:
            _designator = "ecpu based on override"

        calc_ecpu = {}
        calc_ecpu['ecpu'] = _ecpu
        calc_ecpu['unit'] = _unit
        calc_ecpu['designator'] = _designator

        print("calc_ecpu", calc_ecpu)

        return calc_ecpu

    @property
    def calc_price(self):
        """
        price can be calculated 
        from estimated cost
        from avg cost of inventory 
        from ecpu override
        """
        # find amount, and assign designator
        _cost = 0 
        _designator = ""
        _price = 0

        # find cost
        # based on cost override
        # print("### self.inv_stats -->", self.inv_stats)
        if self.ecpu_override is not None:
            _cost = self.ecpu_override
            _designator = "ecpu override"

        # based on existing inventory
        elif self.inv_stats:
            _cost = self.inv_stats['avg_cpu']
            _designator = "avg cpu of available inventory"

        # based on estimated cost per unit
        elif self.ecpu is not None:
            _cost = self.ecpu
            _designator = "estimated cost per unit (ecpu)"

        else:
            _cost = 0
            _designator = "not able to calculate a cost per unit"
            pass

        # calcualte price based on cost
        if self.price_class is not None:
            if self.price_class.is_flat is True:
                _price = _cost + self.price_class.amount
            elif self.price_class.is_markup is True:
                _price = _cost + (_cost * (self.price_class.amount / 100))
            elif self.price_class.is_margin is True:
                _price = _cost / (1 - (self.price_class.amount / 100))
        else:
            _price = 0
            _designator = "please assign a price class"

        if self.price_override is not None:
            _price = self.price_override
            _designator = "price override"

        calc_price = {}
        calc_price['cost'] = _cost
        calc_price['price'] = _price
        calc_price['designator'] = _designator

        return calc_price

    def save(self, *args, **kwargs):
        _calc_ecpu = self.calc_ecpu
        self.ecpu = _calc_ecpu['ecpu']
        self.unit = _calc_ecpu['unit']
        self.ecpu_calc_from = _calc_ecpu['designator']
        _calc_price = self.calc_price
        self.price = _calc_price['price']
        self.price_calc_from = _calc_price['designator']
        super(Item, self).save(*args, **kwargs)


class Part(Item):
    objects = PartManager()

    class Meta:
        proxy = True
        verbose_name_plural = "01. Parts"

    def save(self, *args, **kwargs):
        self.item_type="PART"
        super(Part, self).save(*args, **kwargs)


class Product(Item):
    objects = AllProductManager()

    class Meta:
        proxy = True
        verbose_name_plural = "02a. All Products"

    def save(self, *args, **kwargs):
        self.item_type = "PROD"
        super(Product, self).save(*args, **kwargs)


class SimpleProduct(Item):
    objects = SimpleProductManager()

    class Meta:
        proxy = True
        verbose_name_plural = "02b. Simple Products"

    def save(self, *args, **kwargs):
        self.item_type = "PROD"
        if self.product_type == "":
            self.product_type = "SIMP"
        super(Product, self).save(*args, **kwargs)


class DigitalProduct(Item):
    objects = DigitalProductManager()

    class Meta:
        proxy = True
        verbose_name_plural = "02c. Digital Products"

    def save(self, *args, **kwargs):
        self.item_type = "PROD"
        if self.product_type == "":
            self.product_type = "DIGI"
        super(Product, self).save(*args, **kwargs)


class BundleProduct(Item):
    objects = BundleProductManager()

    class Meta:
        proxy = True
        verbose_name_plural = "02d. Bundle Products"

    def save(self, *args, **kwargs):
        self.item_type = "PROD"
        if self.product_type == "":
            self.product_type = "BUND"
        super(Product, self).save(*args, **kwargs)


class VariableProduct(Item):
    objects = VariableProductManager()

    class Meta:
        proxy = True
        verbose_name_plural = "02e. Varialbe Products"

    def save(self, *args, **kwargs):
        self.item_type = "PROD"
        if self.product_type == "":
            self.product_type = "VARI"
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


class Attribute(models.Model):
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = "03. Attributes"

    def __str__(self):
        return '{}'.format(self.name)


class Term(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        related_name='terms',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=50)
    img = ProcessedImageField(
        upload_to='product_images/%Y/%m/%d',
        # processors=[ResizeToFill(1000, 1000)],
        format='WebP',
        options={'quality': 80},
        blank=True,
        null=True,
        help_text="converts image to .WebP")

    def __str__(self):
        return '{}'.format(self.name)


class ProductAttributeJoin(models.Model):
    """Used for product attributes."""
    items = models.ForeignKey(
        Item,
        related_name='product_att_join',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    attribute = models.ForeignKey(
        Attribute,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    # ManyToMany for product-attributes
    term = models.ManyToManyField(
        Term,
        blank=True)

    def __str__(self):
        return '{}'.format(self.attribute.name)


class Variation(models.Model):
    parent = models.ForeignKey(
        Item,
        related_name='variation_parents',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    items = models.ForeignKey(
        Item,
        related_name='variation_products',
        null=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return '{} : {}'.format(self.parent.sku, self.parent.name)


class VariationAttribute(models.Model):
    items = models.ForeignKey(
        Item,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    variations = models.ForeignKey(
        Variation,
        related_name='variation_attributes',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    attributes = models.ForeignKey(
        Attribute,
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    terms = models.ForeignKey(
        Term,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.variations.product.sku)


class Bundle(models.Model):
    parent = models.ForeignKey(
        Item,
        related_name='bundle_parents',
        on_delete=models.CASCADE)
    items = models.ForeignKey(
        Item,
        related_name='bundle_products',
        null=True,
        on_delete=models.CASCADE)
    quantity_min = models.PositiveSmallIntegerField(default=1)
    quantity_max = models.PositiveSmallIntegerField(blank=True, null=True)
    is_optional = models.BooleanField(default=False)

    def __str__(self):
        return '{} : {}'.format(self.parent.sku, self.parent.name)


class DigitalOption(models.Model):
    item = models.OneToOneField(
        Item,
        related_name='digital_options',
        null=True,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    # other things like a download key, file, expiration date etc ...

    def __str__(self):
        return '{}'.format(self.item.name)


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
    simple_products = models.ForeignKey(
            SimpleProduct,
            related_name="ppj_simple_products",
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    digital_products = models.ForeignKey(
            DigitalProduct,
            related_name="ppj_digital_products",
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    bundle_products = models.ForeignKey(
            BundleProduct,
            related_name="ppj_bundle_products",
            blank=True,
            null=True,
            on_delete=models.CASCADE)
    variable_products = models.ForeignKey(
            VariableProduct,
            related_name="ppj_variable_products",
            blank=True,
            null=True,
            on_delete=models.CASCADE)
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
