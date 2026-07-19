from .setting import Setting
from typing import override, overload

class DifficultyAdjustSetting(Setting):
    @overload
    def __init__(
        elf,
        name: str,
        calculable_name: str | None = None,
        default_value: float | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
        step: float | None = None,
        value: float | None = None,
        original_value: float | None = None,
        ):
        ...

    def __init__(
        self,
        name: str,
        calculable_name: str | None = None,
        default_value=None,
        min_value=None,
        max_value=None,
        step=None,
        value=None,
        original_value=None
        ):
        super().__init__(name=name, calculable_name=calculable_name, default_value=default_value, min_value=min_value, max_value=max_value, step=step, value=value)
        self.__original_value = original_value

    @property
    def original_value(self):
        return self.__original_value

    @original_value.setter
    def original_value(self, new_value):
        """Sets the original value of the setting."""
        if self.min_value is not None and new_value < self.min_value:
            msg = f"Value must be at least {self.min_value}."
            raise ValueError(msg)
        if self.max_value is not None and new_value > self.max_value:
            msg = f"Value must be at most {self.max_value}."
            raise ValueError(msg)
        self.__original_value = new_value

    @property
    def as_json(self) -> dict:
        """Return the setting as a JSON serializable dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "default_value": self.default_value,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "step": self.step,
            "original_value": self.__original_value
        }


    @property
    def as_droid(self) -> dict:
        """Return the setting as a dictionary suitable for osu!droid."""
        return {self.name: {"original": self.__original_value, "adjusted": self.value}}
