from collections import OrderedDict


order_contradictions = OrderedDict(score=None, reasoning=OrderedDict(
            statements=OrderedDict(severity=None, summary=None, reasoning=None)))


def order_output_dict(d: dict, keys_order: OrderedDict) -> OrderedDict:
    """
        Orders the output dictionary based on the given keys order.

        :param d: The input dictionary to be ordered.
        :type d: dict
        :param keys_order: An OrderedDict that specifies the desired order of keys.
                           If a key contains a nested dictionary or list, the nested keys_order should be provided.
        :type keys_order: OrderedDict
        :return: A new OrderedDict with keys ordered as specified in keys_order.
        :rtype: OrderedDict
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
