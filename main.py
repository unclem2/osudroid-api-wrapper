import ossapi
from classes.base.player import Player
from classes.base.beatmap import Beatmap
from classes.base.mods import Mods
from structs.profile import Profile

def main():
    beatmap = Beatmap.get_beatmap(beatmap_id=4933390)
    print(beatmap.to_dict)
    player = Player.from_api(uid=199195)
    print(player.to_dict)
    player = Player.from_api(username="unclem")
    print(player.to_dict)
    player = Player.from_droid_site(uid=199195)
    print(player.to_dict)
    profile = Profile.from_api(uid=199195)
    print(profile.to_dict)

    profile = Profile.from_api(username="unclem")
    print(profile.to_dict)

    profile = Profile.from_droid_site(uid=199195)
    print(profile.to_dict)

    profile = Profile.from_api(uid=199195)
    print(profile.to_dict)
 
main()