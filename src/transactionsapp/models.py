from django.db import models
from itemsapp.models import Item, Part # , ProductPartJoin
#  SimpleProduct, BundleProduct, VariableProduct
from itemsapp.models import Product  # , DigitalProduct
from contactapp.models import Company, Supplier, Location
from django.db.models import Sum, Avg
from django.db import models
from contactapp.models import Person
from django.forms import ValidationError
from ledgerapp.models import Entry, Lot, Batch
import datetime
from django.db.models import Prefetch
from decimal import Decimal



def useall_check(self, detail=None, *args, **kwargs):

    _products_shipped = 0
    _parts_per_product = 0
    _parts_needed = 0
    _quantity = 0
    _add_cogm = 0

    if detail.products:
        _products_shipped = detail.quantity_shipped
        ppj_q = detail.products.ppj_products.all().prefetch_related(
            Prefetch("parts"))
        for ppj in ppj_q:
            if ppj.use_all:
                _parts_per_product = ppj.quantity
                _parts_needed = _products_shipped * _parts_per_product
                # query ledger sum debit_quantity and credit quantity
                # then _remaining_parts = d_qnty - c_qnty
                """ use a function here """
                le_q = Entry.objects.filter(parts=ppj.parts, account='IRAW')
                # and reused here
                agg_stats = le_q.aggregate(
                    Sum('debit_amount'),
                    Sum('credit_amount'),
                    Sum('debit_quantity'),
                    Sum('credit_quantity')
                )

                def check_for_zero(self, myvariable):
                    return myvariable if myvariable is not None else 0

                _d_amount = check_for_zero(self, agg_stats['debit_amount__sum'])
                _c_amount = check_for_zero(self, agg_stats['credit_amount__sum'])
                _d_quantity = check_for_zero(self, agg_stats['debit_quantity__sum'])
                _c_quantity = check_for_zero(self, agg_stats['credit_quantity__sum'])

                _cost = _d_amount - _c_amount
                _quantity = _d_quantity - _c_quantity
                _ave_cpu = _cost / _quantity if _quantity > 0 else 0


                _add_cogm = _quantity * _ave_cpu

    return _quantity, _add_cogm

def adj_qnty_descrepancies(self, le_list, today, product, part, lot, batch,
    location, qnty_shipped, qnty_received, shipping_cpu, *args, **kwargs):

    _le_list = le_list
    _today = today
    _product = product
    _part = part
    _lot = lot
    _batch = batch
    _d_lctn = location
    _c_lctn = location
    _qnty_shipped = qnty_shipped
    _qnty_received = qnty_received
    _shipping_cpu = shipping_cpu

    _item = _part if _part else _product
    _ecpu_plus_shipping = _item.ecpu + _shipping_cpu

    _qnty_discrepancy = 0

    if qnty_shipped > qnty_received:
        _qnty_discrepancy = qnty_shipped - qnty_received
        _d_acct = "ILOS"  # ILOS is an expense accnt for inventory write-off
        _d_qnty = _qnty_discrepancy
        _d_amnt = _qnty_discrepancy * _ecpu_plus_shipping
        _c_qnty = _qnty_discrepancy
        _c_amnt = _qnty_discrepancy * _ecpu_plus_shipping

        if _part:
            _c_acct = "IRAW"
            _note = "ASN: {} inventory loss".format(_part.sku)
        else:  # is product
            _c_acct = "IMER"
            _note = "ASN: {} inventory loss".format(_product.sku)

    if qnty_received > qnty_shipped:
        _qnty_discrepancy = qnty_received - qnty_shipped
        _c_acct = "APAY"  # making the assumption that extra parts and products were paid for
        _d_qnty = _qnty_discrepancy
        _d_amnt = _qnty_discrepancy * _ecpu_plus_shipping
        _c_qnty = _qnty_discrepancy
        _c_amnt = _qnty_discrepancy * _ecpu_plus_shipping

        if _part:
            _d_acct = "IRAW"
            _note = "ASN: {} inventory loss".format(_part.sku)
        else:  # is prooduct
            _d_acct = "IMER"
            _note = "ASN: {} inventory loss".format(_product.sku)

    _le_list = append_le_list(
        self, le_list = _le_list, entry_type="debit", date = _today, 
        acct = _d_acct, lctn = _d_lctn, product = _product, 
        part = _part, lot = _lot, batch = _batch, qnty = _d_qnty, 
        amnt = _d_amnt, note = _note, *args, **kwargs)

    _le_list = append_le_list(
        self, le_list = _le_list, entry_type="credit", date = _today, 
        acct = _c_acct, lctn = _c_lctn, 
        product = _product, part = _part, lot = _lot, batch = _batch, 
        qnty = _c_qnty, amnt = _c_amnt, note = _note, 
        *args, **kwargs)

    return _le_list

