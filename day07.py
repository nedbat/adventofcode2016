#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/7

import re

import pytest


def has_abba(s):
    """Does s have any ABBA in it?"""
    for match in re.finditer(r"(.)(.)\2\1", s):
        if match.group(1) != match.group(2):
            return True
    return False

@pytest.mark.parametrize("s, abba", [
    ("abba", True),
    ("xyzzy", True),
    ("hello world", False),
    ("xaaaax", False),
    ("aaaaxyyzqppqaaaa", True),
])
def test_has_abba(s, abba):
    assert has_abba(s) == abba

def supports_tls(ip):
    inside_brackets = "".join(re.findall(r"\[.*?\]", ip))
    outside_brackets = re.sub(r"\[.*?\]", "#", ip)
    return has_abba(outside_brackets) and not has_abba(inside_brackets)

@pytest.mark.parametrize("ip, supports", [
    ("abba[mnop]qrst", True),
    ("abcd[bddb]xyyx", False),
    ("aaaa[qwer]tyui", False),
    ("ioxxoj[asdfgh]zxcvbn", True),
])
def test_supports_tls(ip, supports):
    assert supports_tls(ip) == supports

def puzzle1():
    with open("day07_input.txt") as inputf:
        num_abba = sum(supports_tls(line) for line in inputf)

    print(f"Puzzle 1: {num_abba} IPs support TLS")

if __name__ == "__main__":
    puzzle1()
