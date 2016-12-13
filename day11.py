#!/usr/bin/env python3.6
#
# http://adventofcode.com/2016/day/11

import collections
import itertools
import textwrap

import pytest

class Floors:
    def __init__(self, things):
        # What floor is the elevator on?
        self.elevator = 1

        # Where each thing is: maps "AG" to a floor number.
        self.things = dict(things)

        # The previous state.
        self.previous = None

        # Check that we got a valid set of things.
        # There should be two of each element.
        firsts = collections.Counter(thing[0] for thing in self.things)
        assert all(v == 2 for v in firsts.values())

        # There should only be XG and XM.
        seconds = set(thing[1] for thing in self.things)
        assert seconds == {"G", "M"}

        # The values have to be valid floor numbers.
        assert all(1 <= f <= 4 for f in self.things.values())

    def __eq__(self, other):
        return self.elevator == other.elevator and self.things == other.things

    def __hash__(self):
        return hash((self.elevator, tuple(self.things.items())))

    def steps_from_start(self):
        steps = 0
        here = self
        while here.previous:
            here = here.previous
            steps += 1
        return steps

    def floor_contents(self):
        """Return a list of four sets, the contents of the four floors."""
        floors = [set() for _ in range(4)]
        for thing, floor in self.things.items():
            floors[floor-1].add(thing)
        return floors

    def is_valid(self):
        """Is this configuration ok? Or will a chip get fried?"""
        # Examine all the chips. Either they are connected to their generator,
        # or there are no other generators on the floor.
        floor_contents = self.floor_contents()
        for thing, floor_num in self.things.items():
            if thing[1] == 'G':
                # Only look at chips
                continue
            if floor_num == self.things[thing[0]+'G']:
                # The chip is on the same floor as its generator, fine.
                continue
            # Are there any other generators on this floor?
            if any(t[1] == 'G' for t in floor_contents[floor_num-1]):
                return False

        return True

    def is_finished(self):
        """We're done if everything is on the fourth floor."""
        return all(v == 4 for v in self.things.values())

    def show(self):
        """Return a multi-line string drawing the floors."""
        num_things = len(self.things)
        elements = sorted(set(t[0] for t in self.things))
        element_order = {e:i for i, e in enumerate(elements)}
        lines = [[f'F{f+1}', '. '] + ['. '] * num_things for f in range(4)]
        for thing, floor in self.things.items():
            column = element_order[thing[0]] * 2 + int(thing[1] == 'M')
            lines[floor-1][column + 2] = thing
        lines[self.elevator-1][1] = 'E '
        return "\n".join(reversed([' '.join(l).strip() for l in lines]))

    def copy(self):
        new = Floors(self.things)
        new.elevator = self.elevator
        return new

    def next_states(self):
        """Produce new Floors reachable one move from here."""
        this_floor = self.floor_contents()[self.elevator-1]

        # Possibilities to move: each thing by itself, and things in pairs.
        movables = [[t] for t in this_floor]
        movables.extend(itertools.combinations(this_floor, 2))

        for things in movables:
            new_floors = []
            if self.elevator > 1:
                new_floors.append(self.elevator - 1)
            if self.elevator < 4:
                new_floors.append(self.elevator + 1)

            for new_floor in new_floors:
                # Try moving them up.
                new = self.copy()
                new.elevator = new_floor
                for thing in things:
                    new.things[thing] = new_floor
                if new.is_valid():
                    new.previous = self
                    yield new

SAMPLE_DATA = {
    "HM": 1, "LM": 1,
    "HG": 2,
    "LG": 3,
}

PUZZLE_INPUT = {
    "SG": 1, "SM": 1, "PG": 1, "PM": 1,
    "TG": 2, "RG": 2, "RM": 2, "CG": 2, "CM": 2,
    "TM": 3,
}

@pytest.mark.parametrize("things", [
    {"AM": 1, "AG": 2},
    SAMPLE_DATA,
    PUZZLE_INPUT,
])
def test_floors_good_construction(things):
    # No exception raised:
    Floors(things)

