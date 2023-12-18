#! /usr/bin/env python3

import fileinput
from collections import namedtuple

class Coord(namedtuple('Coord', ['row', 'col'])):
    def __add__(self, other):
        return Coord(self.row + other.row, self.col + other.col)

    def __mul__(self, n):
        return Coord(self.row * n, self.col * n)

RDLU = Coord(0, 1), Coord(1, 0), Coord(0, -1), Coord(-1, 0)

class Step(namedtuple('Step', ['direction', 'distance', 'color'])):
    def decode(self):
        return Step(RDLU[self.color % 16], self.color // 16, 0)

def solve_part1(steps):
    coord, perimeter, area = Coord(0, 0), 0, 0
    for step in steps:
        coord += step.direction * step.distance
        perimeter += step.distance
        area += coord.col * step.direction.row * step.distance
    return abs(area) + perimeter // 2 + 1

def solve_part2(steps):
    return solve_part1(step.decode() for step in steps)

def parse_direction(direction):
    return RDLU["RDLU".index(direction)]

def parse_color(color):
    return int(color[2:-1], 16)

def parse_step(line):
    direction, distance, color = line.rstrip().split()
    return Step(parse_direction(direction), int(distance), parse_color(color))

steps = [ parse_step(line) for line in fileinput.input() ]

print(f'Part 1: {solve_part1(steps)}')
print(f'Part 2: {solve_part2(steps)}')
