from typing import overload


class Setting:
    @overload
    def __init__(self, name: str, default_value: bool, value: bool = None) -> None: ...

    @overload
    def __init__(
        self,
        name: str,
        default_value: int = None,
        min_value: int = None,
        max_value: int = None,
        step: int = None,
        value: int = None,
    ) -> None: ...

    @overload
    def __init__(
        self,
        name: str,
        default_value: float = None,
        min_value: float = None,
        max_value: float = None,
        step: float = None,
        value: float = None,
    ) -> None: ...

    def __init__(
        self,
        name: str,
        default_value=None,
        min_value=None,
        max_value=None,
        step=None,
        value=None,
    ) -> None:
        self.__name = name
        self.__default_value = default_value
        self.__min = min_value
        self.__max = max_value
        self.__step = step
        self.__value = value

    @property
    def name(self) -> str:
        """Name of the setting."""
        return self.__name

    @property
    def value(self) -> bool | int | float:
        """Current value of the setting."""
        return self.__value if self.__value is not None else self.__default_value

    @value.setter
    def value(self, new_value):
        """Set the value of the setting."""
        if self.__min is not None and new_value < self.__min:
            raise ValueError(f"Value must be at least {self.__min}.")
        if self.__max is not None and new_value > self.__max:
            raise ValueError(f"Value must be at most {self.__max}.")
        self.__value = new_value

    @property
    def default_value(self) -> bool | int | float | None:
        """Default value of the setting."""
        return self.__default_value

    @property
    def min_value(self) -> int | float | None:
        """Minimum value of the setting."""
        return self.__min

    @property
    def max_value(self) -> int | float | None:
        """Maximum value of the setting."""
        return self.__max

    @property
    def step(self) -> int | float | None:
        """Step value for the setting."""
        return self.__step

    @property
    def as_json(self) -> dict:
        """Return the setting as a JSON serializable dictionary."""
        return {
            "name": self.__name,
            "value": self.value,
            "default_value": self.__default_value,
            "min_value": self.__min,
            "max_value": self.__max,
            "step": self.__step,
        }

    @property
    def as_calculatable(self) -> dict:
        """Return the setting as a dictionary for pp calculations."""
        return {
            "name": self.__name,
            "value": self.value,
        }
