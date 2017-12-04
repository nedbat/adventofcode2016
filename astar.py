"""An A* implementation."""

import time
from typing import Iterator, Tuple

from priqueue import PriQueue


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
