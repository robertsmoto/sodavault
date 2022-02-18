from django.contrib import admin
from transactionsapp.models import Transaction, TransactionDetails
from transactionsapp.models import ASN, Transfer


class TransactionDetailsInline(admin.TabularInline):
    model = TransactionDetails
    fields = [
        ('parts', 'products'),
        'quantity_shipped',
        'quantity_received',
        'calc_cpu',
    ]
    readonly_fields = [
        'calc_cpu',
    ]
    extra = 0
    verbose_name = "Transaction Detail"
    verbose_name_plural = "details"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = [
        'is_complete',
        'transaction_number',
        'ship_from_location',
        'ship_from_supplier',
        'ship_to_location',
        'shipping',
        ('est_shipping_date', 'act_shipping_date'),
        ('est_receiving_date', 'act_receiving_date'),
    ]

    inlines = [
        TransactionDetailsInline,
    ]


class TransactionDetailsInline(admin.TabularInline):
    model = TransactionDetails
    fields = [
        ('parts', 'products'),
        'quantity_shipped',
        'quantity_received',
        'calc_cpu',
    ]
    readonly_fields = [
        'calc_cpu',
    ]
    extra = 0
    verbose_name = "ASN Detail"
    verbose_name_plural = "details"


@admin.register(ASN)
class ASNAdmin(admin.ModelAdmin):
    fields = [
        'is_complete',
        'transaction_number',
        'ship_to_location',
        'shipping',
        ('est_shipping_date', 'act_shipping_date'),
        ('est_receiving_date', 'act_receiving_date'),
    ]

    list_filter = [
        'is_complete',
    ]

    inlines = [
        TransactionDetailsInline,
        # NoteInline,
    ]


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    fields = [
        'is_complete',
        'transaction_number',
        'ship_from_location',
        'ship_to_location',
        'shipping',
        ('est_shipping_date', 'act_shipping_date'),
        ('est_receiving_date', 'act_receiving_date'),
    ]

    inlines = [
        TransactionDetailsInline,
        # NoteInline,
    ]
