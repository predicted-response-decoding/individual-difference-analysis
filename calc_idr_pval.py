import os
from logging import getLogger
import hydra
from omegaconf import DictConfig
import pandas as pd

from calc_idr import calc_idr
from manteltest import manteltest
import mytask
from config import get_manual_rating, get_meas_resp_dec, get_pred_resp_dec


logger = getLogger(__name__)

@hydra.main(config_name="config", config_path="conf", version_base=None)
def main(cfg: DictConfig):
    nnmodel = cfg.nnmodel
    task_arg = cfg.task_arg

    t = mytask.get_task_by_arg(task_arg)
    for m in t.msets:
        subjs = t.get_subjects(mset=m)
        pstims_meas = [
            get_meas_resp_dec(mset=m.__name__, task=t.__name__, subj=subj)
            for subj in subjs
        ]
        pstims_pred = [
            get_pred_resp_dec(mset=m.__name__, task=t.__name__, nnmodel=nnmodel, subj=subj)
            for subj in subjs
        ]
        idrvals, a_labels, b_labels = calc_idr(pstims_meas, pstims_pred, is_vector=t.is_vector)
        pvals = manteltest(a_labels, b_labels)
        fname_out = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/idr.csv"
        logger.info(f"Saving {fname_out}")
        os.makedirs(os.path.dirname(fname_out), exist_ok=True)
        pd.DataFrame({"idr": idrvals, "pval": pvals}).to_csv(fname_out, float_format="%.3g", index=False)

        if not t.has_manual_rating: continue

        pstims_behavioral = [
            get_manual_rating(mset=m.__name__, task=t.__name__, subj=subj)
            for subj in subjs
        ]
        idrvals, a_labels, b_labels = calc_idr(pstims_behavioral, pstims_pred, is_vector=t.is_vector)
        pvals = manteltest(a_labels, b_labels)
        fname_out = f"./result/{nnmodel}/{m.__name__}/{t.__name__}/behavioral-idr.csv"
        logger.info(f"Saving {fname_out}")
        pd.DataFrame({"idr": idrvals, "pval": pvals}).to_csv(fname_out, float_format="%.3g", index=False)


if __name__ == "__main__":
    main()
