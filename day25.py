#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/25

import itertools

class Computer:
    def __init__(self, program):
        self.registers = dict.fromkeys("abcd", 0)
        self.program = list(program)
        self.pc = 0
        # A list of: (pc, registers)
        self.states = []
        # A list of output.
        self.output = []

    def run(self):
        while self.pc < len(self.program):
            #print(f"Program: {self.pc}: {self.program}\nRegisters: {self.registers}")
            if self.optimize():
                continue

            inst = self.program[self.pc]
            op = getattr(self, inst[0])
            new = op(*inst[1:])
            if new is None:
                self.pc += 1
            else:
                self.pc = new

    def optimize(self):
        inc_dec_reg = self.is_addition_loop()
        if inc_dec_reg is None:
            return False

        inc_reg, dec_reg = inc_dec_reg
        mul_reg = self.is_multiplication_loop(inc_reg, dec_reg)
        if mul_reg is not None:
            self.registers[inc_reg] += self.registers[dec_reg] * self.registers[mul_reg]
            self.registers[dec_reg] = 0
            self.registers[mul_reg] = 0
            self.pc += 5
        else:
            self.registers[inc_reg] += self.registers[dec_reg]
            self.registers[dec_reg] = 0
            self.pc += 3
        return True

    def is_addition_loop(self):
        """Are we about to execute an addition loop?

        If no, then return None

        If yes, return two registers, the destination and the source.

        """
        next_three = self.program[self.pc:self.pc+3]
        if len(next_three) < 3:
            return
        inst0, inst1, inst2 = next_three
        op0, op1, op2 = inst0[0], inst1[0], inst2[0]
        if (op0, op1, op2) not in [('inc', 'dec', 'jnz'), ('dec', 'inc', 'jnz')]:
            return

        if inst2[2] != -2:
            return

        jnz_reg = inst2[1]
        dec_reg = (inst0 if op0 == 'dec' else inst1)[1]
        inc_reg = (inst0 if op0 == 'inc' else inst1)[1]
        if jnz_reg != dec_reg:
            return
        if inc_reg == dec_reg:
            return

        return inc_reg, dec_reg

    def is_multiplication_loop(self, inc_reg, dec_reg):
        # It's at least an addition loop. Maybe it's also a multiplication
        # loop.
        next_two = self.program[self.pc+3:self.pc+5]
        if len(next_two) != 2:
            return

        inst3, inst4 = next_two
        op3, op4 = inst3[0], inst4[0]
        if (op3, op4) != ('dec', 'jnz'):
            return

        if inst4[2] != -5:
            return

        mul_reg = inst3[1]
        jnz_reg = inst4[1]
        if mul_reg != jnz_reg:
            return

        if mul_reg == inc_reg or mul_reg == dec_reg:
            return

        return mul_reg

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

    def out(self, val):
        val = self.get_val(val)
        state = (self.pc, tuple(self.registers[x] for x in "abcd"))
        if state in self.states:
            return 99999        # Force an end
        self.states.append(state)
        self.output.append(val)

cpy, inc, dec, jnz, tgl, out, a, b, c, d = "cpy inc dec jnz tgl out a b c d".split()

PUZZLE_PROGRAM = [
    (cpy, a, d),
    (cpy, 7, c),
    (cpy, 365, b),
    (inc, d),
    (dec, b),
    (jnz, b, -2),
    (dec, c),
    (jnz, c, -5),
    (cpy, d, a),
    (jnz, 0, 0),
    (cpy, a, b),
    (cpy, 0, a),
    (cpy, 2, c),
    (jnz, b, 2),
    (jnz, 1, 6),
    (dec, b),
    (dec, c),
    (jnz, c, -4),
    (inc, a),
    (jnz, 1, -7),
    (cpy, 2, b),
    (jnz, c, 2),
    (jnz, 1, 4),
    (dec, b),
    (dec, c),
    (jnz, 1, -4),
    (jnz, 0, 0),
    (out, b),
    (jnz, a, -19),
    (jnz, 1, -21),
]

def puzzle1():
    for a in itertools.count(start=1):
        comp = Computer(PUZZLE_PROGRAM)
        comp.registers['a'] = a
        comp.run()
        output = ' '.join(str(v) for v in comp.output)
        print(f"a = {a} gives {len(comp.output)} values: {output}")
        if comp.output == [0, 1]*(len(comp.output)//2):
            break

puzzle1()
