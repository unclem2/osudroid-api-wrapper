"""Used https://github.com/xjunko/Yuzumi/blob/main/objects/beatmap.py as a reference
Original license from xjunko/Yuzumi:

MIT License

Copyright (c) 2021 FireRedz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import dotenv
import os
import requests

dotenv.load_dotenv()


class Beatmap:
    def __init__(self):
        self.beatmap_id: int = None
        self.beatmapset_id: int = None
        self.md5: str = None
        self.artist: str = None
        self.title: str = None
        self.version: str = None
        self.creator: str = None
        self.combo: int = None
        self.ar: float = None
        self.od: float = None
        self.hp: float = None
        self.cs: float = None
        self.bpm: float = None
        self.star: float = None
        self.length: int = None

    @classmethod
    def get_beatmap(cls, beatmap_id: int = None, md5: str = None) -> "Beatmap":
        key = os.getenv("OSU_API_KEY")

        beatmap = cls()
        url = "https://old.ppy.sh/api/get_beatmaps"
        if key is "":
            raise ValueError(
                "API key is not set. Please set the OSU_API_KEY environment variable."
            )
        if beatmap_id is not None:
            params = {"k": key, "b": beatmap_id}
            response = requests.get(url, params=params)
            data = response.json()
            if len(data) == 0:
                return None
            data = data[0]

        elif md5 is not None:
            params = {"k": key, "h": md5}
            response = requests.get(url, params=params)
            data = response.json()
            if len(data) == 0:
                return None
            if data == []:
                return None
            data = data[0]

        beatmap.beatmap_id = int(data["beatmap_id"])
        beatmap.beatmapset_id = int(data["beatmapset_id"])
        beatmap.md5 = data["file_md5"]
        beatmap.artist = data["artist"]
        beatmap.title = data["title"]
        beatmap.version = data["version"]
        beatmap.creator = data["creator"]
        beatmap.ar = float(data["diff_approach"])
        beatmap.od = float(data["diff_overall"])
        beatmap.hp = float(data["diff_drain"])
        beatmap.cs = float(data["diff_size"])
        beatmap.bpm = float(data["bpm"])
        beatmap.star = float(data["difficultyrating"])
        beatmap.length = int(data["total_length"])
        beatmap.combo = int(data["max_combo"])

        return beatmap

    @property
    def to_dict(self):
        return {
            "beatmap_id": self.beatmap_id,
            "beatmapset_id": self.beatmapset_id,
            "md5": self.md5,
            "artist": self.artist,
            "title": self.title,
            "version": self.version,
            "creator": self.creator,
            "ar": self.ar,
            "od": self.od,
            "hp": self.hp,
            "cs": self.cs,
            "bpm": self.bpm,
            "star": self.star,
            "length": self.length,
            "combo": self.combo,
        }
