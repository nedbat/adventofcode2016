#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/7
#
# Things I liked about this solution:
#
# * I learned about using lookahead assertions as a way to find overlapping
#   regex matches.

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

def inside_outside(ip):
    inside_brackets = "".join(re.findall(r"\[.*?\]", ip))
    outside_brackets = re.sub(r"\[.*?\]", "#", ip)
    return inside_brackets, outside_brackets

def supports_tls(ip):
    inside_brackets, outside_brackets = inside_outside(ip)
    return has_abba(outside_brackets) and not has_abba(inside_brackets)

@pytest.mark.parametrize("ip, supports", [
    ("abba[mnop]qrst", True),
    ("abcd[bddb]xyyx", False),
    ("aaaa[qwer]tyui", False),
    ("ioxxoj[asdfgh]zxcvbn", True),
])
def test_supports_tls(ip, supports):
    assert supports_tls(ip) == supports

def all_aba(s):
    """Return a set of AB strings for the ABA matches."""
    return {(m.group(2) + m.group(3)) for m in re.finditer(r"(?=((.)(.)\2))", s)}

def all_bab(s):
    return {aba[1]+aba[0] for aba in all_aba(s)}

@pytest.mark.parametrize("s, abas", [
    ("zazbz", {"za", "zb"}),
    ("azawpddzkqbosmltyxt[zoaaqnowmmwkmfkq]lgusvzwnimvgagupkt[scbjhqdftzssbvnvff]coiaslgcrwvyioxx[jouvwdiwvbsembzf]popmlnhjkoaeahcny", {'ae', 'az', 'ga', 'po', 'vn'}),
])
def test_all_aba(s, abas):
    assert all_aba(s) == abas

@pytest.mark.parametrize("s, babs", [
    ("zazbz", {"az", "bz"}),
])
def test_all_bab(s, babs):
    assert all_bab(s) == babs

def supports_ssl(ip):
    inside_brackets, outside_brackets = inside_outside(ip)
    abas = all_aba(outside_brackets)
    babs = all_bab(inside_brackets)
    return bool(abas & babs)

@pytest.mark.parametrize("ip, supports", [
    ("aba[bab]xyz", True),
    ("xyx[xyx]xyx", False),
    ("aaa[kek]eke", True),
    ("zazbz[bzb]cdb", True),
])
def test_supports_ssl(ip, supports):
    assert supports_ssl(ip) == supports

def puzzle1():
    with open("day07_input.txt") as inputf:
        num_tls = sum(supports_tls(line) for line in inputf)

    print(f"Puzzle 1: {num_tls} IPs support TLS")

def puzzle2():
    with open("day07_input.txt") as inputf:
        num_ssl = sum(supports_ssl(line) for line in inputf)

    print(f"Puzzle 2: {num_ssl} IPs support SSL")

if __name__ == "__main__":
    puzzle1()
    puzzle2()
