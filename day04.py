#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/4

import collections
import re

import pytest

Room = collections.namedtuple("Room", "name, sector_id, checksum")


def parse_room(s):
    match = re.search(r"^([a-z-]+)-(\d+)\[(\w+)\]\s*$", s)
    name, sector_id, checksum = match.groups()
    return Room(name, int(sector_id), checksum)

def test_parse_room():
    assert parse_room('aaaaa-bbb-z-y-x-123[abxyz]') == Room("aaaaa-bbb-z-y-x", 123, "abxyz")

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

def is_real_room(room):
    return most_common_5(room.name) == room.checksum

@pytest.mark.parametrize("room,real", [
    ("aaaaa-bbb-z-y-x-123[abxyz]", True),
    ("a-b-c-d-e-f-g-h-987[abcde]", True),
    ("not-a-real-room-404[oarel]", True),
    ("totally-real-room-200[decoy]", False),
])
def test_is_real_room(room, real):
    assert is_real_room(parse_room(room)) == real

with open("day04_input.txt") as finput:
    rooms = list(map(parse_room, finput))

total = sum(room.sector_id for room in rooms if is_real_room(room))
print(f"Puzzle 1: the total is {total}")
