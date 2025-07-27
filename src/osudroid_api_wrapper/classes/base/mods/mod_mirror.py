from .mod import Mod
from enum import Enum
from .settings import Setting
from typing import override


class FlippedAxes(Enum):
    """Enum for flipped axes in the mirror mod."""

    HORIZONTAL = 0
    VERTICAL = 1
    BOTH = 2


class ModMirror(Mod):
    """ModMirror class represents the mirror mod in osu!droid."""

    def __init__(self, flippedAxes: FlippedAxes = None):
        super().__init__()
        self.name = "Mirror"
        self.acronym = "MR"
        self.is_ranked = False
        self.settings.add_setting(
            Setting(
                name="flippedAxes",
                default_value=FlippedAxes.HORIZONTAL,
                value=flippedAxes,
                min_value=0,
                max_value=2,
                step=1,
            )
        )

    @property
    @override
    def as_standard_mod(self) -> str:
        axis = self.settings.get_setting("flippedAxes").value
        if axis == FlippedAxes.HORIZONTAL.value:
            return f"{self.acronym}(↔)"
        elif axis == FlippedAxes.VERTICAL.value:
            return f"{self.acronym}(↕)"
        elif axis == FlippedAxes.BOTH.value:
            return f"{self.acronym}(↔↕)"
