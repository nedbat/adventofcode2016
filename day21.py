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
        if self.unscramble:
            if i % 2:
                steps = (i+1)//2
            elif i == 0:
                steps = 1
            else:
                steps = ((i+len(self.text))//2)+1
            self.rotate_steps("right", steps)
        else:
            self.rotate_steps("right", 1 + i + (1 if i >= 4 else 0))
        # new position: 2x+1 or 2x+2
        # 
        # reverse:
        # if pos is odd:
        #   2x+1 --> x   newpos is (y-1)/2, so shift left by (x+1)/2
    """
        a b c d e f g
    a   g a b c d e f   1 left 1
    b   f g a b c d e   3 left 2
    c   e f g a b c d   5 left 3
    d   d e f g a b c   0 left 4
    e   b c d e f g a   3 left 6
    f   a b c d e f g   5 left 7
    g   g a b c d e f   0 left 8

        a b c d e f g h
    a   h a b c d e f g     1 left 1    (x+1)/2
    b   g h a b c d e f     3 left 2
    c   f g h a b c d e     5 left 3
    d   e f g h a b c d     7 left 4
    e   c d e f g h a b     2 left 6    (x+8)/2+1
    f   b c d e f g h a     4 left 7
    g   a b c d e f g h     6 left 0
    h   h a b c d e f g     0 left 1
    """

    def reverse(self, x, y):
        self.text[x:y+1] = reversed(self.text[x:y+1])

    def move(self, x, y):
        if self.unscramble:
            x, y = y, x
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
    assert Scrambler().execute(SAMPLE_INSTRUCTIONS.splitlines(), "abcde") == "decab"

def test_unscramble():
    assert Scrambler(unscramble=True).execute(SAMPLE_INSTRUCTIONS.splitlines(), "decab") == "abcde"

def puzzle1():
    start = "abcdefgh"
    with open("day21_input.txt") as finput:
        answer = Scrambler().execute(finput, start)
    print(f"Puzzle 1: the result of scrambling {start} is {answer}")

def puzzle2():
    start = "fbgdceah"
    with open("day21_input.txt") as finput:
        answer = Scrambler(unscramble=True).execute(finput, start)
    print(f"Puzzle 2: the result of unscrambling {start} is {answer}")

if __name__ == "__main__":
    puzzle1()
    puzzle2()
