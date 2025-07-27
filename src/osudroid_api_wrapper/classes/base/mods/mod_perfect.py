from .mod import Mod


class ModPerfect(Mod):
    """ModPerfect class represents the perfect mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Perfect"
        self.acronym = "PF"
