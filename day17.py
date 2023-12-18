#! /usr/bin/env python3

import fileinput
from collections import namedtuple, defaultdict

class BucketQueue:
    def __init__(self):
        self.queue = defaultdict(list)
        self.cost = -1

    def put(self, cost, item):
        assert cost > self.cost
        self.queue[cost].append(item)

    def items(self):
        while len(self.queue) != 0:
            bucket = self.queue[self.cost]
            del self.queue[self.cost]
            while len(bucket) != 0:
                yield self.cost, bucket.pop()
            self.cost += 1

class Coord(namedtuple('Coord', ['row', 'col'])):
    def __add__(self, other):
        return Coord(self.row + other.row, self.col + other.col)

    def turn(self):
        yield Coord(-self.col, self.row)
        yield Coord(self.col, -self.row)

Crucible = namedtuple('Crucible', ['coord', 'heading'])

class Grid:
    def __init__(self, rows):
        self.dim = len(rows)
        assert self.dim == len(rows[0]), 'unimplemented non-square grid'
        self.grid = rows

    def __contains__(self, coord):
        return 0 <= coord.row < self.dim and 0 <= coord.col < self.dim

    def __getitem__(self, coord):
        return self.grid[coord.row][coord.col]

class Solver:
    def __init__(self, grid, stride):
        self.grid = grid
        self.stride = stride

    def neighbors(self, crucible):
        coord, heading = crucible
        delta = 0
        for i in range(1, self.stride.stop):
            coord += heading
            if coord not in self.grid:
                break
            delta += self.grid[coord]
            if i in self.stride:
                for turn in heading.turn():
                    yield delta, Crucible(coord, turn)

    def dijkstra(self):
        queue = BucketQueue()
        queue.put(0, Crucible(Coord(0, 0), Coord(0, 1)))
        queue.put(0, Crucible(Coord(0, 0), Coord(1, 0)))

        visited = set()
        for cost, state in queue.items():
            if state not in visited:
                yield cost, state
                visited.add(state)
                for delta, neighbor in self.neighbors(state):
                    queue.put(cost + delta, neighbor)

    def solve(self):
        goal = Coord(grid.dim - 1, grid.dim - 1)
        return next(cost for cost, state in self.dijkstra() if state.coord == goal)

def solve_part1(grid):
    return Solver(grid, range(1, 4)).solve()

def solve_part2(grid):
    return Solver(grid, range(4, 11)).solve()

def parse_grid(lines):
    return Grid([ list(map(int, line.rstrip())) for line in lines ])

grid = parse_grid(fileinput.input())

print(f'Part 1: {solve_part1(grid)}')
print(f'Part 2: {solve_part2(grid)}')
