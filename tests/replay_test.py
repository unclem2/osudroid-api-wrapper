from osudroid_api_wrapper import Replay


def main():
    replay = Replay.load("2.odr")
    print(replay)


main()
