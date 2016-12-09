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
print(f"There are {num_valid} valid triangles")
