from django.utils import timezone

"""
    ACCOUNT_CHOICES = [
        ('APAY', 'Accounts Payable'),
        ('COGS', 'Cost of Goods Sold'),
        ('CASH', 'Cash Account'),
        ('IRAW', 'Inventory Raw Materials'),
        ('IFIN', 'Inventory Finished Goods'),
        ('ILOS', 'Inventory Loss'),  # expense account for inventory write-off
        ('OWEQ', 'Owner Equity')]

puchase inventory (compon, parts, prods): INVN, 100 APAY
manufact: INVN, INVN
asn: IPROD, IPAR
handling a sale
https://www.accountingtools.com/articles/sales-journal-entry.html
sale: COGS, IPROD

"""


class JournalEntry:
    """Makes the journal entry."""

    def __init__(self, trans: object):
        item = self.trans.item
        lot = self.trans.lot
        quantity = self.trans.quantity
        amount = self.trans.amount
        note = self.trans.note


    def asn(self):
        debit = D(
                # must put in all values #
                )
        credit = C(
                # must put in all values #
                )
        journal_entry(debit=debit, credit=credit)

        return

    def transfer(self):
        return

    def order(self):
        return

    def return_wo_inventory(self):
        return

    def return_w_inventory(self):
        return
