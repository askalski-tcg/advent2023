#! /usr/bin/env python3

import fileinput
from math import sqrt, ceil, floor
from functools import reduce

def ways_to_win(time, distance):
    midpoint = time / 2
    spread = sqrt(midpoint**2 - distance)
    lo, hi = ceil(midpoint - spread), floor(midpoint + spread)
    if lo * (time - lo) == distance: lo += 1
    if hi * (time - hi) == distance: hi -= 1
    return hi - lo + 1

def product(numbers):
    return reduce(lambda acc, val: acc * val, numbers, 1)

def join_numbers(numbers):
    return int(''.join(map(str, numbers)))

def solve_part1(times, distances):
    return product(ways_to_win(time, distance) for time, distance in zip(times, distances))

def solve_part2(times, distances):
    return ways_to_win(join_numbers(times), join_numbers(distances))

def parse_numbers(line):
    return list(map(int, line.split()[1:]))

times, distances = list(map(parse_numbers, fileinput.input()))

print(f'Part 1: {solve_part1(times, distances)}')
print(f'Part 2: {solve_part2(times, distances)}')
