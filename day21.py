#! /usr/bin/env python3

import fileinput
from collections import namedtuple

class Grid:
    def __init__(self, rows):
        self.dim = len(rows)
        assert self.dim == len(rows[0]), 'unimplemented non-square grid'
        self.start = None
        self.grid = set()
        self.populate_grid(rows)
        assert self.start is not None

    def populate_grid(self, rows):
        for r, row in enumerate(rows):
            for c, glyph in enumerate(row):
                if glyph == 'S':
                    assert self.start is None
                    self.start = (r, c)
                elif glyph == '#':
                    self.grid.add((r, c))

    def __contains__(self, coord):
        mapped = (coord[0] % self.dim, coord[1] % self.dim)
        return mapped in self.grid

    def neighbors(self, coord):
        r, c = coord
        candidates = [ (r, c-1), (r, c+1), (r-1, c), (r+1, c) ]
        return set(coord for coord in candidates if coord not in self)

class Stepper:
    def __init__(self, grid):
        self.grid = grid
        self.frontier = set([ grid.start ])
        self.even, self.odd = set(self.frontier), set()

    def step(self):
        neighbors = set()
        for coord in self.frontier:
            neighbors |= self.grid.neighbors(coord)
        self.frontier = neighbors - self.odd
        self.odd |= self.frontier
        self.even, self.odd = self.odd, self.even

    def step_many(self, n):
        for i in range(n):
            self.step()

    def reachable(self):
        return len(self.even)

def solve_part1(grid):
    stepper = Stepper(grid)
    for i in range(64):
        stepper.step()
    return stepper.reachable()

def solve_part2(grid):
    goal = 26501365
    leap = grid.dim * 2

    stepper = Stepper(grid)
    stepper.step_many(goal % leap)
    goal -= goal % leap

    f = [ stepper.reachable() ]

    def quadratic(f):
        return len(f) > 3 and f[-1] - 3*f[-2] + 3*f[-3] - f[-4] == 0

    while not quadratic(f):
        if goal == 0:
            return f[-1]
        stepper.step_many(leap)
        goal -= leap
        f.append(stepper.reachable())

    n = goal // leap
    a, b, c = (n + 1) * (n + 2) // 2, n * (n + 2), n * (n + 1) // 2

    return (a*f[-1] - b*f[-2] + c*f[-3])

grid = Grid([ line.rstrip() for line in fileinput.input() ])

print(f'Part 1: {solve_part1(grid)}')
print(f'Part 2: {solve_part2(grid)}')
