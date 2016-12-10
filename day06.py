#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/6

import collections

import pytest

def most_common_letters(lines, common_index=0):
    counters = None
    for line in lines:
        if not counters:
            counters = [collections.Counter() for _ in line.rstrip()]
        for c, ctr in zip(line, counters):
            ctr[c] += 1

    return "".join(ctr.most_common()[common_index][0] for ctr in counters)

def least_common_letters(lines):
    return most_common_letters(lines, common_index=-1)

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

def test_least_common_letters():
    assert least_common_letters(SAMPLE_INPUT.splitlines()) == "advent"

with open("day06_input.txt") as finput:
    message1 = most_common_letters(finput)

print(f"Puzzle 1: message is {message1}")

with open("day06_input.txt") as finput:
    message2 = least_common_letters(finput)

print(f"Puzzle 2: message is {message2}")
