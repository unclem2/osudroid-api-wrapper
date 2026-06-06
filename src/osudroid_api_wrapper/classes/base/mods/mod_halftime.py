from .mod import Mod


class ModHalfTime(Mod):
    """ModHalftime class represents the halftime mod in osu!droid."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "Half Time"
        self.acronym = "HT"
