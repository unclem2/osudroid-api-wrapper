from .mod import Mod


class ModScoreV2(Mod):
    """ModScoreV2 class represents the score v2 mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Score V2"
        self.acronym = "V2"
        self.is_ranked = False
