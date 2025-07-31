from abc import ABC
import pandas as pd

from mystim import AbstractStimulus, WebAdMovieSet, TVAdMovieSet
from config import SUBJECTS_CSV_PATH


class AbstractTask(ABC):
    arg: str
    title: str
    color: str
    item_names: list[str]
    msets: list[AbstractStimulus]
    is_vector: bool = False
    has_manual_rating: bool = False

    @classmethod
    def get_subjects(cls, mset):
        subj_all = pd.read_csv(SUBJECTS_CSV_PATH)
        subjs = subj_all[subj_all.mset == mset.__name__]
        return subjs.unique_id


class SceneDescriptions(AbstractTask):
    arg = "sd"
    title = "Scene descriptions"
    color = "#f6aa00"
    msets = [WebAdMovieSet, TVAdMovieSet]
    item_names = ["Scene descriptions"]
    is_vector = True


class ImpressionRatings(AbstractTask):
    arg = "ir"
    title = "Impression ratings"
    color = "#005aff"
    msets = [WebAdMovieSet, TVAdMovieSet]
    item_names = [
        "Beautiful",
        "Urban",
        "Nauseating",
        "Cheap",
        "Masculine",
        "Amusing",
        "Modern",
        "Simple",
        "Warm",
        "Sensitive",
        "Intelligent",
        "Static",
        "Human",
        "Clean",
        "Noisy",
        "Lush",
        "Bold",
        "Feminine",
        "Mechanical",
        "Ugly",
        "Rural",
        "Filthy",
        "Traditional",
        "Cute",
        "Gloomy",
        "Complex",
        "Cool",
        "Stupid",
        "Quiet",
        "Dynamic",
    ]


class AdEffectivenessIndices(AbstractTask):
    arg = "ae"
    title = "Ad effectiveness indices"
    color = "#ff4b00"
    msets = [WebAdMovieSet]
    item_names = [
        "Click through rate",
        "25% view completion rate",
        "50% view completion rate",
        "75% view completion rate",
        "100% view completion rate",
    ]


class AdPreferenceVotes(AbstractTask):
    arg = "ap"
    title = "Ad preference votes"
    color = "#03af7a"
    msets = [TVAdMovieSet]
    item_names = [
        "Preference",
        "Cast-Character",
        "Humorous",
        "Sexy",
        "Catchphrase",
        "Music-Sound",
        "Product attractiveness",
        "Persuasive",
        "Lame but lovable",
        "Cutting-edge",
        "Soothing",
        "Story",
        "Honest",
        "Movie-Image",
        "Reputable",
        "Cute",
        "Usage intention",
        "Persistent use",
        "Purchase intention",
    ]


class PreferenceRatings(AbstractTask):
    arg = "pr"
    title = "Preference ratings"
    color = "#880088"
    msets = [TVAdMovieSet]
    item_names = ["Preference ratings"]
    has_manual_rating = True

    @classmethod
    def get_subjects(cls, mset):
        subj_all = pd.read_csv(SUBJECTS_CSV_PATH)
        subjs = subj_all[subj_all.mset == mset.__name__]
        subjs = subjs[subjs[f"manual_PreferenceRatings"] == 1]
        return subjs.unique_id

def get_task_by_arg(arg) -> AbstractTask:
    for stim in AbstractTask.__subclasses__():
        if stim.arg == arg: return stim

    assert 0
