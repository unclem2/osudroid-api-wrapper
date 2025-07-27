from .setting import Setting
from typing import List


class SettingsList:
    """SettingsList class represents a collection of settings for mods in osu!droid."""

    def __init__(self):
        self.__settings: List[Setting] = []

    def add_setting(self, setting: Setting):
        """Add a new setting to the list."""
        self.settings.append(setting)

    @property
    def settings(self) -> List[Setting]:
        """List of settings."""
        return self.__settings

    @settings.setter
    def settings(self, new_settings: List[Setting]):
        """Set the list of settings."""
        if not isinstance(new_settings, list):
            raise TypeError("Settings must be a list of Setting objects.")
        self.__settings = new_settings

    def get_setting(self, name: str) -> Setting | None:
        """Get a setting by its name."""
        for setting in self.__settings:
            if setting.name == name:
                return setting
        return None

    def remove_setting(self, name: str):
        """Remove a setting by its name."""
        self.__settings = [
            setting for setting in self.__settings if setting.name != name
        ]

    def set_value(self, name: str, value: bool | int | float | str):
        """Set the value of a setting by its name."""
        setting = self.get_setting(name)
        if setting:
            setting.value = value
        else:
            raise ValueError(f"Setting '{name}' not found.")

    @property
    def as_json(self) -> list:
        """Return the settings list as a JSON serializable dictionary."""
        return [setting.as_json for setting in self.__settings]

    @property
    def as_calculatable(self) -> dict:
        """Return the settings in a format suitable for calculations."""
        ret = {}
        for setting in self.__settings:
            if setting.value is not None and setting.value != setting.default_value:
                ret[setting.name] = setting.value
        if ret == {}:
            return None
        return ret

    def __iter__(self):
        """Iterate over the settings."""
        return iter(self.__settings)
