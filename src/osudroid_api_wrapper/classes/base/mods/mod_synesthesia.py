from .mod import Mod


class ModSynesthesia(Mod):
    """ModSynesthesia class represents the synesthesia mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Synesthesia"
        self.acronym = "SY"
        self.is_ranked = False
