import itemsapp.models as imodels


def calc_inv(obj: dict, main: dict = None) -> dict:
    """Calculates CPU and current inventory stats."""

    if main is None:
        main = {}

    entry = imodels.Ledger.inventory.all_items(iid=obj.id).agg_counts()
    dquan = entry['dquan'] if entry['dquan'] else 0
    cquan = entry['cquan'] if entry['cquan'] else 0
    camou = entry['camou'] if entry['camou'] else 0
    damou = entry['damou'] if entry['damou'] else 0
    qnty = dquan - cquan
    amnt = damou - camou
    main['quantity'] = qnty
    main['cpu'] = round(amnt / qnty) if qnty > 0 else 0
    main['cpu_display'] = f"${main['cpu']/100 :.2f}"

    return main


def calc_max_inv(obj: dict, main: dict = None) -> dict:

    if main is None:
        main = {}

    jointable = obj.assembly.through.objects.filter(item_id=obj.id)
    if jointable:

        # create a list of dicts, then return the limiting item
        calc_list = []
        for join in jointable.all():
            # unlimited items don't limit inventory
            if join.is_unlimited:
                continue

            idict = join.assembly.inv_display
            idict['sku'] = join.assembly.sku

            cr_max_qnty = 0
            cr_max_desc = "bring assembled items into inventory"

            if join.quantity > 0 and idict['quantity'] > 0:
                cr_max_qnty = idict['quantity'] / join.quantity
                cr_max_desc = "limited by inventory"

            idict['cr_max_qnty'] = cr_max_qnty
            idict['cr_max_desc'] = cr_max_desc

            calc_list.append(idict)

        if not calc_list:
            # inventory is not limited by assembly
            main['cr_max_qnty'] = None
            main['cr_max_desc'] = "create unlimited inventory"
        else:
            calc_list = sorted(calc_list, key=lambda d: d['cr_max_qnty'])
            main['cr_max_qnty'] = round(calc_list[0]['cr_max_qnty'])
            main['cr_max_desc'] = calc_list[0]['cr_max_desc']

    return main


def calc_ecpu(obj: dict, main: dict = None) -> dict:
    """Calculates ECPU and related cost estimate stats."""

    if main is None:
        main = {}

    bid_q = obj.bid_set.filter(is_winning_bid=True)

    # check override
    if obj.cost + obj.cost_shipping > 0:
        main['ecpu'] = round(
                (obj.cost + obj.cost_shipping) / obj.cost_quantity)
        main['ecpu_from'] = "cost override"

    # check winning bid
    elif bid_q:
        bid = bid_q[0]
        main['ecpu'] = round(
                (bid.cost + bid.cost_shipping) / bid.cost_quantity)
        main['ecpu_from'] = "winning bid"

    # check assembled components
    elif imodels.ItemAssemblyJoin.assembly:
        assemb_q = imodels.ItemAssemblyJoin.objects.filter(
            item_id=obj.id).prefetch_related(
                    'assembly')
        ecpu = 0
        for aitem in assemb_q:
            ecpu = ecpu + (
                    aitem.quantity
                    * aitem.assembly.ecpu
                    )
        main['ecpu'] = round(ecpu)
        main['ecpu_from'] = "assembled components"
    else:
        main['ecpu'] = 0
        main['ecpu_from'] = "not calculated"

    # calculates create_max inventory
    main = calc_max_inv(obj=obj, main=main)

    main['ecpu_display'] = f"${main['ecpu']/100 :.2f}"

    return main
