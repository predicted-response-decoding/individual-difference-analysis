import pandas as pd

from config import SUBJECT_DATA_PATH
from labels import AbstractMovieSet, AbstractTask


class SubjectSelector:
    def __init__(self) -> None:
        self.subj_all = pd.read_csv(SUBJECT_DATA_PATH)

    def select(self, mset: AbstractMovieSet, task: AbstractTask):
        subjs = self.subj_all[self.subj_all.mset == mset.name()]
        if task.has_manual_rating:
            subjs = subjs[subjs[f"manual_{task.name()}"] == 1]
        return subjs["subjName"]
