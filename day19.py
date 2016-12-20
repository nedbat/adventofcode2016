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


def last_elf_across(num_elves):
    elves = list(range(1, num_elves+1))
    cur_elf = 0
    while len(elves) > 1:
        if len(elves) % 1000 == 0:
            print(len(elves))
        other_elf = (cur_elf + len(elves) // 2) % len(elves)
        del elves[other_elf]
        if other_elf > cur_elf:
            cur_elf += 1
        cur_elf %= len(elves)
    return elves[0]

def test_last_elf_across():
    assert last_elf_across(5) == 2

def puzzle2():
    # Doing puzzle2 with last_elf_across took 26 minutes, but I don't know what
    # the closed form is! :)
    print(f"Puzzle 2: with {INPUT} elves, elf #{last_elf_across(INPUT)} gets all the presents")

if __name__ == "__main__":
    puzzle1()
    puzzle2()
