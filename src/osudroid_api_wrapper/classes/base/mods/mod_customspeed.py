from typing import override

from .mod import Mod
from .settings import Setting


class ModCustomSpeed(Mod):
    """ModCustomSpeed class represents the custom speed mod in osu!droid."""

    def __init__(self, rateMultiplier: float | None = None) -> None:
        super().__init__()
        self.name = "Custom Speed"
        self.acronym = "CS"
        self.settings.add_setting(
            Setting(
                name="rateMultiplier",
                default_value=1.0,
                value=rateMultiplier,
                min_value=0.5,
                max_value=2.0,
                step=0.05,
            ),
        )

    @property
    @override
    def as_standard_mod(self) -> str:
        return f"{self.acronym}(x{self.settings.get_setting('rateMultiplier').value})"
