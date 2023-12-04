#! /usr/bin/env python3

import fileinput
import re

adjacent_delta = [
    (-1, -1), ( 0, -1), ( 1, -1),
    (-1,  0),           ( 1,  0),
    (-1,  1), ( 0,  1), ( 1,  1) ]

number_start = dict()
number_at = dict()
symbol_at = dict()

def add_coords(a, b):
    return (a[0] + b[0], a[1] + b[1])

def find_neighbors(coord):
    adjacent = (add_coords(coord, delta) for delta in adjacent_delta)
    return set(number_start[adj] for adj in adjacent if adj in number_start)

def coords_to_numbers(coords):
    return [ number_at[coord] for coord in coords ]

def solve_part1():
    part_number_coords = set()
    for coord, symbol in symbol_at.items():
        part_number_coords.update(find_neighbors(coord))
    return sum(coords_to_numbers(part_number_coords))

def solve_part2():
    gears = (coord for coord in symbol_at if symbol_at[coord] == '*')
    gear_numbers = (coords_to_numbers(find_neighbors(coord)) for coord in gears)
    return sum(n[0] * n[1] for n in gear_numbers if len(n) == 2)

def index_new_value(y, xrange, value):
    start = (xrange[0], y)
    if value.isdecimal():
        for x in range(xrange[0], xrange[1]):
            number_start[(x, y)] = start
        number_at[start] = int(value)
    else:
        symbol_at[start] = value

for y, line in enumerate(fileinput.input()):
    for match in re.finditer(r'\d+|[^.]', line.rstrip()):
        index_new_value(y, match.span(), match[0])

print(f'Part 1: {solve_part1()}')
print(f'Part 2: {solve_part2()}')
