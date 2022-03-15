from django.contrib import admin
from django import forms
import copy
from django.db.models import Prefetch, Sum, F
import itemsapp.models
import transactionsapp.models
from django.utils import timezone
import datetime


class AsnDetailsInline(admin.TabularInline):
    model = transactionsapp.models.AsnDetails
    fields = [
            'item',
            'ecpu_display',
            'quantity_shipped',
            'quantity_received',
            'quantity_descrepancy',
            'remark'
            ]
    readonly_fields = ['quantity_descrepancy', 'ecpu_display']
    extra = 0
    verbose_name = "Detail"
    verbose_name_plural = "Details"

#  date: str = datetime.date.today, lot: str = timezone.now


def record_ledger_entry(
        dloc: int, cloc: int, item: int,
        qnty: int, amnt: int, dact: str, cact: str, note: str,
        ) -> None:

    dentry = itemsapp.models.Ledger()
    dentry.location = dloc
    dentry.item = item
    dentry.account = dact
    dentry.debit_quantity = qnty
    dentry.debit_amount = amnt
    dentry.note = note
    dentry.save()

    centry = itemsapp.models.Ledger()
    centry.location = cloc
    centry.item = item
    centry.account = cact
    centry.credit_quantity = qnty
    centry.credit_amount = amnt
    centry.note = note
    centry.save()

    return


class ASNForm(forms.ModelForm):

    class Meta:
        model = transactionsapp.models.ASN
        fields = '__all__'

    def clean_is_complete(self):
        # # can't uncheck bool
        is_complete = self.cleaned_data.get('is_complete', '')
        # if 'is_complete' in self.changed_data and not is_complete:
            # raise forms.ValidationError(
                # "You may not uncheck this after it has been checked complete."
                # )

        # # can't change form once bool is checked
        # any_changed = copy.copy(self.changed_data)
        # if 'is_complete' in any_changed:
            # any_changed.remove('is_complete')

        # if any_changed and is_complete:
            # raise forms.ValidationError(
                # "You may not change this form after it has been checked "
                # "complete"
        #         )
        return is_complete

    def save(self, commit):
        # when bool is checked first time then make journal entry
        is_complete = self.cleaned_data.get('is_complete', '')
        if 'is_complete' in self.changed_data and is_complete:
            print("now do this")

        # assigns proportionate asn costs to each item in the detail
        # cost is assigned only to qnty_received
        details_q = transactionsapp.models.AsnDetails.objects \
            .filter(asn__id=self.instance.id) \
            .select_related('asn') \
            .annotate(dt_tot=(F('quantity_received') * F('item__ecpu'))) \

        agg = details_q.aggregate(agg_tot=Sum('dt_tot'))

        for dt in details_q:
            asn_costs = dt.asn.shipping_cost + dt.asn.other_cost
            # cacls proportionate cost per unit (pcu)
            pcu = asn_costs * (
                    (dt.dt_tot / agg['agg_tot']) / dt.quantity_received)

            cpu = dt.item.ecpu + pcu
            dact = "IRAW"
            if dt.item.__class__.__name__ == "Product":
                dact = "IMER"
            cact = "APAY"

            # note amount based on qnty_shipped, qnty on qnty_received
            # assumes paid for what was shipped
            record_ledger_entry(
                    dloc=dt.asn.receiver,
                    cloc=dt.asn.sender,
                    item=dt.item,
                    qnty=dt.quantity_received,
                    amnt=cpu*dt.quantity_shipped,
                    dact=dact,
                    cact=cact,
                    note="ASN auto-generated",
                    )

        return super().save(commit)


@admin.register(transactionsapp.models.ASN)
class ASNAdmin(admin.ModelAdmin):
    form = ASNForm
    fields = [
            'is_complete',
            'number',
            'date',
            ('sender', 'receiver'),
            'shipping_cost',
            'other_cost',
            ('est_shipping_date', 'act_shipping_date'),
            ('est_receiving_date', 'act_receiving_date')
            ]
    autocomplete_fields = ['sender', 'receiver']
    inlines = [AsnDetailsInline]


@admin.register(transactionsapp.models.Transfer)
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

#     inlines = [
        # TransactionDetailsInline,
        # # NoteInline,
#     ]
