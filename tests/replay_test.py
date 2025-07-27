from osudroid_api_wrapper import Replay


def main():
    replay = Replay.load("tests/7.odr")
    print(replay)


main()
