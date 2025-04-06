class Mods:
    def __init__(self, mods=None):
        self.mods = mods or []
        self.speed_multiplier = None

    @classmethod
    def from_droid_site(cls, mods: str):
        mod_abbreviations = {
            'None': 'NM', 'NoFail': 'NF', 'Easy': 'EZ', 'HalfTime': 'HT',
            'Hidden': 'HD', 'HardRock': 'HR', 'DoubleTime': 'DT', 'Flashlight': 'FL',
            'Precise': 'PR', 'SuddenDeath': 'SD', 'Perfect': 'PF', 'NightCore': 'NC',
        }
        return cls([mod_abbreviations.get(mod, mod) for mod in mods.split(",")])

    @classmethod
    def from_droid_replay(cls, mods: list):
        mod_mapping = {
            "MOD_NOFAIL": "NF", "MOD_EASY": "EZ", "MOD_HIDDEN": "HD",
            "MOD_HARDROCK": "HR", "MOD_SUDDENDEATH": "SD", "MOD_DOUBLETIME": "DT",
            "MOD_RELAX": "RX", "MOD_HALFTIME": "HT", "MOD_NIGHTCORE": "NC",
            "MOD_FLASHLIGHT": "FL", "MOD_SCOREV2": "V2", "MOD_AUTOPILOT": "AP",
            "MOD_AUTO": "AT", "MOD_PRECISE": "PR", "MOD_REALLYEASY": "REZ",
            "MOD_SMALLCIRCLES": "SC", "MOD_PERFECT": "PF", "MOD_SUDDENDEATH": "SU",
        }
        return cls([mod_mapping.get(mod, mod) for mod in mods])

    @classmethod
    def from_droid_api(cls, mods: dict):
        instance = cls(list(mods))
        instance.speed_multiplier = next((mod for mod in mods if mod.startswith("x")), None)
        return instance


    @property
    def to_dict(self):
        return {
            "mods": self.mods,
            "speed_multiplier": self.speed_multiplier
        }