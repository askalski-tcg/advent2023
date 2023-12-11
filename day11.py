#! /usr/bin/env python3

import fileinput
from collections import defaultdict

def preprocess(counts):
    delta_prefix = [ ]
    items = sorted(counts.items())
    _, total = items[0]
    for (x0, _), (x1, count) in zip(items, items[1:]):
        delta_prefix.append((x1 - x0, total))
        total += count
    delta_prefix.append((0, total))
    return delta_prefix

def total_distance(axis, expansion):
    _, num_galaxies = axis[-1]
    total = 0
    for dx, prefix in axis:
        suffix = num_galaxies - prefix
        total += ((dx - 1) * expansion + 1) * prefix * suffix
    return total

def solve_generic(rows, cols, expansion):
    return sum(total_distance(axis, expansion) for axis in (rows, cols))

def solve_part1(rows, cols):
    return solve_generic(rows, cols, 2)

def solve_part2(rows, cols):
    return solve_generic(rows, cols, 1000000)

def parse_galaxies(file):
    rows, cols = defaultdict(int), defaultdict(int)
    for r, row in enumerate(file):
        for c, col in enumerate(row):
            if col == '#':
                rows[r] += 1
                cols[c] += 1
    return preprocess(rows), preprocess(cols)

rows, cols = parse_galaxies(fileinput.input())

print(f'Part 1: {solve_part1(rows, cols)}')
print(f'Part 2: {solve_part2(rows, cols)}')
