"""Rewrite of the CursorOccurrence, Vector classes of rian8337/osu-droid-replay-analyzer
https://github.com/Rian8337/osu-droid-module/blob/master/packages/osu-droid-replay-analyzer/src/data/CursorOccurrence.ts

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


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def to_dict(self):
        return {"x": self.x, "y": self.y}


class CursorOccurrence:
    def __init__(self, x, y, time, id):
        self.position = Vector(x, y)
        self.time = time
        self.id = id

    @property
    def to_dict(self):
        return {"position": self.position.to_dict, "time": self.time,
                "id": self.id}
