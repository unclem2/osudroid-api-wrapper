from osudroid_api_wrapper import Replay
import pytest

def test_replay():
    score = Replay.load("tests/wtf.odr")
    print(score)
