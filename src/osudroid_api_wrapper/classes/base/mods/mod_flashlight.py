from typing import override

from .mod import Mod
from .settings import Setting


class ModFlashlight(Mod):
    """ModFlashlight class represents the flashlight mod in osu!droid."""

    def __init__(self, areaFollowDelay: float | None = None) -> None:
        super().__init__()
        self.name = "Flashlight"
        self.acronym = "FL"
        self.settings.add_setting(
            Setting(
                name="areaFollowDelay",
                calculable_name="follow_delay",
                min_value=0, # 0 for compatibility purposes
                max_value=1.2,
                default_value=0.12,
                value=areaFollowDelay,
                step=0.12,
            ),
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
