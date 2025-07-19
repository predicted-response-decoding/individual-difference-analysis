import numpy as np
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr as _spearmanr


def spearmanr(x, y): return _spearmanr(x, y)[0]

@np.vectorize(signature="(n,m)->(k)")
def get_dist(x_subjs_timeseries):
    return pdist(x_subjs_timeseries, metric="correlation")

def get_vec_dist(x_subjs_vecdims):
    return get_dist(x_subjs_vecdims)

class SynmetricMatricesCorrelation:
    def __init__(self, metric) -> None:
        self.metric = metric

    def calc(self, x, y):
        @np.vectorize(signature="(n),(n)->()")
        def calc_wrapper(x, y): return self.metric(x, y)
        return calc_wrapper(x, y)

class IDRController:
    def __init__(self, mn1, mn2, framework1=None, framework2=None, metric=None) -> None:
        self.mn1 = mn1
        self.mn2 = mn2
        self.framework1 = framework1
        self.framework2 = framework2

    def calc(self, task, manual=False):
        model1_pstims = task.get_pstim(self.framework1, self.mn1)
        model2_pstims = task.get_pstim(self.framework2, self.mn2)
        """
        RSA between measuerd- / predicted-response decoding
        """
        if task.is_vector:
            # transpose: (Subjects, Timeseries, Dimension) -> (Timeseries, Subjects, Dimension)
            model1_pstims = np.array(model1_pstims).transpose(1, 0, 2)
            model2_pstims = np.array(model2_pstims).transpose(1, 0, 2)
            dists_bd = get_vec_dist(model1_pstims).mean(axis=0)
            dists_btl = get_vec_dist(model2_pstims).mean(axis=0)
            dist_items_model1, dist_items_model2 = [dists_bd], [dists_btl]
            idr_items = np.array(spearmanr(dists_bd, dists_btl)).reshape(1,)

        else:
            # transpose: (Subjects, Timeseries, Items) -> (Items, Subjects, Timeseries)
            model1_pstims = np.array(model1_pstims).transpose(2, 0, 1)
            model2_pstims = np.array(model2_pstims).transpose(2, 0, 1)
            dist_items_model1 = get_dist(model1_pstims)
            dist_items_model2 = get_dist(model2_pstims)
            idr_items = SynmetricMatricesCorrelation(spearmanr).calc(dist_items_model1, dist_items_model2)

        return idr_items, dist_items_model1, dist_items_model2

def calc_idr(x, y, is_vector=False):
    """
    RSA between measuerd- / predicted-response decoding
    x: (Subjects, time series, labels) for scalar labels or (subjects, time series, dimension) vector labels
    y: (Subjects, time series, labels) for scalar labels or (subjects, time series, dimension) vector labels
    """
    x = np.asanyarray(x)
    y = np.asanyarray(y)
    if is_vector:
        # transpose: (Subjects, Timeseries, Dimension) -> (Timeseries, Subjects, Dimension)
        model1_pstims = np.array(x).transpose(1, 0, 2)
        model2_pstims = np.array(y).transpose(1, 0, 2)
        dists_bd = get_vec_dist(model1_pstims).mean(axis=0)
        dists_btl = get_vec_dist(model2_pstims).mean(axis=0)
        dist_items_model1, dist_items_model2 = dists_bd.reshape(1, -1), dists_btl.reshape(1, -1)
        idr_items = np.array(spearmanr(dists_bd, dists_btl)).reshape(1,)

    else:
        # transpose: (Subjects, Timeseries, Items) -> (Items, Subjects, Timeseries)
        model1_pstims = np.array(x).transpose(2, 0, 1)
        model2_pstims = np.array(y).transpose(2, 0, 1)
        dist_items_model1 = get_dist(model1_pstims)
        dist_items_model2 = get_dist(model2_pstims)
        idr_items = SynmetricMatricesCorrelation(spearmanr).calc(dist_items_model1, dist_items_model2)

    return idr_items, dist_items_model1, dist_items_model2
