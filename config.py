import h5py


SUBJECTS_CSV_PATH = "./data/subjects.csv"

"""
Get data
"""
def get_manual_rating(mset: str, task: str, subj: str) -> str:
    with h5py.File(f"./data/{mset}/{subj}/{task}/ManualRating.hdf5") as f:
        return f["manualRating"][:]


def get_meas_resp_dec(mset: str, task: str, subj: str) -> str:
    with h5py.File(f"./data/{mset}/{subj}/{task}/MeasRespDec.hdf5") as f:
        return f["pstim"][:]


def get_pred_resp_dec(mset: str, task: str, nnmodel: str, subj: str) -> str:
    with h5py.File(f"./data/{mset}/{subj}/{task}/PredRespDec_{nnmodel}.hdf5") as f:
        return f["pstim"][:]


RCPARAMS_DEFAULT = {
    # 'figure.autolayout': True,
    "figure.figsize": (4, 4),
    "font.size": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "savefig.dpi": 300,
    "figure.dpi": 100,
    "lines.linewidth": .3, #0.7
    "lines.markersize": 4,
    "errorbar.capsize": 4,
    # "lines.markeredgecolor": "k",
    "lines.markeredgewidth": .3,
    "scatter.edgecolors": "k",
    # "axes.linewidth": 0.5,
    "axes.edgecolor": "k",
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
}
