from django.contrib import admin
import ledgerapp.models


@admin.register(ledgerapp.models.Lot)
class LotAdmin(admin.ModelAdmin):
    search_fields = ['identification']


@admin.register(ledgerapp.models.Batch)
class BatchAdmin(admin.ModelAdmin):
    search_fields = ['identification']


@admin.register(ledgerapp.models.Entry)
class LedgerAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'account',
        'part_sku',
        'product_sku',
        'company',
        'store',
        'warehouse',
        'lot',
        'batch',
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
    autocomplete_fields = ['company', 'store', 'warehouse', 'lot', 'batch']

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

