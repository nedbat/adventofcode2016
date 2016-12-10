#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/6

import collections

import pytest

def most_common_letters(lines):
    counters = None
    for line in lines:
        if not counters:
            counters = [collections.Counter() for _ in line.rstrip()]
        for c, ctr in zip(line, counters):
            ctr[c] += 1

    return "".join(ctr.most_common(1)[0][0] for ctr in counters)

SAMPLE_INPUT = """\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""

def test_most_common_letters():
    assert most_common_letters(SAMPLE_INPUT.splitlines()) == "easter"

with open("day06_input.txt") as finput:
    message = most_common_letters(finput)

print(f"Puzzle 1: message is {message}")