def append_le_list(self, le_list, entry_type="", date=None, acct="", lctn=None, 
    product=None, part=None, lot=None, batch=None, qnty=0, amnt=0, note="", *args, **kwargs):

    _le_dict = {}
    _le_dict['date'] = date
    _le_dict['acct'] = acct
    _le_dict['product'] = product
    _le_dict['part'] = part
    _le_dict['lot'] = lot
    _le_dict['batch'] = batch
    _le_dict['lctn'] = lctn
    _le_dict['d_qnty'] = qnty if entry_type == "debit" else None
    _le_dict['d_amnt'] = amnt if entry_type == "debit" else None
    _le_dict['c_qnty'] = qnty if entry_type == "credit" else None
    _le_dict['c_amnt'] = amnt if entry_type == "credit" else None
    _le_dict['note'] = note
    le_list.append(_le_dict)

    return le_list

def qnty_by_batch(self, lid=None, part=None, product=None, total_qnty=0, *args, **kwargs):
    """
    Returns a list of dictionaries, prioritizes by batch.
    Filter by location by specifiying lid (location id)
    """
    _total_qnty = total_qnty
    _batch_list = []

    if _total_qnty == 0:
        return _batch_list

    _part = part
    _product = product

    _q_type = "part" if _part else "product"
    
    _lid = lid

    if _q_type == "part":
        if _lid:
            batch_agg_q = Entry.inventory.parts(pid=_part.id).by_location(lid=_lid).with_batch_agg()
        else:
            batch_agg_q = Entry.inventory.parts(pid=_part.id).with_batch_agg()
        # _le_q = Entry.objects.filter(parts__id=_part.id)

    if _q_type == "product":
        if _lid:
            batch_agg_q = Entry.inventory.products(pid=_product.id).by_location(lid=_lid).with_batch_agg()
        else:
            batch_agg_q = Entry.inventory.products(pid=_product.id).with_batch_agg()

    for batch in batch_agg_q:
        _batch_dict = {}
        _b_d_qnty = batch['d_quantity'] if batch['d_quantity'] else 0
        _b_d_amnt = batch['d_amount'] if batch['d_amount'] else 0
        _b_c_qnty = batch['c_quantity'] if batch['c_quantity'] else 0
        _b_c_amnt = batch['c_amount'] if batch['c_amount'] else 0
        _batch_qnty = _b_d_qnty - _b_c_qnty
        _batch_amnt = _b_d_amnt - _b_c_amnt
        _lctn = Location.objects.get(id=batch['locations'])
        _lot = Lot.objects.get(id=batch['lots'])
        _batch = Batch.objects.get(id=batch['batches'])

        if _total_qnty - _batch_qnty >= 0:
            _qnty = _batch_qnty
            _amnt = _batch_amnt

        else:
            _qnty = _total_qnty
            # this calculates the amount based on cpu if not consuming the entire batch
            _amnt = (_batch_amnt / _batch_qnty) * _total_qnty

        # add data to dict and append _le_list
        _batch_dict['part'] = _part
        _batch_dict['product'] = _product
        _batch_dict['lctn'] =  _lctn
        _batch_dict['lot'] =  _lot
        _batch_dict['batch'] =  _batch
        _batch_dict['qnty'] =  _qnty
        _batch_dict['amnt'] =  round(_amnt, 4)

        # only append dict if _qnty is > 0
        if _qnty > 0:
            _batch_list.append(_batch_dict)

        _total_qnty -= _batch_qnty

        if _total_qnty <= 0:
            # print("return _batch_list", _batch_list)
            return _batch_list