@pytest.mark.parametrize("things", [
    {"AM": 1, "BG": 2},
    {"AM": 1, "AX": 2},
    {"AM": 1, "AG": 17},
    {"AM": 1, "AG": "this isn't even a number"},
    {"AM": 1, "AG": 2, "XM": 3},
])
def test_floors_bad_construction(things):
    with pytest.raises(Exception):
        Floors(things)

@pytest.mark.parametrize("things, floor_contents", [
    ({"AM": 1, "AG": 2}, [{"AM"}, {"AG"}, set(), set()]),
    (SAMPLE_DATA, [{"HM", "LM"}, {"HG"}, {"LG"}, set()]),
    (PUZZLE_INPUT, [{"SG", "SM", "PG", "PM"}, {"TG", "RG", "RM", "CG", "CM"}, {"TM"}, set()]),
])
def test_floor_contents(things, floor_contents):
    floors = Floors(things)
    assert floors.floor_contents() == floor_contents

@pytest.mark.parametrize("things", [
    SAMPLE_DATA,
    PUZZLE_INPUT,
])
def test_floors_is_valid(things):
    floors = Floors(things)
    assert floors.is_valid()

@pytest.mark.parametrize("things, output", [
    (SAMPLE_DATA, """\
            F4 .  .  .  .  .
            F3 .  .  .  LG .
            F2 .  HG .  .  .
            F1 E  .  HM .  LM
            """),
    (PUZZLE_INPUT, """\
            F4 .  .  .  .  .  .  .  .  .  .  .
            F3 .  .  .  .  .  .  .  .  .  .  TM
            F2 .  CG CM .  .  RG RM .  .  TG .
            F1 E  .  .  PG PM .  .  SG SM .  .
            """),
])
def test_show_floors(things, output):
    floors = Floors(things)
    assert floors.show() == textwrap.dedent(output).strip()

@pytest.mark.parametrize("things1, things2, equal", [
    (SAMPLE_DATA, SAMPLE_DATA, True),
    (SAMPLE_DATA, PUZZLE_INPUT, False),
])
def test_equality(things1, things2, equal):
    assert (Floors(things1) == Floors(things2)) == equal

@pytest.mark.parametrize("thingss, num_different", [
    ([SAMPLE_DATA, SAMPLE_DATA], 1),
    ([PUZZLE_INPUT, PUZZLE_INPUT], 1),
    ([SAMPLE_DATA, PUZZLE_INPUT], 2),
])
def test_hash(thingss, num_different):
    s = set(Floors(t) for t in thingss)
    assert len(s) == num_different

def test_next_states():
    floors = Floors(PUZZLE_INPUT)
    floors.elevator = 2
    assert len(set(floors.next_states())) == 7


def find_finish(floors):
    """Find a way to the finish."""
    to_try = [floors]
    seen = set([floors])
    for gen in itertools.count(start=1):
        next_to_try = []
        for floors in to_try:

            #print("="*80)
            #print("Looking at:")
            #print(floors.show())

            for next_floors in floors.next_states():
                #print("-"*40)
                #print(next_floors.show())
                if next_floors not in seen:
                    seen.add(next_floors)
                    if next_floors.is_finished():
                        return next_floors
                    else:
                        next_to_try.append(next_floors)
        print(f"Gen {gen}, seen {len(seen)} states")
        to_try = next_to_try

finish = find_finish(Floors(SAMPLE_DATA))
print(f"Found a sample finish in {finish.steps_from_start()} steps")

if 0:
    print("*"*40)
    finish = find_finish(Floors(PUZZLE_INPUT))
    print(f"Found a puzzle 1 finish in {finish.steps_from_start()} steps")

PUZZLE2_INPUT = dict(PUZZLE_INPUT, **{"DM": 1, "DG": 1, "EM": 1, "EG": 1})
if 1:
    print("*"*40)
    finish = find_finish(Floors(PUZZLE2_INPUT))
    print(f"Found a puzzle 2 finish in {finish.steps_from_start()} steps")
