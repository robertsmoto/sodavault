@property
def calc_ecpu(self):
    _ecpu = 0
    _unit = ""
    _designator = ""

    # check for estimated costs based on winning_bid
    _items_q = None
    _w_bid = None

    if self.item_type == 'PART':
        # print("made it to first PART")
        # query part winning_bid
        _w_bid = self.bid_parts.filter(is_winning_bid=True).first()

    if self.item_type == 'PROD':
        # print("made it to first PROD")
        # query product winning_bid
        _w_bid = self.bid_products.filter(is_winning_bid=True).first()

    # check for ecpu based on winning bid
    if _w_bid:
        # print("_w_bid", _w_bid)
        _cost = 0; _shipping = 0; _quantity = 0; _unit = ""
        _cost = _w_bid.cost if _w_bid.cost is not None else 0
        _shipping = _w_bid.shipping if _w_bid.shipping is not None else 0
        _quantity = _w_bid.quantity
        _unit = _w_bid.units
        _unit = _unit.rstrip('s') # rstrip only from the end of string
        _ecpu = (_cost + _shipping) / _quantity if _quantity > 0 else 0
        _designator = "ecpu based on winning bid"


    # check for ecpu based on assembled parts (for product)
    _items_q = None
    if self.item_type == 'PROD':
        _items_q = self.ppj_products.all().prefetch_related('parts')

    if _items_q:
        _total_ecpu = 0
        for it in _items_q:
            _quantity = it.quantity if it.quantity is not None else 0
            _ecpu = it.parts.ecpu if it.parts.ecpu is not None else 0
            _total_ecpu = _total_ecpu + (_quantity * _ecpu)

        _ecpu = round(_total_ecpu, 4)
        _unit = "pc"
        _designator = "ecpu based on assembled parts"

    # check ecpu based on overrides
    _ecpu = self.ecpu_override if self.ecpu_override is not None else _ecpu
    _unit = self.unit_override if self.unit_override != "" else _unit
    if self.ecpu_override:
        _designator = "ecpu based on override"

    calc_ecpu = {}
    calc_ecpu['ecpu'] = _ecpu
    calc_ecpu['unit'] = _unit
    calc_ecpu['designator'] = _designator

    print("calc_ecpu", calc_ecpu)

    return calc_ecpu