def additional_shipping(
    self, 
    le_list=[], 
    qnty_shipped=0, 
    total_pcs_shipped=0, 
    part=None, 
    product=None,
    today = None,
    d_lctn = None,
    c_lctn = None,
    lot = None,
    batch = None,
    ):

    _le_list = le_list
    _qnty_shipped = qnty_shipped
    _total_pcs_shipped = total_pcs_shipped
    _part = part
    _product = product
    _shipping = self.shipping
    _today = today
    _d_lctn = d_lctn
    _c_lctn = c_lctn
    _lot = lot
    _batch = batch

    _proportional_shipping = Decimal(_qnty_shipped / _total_pcs_shipped) if _total_pcs_shipped > 0 else Decimal(0)
    _d_acct = "IMER" if _product else "IRAW"
    _d_qnty = None
    _d_amnt = round(_shipping * _proportional_shipping, 4)
    _c_acct = "APAY"
    _c_qnty = None
    _c_amnt = round(_shipping * _proportional_shipping, 4)
    _note = "ASN: Additional shipping cost."

    _le_list = append_le_list(
        self, le_list = _le_list, entry_type="debit", date = _today, 
        acct = _d_acct, lctn = _d_lctn, product = _product, 
        part = _part, lot = _lot, batch = _batch, qnty = _d_qnty, 
        amnt = _d_amnt, note = _note)

    _le_list = append_le_list(
        self, le_list = _le_list, entry_type="credit", date = _today, 
        acct = _c_acct, lctn = _d_lctn, 
        product = _product, part = _part, lot = _lot, batch = _batch, 
        qnty = _c_qnty, amnt = _c_amnt, note = _note)

    _shipping_cpu = (_shipping * _proportional_shipping) / _qnty_shipped if _qnty_shipped > 0 else 0
    return _le_list, _shipping_cpu


