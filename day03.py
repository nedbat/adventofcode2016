#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/3

import pytest

def valid_triangle(a, b, c):
    return (
        a + b > c and
        b + c > a and
        c + a > b
    )

@pytest.mark.parametrize("a,b,c,result", [
    (5, 10, 25, False),
    (10, 25, 5, False),
    (25, 5, 10, False),
    (3, 4, 5, True),
])
def test_valid_triangle(a, b, c, result):
    assert valid_triangle(a, b, c) == result

with open("day03_input.txt") as inputf:
    nums = [tuple(map(int, line.strip().split())) for line in inputf]

num_valid = sum(valid_triangle(*abc) for abc in nums)
print(f"Puzzle 1: There are {num_valid} valid triangles")

def read_vertically(inputf):
    inputf = iter(inputf)
    while True:
        nums = []
        for _ in range(3):
            line = next(inputf)
            nums.append(tuple(map(int, line.strip().split())))
        for c in range(3):
            yield nums[0][c], nums[1][c], nums[2][c]

def test_read_vertically():
    the_input = [
        "101 301 501",
        "102 302 502",
        "103 303 503",
        "201 401 601",
        "202 402 602",
        "203 403 603",
    ]
    nums = list(read_vertically(the_input))
    assert nums == [
        (101, 102, 103), (301, 302, 303), (501, 502, 503),
        (201, 202, 203), (401, 402, 403), (601, 602, 603),
    ]

with open("day03_input.txt") as inputf:
    nums = list(read_vertically(inputf))

num_valid = sum(valid_triangle(*abc) for abc in nums)
print(f"Puzzle 2: There are {num_valid} valid triangles when read vertically")
