"""Rewrite of the CursorOccurrenceGroup class of rian8337/osu-droid-replay-analyzer
https://github.com/Rian8337/osu-droid-module/blob/master/packages/osu-droid-replay-analyzer/src/data/CursorOccurrenceGroup.ts

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

from typing import List, Optional
from .cursoroccurrence import CursorOccurrence
from .movementtype import MovementType


class CursorOccurrenceGroup:
    def __init__(
        self,
        down: CursorOccurrence,
        moves: List[CursorOccurrence],
        up: Optional[CursorOccurrence] = None,
    ):
        self._down = down
        self._moves = moves
        self.down = down
        self.up = up

    @property
    def down(self) -> CursorOccurrence:
        return self._down

    @down.setter
    def down(self, value: CursorOccurrence):
        if value.id != MovementType.DOWN:
            raise TypeError(
                "Attempting to set the down cursor occurrence to one with a different movement type."
            )
        self._down = value

    @property
    def moves(self) -> List[CursorOccurrence]:
        return self._moves

    @property
    def up(self) -> Optional[CursorOccurrence]:
        return self._up

    @up.setter
    def up(self, value: Optional[CursorOccurrence]):
        if value and value.id != MovementType.UP:
            raise TypeError(
                "Attempting to set the up cursor occurrence to one with a different movement type."
            )
        self._up = value

    @property
    def start_time(self) -> int:
        return self._down.time

    @property
    def end_time(self) -> int:
        return (
            self._up.time
            if self._up
            else (self._moves[-1].time if self._moves else self._down.time)
        )

    @property
    def duration(self) -> int:
        return self.end_time - self.start_time

    @property
    def all_occurrences(self) -> List[CursorOccurrence]:
        cursors = [self._down, *self._moves]
        if self._up:
            cursors.append(self._up)
        return cursors

    def is_active_at(self, time: int) -> bool:
        return self.start_time <= time <= self.end_time

    def cursor_at(self, time: int) -> Optional[CursorOccurrence]:
        if not self.is_active_at(time):
            return None

        if self._down.time == time:
            return self._down

        if self._up and self._up.time == time:
            return self._up

        # Бинарный поиск в moves
        l, r = 0, len(self._moves) - 1

        while l <= r:
            pivot = l + (r - l) // 2
            if self._moves[pivot].time < time:
                l = pivot + 1
            elif self._moves[pivot].time > time:
                r = pivot - 1
            else:
                return self._moves[pivot]

        # l указывает на первый элемент с time > time, вернём предыдущий
        return self._moves[l - 1] if l > 0 else None

    @property
    def to_dict(self):
        return {
            "down": self._down.to_dict,
            "moves": [move.to_dict for move in self._moves],
            "up": self._up.to_dict if self._up else None,
        }
