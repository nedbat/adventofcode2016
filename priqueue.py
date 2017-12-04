"""A priority queue."""

import heapq
import itertools


class PriorityQueue:
    """A priority queue, with fast containment."""

    # Basically, this as a class:
    # https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes

    REMOVED = object()

    def __init__(self):
        self.q = []
        self.counter = itertools.count()
        self.items = {}

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

    def add(self, item, priority):
        if item in self:
            self.remove(item)
        entry = [priority, next(self.counter), item]
        self.items[item] = entry
        heapq.heappush(self.q, entry)

    def remove(self, item):
        entry = self.items.pop(item)
        entry[2] = self.REMOVED

    def pop(self):
        while self.q:
            _, _, item = heapq.heappop(self.q)
            if item is not self.REMOVED:
                del self.items[item]
                return item
        raise IndexError("Pop from empty priority queue")

    def empty(self):
        return not self.items
