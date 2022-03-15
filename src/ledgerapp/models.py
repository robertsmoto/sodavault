# from django.db import models
# from django.db.models import Sum
# from django.utils import timezone
# import configapp.models
# import contactapp.models
# import datetime
# # import itemsapp.models


# class InventoryQuerySet(models.query.QuerySet):
    # """
    # Can use like this:
    # myq = Entry.inventory.products(pid=9)
    # myq = Entry.inventory.products(pid=9).with_counts()
    # """

    # def parts(self, pid=None):
        # return self.filter(account='IRAW', parts_id=pid)

    # def products(self, pid=None):
        # return self.filter(account='IMER', products_id=pid).order_by('-date')

    # def by_location(self, lid=None):
        # return self.filter(locations_id=lid)

    # def with_counts(self):
        # return self.aggregate(
            # Sum("debit_quantity"),
            # Sum("credit_quantity"),
            # Sum("debit_amount"),
            # Sum("credit_amount"))


# class InventoryManager(models.Manager):
    # def get_queryset(self):
        # return InventoryQuerySet(self.model, using=self._db)


# class Entry(configapp.models.Timestamps, models.Model):
    # location = models.ForeignKey(
        # contactapp.models.Location,
        # related_name="le_location",
        # blank=True,
        # null=True,
        # on_delete=models.CASCADE)
# #     item = models.ForeignKey(
        # # itemsapp.models.Item,
        # # related_name='le_item',
        # # blank=True,
        # # null=True,
        # # on_delete=models.CASCADE)

    # ACCOUNT_CHOICES = [
        # ('APAY', 'Accounts Payable'),
        # ('COGM', 'Cost of Goods Manufactured'),
        # ('COGS', 'Cost of Goods Sold'),
        # ('CASH', 'Cash Account'),
        # ('IRAW', 'Inventory Raw Materials'),
        # ('IMER', 'Inventory Merchandise'),
        # ('ILOS', 'Inventory Loss'),  # expense account for inventory write-off
        # ('OWEQ', 'Owner Equity')]

    # account = models.CharField(
        # choices=ACCOUNT_CHOICES,
        # max_length=4)
    # date = models.DateField(default=datetime.date.today)
    # lot = models.DateTimeField(default=timezone.now)
    # debit_quantity = models.BigIntegerField(blank=True, null=True)
    # debit_amount = models.BigIntegerField(blank=True, null=True)
    # credit_quantity = models.BigIntegerField(blank=True, null=True)
    # credit_amount = models.BigIntegerField(blank=True, null=True)
    # note = models.CharField(max_length=200, blank=True)

    # objects = models.Manager()
    # inventory = InventoryManager.from_queryset(InventoryQuerySet)()

    # @property
    # def item_sku(self):
        # return self.item.sku if self.item else "---"

    # class Meta:
        # verbose_name_plural = "entries"

    # def __str__(self):
#         return self.date.isoformat()
