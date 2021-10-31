from django.contrib import admin
from .models import Entry, Lot, Batch


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    pass

@admin.register(Batch)
class LotAdmin(admin.ModelAdmin):
    pass


@admin.register(Entry)
class LedgerAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'account',
        'part_sku',
        'product_sku',
        'locations',
        'lots',
        'batches',
        'debit_quantity',
        'debit_amount',
        'credit_quantity',
        'credit_amount',
        'note',
    ]
    readonly_fields = [
        'part_sku',
        'product_sku',
    ]
    pass

# class LedgerInline(admin.TabularInline):
    # model = Ledger
    # extra = 0
    # verbose_name = "entry"
    # verbose_name_plural = "entries"
    # fields = [
        # 'account',
        # 'date',
        # 'debit_quantity',
        # 'debit_total',
        # 'credit_quantity',
        # 'credit_total',
    # ]


# @admin.register(LedgerJoin)
# class TransactionJoinAdmin(admin.ModelAdmin):
# #     readonly_fields = [
        # # '_available_inventory',
        # # '_cost_of_inventory',
        # # '_cpu',
        # # ]
    # inlines = [
        # LedgerInline,]

