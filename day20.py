#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/20

import pytest

def int_pairs(lines):
    for line in lines:
        low, high = line.rstrip().split("-")
        yield int(low), int(high)

def test_int_pairs():
    assert list(int_pairs(["5-8", "0-2", "4-7\n"])) == [(5, 8), (0, 2), (4, 7)]


def clip_range(rng, clipper):
    """Return a list of ranges remaining after clipping rng with clipper."""
    if rng[0] > clipper[1] or rng[1] < clipper[0]:
        # No overlap
        return [rng]

    res = []
    if rng[0] < clipper[0]:
        res.append((rng[0], clipper[0]-1))
    if clipper[1] < rng[1]:
        res.append((clipper[1]+1, rng[1]))
    return res

@pytest.mark.parametrize("r0, r1, c0, c1, result", [
    (10, 20, 100, 200, [(10, 20)]),
])
def test_clip_range(r0, r1, c0, c1, result):
    assert clip_range((r0, r1), (c0, c1)) == result


class NumRanges:
    def __init__(self, highest):
        self.ranges = [(0, highest)]

    def remove(self, low, high):
        """Remove low..high from the ranges."""
        new_ranges = []
        for rng in self.ranges:
            new_ranges.extend(clip_range(rng, (low, high)))
        self.ranges = new_ranges

    def first(self):
        return self.ranges[0][0]

    def __len__(self):
        return sum(high-low+1 for low, high in self.ranges)

@pytest.mark.parametrize("clips, result", [
    ([(10, 20)], [(0, 9), (21, 100)]),
    ([(10, 20), (15, 30)], [(0, 9), (31, 100)]),
    ([(10, 20), (50, 60)], [(0, 9), (21, 49), (61, 100)]),
    ([(10, 20), (50, 60), (25, 70)], [(0, 9), (21, 24), (71, 100)]),
    ([(50, 60), (40, 70)], [(0, 39), (71, 100)]),
    ([(50, 60), (40, 70), (0, 10)], [(11, 39), (71, 100)]),
])
def test_remove(clips, result):
    nr = NumRanges(100)
    for low, high in clips:
        nr.remove(low, high)
    assert nr.ranges == result


def first_open(lines):
    nr = NumRanges(4294967295)
    for pair in int_pairs(lines):
        nr.remove(*pair)
    return nr.first()

def test_first_open():
    assert first_open(["5-8", "0-2", "4-7"]) == 3


def puzzle1():
    with open("day20_input.txt") as finput:
        answer = first_open(finput)
    print(f"Puzzle 1: the first open IP is {answer}")

def num_open(lines):
    nr = NumRanges(4294967295)
    for pair in int_pairs(lines):
        nr.remove(*pair)
    return len(nr)

def puzzle2():
    with open("day20_input.txt") as finput:
        answer = num_open(finput)
    print(f"Puzzle 2: there are {answer} open IPs")

if __name__ == "__main__":
    puzzle1()
    puzzle2()
