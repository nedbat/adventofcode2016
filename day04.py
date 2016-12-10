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

    def decrypt_name(self):
        d = []
        for c in self.name:
            if c == '-':
                c = ' '
            else:
                c = rotate_letter(c, self.sector_id)
            d.append(c)
        return "".join(d)

def rotate_letter(c, num):
    """Shift the letter c forward by num, rotating to stay in the alphabet."""
    return chr(((ord(c) - 97) + num) % 26 + 97)

@pytest.mark.parametrize("let,num,res", [
    ("a", 1, "b"),
    ("z", 1, "a"),
    ("a", 27, "b"),
])
def test_rotate_letter(let, num, res):
    assert rotate_letter(let, num) == res

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
    assert Room.parse(room).is_real() == real

with open("day04_input.txt") as finput:
    rooms = list(map(Room.parse, finput))

total = sum(room.sector_id for room in rooms if room.is_real())
print(f"Puzzle 1: the total is {total}")


def test_decrypt_name():
    assert Room.parse("qzmt-zixmtkozy-ivhz-343[xyzzy]").decrypt_name() == "very encrypted name"

for room in rooms:
    if room.is_real():
        print(f"Puzzle 2: {room.decrypt_name()} {room.sector_id}")
