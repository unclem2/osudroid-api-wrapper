import pytest
from osudroid_api_wrapper import Profile


def test_profile_site():
    profile = Profile.from_droid_site(199195)
    assert profile.player.username == "unclem"


def test_profile_api_username():
    profile = Profile.from_api(username="unclem")
    assert profile.player.username == "unclem"


def test_profile_api_uid():
    profile = Profile.from_api(uid=199195)
    assert profile.player.username == "unclem"
