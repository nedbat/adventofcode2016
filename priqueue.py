"""A priority queue."""

import heapq


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
