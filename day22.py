#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/22

import collections
import hashlib
import itertools
import math
import re

import pytest


class Node:
    def __init__(self, x, y, size, used):
        self.x, self.y = x, y
        self.size = size
        self.used = used

    @property
    def avail(self):
        return self.size - self.used

    def __repr__(self):
        return f"<Node ({self.x}, {self.y})>"


def range2d(maxx, maxy):
    for y in range(maxy):
        for x in range(maxx):
            yield x, y

def adjacent_coords(x, y, maxx, maxy):
    if x > 0:
        yield (x, y), (x - 1, y)
    if y > 0:
        yield (x, y), (x, y - 1)
    if x < maxx - 1:
        yield (x, y), (x + 1, y)
    if y < maxy - 1:
        yield (x, y), (x, y + 1)

def all_adjacent_coords(maxx, maxy):
    for x, y in range2d(maxx, maxy):
        yield from adjacent_coords(x, y, maxx, maxy)

class Nodes:
    def __init__(self):
        self.nodes = {}
        self.maxx = 0
        self.maxy = 0

    def __getitem__(self, key):
        return self.nodes[key]

    def __iter__(self):
        return iter(self.nodes.values())

    def read(self, lines):
        for line in lines:
            m = re.search(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T", line)
            if not m:
                continue
            node = Node(*map(int, m.groups()))
            self.nodes[node.x, node.y] = node

        self.maxx = max(n.x for n in self) + 1
        self.maxy = max(n.y for n in self) + 1
        self.data = {(n.x, n.y): n.used for n in self}
        self.adjacent_coords = list(all_adjacent_coords(self.maxx, self.maxy))

with open("day22_input.txt") as finput:
    nodes = Nodes()
    nodes.read(finput)

print(f"{len(nodes.nodes)}")

viable = []
for a, b in itertools.product(nodes, repeat=2):
    if a is not b and a.used != 0 and a.used <= b.avail:
        viable.append((a, b))

print(f"Part 1: there are {len(viable)} viable pairs")

from astar import State, AStar


class MemMoveState(State):
    def __init__(self, nodes, zero_location=None, my_location=None):
        self.nodes = nodes
        if my_location is None:
            my_location = (nodes.maxx - 1, 0)
        self.my_location = my_location
        if zero_location is None:
            zero_location = next((n.x, n.y) for n in nodes if n.used == 0)
        self.zero_location = zero_location

    def __hash__(self):
        return hash((self.zero_location, self.my_location))

    def __eq__(self, other):
        return self.zero_location == other.zero_location and self.my_location == other.my_location

    def is_goal(self):
        return self.my_location == (0, 0)

    def next_states(self, cost):
        for pto, pfrom in adjacent_coords(*self.zero_location, self.nodes.maxx, self.nodes.maxy):
            if self.nodes[pfrom].size > 500:    # hardcoded!
                continue

            nmy_location = self.my_location
            if pfrom == nmy_location:
                nmy_location = pto

            nstate = MemMoveState(self.nodes, pfrom, nmy_location)
            yield nstate, cost + 1

    def guess_completion_cost(self):
        return dist((0, 0), self.my_location) + dist(self.zero_location, self.my_location)

    def summary(self):
        return f"0 at {self.zero_location}, me at {self.my_location}, guess {self.guess_completion_cost()}"


def dist(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])

@pytest.mark.parametrize("pt1, pt2, answer", [
    ((0, 0), (10, 5), 15),
])
def test_dist(pt1, pt2, answer):
    assert dist(pt1, pt2) == answer


def steps_to_move_data(nodes):
    steps = AStar().search(MemMoveState(nodes), log=True)
    return steps

def test_steps_to_move_data():
    nodes = Nodes()
    nodes.read("""\
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
""".splitlines())
    assert steps_to_move_data(nodes) == 7


if __name__ == '__main__':
    with open("day22_input.txt") as finput:
        nodes = Nodes()
        nodes.read(finput)
    steps = steps_to_move_data(nodes)
    print(f"Part 2: moved the goal data in {steps} steps")
