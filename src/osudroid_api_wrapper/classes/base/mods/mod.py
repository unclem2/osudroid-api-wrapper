from abc import ABC, abstractmethod
from typing import List
from .settings.settings_list import SettingsList


class Mod(ABC):
    """Base class for all mods."""

    def __init__(self):
        self.__name: str = None
        self.__acronym: str = None
        self.__settings: SettingsList = SettingsList()
        self.__is_ranked: bool = True

    @property
    def name(self) -> str:
        """Name of the mod."""
        return self.__name

    @name.setter
    def name(self, new_name: str):
        """Set the name of the mod."""
        if self.__name is not None:
            raise ValueError("Name can only be set once.")
        self.__name = new_name

    @property
    def acronym(self) -> str:
        """Acronym of the mod."""
        return self.__acronym

    @acronym.setter
    def acronym(self, new_acronym: str):
        """Set the acronym of the mod."""
        if self.__acronym is not None:
            raise ValueError("Acronym can only be set once.")
        self.__acronym = new_acronym

    @property
    def is_ranked(self) -> bool:
        """Submit status of the mod"""
        return self.__is_ranked

    @is_ranked.setter
    def is_ranked(self, new_is_ranked: bool):
        """Set the ranked status of the mod."""
        self.__is_ranked = new_is_ranked

    @property
    def as_json(self) -> dict:
        """Return the mod as a JSON serializable dictionary."""
        return {
            "name": self.__name,
            "acronym": self.__acronym,
            "settings": self.__settings.as_json,
            "is_ranked": self.__is_ranked,
        }

    @property
    def as_standard_mod(self) -> str:
        """Return the mod as a standard mod instance."""
        return self.__acronym

    @property
    def as_calculatable(self) -> dict:
        """Return the mod in a format suitable for pp calculation."""
        ret = {
            "acronym": self.__acronym,
        }
        if self.__settings.as_calculatable:
            ret["settings"] = self.__settings.as_calculatable
        return ret

    @property
    def settings(self) -> SettingsList:
        """Settings of the mod."""
        return self.__settings

    @settings.setter
    def settings(self, new_settings: SettingsList):
        """Set the settings of the mod."""
        if not isinstance(new_settings, SettingsList):
            raise TypeError("Settings must be an instance of SettingsList.")
        self.__settings = new_settings

    def __repr__(self):
        return f"{self.__name}({self.settings})"

    def __str__(self):
        return f"{self.__name}({self.settings})"
