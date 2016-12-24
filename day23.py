#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/23

import pytest

class Computer:
    def __init__(self, program):
        self.registers = dict.fromkeys("abcd", 0)
        self.program = program
        self.pc = 0
        self.opcodes = 0

    def run(self):
        while self.pc < len(self.program):
            inst = self.program[self.pc]
            op = getattr(self, inst[0])
            new = op(*inst[1:])
            if new is None:
                self.pc += 1
            else:
                self.pc = new
            self.opcodes += 1

    def cpy(self, val, target):
        if isinstance(val, str):
            val = self.registers[val]
        self.registers[target] = val

    def inc(self, target):
        self.registers[target] += 1

    def dec(self, target):
        self.registers[target] -= 1

    def jnz(self, val, offset):
        if isinstance(val, str):
            val = self.registers[val]
        if val != 0:
            return self.pc + offset

cpy, inc, dec, jnz, a, b, c, d = "cpy inc dec jnz a b c d".split()

SAMPLE_PROGRAM = [
    (cpy, 41, a),
    (inc, a),
    (inc, a),
    (dec, a),
    (jnz, a, 2),
    (dec, a),
]

def sample():
    comp = Computer(SAMPLE_PROGRAM)
    comp.run()
    print(f"The sample program leaves {comp.registers['a']} in register a after running {comp.opcodes:,d} opcodes")

sample()

PUZZLE_PROGRAM = [
    (cpy, 1, a),
    (cpy, 1, b),
    (cpy, 26, d),
    (jnz, c, 2),
    (jnz, 1, 5),
    (cpy, 7, c),
    (inc, d),
    (dec, c),
    (jnz, c, -2),
    (cpy, a, c),
    (inc, a),
    (dec, b),
    (jnz, b, -2),
    (cpy, c, b),
    (dec, d),
    (jnz, d, -6),
    (cpy, 17, c),
    (cpy, 18, d),
    (inc, a),
    (dec, d),
    (jnz, d, -2),
    (dec, c),
    (jnz, c, -5),
]

def puzzle1():
    comp = Computer(PUZZLE_PROGRAM)
    comp.run()
    print(f"Puzzle 1 leaves {comp.registers['a']} in register a after running {comp.opcodes:,d} opcodes")

puzzle1()

def puzzle2():
    comp = Computer(PUZZLE_PROGRAM)
    comp.registers['c'] = 1
    comp.run()
    print(f"Puzzle 2 leaves {comp.registers['a']} in register a after running {comp.opcodes:,d} opcodes")

puzzle2()
