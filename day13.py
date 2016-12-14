#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/13

import pytest

def one_bits(n):
    return bin(n)[2:].count('1')

@pytest.mark.parametrize("n, ones", [
    (0, 0),
    (1, 1),
    (256, 1),
    (257, 2),
    (259, 3),
])
def test_one_bits(n, ones):
    assert one_bits(n) == ones


def is_wall(x, y, favorite):
    num = x*x + 3*x + 2*x*y + y + y*y + favorite
    ones = one_bits(num)
    return bool(ones % 2)

@pytest.mark.parametrize("x, y, favorite, res",
    # The top row of the example from the problem.
    [(i, 0, 10, c=='#') for i, c in enumerate(".#.####.##")]
)
def test_is_wall(x, y, favorite, res):
    assert is_wall(x, y, favorite) == res


def neighbors(x, y):
    """Produce the neighbors of x,y still on the positive grid."""
    if x > 0:
        yield x-1, y
    if y > 0:
        yield x, y-1
    yield x+1, y
    yield x, y+1

@pytest.mark.parametrize("x, y, res", [
    (0, 0, {(0, 1), (1, 0)}),
    (8, 8, {(7, 8), (9, 8), (8, 7), (8, 9)}),
    (0, 8, {(0, 7), (0, 9), (1, 8)}),
])
def test_neighbors(x, y, res):
    assert set(neighbors(x, y)) == res

def walk_maze(favorite, target):
    """Returns a list of spots visited while getting to target."""

    start = (1, 1)
    leaves = [start]

    # Map from (x,y) to list of spots visited to get there.
    visited = {start: [start]}

    while leaves:
        next_leaves = []
        for pos in leaves:
            for next_pos in neighbors(*pos):
                if is_wall(*next_pos, favorite):
                    continue
                if next_pos in visited:
                    continue
                path = visited[pos] + [next_pos]
                if next_pos == target:
                    return path
                visited[next_pos] = path
                next_leaves.append(next_pos)
        leaves = next_leaves

def test_walk_maze():
    # The sample.
    assert walk_maze(10, (7, 4)) == [
        (1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (4, 4),
        (4, 5), (5, 5), (6, 5), (6, 4), (7, 4)
    ]


def puzzle1():
    path = walk_maze(1362, (31, 39))
    print(f"It took {len(path)-1} steps to reach (31, 39)")

puzzle1()

