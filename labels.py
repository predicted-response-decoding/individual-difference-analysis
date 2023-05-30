from abc import ABC
from typing import Callable, Dict, List


class ClassNameMixin:
    def __init__(self) -> None:
        self.name: str = self.__class__.__name__


class AbstractMovieSet(ABC, ClassNameMixin):
    arg: str
    title: str


class AbstractTask(ABC, ClassNameMixin):
    arg: str
    title: str
    item_names: List[str]
    colors: Dict[Callable[[], AbstractMovieSet], str]
    is_vector: bool = False
    has_manual_rating: bool = False

    def from_movie_set(self, mset: AbstractMovieSet) -> bool:
        if not (mset.__class__ in self.colors.keys()):
            return False
        self.color = self.colors[mset.__class__]
        self.title_movie_set = mset.title
        return True


class WebAdMovieSet(AbstractMovieSet):
    arg = "web"
    title = "Web ad movie set"


class TVAdMovieSet(AbstractMovieSet):
    arg = "tv"
    title = "TV ad movie set"


MOVIE_SET_CLASS_ALL: List[Callable[[], AbstractMovieSet]] = [
    WebAdMovieSet,
    TVAdMovieSet,
]


class SceneDescriptions(AbstractTask):
    arg = "sd"
    title = "Scene descriptions"
    colors = {WebAdMovieSet: "#fff100", TVAdMovieSet: "#f6aa00"}
    item_names = [""]
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
        "Cast/Character",
        "Humorous",
        "Sexy",
        "Catchphrase",
        "Music/Sound",
        "Product attractiveness",
        "Persuasive",
        "Lame but lovable",
        "Cutting-edge",
        "Soothing",
        "Story",
        "Honest",
        "Movie/Image",
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
    item_names = [""]
    has_manual_rating = True


TASK_CLASS_ALL: List[Callable[[], AbstractTask]] = [
    SceneDescriptions,
    ImpressionRatings,
    AdEffectivenessIndices,
    AdPreferenceVotes,
    PreferenceRatings,
]
