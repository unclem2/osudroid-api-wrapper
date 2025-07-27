from .mod import Mod


class ModReallyEasy(Mod):
    """ModReallyEasy class represents the really-easy mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Really Easy"
        self.acronym = "RE"
        self.is_ranked = False

    # TODO: Manual stats calculation
