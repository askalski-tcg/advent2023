#! /usr/bin/env python3

import fileinput
from collections import namedtuple

class Coord(namedtuple('Coord', ('r', 'c'))):
    def __neg__(self):
        return Coord(-self.r, -self.c)

    def __add__(self, other):
        return Coord(self.r + other.r, self.c + other.c)

    def cross(self, other):
        return self.r * other.c - self.c * other.r

LEFT, RIGHT, UP, DOWN = Coord(0, -1), Coord(0, 1), Coord(-1, 0), Coord(1, 0)

PIPES = {
    '|': [ UP, DOWN ],   '-': [ LEFT, RIGHT ],
    '7': [ LEFT, DOWN ], 'F': [ RIGHT, DOWN ],
    'J': [ LEFT, UP ],   'L': [ RIGHT, UP ],
    '.': [ ]
}

def enumerate_grid(grid):
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            yield Coord(r, c), col

class PipeMaze:
    def __init__(self, grid):
        self.grid = dict(enumerate_grid(grid))
        self.s = self.find_s()
        self.grid[self.s], self.heading = self.unobscure(self.s)

    def find_s(self):
        return next(coord for (coord, value) in self.grid.items() if value == 'S')

    def unobscure(self, s):
        valid = [ d for d in (LEFT, RIGHT, UP, DOWN) if -d in PIPES[self.grid[s + d]] ]
        return next((glyph, dirs[0]) for glyph, dirs in PIPES.items() if valid == dirs)

    def follow_line(self):
        cur, heading = self.s + self.heading, self.heading
        while cur != self.s:
            yield cur, heading
            d0, d1 = PIPES[self.grid[cur]]
            heading = d0 if heading == -d1 else d1
            cur += heading
        yield cur, heading

    def solve_part1(self):
        return len(list(self.follow_line())) // 2

    def solve_part2(self):
        count = sum(coord.cross(heading) for coord, heading in self.follow_line())
        return abs(count) // 2 - self.solve_part1() + 1

maze = PipeMaze(line.rstrip() for line in fileinput.input())

print(f'Part 1: {maze.solve_part1()}')
print(f'Part 2: {maze.solve_part2()}')
