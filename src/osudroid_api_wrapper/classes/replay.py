"""Partial rewrite of the rian8337/osu-droid-replay-analyzer on python

https://github.com/Rian8337/osu-droid-module/tree/master/packages/osu-droid-replay-analyzer

MIT License

Copyright (c) 2021 Rian8337

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

import javaobj.v2
import javaobj.v2.transformers
from stream_unzip import stream_unzip
import javaobj
import struct
import json
import io
from .base.modlist import ModList
from .replay_data.movementtype import MovementType
from .replay_data.cursordata import CursorData
from .replay_data.hitresult import HitResult
from .replay_data.replayobjectdata import ReplayObjectData
from .base.mods import ModDifficultyAdjust, ModFlashlight, ModCustomSpeed, ModReplayV6


class Replay:
    def __init__(self):
        self.replay_file = None
        self.replay_obj = None
        self.map: str = None
        self.file_name: str = None
        self.md5: str = None
        self.unix_date: int = 0
        self.hit300k: int = 0
        self.hit300: int = 0
        self.hit100k: int = 0
        self.hit100: int = 0
        self.hit50: int = 0
        self.hit0: int = 0
        self.score: int = 0
        self.combo: int = 0
        self.rank: str = None
        self.accuracy: float = 0.0
        self.username: str = None
        self.parsed_mods: list = []
        self.converted_mods: ModList = None
        self.__buffer_offset: int = 0
        self.cursor_data: list = []
        self.hit_result_data: list = []

    def __zipped_chunks(self, filename):
        with open(filename, "rb") as f:
            while chunk := f.read(65536):
                yield chunk

    def __calculate_rank(self):
        total_hits = self.hit300 + self.hit100 + self.hit50 + self.hit0
        have_h_mods = False
        for mod in self.converted_mods:
            if mod.acronym == "HD" or mod.acronym == "FL":
                have_h_mods = True
                break
        hit300ratio = self.hit300 / total_hits

        if hit300ratio == 1:
            self.rank = "XH" if have_h_mods else "X"
            return self
        elif hit300ratio >= 0.9:
            if self.hit50 / total_hits <= 0.01 and self.hit0 == 0:
                self.rank = "SH" if have_h_mods else "S"
                return self
            self.rank = "A"
            return self
        elif hit300ratio >= 0.8:
            if self.hit0 == 0:
                self.rank = "A"
                return self
            self.rank = "B"
            return self
        elif hit300ratio >= 0.7:
            if self.hit0 == 0:
                self.rank = "B"
                return self
            self.rank = "C"
            return self
        elif hit300ratio >= 0.6:
            self.rank = "C"
            return self
        else:
            self.rank = "D"
            return self

    def __read_byte(self, replay_data):
        replay_data.seek(self.__buffer_offset)
        self.__buffer_offset += 1
        return struct.unpack(">b", replay_data.read(1))[0]

    def __read_short(self, replay_data):
        replay_data.seek(self.__buffer_offset)
        self.__buffer_offset += 2
        return struct.unpack(">h", replay_data.read(2))[0]

    def __read_int(self, replay_data):
        replay_data.seek(self.__buffer_offset)
        self.__buffer_offset += 4
        return struct.unpack(">i", replay_data.read(4))[0]

    def __read_float(self, replay_data):
        replay_data.seek(self.__buffer_offset)
        self.__buffer_offset += 4
        return struct.unpack(">f", replay_data.read(4))[0]

    def __parse_movement_data(self, replay_data):
        replay_data = io.BytesIO(replay_data)
        size = self.__read_int(replay_data)

        # copypasta begins here
        for i in range(size):
            move_size = self.__read_int(replay_data)
            time = []
            x = []
            y = []
            id = []
            for j in range(0, move_size):
                time.append(self.__read_int(replay_data))
                id.append(time[j] & 3)
                time[j] >>= 2
                if id[j] != MovementType.UP.value:
                    if self.version >= 5:
                        x.append(self.__read_float(replay_data))
                        y.append(self.__read_float(replay_data))
                    else:
                        x.append(self.__read_short(replay_data))
                        y.append(self.__read_short(replay_data))
                else:
                    x.append(-1)
                    y.append(-1)

            cursor_data = CursorData(
                {"size": move_size, "time": time, "x": x, "y": y, "id": id}
            ).to_dict

            self.cursor_data.append(cursor_data["occurrence_groups"])

    def __parse_hitresult_data(self, replay_data):
        replay_data = io.BytesIO(replay_data)

        hitobject_data_lenght = self.__read_int(replay_data)

        for i in range(hitobject_data_lenght):
            replay_object_data = ReplayObjectData(
                accuracy=0.0, tickset=[], result=HitResult.MISS
            )
            replay_object_data.accuracy = self.__read_short(replay_data)
            len = self.__read_byte(replay_data)

            if len > 0:
                bytes = []
                for j in range(len):
                    bytes.append(self.__read_byte(replay_data))
                for j in range(len * 8):
                    replay_object_data.tickset.append(
                        (bytes[len - round(j / 8) - 1] & (1 << round(j % 8))) != 0
                    )

            replay_object_data.result = HitResult(self.__read_byte(replay_data))
            if replay_object_data.result == HitResult.WHY:
                print("reached the end of hitresult data, most likely a bug")
            self.hit_result_data.append(replay_object_data.to_dict)

    @classmethod
    def load(cls, filename):

        replay = cls()
        replay.replay_file = filename

        for file_name, file_size, unzipped_chunks in stream_unzip(
            replay.__zipped_chunks(filename)
        ):

            data_buffer = io.BytesIO()

            try:
                for chunk in unzipped_chunks:
                    data_buffer.write(chunk)
            except Exception as e:
                break

        replay.replay_obj = javaobj.v2.loads(data_buffer.getvalue())

        for fields in replay.replay_obj[0].__dict__["field_data"].values():
            for field, value in fields.items():
                if field.name == "version":
                    replay.version = value

        replay.map = replay.replay_obj[1].value
        replay.file_name = replay.replay_obj[2].value
        replay.md5 = replay.replay_obj[3].value

        if replay.version >= 3:
            (
                replay.unix_date,
                replay.hit300k,
                replay.hit300,
                replay.hit100k,
                replay.hit100,
                replay.hit50,
                replay.hit0,
                replay.score,
                replay.combo,
            ) = struct.unpack(
                ">Qiiiiiiii", io.BytesIO(replay.replay_obj[4].data).read(40)
            )
            replay.username = replay.replay_obj[5].value

            if replay.version <= 6:
                for field in replay.replay_obj[6].__dict__["field_data"].values():
                    for field, value in field.items():
                        if field.name == "elements":
                            for element in value:
                                replay.parsed_mods.append(element.value)
                            break

                replay.converted_mods = ModList.from_droid_replay_v6(replay.parsed_mods)
                replay.converted_mods.add_mod(ModReplayV6())
            else:
                replay.converted_mods = ModList.from_dict(
                    json.loads(replay.replay_obj[6].value)
                )
            replay.accuracy = round(
                (
                    (300 * replay.hit300 + 100 * replay.hit100 + 50 * replay.hit50)
                    / (
                        300
                        * (replay.hit300 + replay.hit100 + replay.hit50 + replay.hit0)
                    )
                )
                * 100,
                2,
            )
            replay.__calculate_rank()

        if replay.version >= 4 and replay.version <= 6:
            modifiers = replay.replay_obj[7].value.split("|")
            for modifier in modifiers:
                if modifier.startswith("AR"):
                    replay.force_ar = float(modifier.replace("AR", ""))
                if modifier.startswith("CS"):
                    replay.force_cs = float(modifier.replace("CS", ""))
                if modifier.startswith("OD"):
                    replay.force_od = float(modifier.replace("OD", ""))
                if modifier.startswith("HP"):
                    replay.force_hp = float(modifier.replace("HP", ""))
                if modifier.startswith("x"):
                    replay.speed_multiplier = float(modifier.replace("x", "") or 1)
                    replay.converted_mods.add_mod(
                        ModCustomSpeed(rateMultiplier=replay.speed_multiplier)
                    )

                if modifier.startswith("FLD"):
                    replay.fl_delay = float(modifier.replace("FLD", "") or 0.12)
                    if fl := replay.converted_mods.get_mod("FL"):
                        fl.settings.set_value("areaFollowDelay", replay.fl_delay)
                    else:
                        replay.converted_mods.add_mod(
                            ModFlashlight(areaFollowDelay=replay.fl_delay)
                        )
            if (
                hasattr(replay, "force_ar")
                or hasattr(replay, "force_cs")
                or hasattr(replay, "force_od")
                or hasattr(replay, "force_hp")
            ):
                replay.converted_mods.add_mod(
                    ModDifficultyAdjust(
                        ar=replay.force_ar if hasattr(replay, "force_ar") else None,
                        cs=replay.force_cs if hasattr(replay, "force_cs") else None,
                        od=replay.force_od if hasattr(replay, "force_od") else None,
                        hp=replay.force_hp if hasattr(replay, "force_hp") else None,
                    )
                )

        buffer_index = 0
        if replay.version <= 2:
            buffer_index = 4
        elif replay.version == 3 or replay.version == 7:
            buffer_index = 7
        elif replay.version >= 4 and replay.version <= 6:
            buffer_index = 8

        replay_data = io.BytesIO()
        for i in range(buffer_index, len(replay.replay_obj)):
            replay_data.write(replay.replay_obj[i].data)

        replay.__parse_movement_data(replay_data.getvalue())
        print(replay.__buffer_offset)
        replay.__parse_hitresult_data(replay_data.getvalue())

        return replay

    def __str__(self):
        string = ""
        for key, value in self.__dict__.items():
            if (
                key == "replay_obj"
                or key == "replay_file"
                or key == "cursor_data"
                or key == "hit_result_data"
            ):
                continue
            if key == "converted_mods":
                string += f"{key}: {value.as_calculatable_mods} \n"
                continue
            string += f"{key}: {value} \n"
        return string
