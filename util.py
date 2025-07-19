def pval_order(p: float, orders=[0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05]) -> str:
    """
    Return p-value order
    """
    orders.sort()
    for order in orders:
        if p < order:
            return f"P < {order}"

    return f"P = {p:.2f}"
