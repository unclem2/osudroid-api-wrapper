"""
Rewrite of the CursorData class of rian8337/osu-droid-replay-analyzer
https://github.com/Rian8337/osu-droid-module/blob/master/packages/osu-droid-replay-analyzer/src/data/CursorData.ts

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
from .cursoroccurrencegroup import CursorOccurrenceGroup
from .movementtype import MovementType


class CursorData:
    def __init__(self, values: dict):
        self.occurrence_groups: List[CursorOccurrenceGroup] = []
        down_occurrence: Optional[CursorOccurrence] = None
        move_occurrences: List[CursorOccurrence] = []

        for i in range(values["size"]):
            occurrence = CursorOccurrence(
                time=values["time"][i],
                x=values["x"][i],
                y=values["y"][i],
                id=MovementType(values["id"][i]),
            )

            if occurrence.id == MovementType.DOWN:
                down_occurrence = occurrence
            elif occurrence.id == MovementType.MOVE:
                move_occurrences.append(occurrence)
            elif occurrence.id == MovementType.UP:
                if down_occurrence:
                    self.occurrence_groups.append(
                        CursorOccurrenceGroup(
                            down=down_occurrence,
                            moves=move_occurrences,
                            up=occurrence,
                        )
                    )
                    down_occurrence = None
                move_occurrences = []

        # Handle any remaining occurrences
        if down_occurrence and move_occurrences:
            self.occurrence_groups.append(
                CursorOccurrenceGroup(down=down_occurrence, moves=move_occurrences)
            )

    @property
    def earliest_occurrence_time(self) -> Optional[int]:
        return self.occurrence_groups[0].start_time if self.occurrence_groups else None

    @property
    def latest_occurrence_time(self) -> Optional[int]:
        return self.occurrence_groups[-1].end_time if self.occurrence_groups else None

    @property
    def total_occurrences(self) -> int:
        return sum(
            1 + len(group.moves) + (1 if group.up else 0)
            for group in self.occurrence_groups
        )

    @property
    def all_occurrences(self) -> List[CursorOccurrence]:
        return [
            occurrence
            for group in self.occurrence_groups
            for occurrence in group.all_occurrences
        ]

    @property
    def to_dict(self):
        return {
            "occurrence_groups": [group.to_dict for group in self.occurrence_groups]
        }
