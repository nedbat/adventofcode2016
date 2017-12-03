"""
http://adventofcode.com/2016/day/24
"""


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


with open('day24_input.txt') as finput:
    ducts = Ducts.read(finput)
print(ducts.show())
print(len(ducts.locations))

print('-' * 80)

trimmed = ducts.trim()
print(trimmed.show())
print(len(trimmed.locations))
