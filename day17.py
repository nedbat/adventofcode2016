#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/17

import collections
import hashlib

import pytest

State = collections.namedtuple("State", "x, y, path")

DELTAS = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

def is_open(c):
    return c in "bcdef"

def next_steps(x, y, passcode, path):
    """Generate next possible steps from here."""
    h = hashlib.md5((passcode + path).encode("ascii")).hexdigest()
    if y > 1 and is_open(h[0]):
        yield "U"
    if y < 4 and is_open(h[1]):
        yield "D"
    if x > 1 and is_open(h[2]):
        yield "L"
    if x < 4 and is_open(h[3]):
        yield "R"

@pytest.mark.parametrize("x, y, passcode, path, result", [
    (1, 1, "hijkl", "", ["D"]),
    (1, 2, "hijkl", "D", ["U", "R"]),
    (2, 2, "hijkl", "DR", []),
    (1, 1, "hijkl", "DU", ["R"]),
    (2, 1, "hijkl", "DUR", []),
])
def test_next_steps(x, y, passcode, path, result):
    assert list(next_steps(x, y, passcode, path)) == result

def walk_room(passcode, shortest=True):
    possibilities = [State(1, 1, "")]
    solution = ""

    while possibilities:
        next_possibilities = []
        for x, y, path in possibilities:
            for direction in next_steps(x, y, passcode, path):
                new_path = path + direction
                new_x = x + DELTAS[direction][0]
                new_y = y + DELTAS[direction][1]
                if (new_x, new_y) == (4, 4):
                    if shortest:
                        return new_path
                    elif len(new_path) > len(solution):
                        solution = new_path
                else:
                    next_possibilities.append(State(new_x, new_y, new_path))

        possibilities = next_possibilities

    return solution

@pytest.mark.parametrize("passcode, result", [
    ('ihgpwlah', 'DDRRRD'),
    ('kglvqrro', 'DDUDRLRRUDRD'),
    ('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'),
])
def test_walk_room(passcode, result):
    assert walk_room(passcode) == result


INPUT = "njfxhljp"

def puzzle1():
    print(f"Puzzle 1: shortest path is {walk_room(INPUT)}")


@pytest.mark.parametrize("passcode, result", [
    ('ihgpwlah', 370),
    ('kglvqrro', 492),
    ('ulqzkmiv', 830),
])
def test_walk_room_longest(passcode, result):
    assert len(walk_room(passcode, shortest=False)) == result


def puzzle2():
    print(f"Puzzle 2: longest path is {len(walk_room(INPUT, shortest=False))} long")

if __name__ == "__main__":
    puzzle1()
    puzzle2()
