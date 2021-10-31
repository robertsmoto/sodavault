from .models import Ledger

"""
function to retrieve part and product information from ledgerapp
"""
def get_ledger_stats(prodid=None, partid=None):
    l_entries = Ledger.objects.filter(product=prodid, part=partid)
    print("l_entries", l_entries)
    return l_entries

