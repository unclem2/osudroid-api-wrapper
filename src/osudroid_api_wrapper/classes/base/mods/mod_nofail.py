from .mod import Mod


class ModNoFail(Mod):
    """ModNoFail class represents the no-fail mod in osu!droid."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "No Fail"
        self.acronym = "NF"
