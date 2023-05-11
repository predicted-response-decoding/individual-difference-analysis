import pandas as pd
from config import SUBJECT_DATA_PATH


class SubjectSelector:
    def __init__(self) -> None:
        self.subjs_default = pd.read_csv(SUBJECT_DATA_PATH)

    def select(self, mset, task):
        subjs = self.subjs_default[self.subjs_default.mset == mset.__name__]
        if task().has_manual_rating:
            subjs = subjs[subjs[f'manual_{task.__name__}'] == 1]
        return subjs['subjName']
