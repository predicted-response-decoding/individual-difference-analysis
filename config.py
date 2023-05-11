SUBJECT_DATA_PATH = "data/SubjectData.csv"
MANUAL_RATING_PATH = (
    lambda mset, task, subj: f"data/{mset}/{subj}/{task}/ManualRating.hdf5"
)
MEAS_RESP_DEC_PATH = (
    lambda mset, task, subj: f"data/{mset}/{subj}/{task}/MeasRespDec_Ctx.hdf5"
)
PRED_RESP_DEC_PATH = (
    lambda mset, task, subj: f"data/{mset}/{subj}/{task}/PredRespDec_VGG16_SoundNet_AR2000_Ctx.hdf5"
)


RC_PARAMS_DEFAULT = {
    "figure.figsize": (4, 4),
    "font.size": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "savefig.dpi": 300,
    "figure.dpi": 100,
    "patch.facecolor": "w",
}