def create_le_list(self, ttype=None, *args, **kwargs):
    # need to consider that this function can be for existing inventory
    # as well as bringing in new inventory

    _ttype = ttype
    _error = 0
    _le_list = []

    _detail_q = self.TransactionDetails.all().prefetch_related(
        Prefetch('parts'),
        Prefetch('products')
    )

    _pcs_shipped_q = _detail_q.aggregate(Sum('quantity_shipped'))
    _total_pcs_shipped = _pcs_shipped_q['quantity_shipped__sum']

    for detail in _detail_q:
        _part = None
        _part_id = None
        _product = None
        _product_id = None
        _sku = ""
        _ecpu = 0
        
        # these are temporary
        _lot = None
        _batch = None

        if detail.parts:
            # _item = detail.parts
            _part = detail.parts
            _part_id = detail.parts.id
            _sku = detail.parts.sku
            _ecpu = detail.parts.ecpu
            # # probleem retrieving lots and batches
            # _lot = detail.parts.le_parts.lots if detail.parts.le_parts.lots else None
            # _batch = detail.parts.le_parts.batches if detail.parts.le_parts.batches else None
            _part.save()  # saving to ensure ecpu is calculated correctly
        else:
            # _item = detail.products
            _product = detail.products
            _product_id = detail.products.id
            _sku = detail.products.sku
            _ecpu = detail.products.ecpu

            # # problem retrieving lot ... check with REPL
            # _lot = detail.products.le_products.lots if detail.products.le_products.lots else None
            # _batch = detail.products.le_products.batches if detail.products.le_products.batches else None
            _product.save()  # saving to ensure ecpu is caluclated correctly

        _today = datetime.datetime.now().strftime("%Y-%m-%d")
        _time = datetime.datetime.now().strftime("%H%M%S")
        _qnty_shipped = detail.quantity_shipped
        _qnty_received = detail.quantity_received
        _ship_from_supplier = self.ship_from_supplier
        _ship_from_location = self.ship_from_location
        _ship_to_location = self.ship_to_location
        _shipping = self.shipping

        _pp_q = None
        if _product:
            _pp_q = _product.ppj_products.all()

        """
        if part and product exists in inventory, then there will already be
        a lot and batch
        """
        if _lot is None:
            _lot, created = Lot.objects.get_or_create(number = "{} {}".format(_today, _sku)) 
                    
        #  everytime a part or product is created it gets a unique batch
        if _batch is None:
            _batch = Batch()
            _batch.save()  # save to get batch.id
            _batch.number = "{} {} {}".format(_today, _time, _sku) 
            _batch.save()

        """
        Different conditions for methods:
        1. Adding New inventory (needs new lot / batch)
        1a. Adding New product inventory with parts (needs new lot / batch, and reduce inventory)
        2. Transferring inventory (needs to transfer from lot, batch)
        3. Reducing inventory (reduce from location and lot / batch)
        """

        if _ttype == "ASN":

            _d_qnty = _qnty_shipped
            _d_amnt = _qnty_shipped * _ecpu
            _d_lctn = _ship_to_location
            _c_qnty = _qnty_shipped
            _c_amnt = _qnty_shipped * _ecpu
            _c_lctn = _ship_to_location

            # bring part into inventory
            if _part:
                _d_acct = "IRAW"; _c_acct = "APAY"
                _note = "ASN: Bring {} into inventory".format(_part.sku)

            # bring product into inventory
            else:
                # if product is assembled from parts credit "COGM" 
                # otherwise credit "APAY"
                _d_acct = "IMER"; _c_acct = "COGM" if _pp_q else "APAY"
                _note = "ASN: Bring {} into inventory".format(_product.sku)
                
            _le_list = append_le_list(
                self, le_list = _le_list, entry_type="debit", date = _today, 
                acct = _d_acct, lctn = _d_lctn, product = _product, 
                part = _part, lot = _lot, batch = _batch, qnty = _d_qnty, 
                amnt = _d_amnt, note = _note, *args, **kwargs)

            _le_list = append_le_list(
                self, le_list = _le_list, entry_type="credit", date = _today, 
                acct = _c_acct, lctn = _c_lctn, 
                product = _product, part = _part, lot = _lot, batch = _batch, 
                qnty = _c_qnty, amnt = _c_amnt, note = _note, *args, **kwargs)
            

        if _ttype == "TRS":
            """
            # the front end should filter the list by location
            # the backend should credit inventory by location/batch
            """

            _d_lctn = _ship_to_location
            _c_lctn = _ship_from_location

            if _part:
                _d_acct = "IRAW"; _c_acct = "IRAW"
                _inv_counts = Entry.inventory.parts(pid=_part_id).by_location(lid=_c_lctn.id).with_counts()
            else:
                _d_acct = "IMER"; _c_acct = "IMER"
                _inv_counts = Entry.inventory.products(pid=_product_id).by_location(lid=_c_lctn.id).with_counts()


            # verify that there are enough parts or products to ship from location
            _d_qnty_sum = _inv_counts['debit_quantity__sum'] if _inv_counts['debit_quantity__sum'] else 0
            _c_qnty_sum = _inv_counts['credit_quantity__sum'] if _inv_counts['credit_quantity__sum'] else 0

            # can't ship more than you have in current inventory
            if _qnty_shipped > (_d_qnty_sum - _c_qnty_sum):
                _error += 1

            # create batch list
            _lid = _ship_from_location.id
            _batch_list = qnty_by_batch(
                self, lid=_lid, part=_part, product=_product, total_qnty=_qnty_shipped, *args, **kwargs)

            # unpack batch list and add journal entries
            # add the ledger entries to _le_list from #1, #2 above
            for batch in _batch_list:

                _part = batch['part'] 
                _product = batch['product']
                _lot = batch['lot']
                _batch = batch['batch']
                _d_qnty = batch['qnty']
                _d_amnt = batch['amnt']
                _c_qnty = batch['qnty']
                _c_amnt = batch['amnt']

                if _part:
                    _note = "TRS: {} from {} to {}".format(
                        _part.sku, _c_lctn.name, _d_lctn.name)
                if _product:
                    _note = "TRS: {} from {} to {}".format(
                        _product.sku, _c_lctn.name, _d_lctn.name)

                _le_list = append_le_list(
                    self, le_list = _le_list, entry_type="debit", date = _today, 
                    acct = _d_acct, lctn = _d_lctn, product = _product, 
                    part = _part, lot = _lot, batch = _batch, qnty = _d_qnty, 
                    amnt = _d_amnt, note = _note, *args, **kwargs)

                _le_list = append_le_list(
                    self, le_list = _le_list, entry_type="credit", date = _today, 
                    acct = _c_acct, lctn = _c_lctn, 
                    product = _product, part = _part, lot = _lot, batch = _batch, 
                    qnty = _c_qnty, amnt = _c_amnt, note = _note, 
                    *args, **kwargs)

        # check for additional shipping costs
        # shipping should be allocated proportionally to each part or product by location, lot and batch
        _shipping_cpu = 0
        if _shipping:
            _le_list, _shipping_cpu = additional_shipping(
                self, 
                le_list=_le_list, 
                qnty_shipped=_qnty_shipped, 
                total_pcs_shipped=_total_pcs_shipped, 
                part=_part, 
                product=_product,
                today=_today,
                d_lctn=_d_lctn,
                c_lctn=_c_lctn,
                lot=_lot,
                batch=_batch)

        print("shipping cpu", _shipping_cpu)
        # check if there was shipping descrepancy
        if _qnty_shipped != _qnty_received:
            _le_list = adj_qnty_descrepancies(
                self, le_list=_le_list, today=_today, product=_product, 
                part=_part, lot=_lot, batch=_batch, location=_ship_to_location, 
                qnty_shipped=_qnty_shipped, qnty_received=_qnty_received,
                shipping_cpu = _shipping_cpu,
                *args, **kwargs)

        # check if product is made from parts, and reduce parts from inventory
        # this only occurs if bringing product into inventory
        if _ttype == "ASN" and _pp_q:

            """
            # check use_all
            # use all should credit all batches and ignore remainder
            _remaining_parts, _add_cogm = useall_check(self, detail, *args, **kwargs)
            """

            # verify there are enough parts inventory to create the product
            _product_max_inv = _product.calc_max_new_inventory[1]['max_quantity']
            
            if _qnty_shipped > _product_max_inv:
                _error += 1

            for pp in _pp_q:
                _pp_qnty = pp.quantity
                _pp_is_unlimited = pp.is_unlimited
                _pp_use_all = pp.use_all
                _pp_part = pp.parts
                _pp_part_ecpu = _pp_part.ecpu
                _item_list = []
                _batch_list = []
                _total_qnty = _pp_qnty * _qnty_shipped

                if _pp_is_unlimited is True:
                    print("im unlimited", _pp_part)
                    """
                    1. is_unlimited = True
                        Part inventory is not tracked. It is purchased as needed.
                        debit "COGM" (amnt only) and credit "APAY" (amnt only).
                        There is no need in this case to reduce inventory by batch.
                    """
                    _d_acct = "COGM"
                    _d_qnty = _total_qnty
                    _d_amnt = (_pp_part_ecpu * _pp_qnty) * _qnty_shipped 
                    _c_acct = "APAY"
                    _c_qnty = _total_qnty
                    _c_amnt = (_pp_part_ecpu * _pp_qnty) * _qnty_shipped

                    print("vars", _pp_is_unlimited, _pp_qnty, _pp_part_ecpu)
                    # add the ledger entries
                    _le_list = append_le_list(
                        self, le_list = _le_list, entry_type="debit", date = _today, 
                        acct = _d_acct, lctn = _d_lctn, product = _product, 
                        part = _pp_part, lot = _lot, batch = _batch, qnty = _d_qnty, 
                        amnt = _d_amnt, note = _note, *args, **kwargs)

                    _le_list = append_le_list(
                        self, le_list = _le_list, entry_type="credit", date = _today, 
                        acct = _c_acct, lctn = _c_lctn, 
                        product = _product, part = _pp_part, lot = _lot, batch = _batch, 
                        qnty = _c_qnty, amnt = _c_amnt, note = _note, 
                        *args, **kwargs)

                elif _pp_use_all is True:
                    print("im use_all", _pp_part)
                    """
                    2. use_all = True
                        Part is in current inventory "IRAW", but must use all
                        of the inventory when creating a product.
                        debit "COGM" (amount only), credit "IRAW" (qnty and amnt)

                    """
                    _d_acct = "COGM"
                    _c_acct = "IRAW"
                    _total_qnty = pp.parts.inv_stats['quantity'] if pp.parts.inv_stats else 0
                    # pass to function

                else:
                    print("im other", _pp_part)
                    """
                    3. is_unlimited = False and use_all is False
                        Part is in current innventory "IRAW"
                        This is a normal condition. And means that there is 
                        current available inventory in "IRAW".
                        debit "COGM" (amnt only), credit "IRAW" (qnty and amnt)
                    """
                    _d_acct = "COGM"
                    _c_acct = "IRAW"
                    # pass to function

                _batch_list = qnty_by_batch(
                    self, lid=None, part=_pp_part, product=None, total_qnty=_total_qnty, *args, **kwargs)

                if _batch_list:
                    # add the ledger entries to _le_list from #1, #2 above
                    for batch in _batch_list:

                        _part = batch['part'] 
                        _product = batch['product']
                        _lctn = batch['lctn']
                        _lot = batch['lot']
                        _batch = batch['batch']
                        _d_qnty = batch['qnty']
                        _d_amnt = batch['amnt']
                        _c_qnty = batch['qnty']
                        _c_amnt = batch['amnt']
                        _note = "ASN: Auto credit by batch"

                        _le_list = append_le_list(
                            self, le_list = _le_list, entry_type="debit", date = _today, 
                            acct = _d_acct, lctn = _lctn, product = _product, 
                            part = _part, lot = _lot, batch = _batch, qnty = _d_qnty, 
                            amnt = _d_amnt, note = _note, *args, **kwargs)

                        _le_list = append_le_list(
                            self, le_list = _le_list, entry_type="credit", date = _today, 
                            acct = _c_acct, lctn = _lctn, 
                            product = _product, part = _part, lot = _lot, batch = _batch, 
                            qnty = _c_qnty, amnt = _c_amnt, note = _note, 
                            *args, **kwargs)

    return _error, _le_list

