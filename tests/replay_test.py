from osudroid_api_wrapper import Replay

def test_replay_load():
    replay = Replay().load("tests/5.odr")
    print(replay)
    assert replay.username == "unclem"