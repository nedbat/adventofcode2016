#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/16

import itertools

import pytest


ZERO_ONE = str.maketrans("01", "10")

def reverse01(s):
    """Reverse a string, and swap 0 and 1."""
    return s.translate(ZERO_ONE)[::-1]

@pytest.mark.parametrize("s, r", [
    ("1000", "1110"),
    ("01001", "01101"),
])
def test_reverse01(s, r):
    assert reverse01(s) == r


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

def dragon_iterative(seed, steps):
    d = seed
    for _ in range(steps):
        d = d + "0" + reverse01(d)
    return d

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon_iterative(s, n, d):
    assert dragon_iterative(s, n) == d


def dragon_recursive(seed, steps):
    if steps == 0:
        return seed
    else:
        d = dragon_recursive(seed, steps-1)
        return d + "0" + reverse01(d)

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon_recursive(s, n, d):
    assert dragon_recursive(s, n) == d


def dragon_gen(seed, steps, reverse=False):
    if reverse:
        if steps == 0:
            yield from reverse01(seed)
        else:
            yield from dragon_gen(seed, steps-1, reverse=not reverse)
            yield "1"
            yield from dragon_gen(seed, steps-1, reverse=reverse)
    else:
        if steps == 0:
            yield from seed
        else:
            yield from dragon_gen(seed, steps-1, reverse=reverse)
            yield "0"
            yield from dragon_gen(seed, steps-1, reverse=not reverse)

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon_gen(s, n, d):
    assert "".join(dragon_gen(s, n)) == d


def dragon_infinite(seed):
    """Generate characters of dragon forever."""
    yield from seed
    for steps in itertools.count():
        yield "0"
        yield from dragon_gen(seed, steps, reverse=True)

def dragon_finite(seed, length):
    return "".join(itertools.islice(dragon_infinite(seed), length))

@pytest.mark.parametrize("s, n, d", DRAGON_TESTS)
def test_dragon_finite(s, n, d):
    assert dragon_finite(s, len(d)) == d


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


def disk_checksum(seed, length):
    return checksum(dragon_finite(seed, length))

def test_disk_checksum():
    assert disk_checksum("10000", 20) == "01100"


INPUT = "10011111011011001"

def puzzle1():
    print(f"Puzzle 1: the checksum is {disk_checksum(INPUT, 272)}")

def puzzle2():
    print(f"Puzzle 2: the checksum is {disk_checksum(INPUT, 35651584)}")

if __name__ == "__main__":
    puzzle1()
    puzzle2()
