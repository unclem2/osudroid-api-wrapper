from .mod import Mod
from .settings import Setting
from typing import override


class ModHidden(Mod):
    """ModHidden class represents the hidden mod in osu!droid."""

    def __init__(self, isOnlyFadeApproachCircles: bool = False):
        super().__init__()
        self.name = "Hidden"
        self.acronym = "HD"
        self.settings.add_setting(
            Setting(
                name="isOnlyFadeApproachCircles",
                default_value=False,
                value=isOnlyFadeApproachCircles,
            )
        )

    @property
    @override
    def as_standard_mod(self) -> str:
        # This mod have options, but for some reason they are not displayed in the game
        return self.acronym
