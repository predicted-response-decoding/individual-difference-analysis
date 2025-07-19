from abc import ABC
from typing import Callable, Dict, List
import pandas as pd

from movieset import AbstractMovieSet, WebAdMovieSet, TVAdMovieSet
from config import SUBJECTS_CSV_PATH


class AbstractTask(ABC):
    arg: str
    title: str
    item_names: List[str]
    colors: Dict[Callable[[], AbstractMovieSet], str]
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
    colors = {WebAdMovieSet: "#fff100", TVAdMovieSet: "#f6aa00"}
    item_names = ["Scene descriptions"]
    is_vector = True


class ImpressionRatings(AbstractTask):
    arg = "ir"
    title = "Impression ratings"
    colors = {WebAdMovieSet: "#4dc4ff", TVAdMovieSet: "#005aff"}
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
    colors = {WebAdMovieSet: "#ff4b00"}
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
    colors = {TVAdMovieSet: "#03af7a"}
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
    colors = {TVAdMovieSet: "#000000"}
    item_names = ["Preference ratings"]
    has_manual_rating = True

    @classmethod
    def get_subjects(cls, mset):
        subj_all = pd.read_csv(SUBJECTS_CSV_PATH)
        subjs = subj_all[subj_all.mset == mset.__name__]
        subjs = subjs[subjs[f"manual_PreferenceRatings"] == 1]
        return subjs.unique_id
