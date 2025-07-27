from .mod import Mod
from .settings import Setting
from enum import Enum
from typing import override


class ApproachStyle(Enum):
    """Enum for approach styles in the approach different mod."""

    LINEAR = 0
    GRAVITY = 1
    IN_OUT_1 = 2
    IN_OUT_2 = 3
    ACCELERATE_1 = 4
    ACCELERATE_2 = 5
    ACCELERATE_3 = 6
    DECELERATE_1 = 7
    DECELERATE_2 = 8
    DECELERATE_3 = 9
    BOUNCE_IN = 10
    BOUNCE_OUT = 11
    BOUNCE_IN_OUT = 12


class ModApproachDifferent(Mod):
    """ModApproachDifferent class represents the approach different mod in osu!droid."""

    def __init__(self, scale: float = None, style: ApproachStyle = None):
        super().__init__()
        self.name = "Approach Different"
        self.acronym = "AD"
        self.is_ranked = False
        self.settings.add_setting(
            Setting(
                name="scale",
                default_value=3.0,
                value=scale,
                min_value=1.5,
                max_value=10.0,
                step=0.1,
            )
        )
        self.settings.add_setting(
            Setting(
                name="style",
                default_value=ApproachStyle.LINEAR,
                value=style,
                min_value=0,
                max_value=len(ApproachStyle) - 1,
                step=1,
            )
        )

    @property
    @override
    def as_standard_mod(self):
        # This mod have options, but for some reason it is not displayed in the game
        return self.__acronym
