from .mod import Mod


class ModEasy(Mod):
    """ModEasy class represents the easy mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Easy"
        self.acronym = "EZ"
