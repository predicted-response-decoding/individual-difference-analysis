from typing import Any, Dict, List, Tuple

import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr
from tqdm import tqdm

from config import (
    MANUAL_RATING_PATH,
    MEAS_RESP_DEC_PATH,
    PRED_RESP_DEC_PATH,
    RC_PARAMS_DEFAULT,
)
from subject_selector import SubjectSelector
from util import (
    makedirs_or_pass,
    matrixify_ndarray,
    pval_order,
    vectorize_ndarray,
)

plt.rcParams.update(RC_PARAMS_DEFAULT)

from labels import AbstractMovieSet, AbstractTask


def read_manual_rating(
    mset: AbstractMovieSet, task: AbstractTask, subj: str
) -> np.ndarray:
    with h5py.File(MANUAL_RATING_PATH(mset.name, task.name, subj), "r") as f:
        return f["manualRating"][()]


def read_pstim_from_meas_resp_dec(
    mset: AbstractMovieSet, task: AbstractTask, subj: str
) -> np.ndarray:
    with h5py.File(MEAS_RESP_DEC_PATH(mset.name, task.name, subj), "r") as f:
        return f["pstim"][()]


def read_pstim_from_pred_resp_dec(
    mset: AbstractMovieSet, task: AbstractTask, subj: str
) -> np.ndarray:
    with h5py.File(PRED_RESP_DEC_PATH(mset.name, task.name, subj), "r") as f:
        return f["pstim"][()]


def calc_pair_dist(
    msets: List[AbstractMovieSet],
    tasks: List[AbstractTask],
    is_for_manual=False,
) -> Tuple[dict, dict, dict]:
    subj_all = SubjectSelector()

    dist_all: dict = {}
    rvals: dict = {}
    pvals: dict = {}
    for mset in msets:
        dist_all[mset] = {}
        rvals[mset] = {}
        pvals[mset] = {}
        for task in tasks:
            exists_combination = task.from_movie_set(mset)
            if (not exists_combination) or (
                is_for_manual and not task.has_manual_rating
            ):
                continue

            subjs = subj_all.select(mset, task)

            # Extract all subjects' decoding
            if is_for_manual:
                x_resp = matrixify_ndarray(
                    lambda subj: read_manual_rating(mset, task, subj), subjs
                )
            else:
                x_resp = matrixify_ndarray(
                    lambda subj: read_pstim_from_meas_resp_dec(
                        mset, task, subj
                    ),
                    subjs,
                )
            pred_resp_dec = matrixify_ndarray(
                lambda subj: read_pstim_from_pred_resp_dec(mset, task, subj),
                subjs,
            )

            dist_all[mset][task] = []
            rvals[mset][task] = []
            pvals[mset][task] = []
            if task.is_vector:
                # (subject: 40, time: 1200, w2v_dim: 100) -> (1200, 40, 100)
                x_resp = x_resp.transpose(1, 0, 2)
                pred_resp_dec = pred_resp_dec.transpose(1, 0, 2)
                n_time = pred_resp_dec.shape[0]
                dists_x = vectorize_ndarray(
                    lambda time_i: pdist(x_resp[time_i], metric="correlation"),
                    range(n_time),
                )
                dists_pred = vectorize_ndarray(
                    lambda time_i: pdist(
                        pred_resp_dec[time_i], metric="correlation"
                    ),
                    range(n_time),
                )
                dists_x = dists_x.mean(axis=0)
                dists_pred = dists_pred.mean(axis=0)
                dist_all[mset][task].append([dists_x, dists_pred])

                r, p = spearmanr(dists_x, dists_pred)
                rvals[mset][task].append(r)
                pvals[mset][task].append(p)

            else:
                # (subject: 40, time: 1200, item: 30) -> (30, 40, 1200)
                x_resp = x_resp.transpose(2, 0, 1)
                pred_resp_dec = pred_resp_dec.transpose(2, 0, 1)
                for k in range(pred_resp_dec.shape[0]):
                    dists_x = pdist(x_resp[k], metric="correlation")
                    dists_pred = pdist(pred_resp_dec[k], metric="correlation")
                    dist_all[mset][task].append([dists_x, dists_pred])
                    r, p = spearmanr(dists_x, dists_pred)
                    rvals[mset][task].append(r)
                    pvals[mset][task].append(p)

    return dist_all, rvals, pvals


class PairDistPlotter:
    __is_for_manual: bool = False
    __xlabel: str = (
        "Participant-pair dissimilarity\nfor measured-response decoding"
    )
    __ylabel: str = (
        "Participant-pair dissimilarity\nfor predicted-response decoding"
    )

    def plot(
        self,
        x: np.ndarray,
        y: np.ndarray,
        rval: float,
        pval: float,
    ) -> object:
        fig, ax = plt.subplots()
        ax.scatter(x, y, s=12, c=self.__color, edgecolor="none")
        ax.set_title(self.__title, fontsize=12)
        ax.set_xlabel(self.__xlabel, fontsize=10)
        ax.set_ylabel(self.__ylabel, fontsize=10)
        ax.text(
            0.02,
            0.97,
            f"IDR = {rval:.2f}",
            ha="left",
            va="top",
            fontsize=10,
            transform=ax.transAxes,
        )
        ax.text(
            0.02,
            0.9,
            f"{pval_order(pval)}",
            ha="left",
            va="top",
            fontsize=10,
            transform=ax.transAxes,
        )
        return fig

    def for_manual(self) -> None:
        self.__is_for_manual = True
        self.__xlabel = "Participant-pair dissimilarity\nof manual ratings"

    def set_title(self, task_from_mset: AbstractTask, k: int) -> None:
        title_item = (
            ""
            if task_from_mset.item_names[k] == ""
            else f"\n - {task_from_mset.item_names[k]}"
        )
        self.__title = f"{task_from_mset.title} ({task_from_mset.title_movie_set}){title_item}"
        self.__color = task_from_mset.color

    def plot_all_mset_task(
        self, dist_all: dict, rvals: dict, pvals: dict
    ) -> dict:
        figs: dict = {}

        for mset in dist_all:
            figs[mset] = {}

            tasks = dist_all[mset]
            for task in tasks:
                figs[mset][task] = []

                for item_i in range(len(dist_all[mset][task])):
                    dists_x, dists_pred_resp_dec = (
                        dist_all[mset][task][item_i][0],
                        dist_all[mset][task][item_i][1],
                    )
                    rval, pval = (
                        rvals[mset][task][item_i],
                        pvals[mset][task][item_i],
                    )
                    task.from_movie_set(mset)
                    self.set_title(task, item_i)
                    fig = self.plot(dists_x, dists_pred_resp_dec, rval, pval)
                    figs[mset][task].append(fig)
        return figs

    def save_all_mset_task(
        self, figs: Dict[AbstractMovieSet, Dict[AbstractTask, Any]]
    ) -> None:
        for mset in figs.keys():
            res_mset_dir = f"result/{mset.name}"
            makedirs_or_pass(res_mset_dir)
            for task in figs[mset].keys():
                task.from_movie_set(mset)
                for item_i, fig in tqdm(enumerate(figs[mset][task])):
                    title_item = (
                        ""
                        if task.item_names[item_i] == ""
                        else f" - {task.item_names[item_i]}"
                    )
                    fname = f"{task.title}{title_item}".replace("/", " or ")
                    if self.__is_for_manual:
                        fname += " (manual rating)"
                    fig.savefig(
                        f"{res_mset_dir}/{fname}.png",
                        dpi=300,
                        bbox_inches="tight",
                    )
                    plt.close(fig)
