#!/usr/bin/env python3.6

import pytest

def steps(directions):
    """Turn a string of directions into a series of (dir, dist) tuples."""
    for word in directions.split(","):
        word = word.strip()
        yield word[0], int(word[1:])

def test_steps():
    assert list(steps("R1, L3, R14")) == [('R', 1), ('L', 3), ('R', 14)]

DELTAS = {
    'R': {
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1),
    },
}

DELTAS['L'] = {new:old for old, new in DELTAS['R'].items()}

def walk(directions):
    x, y = 0, 0
    dxdy = (0, 1)
    for turn, distance in steps(directions):
        dxdy = DELTAS[turn][dxdy]
        x += dxdy[0] * distance
        y += dxdy[1] * distance

    return x, y


@pytest.mark.parametrize("directions,result", [
    ("R2, L3", (2, 3)),
    ("R2, R2, R2", (0, -2)),
    ("R5, L5, R5, R3", (10, 2)),
])
def test_walk(directions, result):
    assert walk(directions) == result

puzzle_input = "L3, R2, L5, R1, L1, L2, L2, R1, R5, R1, L1, L2, R2, R4, L4, L3, L3, R5, L1, R3, L5, L2, R4, L5, R4, R2, L2, L1, R1, L3, L3, R2, R1, L4, L1, L1, R4, R5, R1, L2, L1, R188, R4, L3, R54, L4, R4, R74, R2, L4, R185, R1, R3, R5, L2, L3, R1, L1, L3, R3, R2, L3, L4, R1, L3, L5, L2, R2, L1, R2, R1, L4, R5, R4, L5, L5, L4, R5, R4, L5, L3, R4, R1, L5, L4, L3, R5, L5, L2, L4, R4, R4, R2, L1, L3, L2, R5, R4, L5, R1, R2, R5, L2, R4, R5, L2, L3, R3, L4, R3, L2, R1, R4, L5, R1, L5, L3, R4, L2, L2, L5, L5, R5, R2, L5, R1, L3, L2, L2, R3, L3, L4, R2, R3, L1, R2, L5, L3, R4, L4, R4, R3, L3, R1, L3, R5, L5, R1, R5, R3, L1"
final = walk(puzzle_input)
distance = abs(final[0]) + abs(final[1])
print(f"{final}, therefore {distance}")
