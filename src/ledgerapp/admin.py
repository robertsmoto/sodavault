# from django.contrib import admin
# import ledgerapp.models


# @admin.register(ledgerapp.models.Entry)
# class LedgerAdmin(admin.ModelAdmin):

    # list_display = [
        # 'date',
        # 'account',
        # # 'item_sku',
        # 'location',
        # 'lot',
        # 'debit_quantity',
        # 'debit_amount',
        # 'credit_quantity',
        # 'credit_amount',
        # 'note',
    # ]
    # readonly_fields = ['item_sku']
    # # autocomplete_fields = ['location', 'item']

    # # def item_sku(self, obj):
    # #     return obj.item.sku if obj.item else "hello"

# # # class LedgerInline(admin.TabularInline):
    # # # model = Ledger
    # # # extra = 0
    # # # verbose_name = "entry"
    # # # verbose_name_plural = "entries"
    # # # fields = [
        # # # 'account',
        # # # 'date',
        # # # 'debit_quantity',
        # # # 'debit_total',
        # # # 'credit_quantity',
        # # # 'credit_total',
    # # # ]


# # # @admin.register(LedgerJoin)
# # # class TransactionJoinAdmin(admin.ModelAdmin):
# # # #     readonly_fields = [
        # # # # '_available_inventory',
        # # # # '_cost_of_inventory',
        # # # # '_cpu',
        # # # # ]
    # # # inlines = [
#         # # LedgerInline,]
