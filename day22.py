#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/22

import collections
import itertools
import re

import pytest


Node = collections.namedtuple("Node", "x, y, size, used, avail")

def read_nodes(lines):
    nodes = {}
    for line in lines:
        m = re.search(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T", line)
        if not m:
            continue
        node = Node(*map(int, m.groups()))
        nodes[node.x, node.y] = node
    return nodes

with open("day22_input.txt") as finput:
    nodes = read_nodes(finput)

print(f"{len(nodes)}")

viable = []
for a, b in itertools.product(nodes.values(), repeat=2):
    if a is not b and a.used != 0 and a.used <= b.avail:
        viable.append((a, b))

print(f"Puzzle 1: there are {len(viable)} viable pairs")
