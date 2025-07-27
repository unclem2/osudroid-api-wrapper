from .mod import Mod


class ModDoubleTime(Mod):
    """ModDoubleTime class represents the doubletime mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Double Time"
        self.acronym = "DT"
