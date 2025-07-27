from .mod import Mod


class ModHardRock(Mod):
    """ModHardRock class represents the hardrock mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Hard Rock"
        self.acronym = "HR"
