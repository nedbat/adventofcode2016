#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/9

import re

import pytest

AXB = re.compile(r"\((\d+)x(\d+)\)")

def decompress(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '(':
            m = AXB.match(s, i)
            assert m
            i += m.end() - m.start()
            length = int(m.group(1))
            repeat = int(m.group(2))
            chunk = s[i:i+length]
            i += length
            out.append(chunk * repeat)
        else:
            if not c.isspace():
                out.append(c)
            i += 1
    return ''.join(out)

@pytest.mark.parametrize("s, res", [
    ("ADVENT", "ADVENT"),
    ("A(1x5)BC", "ABBBBBC"),
    ("(3x3)XYZ", "XYZXYZXYZ"),
    ("A(2x2)BCD(2x2)EFG", "ABCBCDEFEFG"),
    ("(6x1)(1x3)A", "(1x3)A"),
    ("X(8x2)(3x3)ABCY", "X(3x3)ABC(3x3)ABCY"),
])
def test_decompress(s, res):
    assert decompress(s) == res

def puzzle1():
    with open("day09_input.txt") as finput:
        decompressed = decompress(finput.read())
    print(f"Puzzle 1: decompressed length is {len(decompressed)}")

def decompress2(s):
    while "(" in s:
        print(f"Length is {len(s):,d}")
        s = decompress(s)
    return s

def decompress2_length(s):
    total = 0
    i = 0
    while i < len(s):
        c = s[i]
        if c == '(':
            m = AXB.match(s, i)
            assert m
            i += m.end() - m.start()
            length = int(m.group(1))
            repeat = int(m.group(2))
            chunk = s[i:i+length]
            i += length
            total += decompress2_length(chunk) * repeat
        else:
            if not c.isspace():
                total += 1
            i += 1
    return total

@pytest.mark.parametrize("s, res", [
    ("(3x3)XYZ", 9),
    ("X(8x2)(3x3)ABCY", 20),
    ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
    ("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", 445),
])
def test_decompress2_length(s, res):
    assert decompress2_length(s) == res

def puzzle2():
    with open("day09_input.txt") as finput:
        decompressed_length = decompress2_length(finput.read())
    print(f"Puzzle 2: decompressed length is {decompressed_length}")

if __name__ == "__main__":
    puzzle1()
    puzzle2()
