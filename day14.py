#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/14

import collections
import hashlib
import itertools
import re

import pytest

def triple(s):
    """Return the character that occurs as a triple, or None."""
    m = re.search(r"(.)\1\1", s)
    if m:
        return m.group(1)

@pytest.mark.parametrize("s, t", [
    ("hello there", None),
    ("aaa", "a"),
    ("0123345xxx112315zzz124xx", "x"),
])
def test_triple(s, t):
    assert triple(s) == t


def hashes(salt):
    """Produce the hashes of salt+0, salt+1, ..."""
    for i in itertools.count():
        yield i, hashlib.md5(f"{salt}{i}".encode("ascii")).hexdigest()

@pytest.mark.parametrize("salt, first_three", [
    ("abc", [
        (0, '577571be4de9dcce85a041ba0410f29f'),
        (1, '23734cd52ad4a4fb877d8a1e26e5df5f'),
        (2, '63872b5565b2179bd72ea9c339192543'),
    ]),
])
def test_hashes(salt, first_three):
    assert list(itertools.islice(hashes(salt), 3)) == first_three


class PeekableIterator:
    def __init__(self, source):
        self.source = iter(source)
        self.lookahead = collections.deque()

    def __iter__(self):
        return self

    def __next__(self):
        if self.lookahead:
            return self.lookahead.popleft()
        else:
            return next(self.source)

    def peek(self, index):
        assert index > 0
        while index > len(self.lookahead):
            self.lookahead.append(next(self.source))
        return self.lookahead[index-1]

def test_peekable():
    p = PeekableIterator(itertools.count())
    assert next(p) == 0
    assert next(p) == 1
    assert p.peek(1) == 2
    assert p.peek(100) == 101
    assert next(p) == 2
    assert p.peek(1) == 3


def key_indexes(salt):
    """Produce successive key indexes from salt."""
    p = PeekableIterator(hashes(salt))
    for index, hash in p:
        t = triple(hash)
        if t:
            # The hash has a triple, see if there's a quint in any of the next
            # 1000 hashes.
            for i in range(1, 1001):
                _, peek_hash = p.peek(i)
                if t*5 in peek_hash:
                    # This is a key!
                    yield index

def test_key_indexes():
    ki = key_indexes("abc")
    assert next(ki) == 39

def complete_keys(salt):
    """Return a list of 64 key indexes for salt."""
    return list(itertools.islice(key_indexes(salt), 64))

def test_complete_keys():
    # The sample from the problem.
    complete = complete_keys("abc")
    assert len(complete) == 64
    assert complete[0] == 39
    assert complete[1] == 92
    assert complete[63] == 22728


INPUT = 'zpqevtbw'

def puzzle1():
    complete = complete_keys(INPUT)
    print(f"Puzzle 1: the 64th key is at index {complete[63]}")

if __name__ == "__main__":
    puzzle1()
