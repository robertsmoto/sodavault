@property
def calc_price(self):
    """
    price can be calculated 
    from estimated cost
    from avg cost of inventory 
    from ecpu override
    """
    # find amount, and assign designator
    _cost = 0 
    _designator = ""
    _price = 0

    # find cost
    # based on cost override
    # print("### self.inv_stats -->", self.inv_stats)
    if self.ecpu_override is not None:
        _cost = self.ecpu_override
        _designator = "ecpu override"

    # based on existing inventory
    elif self.inv_stats:
        _cost = self.inv_stats['avg_cpu']
        _designator = "avg cpu of available inventory"

    # based on estimated cost per unit
    elif self.ecpu is not None:
        _cost = self.ecpu
        _designator = "estimated cost per unit (ecpu)"

    else:
        _cost = 0
        _designator = "not able to calculate a cost per unit"
        pass

    # calcualte price based on cost
    if self.price_class is not None:
        if self.price_class.is_flat is True:
            _price = _cost + self.price_class.amount
        elif self.price_class.is_markup is True:
            _price = _cost + (_cost * (self.price_class.amount / 100))
        elif self.price_class.is_margin is True:
            _price = _cost / (1 - (self.price_class.amount / 100))
    else:
        _price = 0
        _designator = "please assign a price class"

    if self.price_override is not None:
        _price = self.price_override
        _designator = "price override"

    calc_price = {}
    calc_price['cost'] = _cost
    calc_price['price'] = _price
    calc_price['designator'] = _designator

    return calc_price

