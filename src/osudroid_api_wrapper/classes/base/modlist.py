from .mods import (
    Mod,
    ModApproachDifferent,
    ModAuto,
    ModAutopilot,
    ModCustomSpeed,
    ModDifficultyAdjust,
    ModDoubleTime,
    ModEasy,
    ModFlashlight,
    ModHardRock,
    ModHalfTime,
    ModHidden,
    ModMuted,
    ModNightcore,
    ModNoFail,
    ModPerfect,
    ModPrecise,
    ModReallyEasy,
    ModRelax,
    ModScoreV2,
    ModSuddenDeath,
    ModSynesthesia,
    ModTraceable,
    ModWindDown,
    ModWindUp,
    ModRandom,
    ModMirror,
    ModFreezeFrame,
    ModSmallCircles,
    ModReplayV6,
)
from typing import List
import re
import json

# TODO: Fix mod order, remove repeated mapping declarations, check acronyms, add missing mods


class ModList:

    def __init__(self, mods=None):
        self.__mods: List[Mod] = mods

    @classmethod
    def from_droid_site(cls, mods: str):

        mod_abbreviations: dict[str, type[Mod]] = {
            "None": "",
            "Easy": ModEasy,
            "HalfTime": ModHalfTime,
            "NoFail": ModNoFail,
            "ReallyEasy": ModReallyEasy,
            "DoubleTime": ModDoubleTime,
            "Flashlight": ModFlashlight,
            "HardRock": ModHardRock,
            "Hidden": ModHidden,
            "Nightcore": ModNightcore,
            "Perfect": ModPerfect,
            "Precise": ModPrecise,
            "SuddenDeath": ModSuddenDeath,
            "Traceable": ModTraceable,
        }
        mod_list = []
        for mod in mods.split(","):
            mod = mod.strip()
            if mod.startswith("CustomSpeed"):
                mod_list.append(ModCustomSpeed(float(mod.split("(")[1][:-2])))
                continue

            if mod in mod_abbreviations:
                if mod == "None":
                    continue
                mod_list.append(mod_abbreviations[mod]())

            else:
                raise ValueError(f"Unknown mod: {mod}")

        return cls(mod_list)

    @classmethod
    def from_droid_replay_v6(cls, mods: list):
        mod_mapping = {
            "MOD_NOFAIL": ModNoFail,
            "MOD_EASY": ModEasy,
            "MOD_HIDDEN": ModHidden,
            "MOD_HARDROCK": ModHardRock,
            "MOD_SUDDENDEATH": ModSuddenDeath,
            "MOD_DOUBLETIME": ModDoubleTime,
            "MOD_RELAX": ModRelax,
            "MOD_HALFTIME": ModHalfTime,
            "MOD_NIGHTCORE": ModNightcore,
            "MOD_FLASHLIGHT": ModFlashlight,
            "MOD_SCOREV2": ModScoreV2,
            "MOD_AUTOPILOT": ModAutopilot,
            "MOD_AUTO": ModAuto,
            "MOD_PRECISE": ModPrecise,
            "MOD_REALLYEASY": ModReallyEasy,
            "MOD_SMALLCIRCLES": ModSmallCircles,
            "MOD_PERFECT": ModPerfect,
            "MOD_SUDDENDEATH": ModSuddenDeath,
        }
        mod_list = []
        for mod in mods:
            if mod in mod_mapping:
                mod_list.append(mod_mapping[mod]())
            else:
                raise ValueError(f"Unknown mod: {mod}")

        return cls(mod_list)

    @classmethod
    def from_dict(cls, mods: list):
        mod_classes: List[type[Mod]] = [
            ModEasy,
            ModHalfTime,
            ModNoFail,
            ModReallyEasy,
            ModDoubleTime,
            ModFlashlight,
            ModHardRock,
            ModHidden,
            ModNightcore,
            ModPerfect,
            ModPrecise,
            ModSuddenDeath,
            ModTraceable,
            ModAuto,
            ModAutopilot,
            ModRelax,
            ModCustomSpeed,
            ModDifficultyAdjust,
            ModMirror,
            ModRandom,
            ModScoreV2,
            ModApproachDifferent,
            ModFreezeFrame,
            ModMuted,
            ModSynesthesia,
            ModWindDown,
            ModWindUp,
        ]

        mod_mapping = {cls_().acronym: cls_() for cls_ in mod_classes}

        mod_list = []
        for mod in mods:
            acronym = mod["acronym"]
            if acronym in mod_mapping:
                mod_instance = mod_mapping[acronym]
                settings = mod.get("settings", {})
                for key, value in settings.items():
                    try:
                        mod_instance.settings.set_value(key, value)
                    except ValueError as e:
                        raise ValueError(
                            f"Invalid setting '{key}' for mod '{acronym}': {e}"
                        )
                mod_list.append(mod_instance)

        return cls(mod_list)

    @classmethod
    def from_droid_letters(cls, mods: str):
        mod_mapping: dict[str, type[Mod]] = {
            "n": ModNoFail,
            "e": ModEasy,
            "h": ModHidden,
            "r": ModHardRock,
            "u": ModSuddenDeath,
            "d": ModDoubleTime,
            "x": ModCustomSpeed,
            "t": ModHalfTime,
            "c": ModNightcore,
            "i": ModFlashlight,
            "v": ModScoreV2,
            "p": ModAutopilot,
            "a": ModApproachDifferent,
            "s": ModPrecise,
            "l": ModReallyEasy,
            "m": ModSynesthesia,
            "f": ModPerfect,
            "b": ModTraceable,
        }
        mod_list = []
        mod_chars = re.sub(r"\bx\d+\.\d+\b|[^a-z]", "", mods)
        for char in mod_chars:
            if char in mod_mapping:
                mod_list.append(mod_mapping[char]())
            else:
                raise ValueError(f"Unknown mod character: {char}")

        matchar = re.search(r"\bAR(\d+\.\d+)\b", mods)
        matchcs = re.search(r"\bCS(\d+\.\d+)\b", mods)
        matchod = re.search(r"\bOD(\d+\.\d+)\b", mods)
        matchhp = re.search(r"\bHP(\d+\.\d+)\b", mods)
        matchsm = re.search(r"\bx(\d+\.\d+)\b", mods, re.IGNORECASE)
        matchfld = re.search(r"\bFLD(\d+\.\d+)\b", mods)

        if matchar or matchcs or matchod or matchhp:
            da = ModDifficultyAdjust(
                ar=float(matchar.group(1)) if matchar else None,
                cs=float(matchcs.group(1)) if matchcs else None,
                od=float(matchod.group(1)) if matchod else None,
                hp=float(matchhp.group(1)) if matchhp else None,
            )
            mod_list.append(da)
        if matchsm:
            mod_list.append(ModCustomSpeed(float(matchsm.group(1))))
        if matchfld:
            if mod_list.count(ModFlashlight) == 0:
                mod_list.append(ModFlashlight(matchfld.group(1)))
        return cls(mod_list)

    @property
    def mods(self) -> List[Mod]:
        """List of mods."""
        return self.__mods

    def get_mod(self, acronym: str) -> Mod | None:
        """Get a mod by its acronym."""
        for mod in self.__mods:
            if mod.acronym == acronym:
                return mod
        return None

    def add_mod(self, mod: Mod):
        """Add a new mod to the list."""
        if not isinstance(mod, Mod):
            raise TypeError("mod must be an instance of Mod.")
        self.__mods.append(mod)

    @property
    def as_json(self) -> List[dict]:
        """Return the mod list as a JSON serializable list with full mod details."""
        return [mod.as_json for mod in self.__mods]

    @property
    def as_standard_mods(self) -> str:
        """Return the mod list as a string of mod acronyms and settings."""
        return "".join(mod.as_standard_mod for mod in self.__mods if mod.acronym)

    @property
    def as_calculatable_mods(self) -> list:
        """Return the mod list as a string of mods suitable for pp calculation."""
        return [mod.as_calculatable for mod in self.__mods]

    @property
    def as_json_string(self) -> str:
        """Return the mod list as a JSON string."""
        return json.dumps(self.as_calculatable_mods, separators=(",", ":"))

    def __iter__(self):
        """Iterate over the mods."""
        return iter(self.__mods)
