#! /usr/bin/env python3

import fileinput

class Grid:
    def __init__(self, rows):
        self.dim = len(rows)
        assert(self.dim == len(rows[0]))
        self.grid = [ list(row) for row in rows ]

    def __getitem__(self, key):
        r, c = key
        return self.grid[r][c]

    def __setitem__(self, key, val):
        r, c = key
        self.grid[r][c] = val

    def key(self):
        return tuple(tuple(row) for row in self.grid)

    def tilt(self, transform):
        for c in range(self.dim):
            d = 0
            for r in range(self.dim):
                i = transform(r, c)
                if self[i] == '#':
                    d = r + 1
                elif self[i] == 'O':
                    j = transform(d, c)
                    self[i], self[j] = self[j], self[i]
                    d += 1

    def tilt_north(self):
        self.tilt(lambda r, c: (r, c))

    def tilt_west(self):
        self.tilt(lambda r, c: (c, r))

    def tilt_south(self):
        self.tilt(lambda r, c: (self.dim - r - 1, c))

    def tilt_east(self):
        self.tilt(lambda r, c: (c, self.dim - r - 1))

    def spin_cycle(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def total_load(self):
        total = 0
        for i, row in enumerate(self.grid):
            total += (self.dim - i) * len([ cell for cell in row if cell == 'O' ])
        return total

def solve_part1(rows):
    grid = Grid(rows)
    grid.tilt_north()
    return grid.total_load()

def solve_part2(rows):
    CYCLES = 1_000_000_000

    grid = Grid(rows)
    seen, load = {}, []
    for i in range(CYCLES + 1):
        key = grid.key()
        if key in seen:
            start = seen[key]
            period = i - start
            return load[start + (CYCLES - start) % period]

        seen[key] = i
        load.append(grid.total_load())
        grid.spin_cycle()

    return grid.total_load()

rows = [ line.rstrip() for line in fileinput.input() ]

print(f'Part 1: {solve_part1(rows)}')
print(f'Part 2: {solve_part2(rows)}')
