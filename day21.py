#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/21

import re

import pytest


class Scrambler:

    def __init__(self, unscramble=False):
        self.unscramble = unscramble
        self.text = None

    def swap_position(self, x, y):
        self.text[x], self.text[y] = self.text[y], self.text[x]

    def swap_letter(self, a, b):
        self.swap_position(self.text.index(a), self.text.index(b))

    def rotate_steps(self, right_left, x):
        x %= len(self.text)
        right = right_left == "right"
        if self.unscramble:
            right = not right
        if right:
            x = -x
        self.text = self.text[x:] + self.text[:x]

    def rotate_position(self, a):
        i = self.text.index(a)
        self.rotate_steps("right", 1 + i + (1 if i >= 4 else 0))

    def reverse(self, x, y):
        self.text[x:y+1] = reversed(self.text[x:y+1])

    def move(self, x, y):
        self.text.insert(y, self.text.pop(x))

    OPS = [
        ("swap position (\d+) with position (\d+)", "swap_position", (int, int)),     # means that the letters at indexes X and Y (counting from 0) should be swapped.
        ("swap letter (.) with letter (.)", "swap_letter", (str, str)),               # means that the letters X and Y should be swapped (regardless of where they appear in the string).
        ("rotate (\S+) (\d+) steps?", "rotate_steps", (str, int)),                    # means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
        ("rotate based on position of letter (.)", "rotate_position", (str,)),        # means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
        ("reverse positions (\d+) through (\d+)", "reverse", (int, int)),             # means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
        ("move position (\d+) to position (\d+)", "move", (int, int)),                # means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.
    ]

    def execute(self, instructions, s):
        if self.unscramble:
            instructions = reversed(list(instructions))
        self.text = list(s)
        for instruction in instructions:
            for pat, opfn, types in self.OPS:
                m = re.match(pat, instruction)
                if not m:
                    continue
                args = [typefn(t) for typefn, t in zip(types, m.groups())]
                getattr(self, opfn)(*args)
                print(f"After {opfn} {args}: {self.text}")
        return "".join(self.text)

SAMPLE_INSTRUCTIONS = """\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""

def test_execute():
    assert Scrambler().execute(SAMPLE_INSTRUCTIONS.splitlines(), "abcde") == "decab" "x"

def test_unscramble():
    assert Scrambler(unscramble=True).execute(SAMPLE_INSTRUCTIONS.splitlines(), "decab") == "abcde"

def puzzle1():
    start = "abcdefgh"
    with open("day21_input.txt") as finput:
        answer = Scrambler().execute(finput, start)
    print(f"Puzzle 1: the result of scrambling {start} is {answer}")

def puzzle2():
    global REVERSE  # ick
    start = "fbgdceah"
    REVERSE = True
    with open("day21_input.txt") as finput:
        answer = Scrambler(unscramble=True).execute(finput, start)
    print(f"Puzzle 2: the result of unscrambling {start} is {answer}")

if __name__ == "__main__":
    puzzle1()
    puzzle2()
