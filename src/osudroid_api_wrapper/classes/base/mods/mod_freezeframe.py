from .mod import Mod


class ModFreezeFrame(Mod):
    """ModFreezeFrame class represents the freeze frame mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Freeze Frame"
        self.acronym = "FR"
        self.is_ranked = False
