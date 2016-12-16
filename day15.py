#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/15

import itertools

import pytest

def find_alignment(disks):
    """
    disks: [(positions, position0), ...]
    """
    factors = []
    for i, (positions, position0) in enumerate(disks, start=1):
        factors.append((positions, (positions-position0-i) % positions))
    print(factors)

    for t in itertools.count():
        if all(t % mod == remainder for mod, remainder in factors):
            return t

SAMPLE = [(5, 4), (2, 1)]
print(find_alignment(SAMPLE))

INPUT = [(5, 2), (13, 7), (17, 10), (3, 2), (19, 9), (7, 0)]
print(find_alignment(INPUT))

INPUT2 = INPUT + [(11, 0)]
print(find_alignment(INPUT2))
