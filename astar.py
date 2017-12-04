"""An A* implementation."""

import time
from typing import Iterator, Tuple

from priqueue import PriorityQueue


class State:
    """Abstract interface for a State for AStar."""
    def is_goal(self) -> bool:
        pass

    def next_states(self, cost) -> Iterator[Tuple['State', float]]:
        pass

    def guess_completion_cost(self) -> float:
        """Guess at the cost to reach the goal. Must not overestimate."""
        pass


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
        self.candidates = PriorityQueue()
        self.costs = {}
        self.visited = set()
        self.came_from = {}

    def add_candidate(self, state, cost):
        total_cost = cost + state.guess_completion_cost()
        self.costs[state] = cost
        self.candidates.add(state, total_cost)

    def search(self, start_state):
        should_log = OnceEvery(seconds=5)
        self.add_candidate(start_state, 0)
        self.came_from[start_state] = None
        while True:
            if self.candidates.empty():
                cost = -1
                break
            best = self.candidates.pop()
            cost = self.costs[best]
            if should_log.now():
                print(f"cost {cost}; {len(self.visited)} visited, {len(self.candidates)} candidates")
            if best.is_goal():
                break
            self.visited.add(best)
            for nstate, ncost in best.next_states(cost):
                if nstate in self.visited:
                    continue
                if nstate in self.candidates:
                    continue
                self.add_candidate(nstate, ncost)
                self.came_from[nstate] = best

        print(f"{len(self.visited)} visited, {len(self.candidates)} candidates remaining")
        return cost
