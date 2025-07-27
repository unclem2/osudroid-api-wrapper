from .mod import Mod
from .settings import SettingsList, Setting
from typing import override


class ModFlashlight(Mod):
    """ModFlashlight class represents the flashlight mod in osu!droid."""

    def __init__(self, areaFollowDelay: float = None):
        super().__init__()
        self.name = "Flashlight"
        self.acronym = "FL"
        self.settings.add_setting(
            Setting(
                name="areaFollowDelay",
                min_value=0.12,
                max_value=1.2,
                default_value=0.12,
                value=areaFollowDelay,
                step=0.12,
            )
        )

    @property
    @override
    def as_standard_mod(self) -> str:
        if (
            self.settings.get_setting("areaFollowDelay").value is not None
            and self.settings.get_setting("areaFollowDelay").value
            != self.settings.get_setting("areaFollowDelay").default_value
        ):
            return (
                f"{self.acronym}({self.settings.get_setting('areaFollowDelay').value}s)"
            )
        return self.acronym
