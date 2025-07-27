from .mod import Mod


class ModTraceable(Mod):
    """ModTraceable class represents the traceable mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Traceable"
        self.acronym = "TC"
