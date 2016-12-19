#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/19

import pytest

def last_elf(num_elves):
    # Closed-form solution: tack on a zero, drop the highest bit, and that's
    # the zero-based number of the last elf.
    return int(bin(num_elves)[3:]+"0", 2)+1

def test_last_elf():
    assert last_elf(5) == 3

INPUT = 3001330

def puzzle1():
    print(f"Puzzle 1: with {INPUT} elves, elf #{last_elf(INPUT)} gets all the presents")

if __name__ == "__main__":
    puzzle1()
