"""
http://adventofcode.com/2016/day/24
"""

import heapq
import textwrap
import time
from typing import Iterator, Tuple


class Ducts:
    def __init__(self):
        self.locations = set()
        self.goals = set()
        self.start = None
        self.original = set()

    @classmethod
    def read(cls, lines):
        self = cls()
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '#':
                    continue
                self.locations.add((col, row))
                if char == '.':
                    continue
                elif char == '0':
                    self.start = (col, row)
                else:
                    self.goals.add((col, row))
        return self

    def show(self):
        out = []
        width = max(col for col, row in self.locations)
        height = max(row for col, row in self.locations)
        for row in range(height+1):
            for col in range(width):
                if (col, row) in self.goals:
                    char = '@'
                elif (col, row) == self.start:
                    char = '0'
                elif (col, row) in self.locations:
                    char = '#'
                elif (col, row) in self.original:
                    char = ' '
                else:
                    char = '.'
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

    print('-' * 80)

    trimmed = ducts.trim()
    print(trimmed.show())
    print(len(trimmed.locations))


class PriQueue:
    """A priority queue, with fast containment."""
    def __init__(self):
        self.q = []

    def __len__(self):
        return len(self.q)

    def push(self, item):
        heapq.heappush(self.q, item)

    def pop(self):
        val = heapq.heappop(self.q)
        return val

    def empty(self):
        return not self.q


class State:
    """Abstract interface for a State for AStar."""
    def is_goal(self) -> bool:
        pass

    def next_states(self, cost) -> Iterator[Tuple['State', float]]:
        pass

    def guess_completion_cost(self) -> float:
        """Guess at the cost to reach the goal. Must not overestimate."""
        pass


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

    def __lt__(self, other):
        return self.pos < other.pos

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
            yield DuctExplorerState(self.ducts, nxy, goals), cost + 1

    def guess_completion_cost(self):
        #return len(self.goals_to_go)
        if self.goals_to_go:
            costs = []
            x, y = self.pos
            for gx, gy in self.goals_to_go:
                costs.append(abs(gx - x) + abs(gy - y))
            return max(costs)
        else:
            return 0


class OnceEvery:
    """An object whose .now() method is true once every N seconds."""
    def __init__(self, seconds):
        self.delta = seconds
        self.last_true = 0

    def now(self):
        ret = time.time() > self.last_true + self.delta
        if ret:
            self.last_true = time.time()
        return ret


class AStar:
    def __init__(self):
        self.candidates = PriQueue()
        self.candidates_set = set()
        self.visited = set()
        self.came_from = {}

    def queue_state(self, state, cost):
        total_cost = cost + state.guess_completion_cost()
        qentry = (total_cost, cost, state)
        self.candidates.push(qentry)

    def search(self, start_state):
        should_log = OnceEvery(seconds=5)
        self.queue_state(start_state, 0)
        self.candidates_set.add(start_state)
        self.came_from[start_state] = None
        while True:
            if self.candidates.empty():
                cost = -1
                break
            qentry = self.candidates.pop()
            _, cost, best = qentry
            self.candidates_set.remove(best)
            if should_log.now():
                print(f"cost {cost}; {len(self.visited)} visited, {len(self.candidates)} candidates")
            if best.is_goal():
                break
            self.visited.add(best)
            for nstate, ncost in best.next_states(cost):
                if nstate in self.visited:
                    continue
                if nstate in self.candidates_set:
                    continue
                self.queue_state(nstate, ncost)
                self.candidates_set.add(nstate)
                self.came_from[nstate] = best

        print(f"{len(self.visited)} visited, {len(self.candidates)} candidates remaining")
        return cost

def test_astar():
    test_ducts = Ducts.read(textwrap.dedent("""\
        ###########
        #0.1.....2#
        #.#######.#
        #4.......3#
        ###########
        """).splitlines())
    cost = AStar().search(DuctExplorerState(test_ducts))
    assert cost == 14


if __name__ == '__main__':
    with open('day24_input.txt') as finput:
        ducts = Ducts.read(finput)
    cost = AStar().search(DuctExplorerState(ducts))
    print(f"Part 1: fewest steps is {cost}")
