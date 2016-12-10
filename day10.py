#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/10

import collections
import re

import pytest


class Bot:
    def __init__(self, num):
        self.num = num

        # List of ints.
        self.chips = []

        # Will be a pair of lists to give chips to (low, high)
        self.gives_to = None

class Factory:
    def __init__(self):
        # Maps bot numbers to Bots.
        self.bots = collections.defaultdict(Bot)

        # Maps tuple of low/high to the bot number that compared them.
        self.comparers = {}

        # Maps output bin numbers to list of chips.
        self.outputs = collections.defaultdict(list)

    def get_bot(self, bot_num):
        if bot_num not in self.bots:
            self.bots[bot_num] = Bot(bot_num)
        return self.bots[bot_num]

    def give_value(self, value, bot_num):
        bot = self.get_bot(bot_num)
        bot.chips.append(value)

    def direct_bot(self, bot_num, low_kind, low_num, high_kind, high_num):
        bot = self.get_bot(bot_num)
        assert bot.gives_to is None
        if low_kind == "bot":
            low_target = self.get_bot(low_num).chips
        else:
            low_target = self.outputs[low_num]
        if high_kind == "bot":
            high_target = self.get_bot(high_num).chips
        else:
            high_target = self.outputs[high_num]
        bot.gives_to = (low_target, high_target)

    def run(self):
        while True:
            # Find bots with two chips.
            ready = []
            for bot in self.bots.values():
                assert len(bot.chips) <= 2
                if len(bot.chips) == 2:
                    ready.append(bot)
            if not ready:
                break
            for bot in ready:
                chips = sorted(bot.chips)
                self.comparers[tuple(chips)] = bot
                bot.gives_to[0].append(chips[0])
                bot.gives_to[1].append(chips[1])
                bot.chips.clear()

def parse(instructions, factory):
    for inst in instructions:
        m = re.match(r"value (\d+) goes to bot (\d+)", inst)
        if m:
            value, bot_num = m.groups()
            factory.give_value(int(value), int(bot_num))
        else:
            m = re.match(r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)", inst)
            if m:
                bot_num, low_kind, low_num, high_kind, high_num = m.groups()
                factory.direct_bot(int(bot_num), low_kind, int(low_num), high_kind, int(high_num))
            else:
                raise Exception(f"WUT? {inst}")


def test_factory():
    instructions = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""
    factory = Factory()
    parse(instructions.splitlines(), factory)
    factory.run()
    assert factory.outputs[0] == [5]
    assert factory.outputs[1] == [2]
    assert factory.outputs[2] == [3]
    assert factory.comparers[(2, 5)].num == 2

def puzzle1():
    factory = Factory()
    with open("day10_input.txt") as inputf:
        parse(inputf, factory)
    factory.run()
    bot = factory.comparers[(17, 61)]
    print(f"Puzzle 1: it was bot {bot.num} that compared 17 and 61")
    for output_num in range(3):
        print(f"Output {output_num}: {factory.outputs[output_num]}")

if __name__ == "__main__":
    puzzle1()
