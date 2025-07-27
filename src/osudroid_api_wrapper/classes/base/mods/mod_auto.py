from .mod import Mod


class ModAuto(Mod):
    """ModAutoplay class represents the autoplay mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Auto"
        self.acronym = "AT"
        self.is_ranked = False
