#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/5

import hashlib
import itertools

import pytest

def zero_hashes(door_id):
    for index in itertools.count():
        h = hashlib.md5(f"{door_id}{index}".encode("ascii")).hexdigest()
        if h.startswith("00000"):
            yield h

def door_password_digits(door_id):
    for zero_hash in zero_hashes(door_id):
        yield zero_hash[5]

def door_password(door_id):
    return "".join(itertools.islice(door_password_digits(door_id), 8))

def test_door_password():
    assert door_password("abc") == "18f47a30"

def password_digit_positions(door_id):
    for zero_hash in zero_hashes(door_id):
        yield int(zero_hash[5], 16), zero_hash[6]

def test_password_digit_positions():
    assert list(itertools.islice(password_digit_positions("abc"), 3)) == [(1, "5"), (8, "f"), (15, "9")]

def print_decrypting_password(door_id):
    digits = ["_"] * 8
    for position, digit in password_digit_positions(door_id):
        if position >= len(digits) or digits[position] != '_':
            continue
        digits[position] = digit
        print("".join(digits))
        if "_" not in digits:
            break

if __name__ == "__main__":
    door_id = "reyedfim"

    password = door_password(door_id)
    print(f"Puzzle 1: the password for {door_id} is {password}")

    print("Puzzle 2:")
    print_decrypting_password(door_id)
