from .mod import Mod


class ModPrecise(Mod):
    """ModPrecise class represents the precise mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Precise"
        self.acronym = "PR"

    # TODO: manual OD calculation
