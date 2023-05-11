class MovieSetDefault:
    def __init__(self) -> None:
        self.arg: str
        self.title: str


class TaskDefault:
    def __init__(self) -> None:
        self.arg: str
        self.title: str
        self.item_names: list
        self.colors: dict
        self.isVector: bool = False
        self.has_manual_rating: bool = False

    def from_movie_set(self, mset) -> None:
        if not (mset in self.colors.keys()):
            return False
        self.color = self.colors[mset]
        self.title_movie_set = mset().title
        return True


class WebAdMovieSet(MovieSetDefault):
    def __init__(self) -> None:
        super().__init__()
        self.arg = "web"
        self.title = "Web ad movie set"


class TVAdMovieSet(MovieSetDefault):
    def __init__(self) -> None:
        super().__init__()
        self.arg = "tv"
        self.title = "TV ad movie set"


MOVIE_SET_ALL = [WebAdMovieSet, TVAdMovieSet]


class SceneDescriptions(TaskDefault):
    def __init__(self) -> None:
        super().__init__()
        self.arg = "sd"
        self.title = "Scene descriptions"
        self.colors = {WebAdMovieSet: "#fff100", TVAdMovieSet: "#f6aa00"}
        self.item_names = [""]
        self.isVector = True


class ImpressionRatings(TaskDefault):
    def __init__(self) -> None:
        super().__init__()
        self.arg = "ir"
        self.title = "Impression ratings"
        self.colors = {WebAdMovieSet: "#4dc4ff", TVAdMovieSet: "#005aff"}
        self.item_names = [
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


class AdEffectivenessIndices(TaskDefault):
    def __init__(self) -> None:
        super().__init__()
        self.arg = "ae"
        self.title = "Ad effectiveness indices"
        self.colors = {WebAdMovieSet: "#ff4b00"}
        self.item_names = [
            "Click through rate",
            "25% view completion rate",
            "50% view completion rate",
            "75% view completion rate",
            "100% view completion rate",
        ]


class AdPreferenceVotes(TaskDefault):
    def __init__(self) -> None:
        super().__init__()
        self.arg = "ap"
        self.title = "Ad preference votes"
        self.colors = {TVAdMovieSet: "#03af7a"}
        self.item_names = [
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


class PreferenceRatings(TaskDefault):
    def __init__(self) -> None:
        super().__init__()
        self.arg = "pr"
        self.title = "Preference ratings"
        self.colors = {TVAdMovieSet: "#000000"}
        self.item_names = [""]
        self.has_manual_rating = True


TASK_ALL = [
    SceneDescriptions,
    ImpressionRatings,
    AdEffectivenessIndices,
    AdPreferenceVotes,
    PreferenceRatings,
]
