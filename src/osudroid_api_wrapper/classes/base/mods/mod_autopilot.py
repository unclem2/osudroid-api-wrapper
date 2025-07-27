from .mod import Mod


class ModAutopilot(Mod):
    """ModAutopilot class represents the autopilot mod in osu!droid."""

    def __init__(self):
        super().__init__()
        self.name = "Autopilot"
        self.acronym = "AP"
        self.is_ranked = False
