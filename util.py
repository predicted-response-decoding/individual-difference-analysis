import numpy as np


def pval_order(p: float, orders=[0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05]) -> str:
    """
    Return p-value order
    """
    orders.sort()
    for order in orders:
        if p < order:
            return f"P < {order}"

    return f"P = {p:.2f}"

def binrange_bins0_1(x):
    binrange = [0, 0]
    while np.any(x < binrange[0]): binrange[0] -= 0.1
    while np.any(binrange[1] <= x): binrange[1] += 0.1
    bins = round(10 * (binrange[1] - binrange[0]))
    assert bins == round(10 * (binrange[1] - binrange[0])), [bins, 10 * (binrange[1] - binrange[0])]
    return binrange, bins
