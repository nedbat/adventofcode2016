#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/23

import pytest

class Computer:
    def __init__(self, program):
        self.registers = dict.fromkeys("abcd", 0)
        self.program = list(program)
        self.pc = 0
        self.opcodes = 0

    def run(self):
        while self.pc < len(self.program):
            #print(f"Program: {self.pc}: {self.program}\nRegisters: {self.registers}")
            inst = self.program[self.pc]
            op = getattr(self, inst[0])
            new = op(*inst[1:])
            if new is None:
                self.pc += 1
            else:
                self.pc = new
            self.opcodes += 1

    def get_val(self, val):
        if isinstance(val, str):
            val = self.registers[val]
        return val

    def cpy(self, val, target):
        if isinstance(target, int):
            return
        val = self.get_val(val)
        self.registers[target] = val

    def inc(self, target):
        if isinstance(target, int):
            return
        self.registers[target] += 1

    def dec(self, target):
        if isinstance(target, int):
            return
        self.registers[target] -= 1

    def jnz(self, val, offset):
        val = self.get_val(val)
        offset = self.get_val(offset)
        if val != 0:
            return self.pc + offset

    TOGGLES = {
        'cpy': 'jnz',
        'jnz': 'cpy',
        'inc': 'dec',
        'dec': 'inc',
        'tgl': 'inc',
    }

    def tgl(self, offset):
        offset = self.get_val(offset)
        insti = self.pc + offset
        if insti < 0 or insti >= len(self.program):
            # Do nothing if trying to toggle outside the program.
            return
        inst = self.program[insti]
        new_inst = [self.TOGGLES[inst[0]]]
        new_inst.extend(inst[1:])
        self.program[insti] = tuple(new_inst)

cpy, inc, dec, jnz, tgl, a, b, c, d = "cpy inc dec jnz tgl a b c d".split()

SAMPLE_PROGRAM = [
    (cpy, 2, a),
    (tgl, a),
    (tgl, a),
    (tgl, a),
    (cpy, 1, a),
    (dec, a),
    (dec, a),
]

def sample():
    comp = Computer(SAMPLE_PROGRAM)
    comp.run()
    print(f"The sample program leaves {comp.registers['a']} in register a after running {comp.opcodes:,d} opcodes")

sample()

PUZZLE_PROGRAM = [
    (cpy, a, b),
    (dec, b),
    (cpy, a, d),
    (cpy, 0, a),
    (cpy, b, c),
    (inc, a),
    (dec, c),
    (jnz, c, -2),
    (dec, d),
    (jnz, d, -5),
    (dec, b),
    (cpy, b, c),
    (cpy, c, d),
    (dec, d),
    (inc, c),
    (jnz, d, -2),
    (tgl, c),
    (cpy, -16, c),
    (jnz, 1, c),
    (cpy, 80, c),
    (jnz, 77, d),
    (inc, a),
    (inc, d),
    (jnz, d, -2),
    (inc, c),
    (jnz, c, -5),
]

def puzzle1():
    comp = Computer(PUZZLE_PROGRAM)
    comp.registers['a'] = 7
    comp.run()
    print(f"Puzzle 1 leaves {comp.registers['a']} in register a after running {comp.opcodes:,d} opcodes")

puzzle1()

def puzzle2():
    comp = Computer(PUZZLE_PROGRAM)
    comp.registers['a'] = 12
    comp.run()
    print(f"Puzzle 2 leaves {comp.registers['a']} in register a after running {comp.opcodes:,d} opcodes")

puzzle2()
