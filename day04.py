#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/4

import collections
import re

import pytest

class Room(collections.namedtuple("Room", "name, sector_id, checksum")):

    @classmethod
    def parse(cls, s):
        match = re.search(r"^([a-z-]+)-(\d+)\[(\w+)\]\s*$", s)
        name, sector_id, checksum = match.groups()
        return cls(name, int(sector_id), checksum)

    def is_real(self):
        return most_common_5(self.name) == self.checksum


def test_parse_room():
    assert Room.parse('aaaaa-bbb-z-y-x-123[abxyz]') == Room("aaaaa-bbb-z-y-x", 123, "abxyz")

def most_common_5(s):
    c = collections.Counter(s.replace("-", ""))
    five = c.most_common()
    five = sorted(five, key=lambda let_num: let_num[0])
    five = sorted(five, key=lambda let_num: let_num[1], reverse=True)
    return "".join(let_num[0] for let_num in five[:5])

@pytest.mark.parametrize("name,five", [
    ("aaaaa-bbb-z-y-x", "abxyz"),
    ("aaaaa-bbb-x-y-z", "abxyz"),
    ("a-b-c-d-e-f-g-h", "abcde"),
    ("not-a-real-room", "oarel"),
])
def test_most_common_5(name, five):
    assert most_common_5(name) == five

@pytest.mark.parametrize("room,real", [
    ("aaaaa-bbb-z-y-x-123[abxyz]", True),
    ("a-b-c-d-e-f-g-h-987[abcde]", True),
    ("not-a-real-room-404[oarel]", True),
    ("totally-real-room-200[decoy]", False),
])
def test_is_real_room(room, real):
    assert Room.parse(room).is_real == real

with open("day04_input.txt") as finput:
    rooms = list(map(Room.parse, finput))

total = sum(room.sector_id for room in rooms if room.is_real())
print(f"Puzzle 1: the total is {total}")
