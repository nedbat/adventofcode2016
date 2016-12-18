#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/18

import pytest


def triples(s):
    return [''.join(abc) for abc in zip(s, s[1:], s[2:])]

@pytest.mark.parametrize("s, result", [
    ('abcdef', ['abc', 'bcd', 'cde', 'def']),
])
def test_triples(s, result):
    assert triples(s) == result


def next_row(prev_row):
    next_row = ''
    for lcr in triples('.' + prev_row + '.'):
        is_trap = (lcr in ['^^.', '.^^', '^..', '..^'])
        next_row += '^' if is_trap else '.'
    return next_row

@pytest.mark.parametrize("prev_row, result", [
    ('..^^.', '.^^^^'),
])
def test_next_row(prev_row, result):
    assert next_row(prev_row) == result


def rows(start_row, limit):
    row = start_row
    for _ in range(limit):
        yield row
        row = next_row(row)

def count_safe_tiles(start_row, limit):
    safe_tiles = 0
    for row in rows(start_row, limit):
        safe_tiles += row.count('.')
    return safe_tiles

def test_count_safe_tiles():
    assert count_safe_tiles('.^^.^.^^^^', 10) == 38


INPUT = '.^..^....^....^^.^^.^.^^.^.....^.^..^...^^^^^^.^^^^.^.^^^^^^^.^^^^^..^.^^^.^^..^.^^.^....^.^...^^.^.'

def puzzle1():
    print(f"Puzzle 1: there are {count_safe_tiles(INPUT, 40)} safe tiles.")

def puzzle2():
    print(f"Puzzle 2: there are {count_safe_tiles(INPUT, 400000)} safe tiles.")

if __name__ == "__main__":
    puzzle1()
    puzzle2()
