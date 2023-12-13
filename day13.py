#! /usr/bin/env python3

import fileinput

class Grid:
    def __init__(self, text):
        self.grid = text.split('\n')
        self.rows, self.cols = len(self.grid), len(self.grid[0])

    def get(self, row, col):
        return self.grid[row][col]

    def getT(self, row, col):
        return self.grid[col][row]

    def transpose(self):
        self.rows, self.cols = self.cols, self.rows
        self.get,  self.getT = self.getT, self.get
        return self

    def row_errors(self, r0, r1):
        return sum(1 for i in range(self.cols) if self.get(r0, i) != self.get(r1, i))

    def hreflect_errors(self, r):
        return sum(self.row_errors(r - i - 1, r + i) for i in range(min(r, self.rows - r)))

    def find_reflection(self, errors):
        return next((r for r in range(1, self.rows) if self.hreflect_errors(r) == errors), 0)

def solve(grids, errors):
    def solve_one(grid):
        return sum(weight * grid.transpose().find_reflection(errors) for weight in (1, 100))
    return sum(solve_one(grid) for grid in grids)

def solve_part1(grids):
    return solve(grids, 0)

def solve_part2(grids):
    return solve(grids, 1)

def parse_grids(text):
    return [ Grid(grid) for grid in text.rstrip().split('\n\n') ]

grids = parse_grids(''.join(fileinput.input()))

print(f'Part 1: {solve_part1(grids)}')
print(f'Part 2: {solve_part2(grids)}')
