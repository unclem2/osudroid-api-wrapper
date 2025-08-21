from osudroid_api_wrapper import ModList
import pytest
from osudroid_api_wrapper import mods
import logging
import pytest
from osudroid_api_wrapper import ModList
from osudroid_api_wrapper import mods
from osudroid_api_wrapper.classes.base.mods.mod import Mod
from osudroid_api_wrapper.classes.base.mods.settings.settings_list import SettingsList

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_modlist_from_droid_site():

    mods_data = [
        
        {"acronym": "PR"},
        {"acronym": "FL", "settings": {"areaFollowDelay": 0.96}},
        {"acronym": "HT"},
        {"acronym": "CS", "settings": {"rateMultiplier": 1.3}},
        {"acronym": "MR", "settings": {"flippedAxes": 1}},
        {"acronym": "WU", "settings": {"initialRate": 0.8, "finalRate": 1.35}},
        {"acronym": "SY"},
        {"acronym": "RX"},
        {"acronym": "DA", "settings": {"cs": 9.4, "ar": 6.1, "od": 7, "hp": 6}},
        {"acronym": "TC"},
        {"acronym": "FR"},
        {"acronym": "RD", "settings": {"seed": 129393216, "angleSharpness": 4.9}},
        {
            "acronym": "MU",
            "settings": {
                "inverseMuting": True,
                "enableMetronome": False,
                "muteComboCount": 100,
                "affectsHitSounds": False,
            },
        },
    ]
    mod_list = ModList.from_dict(mods_data)
    logger.info(mod_list.as_json)
    logger.info(mod_list.as_calculable_mods)
    logger.info(mod_list.as_standard_mods)
    assert isinstance(mod_list.as_json, list)
    assert isinstance(mod_list.as_calculable_mods, list)
    assert isinstance(mod_list.as_standard_mods, str)
    assert len(mod_list.mods) == len(mods_data)

