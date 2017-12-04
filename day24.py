"""
http://adventofcode.com/2016/day/24
"""

import collections
import itertools
import string
import textwrap

from colorama import Fore, Back, Style
import pytest

from astar import State, AStar


class Ducts:
    def __init__(self):
        self.locations = set()
        self.goals = set()
        self.start = None
        self.original = set()

    @classmethod
    def read(cls, lines, goals='123456789'):
        self = cls()
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '.':
                    self.locations.add((col, row))
                elif char == '0':
                    self.locations.add((col, row))
                    self.start = (col, row)
                elif char in goals:
                    self.locations.add((col, row))
                    self.goals.add((col, row))
        return self

    def show(self):
        numchars = string.ascii_lowercase + string.ascii_uppercase
        out = []
        width = max(col for col, row in self.locations)
        height = max(row for col, row in self.locations)
        for row in range(height+1):
            for col in range(width):
                if (col, row) in self.goals:
                    char = Back.RED + Fore.WHITE + '@' + Style.RESET_ALL
                elif (col, row) == self.start:
                    char = Back.GREEN + Fore.WHITE + '0' + Style.RESET_ALL
                elif (col, row) in self.locations:
                    char = '#'
                elif (col, row) in self.original:
                    char = ' '
                else:
                    char = Style.DIM + '.' + Style.RESET_ALL
                out.append(char)
            out.append('\n')
        return ''.join(out)

    def trim(self):
        """Produce a new Ducts with dead-ends removed."""
        locs = set(self.locations)
        while True:
            new_locs = set()
            for x, y in locs:
                if (x, y) in self.goals:
                    new_locs.add((x, y))
                elif (x, y) == self.start:
                    new_locs.add((x, y))
                else:
                    nextto = 0
                    for nx, ny in neighbors(x, y):
                        if (nx, ny) in locs:
                            nextto += 1
                    if nextto > 1:
                        new_locs.add((x, y))
            if new_locs == locs:
                break
            locs = new_locs

        trimmed = self.__class__()
        trimmed.original = self.locations
        trimmed.locations = locs
        trimmed.goals = self.goals
        trimmed.start = self.start
        return trimmed


def neighbors(x, y):
    """Produce coordinates of orthogonal neighbors."""
    yield x + 1, y
    yield x - 1, y
    yield x, y - 1
    yield x, y + 1


if 0:
    with open('day24_input.txt') as finput:
        ducts = Ducts.read(finput)
    print(ducts.show())
    print(len(ducts.locations))

if 0:
    print('-' * 80)

    trimmed = ducts.trim()
    print(trimmed.show())
    print(len(trimmed.locations))


class DuctExplorerState(State):
    def __init__(self, ducts, pos=None, goals_to_go=None):
        self.ducts = ducts
        self.pos = pos or ducts.start
        self.goals_to_go = goals_to_go if goals_to_go is not None else ducts.goals

    def __repr__(self):
        return f"<DES {self.pos} {len(self.goals_to_go)}>"

    def __hash__(self):
        return hash((self.pos, tuple(sorted(self.goals_to_go))))

    def __eq__(self, other):
        return (
            self.ducts is other.ducts and
            self.pos == other.pos and
            self.goals_to_go == other.goals_to_go
        )

    def is_goal(self):
        # This is a goal state if we have no more goal positions to visit.
        return not self.goals_to_go

    def next_states(self, cost):
        for nxy in neighbors(*self.pos):
            if nxy not in self.ducts.locations:
                continue
            goals = self.goals_to_go
            if nxy in goals:
                goals = goals - {nxy}
            nstate = DuctExplorerState(self.ducts, nxy, goals)
            yield nstate, cost + 1

    def guess_completion_cost(self):
        return len(self.goals_to_go)
        if self.goals_to_go:
            costs = []
            x, y = self.pos
            for gx, gy in self.goals_to_go:
                costs.append(abs(gx - x) + abs(gy - y))
            return max(costs)
        else:
            return 0


@pytest.mark.parametrize("cost, map", [
    (14, """\
        ###########
        #0.1.....2#
        #.#######.#
        #4.......3#
        ###########
        """),
    (3, """\
        #####
        #0..#
        #.#1#
        #.#.#
        #.#.#
        #...#
        #####
        """),
    (4, """\
        #####
        #0..#
        #.#.#
        #.#.#
        #.#.#
        #1..#
        #####
        """),
    (7, """\
        #######
        #0....#
        #.#.#.#
        #.#...#
        #.#4###
        #123###
        #######
        """),
])
def test_astar(cost, map):
    test_ducts = Ducts.read(textwrap.dedent(map).splitlines())
    actual_cost = AStar().search(DuctExplorerState(test_ducts))
    assert cost == actual_cost


if __name__ == '__main__':
    with open('day24_input.txt') as finput:
        ducts = Ducts.read(finput)
    ducts = ducts.trim()
    try:
        cost = AStar().search(DuctExplorerState(ducts))
        print(f"Part 1: fewest steps is {cost}")
    except:
        print(ducts.show())
