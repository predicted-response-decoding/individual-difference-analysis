import numpy as np
from scipy.stats import rankdata
from scipy.spatial.distance import squareform


def n_comb2n(n_comb):
    """
    Get number of subjects from number of subject pairs
    """
    s = 1
    t = 2 ** 18
    while s != t:
        m = (s + t) // 2
        m_comb = m * (m - 1) // 2
        if m_comb < n_comb: s = m + 1
        elif n_comb <= m_comb: t = m

    return s


def manteltest(x, y, seed=0, n_trial=100000):
    """
    x: np.ndarray[D] or np.ndarray[N, D]
    y: np.ndarray[D] or np.ndarray[N, D]
    Return:
        np.ndarray[N, D]
    """
    if seed is not None: np.random.seed(seed)
    x = np.asanyarray(x)
    y = np.asanyarray(y)
    assert x.shape == y.shape
    assert x.ndim in [1, 2]
    # Make every inputs matricized
    if x.ndim == 1:
        x = x.reshape(1, -1)
        y = y.reshape(1, -1)

    # Calculate no. of elements from no. of combinations
    d_comb = x.shape[1]
    d = n_comb2n(d_comb)
    # Ranknize and normalize
    x[...] = rankdata(x, axis=1).astype("f")
    x -= x.mean(axis=1, keepdims=True)
    x /= x.std(axis=1, keepdims=True)
    y[...] = rankdata(y, axis=1).astype("f")
    y -= y.mean(axis=1, keepdims=True)
    y /= y.std(axis=1, keepdims=True) * d_comb
    idx_comb_sqf = squareform(np.arange(d_comb))
    shuffled_x_trials = np.empty((n_trial, x.shape[0], d_comb))
    idx = np.arange(d)
    for i_trial in range(n_trial):
        # Randomize element indices
        np.random.shuffle(idx)
        # Permutate combination indices according to the indices
        shuffled_idx_comb = squareform(idx_comb_sqf[idx][:, idx])
        # Permutate x
        shuffled_x_trials[i_trial] = x[:, shuffled_idx_comb]

    r = (x * y).sum(axis=1)
    assert np.all((-1 < r) & (r < 1))
    null_distrib =  (shuffled_x_trials * y).sum(axis=2)
    assert np.all((-1 < null_distrib) & (null_distrib < 1))
    pvals = (r <= null_distrib).mean(axis=0)
    return pvals
