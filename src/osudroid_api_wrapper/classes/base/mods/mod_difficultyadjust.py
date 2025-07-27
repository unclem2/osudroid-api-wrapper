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
            Setting(name="ar", value=ar, min_value=0.0, max_value=12.5, step=0.1)
        )
        self.settings.add_setting(
            Setting(name="cs", value=cs, min_value=0.0, max_value=15.0, step=0.1)
        )
        self.settings.add_setting(
            Setting(name="od", value=od, min_value=0.0, max_value=11.0, step=0.1)
        )
        self.settings.add_setting(
            Setting(name="hp", value=hp, min_value=0.0, max_value=11.0, step=0.1)
        )
        self.is_ranked = False

    @property
    @override
    def as_standard_mod(self) -> str:
        string = f"{self.acronym}"
        stats = ", ".join(
            f"{setting.name.upper()}{setting.value}"
            for setting in self.settings
            if (setting.value is not None and setting.value != setting.default_value)
        )
        return f"{string}({stats})" if stats else string
