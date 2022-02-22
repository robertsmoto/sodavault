import itemsapp.models


def calc_ecpu(main: dict) -> dict:
    """Recursive function that calculates the estimated cost per unit.
    Begin with 'start_ids' key as a list of one or more obj.ids
    formatted: main = {'start_ids': [17]}"""

    main['ecpu'] = 0 if 'ecpu' not in main else main['ecpu']
    main['ecpu_fcnt'] = 0 if 'ecpu_fcnt' not in main else main['ecpu_fcnt']

    def check_for_list(main: dict) -> (int, int, dict):
        item_id = None
        qnty_multby = 1
        if main['start_ids']:
            item_id = main['start_ids'].pop()
        if isinstance(item_id, list):
            if item_id:
                hold_ids = item_id
                item_id = hold_ids.pop()
                if hold_ids:
                    main['start_ids'].append(hold_ids)
            else:
                check_for_list(main)
        if isinstance(item_id, tuple):
            qnty_multby = item_id[0]
            item_id = item_id[1]

        return qnty_multby, item_id, main

    qnty_multby, item_id, main = check_for_list(main)

    if not item_id:
        return main

    item = itemsapp.models.Item.objects \
        .prefetch_related(
                'bid_components',
                'bid_parts',
                'bid_products',
                ) \
        .get(id=item_id)

    # bid queries
    bids = (
            item.bid_components.filter(is_winning_bid=True) |
            item.bid_parts.filter(is_winning_bid=True) |
            item.bid_products.filter(is_winning_bid=True)
            )

    # component queries
    new_ids = itemsapp.models.ComponentJoin.objects \
        .values_list('quantity', 'to_item_id') \
        .filter(from_item_id=item_id)

    # check override
    if item.cost + item.cost_shipping > 0:
        main['ecpu'] = main['ecpu'] + (
                qnty_multby
                * ((item.cost + item.cost_shipping) / item.cost_quantity)
                )
        main['ecpu_fcnt'] = 1 if main['ecpu_fcnt'] == 0 else main['ecpu_fcnt']

    # check winning bid
    elif len(bids) > 0:
        bid = bids[0]
        main['ecpu'] = main['ecpu'] + (
                qnty_multby
                * ((bid.cost + bid.cost_shipping) / bid.cost_quantity)
                )

        main['ecpu_fcnt'] = 2 if main['ecpu_fcnt'] == 0 else main['ecpu_fcnt']

    # check components
    elif new_ids:
        main['start_ids'].append(list(new_ids))

    # return condition
    print("main @ end",  main)
    if len(main['start_ids']) > 0:
        main['ecpu_fcnt'] += 1
        return calc_ecpu(main=main)
    else:
        print("this is the end")
        if main['ecpu_fcnt'] == 1:
            main['ecpu_from'] = "cost override"
        elif main['ecpu_fcnt'] == 2:
            main['ecpu_from'] = "winning bid"
        else:
            main['ecpu_from'] = "component costs"

        main.pop('start_ids')
        main.pop('ecpu_fcnt')
        return main
