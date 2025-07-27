from .mod import Mod
from .settings import Setting
from typing import override


class ModWindUp(Mod):
    """ModWindUp class represents the wind up mod in osu!droid."""

    def __init__(self, initialRate: float = None, finalRate: float = None):
        super().__init__()
        self.name = "Wind Up"
        self.acronym = "WU"
        self.is_ranked = False
        self.settings.add_setting(
            Setting(
                name="initialRate",
                default_value=1.0,
                value=initialRate,
                min_value=0.5,
                max_value=1.95,
                step=0.05,
            )
        )
        self.settings.add_setting(
            Setting(
                name="finalRate",
                default_value=1.5,
                value=finalRate,
                min_value=0.55,
                max_value=2.0,
                step=0.05,
            )
        )

    @property
    @override
    def as_standard_mod(self) -> str:
        initial_rate = self.settings.get_setting("initialRate").value
        final_rate = self.settings.get_setting("finalRate").value
        if initial_rate is None:
            initial_rate = self.settings.get_setting("initialRate").default_value
        if final_rate is None:
            final_rate = self.settings.get_setting("finalRate").default_value
        return f"{self.acronym}({initial_rate}x - {final_rate}x)"
