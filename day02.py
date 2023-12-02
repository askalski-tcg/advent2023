#! /usr/bin/env python3

import fileinput
import re
from collections import defaultdict
from functools import reduce

class RGB:
    def __init__(self, r=0, g=0, b=0):
        self.R, self.G, self.B = r, g, b

    def power(self):
        return self.R * self.G * self.B

    def any_greater(self, rgb):
        return self.R > rgb.R or self.G > rgb.G or self.B > rgb.B

    def max(self, rgb):
        return RGB(max(self.R, rgb.R), max(self.G, rgb.G), max(self.B, rgb.B))

def solve_part1(games):
    limit = RGB(12, 13, 14)

    def over_limit(game):
        return any(rgb for rgb in game if rgb.any_greater(limit))

    return sum(id for id, game in games if not over_limit(game))

def solve_part2(games):
    def minimum_needed(game):
        return reduce(lambda x, y: x.max(y), game)

    return sum(minimum_needed(game).power() for id, game in games)

def parse_rgb(rgb):
    cubes = defaultdict(int)

    for count, color in re.findall(r'(\d+) (\w+)', rgb):
        cubes[color] = int(count)

    return RGB(cubes['red'], cubes['green'], cubes['blue'])

def parse_game(game):
    m = re.match(r'Game (\d+): (.+)', game)

    id, rgbs = int(m[1]), m[2].split(';')

    return id, list(map(parse_rgb, rgbs))

games = [ parse_game(game) for game in fileinput.input() ]

print(f'Part 1: {solve_part1(games)}')
print(f'Part 2: {solve_part2(games)}')
