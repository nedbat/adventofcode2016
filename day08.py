#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/8

import re

import pytest

class Screen:
    def __init__(self, width, height):
        self.pixels = [['.'] * width for _ in range(height)]

    def count_on(self):
        return sum(pixel == '#' for row in self.pixels for pixel in row)

    def rows(self):
        return [''.join(row) for row in self.pixels]

    def print(self):
        print("\n".join(self.rows()))

    def rect(self, a, b):
        for c in range(a):
            for r in range(b):
                self.pixels[r][c] = '#'

    def rotate_row(self, row, by):
        self.pixels[row] = rotate(self.pixels[row], by)

    def rotate_column(self, col, by):
        pixels = [row[col] for row in self.pixels]
        pixels = rotate(pixels, by)
        for row, new_pixel in zip(self.pixels, pixels):
            row[col] = new_pixel

def rotate(seq, by):
    by = len(seq) - (by % len(seq))
    return seq[by:] + seq[:by]

@pytest.mark.parametrize("s, by, res", [
    ("abcdefg", 1, "gabcdef"),
    ("abcdefg", 4, "defgabc"),
    ("abcdefg", 0, "abcdefg"),
    ([1, 2, 3, 4, 5], 3, [3, 4, 5, 1, 2]),
])
def test_rotate(s, by, res):
    assert rotate(s, by) == res

def test_construction():
    screen = Screen(width=7, height=3)
    assert screen.count_on() == 0
    assert screen.rows() == [
        '.......',
        '.......',
        '.......',
    ]

def test_rect():
    screen = Screen(width=7, height=3)
    screen.rect(3, 2)
    assert screen.count_on() == 6
    assert screen.rows() == [
        '###....',
        '###....',
        '.......',
    ]

def test_rotate_row_column():
    screen = Screen(width=7, height=3)
    screen.rect(3, 2)
    screen.rotate_column(1, 1)
    assert screen.rows() == [
        '#.#....',
        '###....',
        '.#.....',
    ]
    screen.rotate_row(0, 4)
    assert screen.rows() == [
        '....#.#',
        '###....',
        '.#.....',
    ]
    screen.rotate_column(1, 1)
    assert screen.rows() == [
        '.#..#.#',
        '#.#....',
        '.#.....',
    ]

def execute(screen, instructions):
    for inst in instructions:
        screen.print()
        print(inst)
        m = re.search(r"""
            (
                (?P<rect>rect) |
                (?P<row>rotate\ row) |
                (?P<col>rotate\ column)
            )
            [^\d]*
            (?P<num1>\d+)[^\d]*(?P<num2>\d+)
        """, inst, flags=re.VERBOSE)
        if m:
            num1 = int(m.group('num1'))
            num2 = int(m.group('num2'))
            if m.group('rect'):
                screen.rect(num1, num2)
            elif m.group('row'):
                screen.rotate_row(num1, num2)
            elif m.group('col'):
                screen.rotate_column(num1, num2)
            else:
                print(f"WUT? {inst!r}")
        else:
            print(f"HUH? {inst!r}")


def puzzle1():
    screen = Screen(width=50, height=6)
    with open("day08_input.txt") as finput:
        execute(screen, finput)
    print("Puzzle 1: final screen is:")
    screen.print()
    print(f"There are {screen.count_on()} pixels on")

if __name__ == "__main__":
    puzzle1()
