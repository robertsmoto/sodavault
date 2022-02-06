@property
def inv_stats(self):

    _le_q = None
    if self.item_type == 'PART':
        _le_q = self.le_parts.filter(account='IRAW').aggregate(
                Sum('debit_amount'),
            Sum('credit_amount'),
            Sum('debit_quantity'),
            Sum('credit_quantity'))

    if self.item_type == 'PROD':
        _le_q = self.le_products.filter(account='IMER').aggregate(
            Sum('debit_amount'),
            Sum('credit_amount'),
            Sum('debit_quantity'),
            Sum('credit_quantity'))

    """
    'debit_amount__sum': Decimal('3363.66'),
    'credit_amount__sum': None,
    'debit_quantity__sum': Decimal('10000.00'),
    'credit_quantity__sum': None
    """

    def check_for_zero(self, myvariable):
        return 0 if myvariable is None else myvariable

    _d_amount = 0
    _c_amount = 0
    _d_quantity = 0
    _c_quantity = 0

    if _le_q:
        _d_amount = check_for_zero(self, _le_q['debit_amount__sum'])
        _c_amount = check_for_zero(self, _le_q['credit_amount__sum'])
        _d_quantity = check_for_zero(self, _le_q['debit_quantity__sum'])
        _c_quantity = check_for_zero(self, _le_q['credit_quantity__sum'])

    _cost = _d_amount - _c_amount
    _quantity = _d_quantity - _c_quantity
    _avg_cpu = _cost / _quantity if _quantity > 0 else 0

    inv_stats_dict = {}

    if _quantity == 0:
        _cost = 0
        _quantity = 0
        _avg_cpu = 0

    else:
        inv_stats_dict['cost'] = _cost
        inv_stats_dict['quantity'] = _quantity
        inv_stats_dict['avg_cpu'] = _avg_cpu

    # print("inv_stats_dict", inv_stats_dict)
    return inv_stats_dict
    # inv_stats['cost'], inv_stats['quantity'], inv_stats['avg_cpu']

@property
def available_inventory(self):
    inv_stats = self.inv_stats
    # print("here inv_stas", inv_stats)
    if inv_stats:
        return "{} units available. {} total cost. {} avg cpu".format(
            int(inv_stats['quantity']),
            round(inv_stats['cost'], 2),
            round(inv_stats['avg_cpu'], 4)
        )
    else:
        return "No available inventory"

@property
def calc_max_new_inventory(self):

    # checks there is ecpu assigned to part
    if self.ecpu == 0:
        return """Before you can create new inventory, you must assign a cost. 
            You can assign costs by creating winning bids, assembling products
            from parts, or by entering an estimated cost override (ecpu override).
            """

    # for products assembed from parts, may be limited by parts inventory
    _pid = None
    _ppj_q = None
    _part_inv = []
    _part_dict = {}
    # query is_unlimted = False,
    # because an unlimited Part does not limit the creation of a Product
    if self.item_type == "PROD":
        _pid = self.id
        print("self.id, self.name", self.id, self.name)
        _ppj_q = ProductPartJoin.objects.filter(
            products_id=_pid, 
            is_unlimited=False
        ).prefetch_related(
            Prefetch('parts'))
    if _ppj_q:
        for ppj in _ppj_q:
            _part_dict = {}
            if ppj.parts.inv_stats:
                _part_dict['id'] = ppj.parts.id
                _part_dict['name'] = ppj.parts.name
                _part_dict['total_quantity'] = math.floor(
                        ppj.parts.inv_stats['quantity'])
                _part_dict['max_quantity'] = math.floor(
                        ppj.parts.inv_stats['quantity'] / ppj.quantity)
            else:
                _part_dict['id'] = ppj.parts.id
                _part_dict['name'] = ppj.parts.name
                _part_dict['total_quantity'] = 0
                _part_dict['max_quantity'] = 0 

            _part_inv.append(_part_dict)

        def by_max_quantity(p_list):
            return p_list['max_quantity']

        _part_inv.sort(key=by_max_quantity)

        print("_part_inv", _part_inv)

        # change the return to include meaningful information
        if len(_part_inv) > 0:
            _part_inv[0]['is_limited'] = True
            return """This product is assembled from parts. You can bring a maximum 
                number of {} new pcs into inventory. New inventory is currently 
                limted by {} which currently has {} pcs in stock.
                """.format(
                    _part_inv[0]['max_quantity'],
                    _part_inv[0]['name'],
                    _part_inv[0]['total_quantity']
                ), _part_inv[0]
        else:
            _part_inv.append(_part_dict)
            _part_inv[0]['is_limited'] = False
            _part_inv[0]['max_quantity'] = None
            return """This product is assembled from parts, however,
                it is not limited by the inventory of those parts.""", _part_inv[0]

    # may create unlimited inventory
    else:
        _part_inv.append(_part_dict)
        _part_inv[0]['is_limited'] = False
        _part_inv[0]['max_quantity'] = None
        return "You may create unlimited new inventory for this item.", _part_inv[0]

@property
def max_new_inventory(self):
    return self.calc_max_new_inventory[0]

