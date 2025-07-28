from .mod import Mod

class ModReplayV6(Mod):
    def __init__(self):
        super().__init__()
        self.acronym = "RV6"
        self.name = "Replay V6"
        self.is_ranked = False
        