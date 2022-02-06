from django.contrib import admin
from transactionsapp.models import Note, Bid
from transactionsapp.models import Transaction, TransactionDetails 
from transactionsapp.models import ASN, Transfer
from ledgerapp.models import Entry
from django.forms import ModelForm
import datetime
from django.contrib import admin
from itemsapp.models import Product  # , Variation
from django.forms.models import ModelForm
from django.db.models.query import Prefetch 


class NoteInline(admin.TabularInline):
    model = Note
    extra = 0
    verbose_name = "note"
    verbose_name_plural = "notes"

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
        NoteInline,
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
        NoteInline,
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
        NoteInline,
    ]

