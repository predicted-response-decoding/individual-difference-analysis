import os
from typing import Any, Callable, Iterable, List

import numpy as np
from statsmodels.stats.multitest import fdrcorrection

"""
Make p-values FDR corrected
"""


def tofdr(pvals: dict) -> dict:
    all_pvals: list = []
    for mset in pvals:
        for task in pvals[mset]:
            all_pvals.append(pvals[mset][task])

    if len(all_pvals) == 0:
        return pvals

    all_pvals_flattened = np.hstack(all_pvals)
    _, all_fdr_pvals = fdrcorrection(all_pvals_flattened)
    all_fdr_pvals = all_fdr_pvals.tolist()

    fdr_pvals: dict = {}
    for mset in pvals:
        fdr_pvals[mset] = {}
        for task in pvals[mset]:
            fdr_pvals[mset][task] = all_fdr_pvals[: len(pvals[mset][task])]
            all_fdr_pvals = all_fdr_pvals[len(pvals[mset][task]) :]

    return fdr_pvals


"""
Return p-value order
"""


def pval_order(p: float) -> str:
    if p >= 0.05:
        pval_str = f"P = {p:.3g}"
    else:
        orders = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05]
        for order in orders:
            if p < order:
                pval_str = f"P < {order}"
                break
    return pval_str


"""
Other utility
"""


def map_list(f: Callable[[Any], Any], iter: Iterable[Any]) -> List[Any]:
    return list(map(f, iter))


def vectorize_ndarray(
    f: Callable[[Any], np.ndarray], iter: Iterable[Any]
) -> np.ndarray:
    return np.vectorize(f, otypes=[np.ndarray])(iter)


def matrixify_ndarray(
    f: Callable[[Any], np.ndarray], iter: Iterable[Any]
) -> np.ndarray:
    return np.array(list(map(f, iter)))


def makedirs_or_pass(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
