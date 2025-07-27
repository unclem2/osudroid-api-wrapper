from .mod import Mod


class ModRelax(Mod):
    """ModRelax class represents the relax mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Relax"
        self.acronym = "RX"
        self.is_ranked = False
