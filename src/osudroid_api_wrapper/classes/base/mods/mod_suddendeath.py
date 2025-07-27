from .mod import Mod


class ModSuddenDeath(Mod):
    """ModSuddenDeath class represents the sudden-death mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Sudden Death"
        self.acronym = "SD"
