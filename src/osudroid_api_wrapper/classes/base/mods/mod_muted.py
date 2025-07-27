from .mod import Mod
from .settings import Setting
from typing import override


class ModMuted(Mod):
    """ModMuted class represents the muted mod in osu!droid."""

    def __init__(
        self,
        inverseMuting: bool = False,
        enableMetronome: bool = False,
        muteComboCount: int = 100,
        affectsHitSounds: bool = False,
    ):
        super().__init__()
        self.name = "Muted"
        self.acronym = "MU"
        self.is_ranked = False
        self.settings.add_setting(
            Setting(
                name="inverseMuting",
                default_value=False,
                value=inverseMuting,
            )
        )
        self.settings.add_setting(
            Setting(
                name="enableMetronome",
                default_value=False,
                value=enableMetronome,
            )
        )
        self.settings.add_setting(
            Setting(
                name="muteComboCount",
                default_value=100,
                value=muteComboCount,
                min_value=0,
                max_value=500,
                step=1,
            )
        )
        self.settings.add_setting(
            Setting(
                name="affectsHitSounds",
                default_value=False,
                value=affectsHitSounds,
            )
        )

    @property
    @override
    def as_standard_mod(self) -> str:
        # This mod has options, but for some reason they are not displayed in the game
        return self.acronym
