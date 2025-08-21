from .mod import Mod
from .settings import Setting
from typing import override


class ModDifficultyAdjust(Mod):
    """ModDifficultyAdjust class represents the difficulty adjustment mod in osu!droid."""

    def __init__(
        self, ar: float = None, cs: float = None, od: float = None, hp: float = None
    ):

        super().__init__()
        self.name = "Difficulty Adjust"
        self.acronym = "DA"
        self.settings.add_setting(
            Setting(name="approach_rate", alternative_names=["ar"], value=ar, min_value=0.0, max_value=12.5, step=0.1)
        )
        self.settings.add_setting(
            Setting(name="circle_size", alternative_names=["cs"], value=cs, min_value=0.0, max_value=15.0, step=0.1)
        )
        self.settings.add_setting(
            Setting(name="overall_difficulty", alternative_names=["od"], value=od, min_value=0.0, max_value=11.0, step=0.1)
        )
        self.settings.add_setting(
            Setting(name="drain_rate", alternative_names=["hp"], value=hp, min_value=0.0, max_value=11.0, step=0.1)
        )
        self.is_ranked = False

    @property
    @override
    def as_standard_mod(self) -> str:
        string = f"{self.acronym}"
        stats = ", ".join(
            f"{setting.alternative_names[0].upper()}{setting.value}"
            for setting in self.settings
            if (setting.value is not None and setting.value != setting.default_value)
        )
        return f"{string}({stats})" if stats else string

    @property
    @override
    def as_droid_mod(self) -> dict:
        ret = {
            "acronym": self.acronym,
            "settings": {}
        }
        if self.settings.as_calculatable:
            for setting in self.settings:
                ret["settings"][setting.alternative_names[0]] = setting.value
        return ret
