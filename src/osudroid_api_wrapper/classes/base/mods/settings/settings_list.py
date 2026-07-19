
from .setting import Setting


class SettingsList:
    """SettingsList class represents a collection of settings for mods in osu!droid."""

    def __init__(self) -> None:
        self.__settings: list[Setting] = []

    def add_setting(self, setting: Setting) -> None:
        """Add a new setting to the list."""
        self.settings.append(setting)

    @property
    def settings(self) -> list[Setting]:
        """List of settings."""
        return self.__settings

    @settings.setter
    def settings(self, new_settings: list[Setting]) -> None:
        """Set the list of settings."""
        if not isinstance(new_settings, list):
            msg = "Settings must be a list of Setting objects."
            raise TypeError(msg)
        self.__settings = new_settings

    def get_setting(self, name: str) -> Setting | None:
        """Get a setting by its name."""
        for setting in self.__settings:
            if setting.name == name:
                return setting
            if name == setting.calculable_name:
                return setting
        return None

    def remove_setting(self, name: str) -> None:
        """Remove a setting by its name."""
        self.__settings = [
            setting
            for setting in self.__settings
            if name not in (setting.name, setting.calculable_name)
        ]

    def set_value(self, name: str, value: bool | float | str) -> None:
        """Set the value of a setting by its name."""
        setting = self.get_setting(name)
        if setting:
            setting.value = value
        else:
            msg = f"Setting '{name}' not found."
            raise ValueError(msg)

    @property
    def as_json(self) -> list:
        """Return the settings list as a JSON serializable dictionary."""
        return [setting.as_json for setting in self.__settings]

    @property
    def as_calculable(self) -> dict:
        """Return the settings in a format suitable for calculations."""
        ret = {}
        for setting in self.__settings:
            if setting.value is not None and setting.value != setting.default_value:
                ret.update(setting.as_calculable)
        return ret

    @property
    def as_droid(self) -> dict:
        """Return the settings in a format suitable for osu!droid."""
        ret = {}
        for setting in self.__settings:
            if setting.value is not None and setting.value != setting.default_value:
                ret.update(setting.as_droid)
        return ret

    def __iter__(self):
        """Iterate over the settings."""
        return iter(self.__settings)
