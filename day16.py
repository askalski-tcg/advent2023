#! /usr/bin/env python3

import fileinput
from collections import namedtuple

class Coord(namedtuple('Coord', ['row', 'col'])):
    def __add__(self, other):
        return Coord(self.row + other.row, self.col + other.col)

    def encounter(self, tile):
        match tile:
            case '-':
                return [ self ] if self.row == 0 else [ Coord(0, -1), Coord(0, 1) ]
            case '|':
                return [ self ] if self.col == 0 else [ Coord(-1, 0), Coord(1, 0) ]
            case '/':
                return [ Coord(-self.col, -self.row) ]
            case '\\':
                return [ Coord(self.col, self.row) ]
            case _:
                return [ self ]

class Beam(namedtuple('Beam', ['coord', 'heading'])):
    def step(self):
        return Beam(self.coord + self.heading, self.heading)

    def encounter(self, tile):
        return (Beam(self.coord, heading).step() for heading in self.heading.encounter(tile))

class Grid:
    def __init__(self, rows):
        self.dim = len(rows)
        assert len(rows[0]) == self.dim, 'unimplemented non-square grid'
        self.grid = rows

    def __contains__(self, coord):
        return 0 <= coord.row < self.dim and 0 <= coord.col < self.dim

    def __getitem__(self, coord):
        return self.grid[coord.row][coord.col]

    def ingresses(self):
        for start, delta in [ (0, +1), (self.dim - 1, -1) ]:
            for i in range(self.dim):
                yield Beam(Coord(start, i), Coord(delta, 0))
                yield Beam(Coord(i, start), Coord(0, delta))

def dfs(start, neighbors):
    visited = set()
    frontier = [ start ]
    while any(frontier):
        current = frontier.pop()
        visited.add(current)
        frontier.extend(n for n in neighbors(current) if n not in visited)
    return visited

def illuminate(grid, start):
    def neighbors(beam):
        return (n for n in beam.encounter(grid[beam.coord]) if n.coord in grid)
    return len(set(beam.coord for beam in dfs(start, neighbors)))

def solve_part1(grid):
    return illuminate(grid, Beam(Coord(0, 0), Coord(0, +1)))

def solve_part2(grid):
    return max(illuminate(grid, start) for start in grid.ingresses())

grid = Grid([ line.rstrip() for line in fileinput.input() ])

print(f'Part 1: {solve_part1(grid)}')
print(f'Part 2: {solve_part2(grid)}')
