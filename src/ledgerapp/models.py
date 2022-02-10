from django.db import models
from configapp.models import Timestamps
from contactapp.models import Location
from itemsapp.models import Part, Product
import datetime
from django.db.models import Sum
from django.db.models import Prefetch
from django.db.models.functions import Coalesce
from django.db.models import IntegerField
from django.urls import resolve



class Lot(Timestamps, models.Model):
    number = models.CharField(
        max_length=100,
        blank=True,)
    created = models.DateField(default=datetime.date.today)
    expires = models.DateField(
        blank=True, null=True)
    description = models.CharField(
        max_length=200,
        blank=True,)

    def __str__(self):
        return "{}".format(self.number)

class Batch(Timestamps, models.Model):
    number = models.CharField(
        max_length=100,
        blank=True,)
    created = models.DateField(default=datetime.date.today)
    expires = models.DateField(
        blank=True, null=True)
    description = models.CharField(
        max_length=200,
        blank=True,)

    def __str__(self):
        return "{}".format(self.number)

class InventoryQuerySet(models.query.QuerySet):
    """
    Can use like this:
    myq = Entry.inventory.products(pid=9)
    myq = Entry.inventory.products(pid=9).with_counts()
    """
    def parts(self, pid=None):
        return self.filter(account='IRAW', parts_id=pid)

    def products(self, pid=None):
        return self.filter(account='IMER', products_id=pid).order_by('-date')

    def by_location(self, lid=None):
        return self.filter(locations_id=lid)

    def with_counts(self):
        return self.aggregate(
            Sum("debit_quantity"),
            Sum("credit_quantity"),
            Sum("debit_amount"),
            Sum("credit_amount"))

    def with_batch_agg(self):
        return self.values(
            'batches__created_date', 'locations', 'lots', 'batches'
        ).order_by(
            '-batches__created_date'
        ).annotate(
            d_quantity=Sum('debit_quantity'),
            d_amount=Sum('debit_amount'),
            c_quantity=Sum('credit_quantity'),
            c_amount=Sum('credit_amount'),
        ).exclude(d_quantity=0)

class InventoryManager(models.Manager):
    def get_queryset(self):
        return InventoryQuerySet(self.model, using=self._db)

class Entry(Timestamps, models.Model):
    lots = models.ForeignKey(
        Lot,
        related_name='le_lots',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    batches = models.ForeignKey(
        Batch,
        related_name='le_batches',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    locations = models.ForeignKey(
        Location,
        related_name='le_locations',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    parts = models.ForeignKey(
        Part,
        related_name='le_parts',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    products = models.ForeignKey(
        Product,
        related_name='le_products',
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

    account=models.CharField(
        choices = ACCOUNT_CHOICES,
        max_length = 4)
    date = models.DateField(default=datetime.date.today)
    debit_quantity = models.DecimalField(
        decimal_places=2, max_digits=11, blank=True, null=True)
    debit_amount = models.DecimalField(
        decimal_places=2, max_digits=11, blank=True, null=True)
    credit_quantity = models.DecimalField(
        decimal_places=2, max_digits=11, blank=True, null=True)
    credit_amount = models.DecimalField(
        decimal_places=2, max_digits=11, blank=True, null=True)
    note=models.CharField(
        max_length = 200,
        blank=True)


    objects = models.Manager() # The default manager.
    inventory = InventoryManager.from_queryset(InventoryQuerySet)() # The Inventory-specific manager.

    def part_sku(self):
        return self.parts.sku if self.parts else "---"

    def product_sku(self):
        return self.products.sku if self.products else "---"

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return self.date.strftime("%Y %m %d")

