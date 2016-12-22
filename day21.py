#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/21

import re

import pytest

REVERSE = False

def swap_position(s, x, y):
    s[x], s[y] = s[y], s[x]
    return s

def swap_letter(s, a, b):
    return swap_position(s, s.index(a), s.index(b))

def rotate_steps(s, right_left, x):
    x %= len(s)
    right = right_left == "right"
    if REVERSE:
        right = not right
    if right:
        x = -x
    s = s[x:] + s[:x]
    return s

def rotate_position(s, a):
    i = s.index(a)
    return rotate_steps(s, "right", 1 + i + (1 if i >= 4 else 0))

def reverse(s, x, y):
    s[x:y+1] = reversed(s[x:y+1])
    return s

def move(s, x, y):
    s.insert(y, s.pop(x))
    return s

OPS = [
    ("swap position (\d+) with position (\d+)", swap_position, (int, int)),     # means that the letters at indexes X and Y (counting from 0) should be swapped.
    ("swap letter (.) with letter (.)", swap_letter, (str, str)),               # means that the letters X and Y should be swapped (regardless of where they appear in the string).
    ("rotate (\S+) (\d+) steps?", rotate_steps, (str, int)),                    # means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
    ("rotate based on position of letter (.)", rotate_position, (str,)),        # means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
    ("reverse positions (\d+) through (\d+)", reverse, (int, int)),             # means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
    ("move position (\d+) to position (\d+)", move, (int, int)),                # means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.
]

def execute(instructions, s):
    s = list(s)
    for instruction in instructions:
        for pat, opfn, types in OPS:
            m = re.match(pat, instruction)
            if not m:
                continue
            args = [typefn(t) for typefn, t in zip(types, m.groups())]
            s = opfn(s, *args)
            print(f"After {opfn.__name__} {args}: {s}")
    return "".join(s)

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
    assert execute(SAMPLE_INSTRUCTIONS.splitlines(), "abcde") == "decab"

def puzzle1():
    start = "abcdefgh"
    with open("day21_input.txt") as finput:
        answer = execute(finput, start)
    print(f"Puzzle 1: the result of scrambling {start} is {answer}")

def puzzle2():
    global REVERSE  # ick
    start = "fbgdceah"
    REVERSE = True
    with open("day21_input.txt") as finput:
        answer = execute(reversed(list(finput)), start)
    print(f"Puzzle 2: the result of unscrambling {start} is {answer}")

if __name__ == "__main__":
    puzzle1()
    puzzle2()



# LOL: dabeaz's crazy example of valid py 3.6 code.
def spam():
    X: auto @ property.template<T> X(*T, ...) = object
    class Y(X):
        pass
    return Y()