def record_ledger_entries(self, entry=None, *args, **kwargs):
    _entry = entry
    _product = _entry['product'] if _entry['product'] else None
    _part = _entry['part'] if _entry['part'] else None

    entry = Entry(
        date = _entry['date'],
        account = _entry['acct'],
        products = _entry['product'],
        parts = _entry['part'],
        lots = _entry['lot'],
        batches = _entry['batch'],
        locations = _entry['lctn'],
        debit_quantity = _entry['d_qnty'],
        debit_amount = _entry['d_amnt'],
        credit_quantity = _entry['c_qnty'],
        credit_amount = _entry['c_amnt'],
        note = _entry['note']
    )
    entry.save()

    if _product:
        _product.save()
    if _part:
        _part.save()

    return


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('ASN', 'Advanced Shipping Notice'),
        ('TRS', 'Transfer'),
        ('ADJ', 'Inventory Adjustment'),
        ('ORD', 'Order'),
        ('RET', 'Return'),
    ]
    transaction_type = models.CharField(
        max_length=3,
        blank=True,
        choices=TRANSACTION_TYPE_CHOICES,  
    )
    transaction_number = models.CharField(max_length=100)
    ship_from_supplier = models.ForeignKey(
        Supplier,
        related_name = 'ship_from_supplier',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    ship_from_location = models.ForeignKey(
        Location,
        related_name = 'ship_from_location',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    ship_to_location = models.ForeignKey(
        Location,
        related_name = 'ship_to_location',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    est_shipping_date = models.DateField(
        blank=True,
        null=True)
    act_shipping_date = models.DateField(
        blank=True,
        null=True)
    est_receiving_date = models.DateField(
        blank=True,
        null=True)
    act_receiving_date = models.DateField(
        blank=True,
        null=True)
    shipping = models.DecimalField(
        max_digits=14, decimal_places=4, null=True, blank=True,
        help_text="Shipping and handling costs associated with this transaction")
    is_complete = models.BooleanField(
        default=False,
        help_text="""
            Make sure information in this transaction is correct. 
            Once is_complete is checked, it cannot be unchecked.""")

    _original_complete = None
    _le_list = []
    _error = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_complete = self.is_complete

    def clean(self):
        # check if is_complete has changed and is_complete is true
        if self._original_complete is True:  #  and self._original_complete != self.is_complete
            # can't change a Transaction once it is complete
            raise ValidationError("You may not change a Transaction once the field 'Is complete' is checked True.")
            """
            to assign validation error to a speciific field
            {'is_complete': ("You may not change a Transaction once 
                    the field 'Is complete' is checked True.")}
            """
        if self._error != 0:
            # not sufficient parts availble
            raise ValidationError("You may not change a Transaction once the field 'Is complete' is checked True.")

    def save(self, *args, **kwargs):
        """
        ('ASN', 'Advanced Shipping Notice'),
        ('TRS', 'Transfer'),
        ('ADJ', 'Inventory Adjustment'),
        ('ORD', 'Order'),
        ('RET', 'Return'),
        """
        # save the current record
        super().save(*args, **kwargs)

        _error = 0
        _le_list = None

        if (self._original_complete is False 
            and self._original_complete != self.is_complete):

            # make the _le_list
            _ttype = self.transaction_type
            _error, _le_list = create_le_list(self, ttype=_ttype)

        print("error03", _error)
        print("le_list", _le_list)

        if _error == 0 and _le_list:
            for entry in _le_list:
                record_ledger_entries(self, entry=entry, *args, **kwargs)

            print("error04", _error)
        
        else:
            print("error05", _error)
            print("there is an error")

    def __str__(self):
        return self.transaction_number

class TransactionDetails(models.Model):
    transactions = models.ForeignKey(
        Transaction,
        related_name = 'TransactionDetails',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    parts = models.ForeignKey(
        Part,
        related_name = 'Parts_TransactionDetails',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    products = models.ForeignKey(
        Product,
        related_name = 'Products_TransactionDetails',
        blank=True,
        null=True,
        on_delete=models.CASCADE)

    """
    Think about adding parts and products that will allow for transfers,
    and add additional shipping costs to cost_per_unit 
    """

    quantity_shipped = models.IntegerField(
        blank=True,
        null=True,
        help_text="Quantity shipped.")


    quantity_received = models.IntegerField(
        blank=True,
        null=True,
        help_text="Quantity received.")

    @property
    def calc_cpu(self):
        if self.parts:
            cpu = self.parts.calc_cpu
        elif self.products:
            cpu = self.products.calc_cpu
        else:
            cpu = {'cpu': None, 'unit': None}
            # print("no cpu calculated -- maybe put error message here ?? ")
        return cpu 

    """
    define a save methood, on is_complete that creates a journal entry
    to compensate for any discrepancies in shipping
    """
    def save(self, *args, **kwargs):
        if not self.quantity_received:
            self.quantity_received = self.quantity_shipped
        super(TransactionDetails, self).save(*args, **kwargs)

    def __str__(self):
        return self.transactions.transaction_number

class ASNManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transaction_type='ASN')

class ASN(Transaction):
    objects = ASNManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.transaction_type == '':
            self.transaction_type='ASN'
        super(ASN, self).save(*args, **kwargs)

class TransferManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transaction_type='TRS')

class Transfer(Transaction):
    objects = TransferManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.transaction_type == '':
            self.transaction_type='TRS'
        super(Transfer, self).save(*args, **kwargs)

class InvAdustmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transaction_type='ADJ')

class InvAdjustment(Transaction):
    objects = InvAdustmentManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.transaction_type == '':
            self.transaction_type='ADJ'
        super(InvAdjustment, self).save(*args, **kwargs)

class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transaction_type='ORD')

class Order(Transaction):
    objects = OrderManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.transaction_type == '':
            self.transaction_type='ORD'
        super(Order, self).save(*args, **kwargs)

class ReturnManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(transaction_type='RET')

class Return(Transaction):
    objects = ReturnManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        # add the transaction_type if missing
        if self.transaction_type == '':
            self.transaction_type='RET'
        super(Return, self).save(*args, **kwargs)
