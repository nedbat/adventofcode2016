#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/16

import itertools

import pytest


def swap01(s):
    return s.replace('0', '*').replace('1', '0').replace('*', '1')

@pytest.mark.parametrize("s, r", [
    ("0000", "1111"),
    ("01001", "10110"),
])
def test_swap01(s, r):
    assert swap01(s) == r


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

def dragon_iterative(seed, level):
    d = seed
    while level > 0:
        d = d + "0" + swap01(d)[::-1]
        level -= 1
    return d

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon_iterative(s, n, d):
    assert dragon_iterative(s, n) == d


def dragon_recursive(seed, level):
    if level == 0:
        return seed
    d = dragon_recursive(seed, level-1)
    return d + "0" + swap01(d)[::-1]

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon_recursive(s, n, d):
    assert dragon_recursive(s, n) == d


def dragon_recursive_generator(seed, level, reverse=False):
    if reverse:
        if level == 0:
            yield from swap01(seed)[::-1]
        else:
            yield from dragon_recursive_generator(seed, level-1, reverse=not reverse)
            yield "1"
            yield from dragon_recursive_generator(seed, level-1, reverse=reverse)
    else:
        if level == 0:
            yield from seed
        else:
            yield from dragon_recursive_generator(seed, level-1, reverse=reverse)
            yield "0"
            yield from dragon_recursive_generator(seed, level-1, reverse=not reverse)

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon_recursive_generator(s, n, d):
    assert "".join(dragon_recursive_generator(s, n)) == d


def dragon_infinite(seed):
    yield from seed
    for level in itertools.count():
        yield "0"
        yield from dragon_recursive_generator(seed, level, reverse=True)

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon_infinite(s, n, d):
    assert "".join(itertools.islice(dragon_infinite(s), len(d))) == d


def pairs(s):
    """Yield successive two-character strings"""
    for i in range(0, len(s), 2):
        yield s[i:i+2]

@pytest.mark.parametrize("s, res", [
    ("abcdef", ["ab", "cd", "ef"]),
])
def test_pairs(s, res):
    assert list(pairs(s)) == res


def checksum(s):
    check = s
    while len(check) % 2 == 0:
        check = "".join("1" if a == b else "0" for a, b in pairs(check))
    return check

def test_checksum():
    assert checksum("110010110100") == "100"


def disk_checksum(initial, length):
    pass
