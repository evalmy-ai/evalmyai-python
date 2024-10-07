from collections import OrderedDict

order_contradictions = OrderedDict(
    scores=OrderedDict(score=None),
    reasoning=OrderedDict(
        statements=OrderedDict(severity=None, summary=None, reasoning=None)
    ),
)

order_f1 = OrderedDict(
    scores=OrderedDict(OrderedDict(f1=None, correctness=None, completeness=None)),
    reasoning=OrderedDict(
        statements=OrderedDict(severity=None, summary=None, reasoning=None)
    ),
)


def order_output_dict(d: dict, keys_order: OrderedDict) -> OrderedDict:
    """Orders the output dictionary based on the given keys order.

    Args:
        d (dict): The input dictionary to be ordered.
        keys_order (OrderedDict): An OrderedDict that specifies the desired
            order of keys. If a key contains a nested dictionary or list, the
            nested keys_order should be provided.

    Returns:
        OrderedDict: A new OrderedDict with keys ordered as specified in
        keys_order.
    """

    res = OrderedDict()

    for key in keys_order:
        if key in d:
            if isinstance(d[key], dict):
                res[key] = order_output_dict(d[key], keys_order[key])
            elif isinstance(d[key], list):
                res[key] = [order_output_dict(item, keys_order[key]) for item in d[key]]
            else:
                res[key] = d[key]
    return res
