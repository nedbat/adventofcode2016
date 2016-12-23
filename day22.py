#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/22

import collections
import hashlib
import itertools
import re

import pytest


class Node:
    def __init__(self, x, y, size, used, avail):
        self.x, self.y = x, y
        self.size = size
        self.used = used
        self.avail = avail

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

maxx = max(n.x for n in nodes.values())
maxy = max(n.y for n in nodes.values())
print(f"maxx is {maxx}, maxy is {maxy}")

for y in range(maxy+1):
    for x in range(maxx+1):
        empty = nodes[x, y].used == 0
        c = "_" if empty else "#"
        print(c, end="")
    print()

def moves(n1, n2):
    if n1.used != 0 and n1.used <= n2.avail:
        yield (n1, n2)

def possible_moves(nodes):
    for node in nodes.values():
        if node.x < maxx:
            other = nodes[node.x+1, node.y]
            yield from moves(node, other)
            yield from moves(other, node)
        if node.y < maxy:
            other = nodes[node.x, node.y+1]
            yield from moves(node, other)
            yield from moves(other, node)

possibles = list(possible_moves(nodes))
print(f"{len(possibles)} possible moves")
print(possibles)

def nodes_fingerprint(nodes):
    canon = sorted((n.x, n.y, n.used) for n in nodes.values())
    return hashlib.md5(str(canon).encode('ascii')).hexdigest()

class Walker:
    def __init__(self, nodes, goal, target):
        self.nodes = nodes
        self.goal = goal
        self.target = target
        self.minimum = 99999999
        self.seen = set()

    def step(self, steps):
        if self.goal == self.target:
            self.minimum = steps
            yield steps
        elif steps < self.minimum:
            fingerprint = nodes_fingerprint(self.nodes)
            if fingerprint not in self.seen:
                self.seen.add(fingerprint)
                for from_node, to_node in list(possible_moves(self.nodes)):
                    # Save and update the goal
                    old_goal = self.goal
                    if from_node == self.goal:
                        self.goal = to_node

                    # Move the data.
                    data_moving = from_node.used
                    to_node.used += data_moving
                    from_node.used = 0

                    # Continue searching.
                    yield from self.step(steps+1)

                    # Restore the state.
                    to_node.used -= data_moving
                    from_node.used = data_moving
                    self.goal = old_goal

walker = Walker(nodes, (maxx, 0), (0, 0))
print(list(walker.step(0)))
print(len(walker.seen))
