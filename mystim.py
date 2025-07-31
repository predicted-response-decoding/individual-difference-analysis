from abc import ABC
import pandas as pd

from config import SUBJECTS_CSV_PATH

class AbstractStimulus(ABC):
    arg: str
    title: str

    @classmethod
    def get_subjects(cls):
        subj_all = pd.read_csv(SUBJECTS_CSV_PATH)
        subjs = subj_all[subj_all.mset == cls.__name__]
        return subjs.unique_id


class WebAdMovieSet(AbstractStimulus):
    arg = "web"
    title = "Web ad movie set"


class TVAdMovieSet(AbstractStimulus):
    arg = "tv"
    title = "TV ad movie set"
