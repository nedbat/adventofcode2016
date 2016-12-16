#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/16

import pytest


def swap01(s):
    return s.replace('0', '*').replace('1', '0').replace('*', '1')

@pytest.mark.parametrize("s, r", [
    ("0000", "1111"),
    ("01001", "10110"),
])
def test_swap01(s, r):
    assert swap01(s) == r


def dragon1(seed, level):
    if level == 0:
        return seed
    d = dragon1(seed, level-1)
    return d + "0" + swap01(d)[::-1]

DRAGON_TESTS = [
    ("1", 1, "100"),
    ("0", 1, "001"),
    ("11111", 1, "11111000000"),
    ("111100001010", 1, "1111000010100101011110000"),
    ("1", 2, "1000110"),
    ("1", 3, "100011001001110"),
    ("1", 4, "1000110010011100100011011001110"),
    ("1", 5, "100011001001110010001101100111001000110010011101100011011001110"),
]

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon1(s, n, d):
    assert dragon1(s, n) == d


def dragon2(seed, level, reverse=False):
    if reverse:
        if level == 0:
            yield from swap01(seed)[::-1]
        else:
            yield from dragon2(seed, level-1, reverse=not reverse)
            yield "1"
            yield from dragon2(seed, level-1, reverse=reverse)
    else:
        if level == 0:
            yield from seed
        else:
            yield from dragon2(seed, level-1, reverse=reverse)
            yield "0"
            yield from dragon2(seed, level-1, reverse=not reverse)

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon2(s, n, d):
    assert "".join(dragon2(s, n)) == d
