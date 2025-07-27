from .mod import Mod
from .settings import Setting
from typing import override


class ModRandom(Mod):
    """ModRandom class represents the random mod in osu!droid."""

    def __init__(self, seed: int = None, angle_sharpness: float = None):
        super().__init__()
        self.name = "Random"
        self.acronym = "RD"
        self.is_ranked = False
        self.settings.add_setting(
            Setting(
                name="seed",
                default_value=0,
                value=seed,
                min_value=0,
                max_value=4294967295,
                step=1,
            )
        )
        self.settings.add_setting(
            Setting(
                name="angleSharpness",
                default_value=7.0,
                value=angle_sharpness,
                min_value=1.0,
                max_value=10.0,
                step=0.1,
            )
        )

    @property
    @override
    def as_standard_mod(self) -> str:
        # This mod has options, but for some reason they are not displayed in the game
        return self.acronym
