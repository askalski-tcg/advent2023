#! /usr/bin/env python3

import fileinput
from collections import namedtuple, defaultdict
import networkx as nx

Coord = namedtuple('Coord', list('xyz'))

class Brick:
    def __init__(self, start, end):
        self.x = Brick.to_range(start.x, end.x)
        self.y = Brick.to_range(start.y, end.y)
        self.z = Brick.to_range(start.z, end.z)

    def __lt__(self, other):
        return self.z.start < other.z.start

    def to_range(start, end):
        return range(start, end + 1) if start < end else range(end, start + 1)

    def footprint(self):
        for x in self.x:
            for y in self.y:
                yield x, y

    def settle(self, z0):
        self.z = range(z0, z0 + len(self.z))
        return self.z.stop

class Tower:
    def __init__(self, bricks):
        self.heightmap = defaultdict(lambda: (1, -1))

        G = nx.DiGraph()
        for i, brick in enumerate(sorted(bricks)):
            for support in self.settle(brick, i):
                G.add_edge(support, i)

        self.num_bricks = len(G.nodes) - 1

        dom = nx.immediate_dominators(G, -1)
        self.dominators = [ (i, d) for i, d in dom.items() if d != -1 ]

    def settle(self, brick, i):
        foundation = [ self.heightmap[x, y] for x, y in brick.footprint() ]

        z0 = max(foundation)[0]
        yield from (support for z, support in foundation if z == z0)

        z1 = brick.settle(z0)
        for x, y in brick.footprint():
            self.heightmap[x, y] = z1, i

    def solve_part1(self):
        critical = set(d for _, d in self.dominators)
        return self.num_bricks - len(critical)

    def solve_part2(self):
        chain = defaultdict(int)
        for i, d in sorted(self.dominators, reverse=True):
            chain[d] += chain[i] + 1
        return sum(chain.values())

def parse_coord(word):
    return Coord(*map(int, word.split(',')))

def parse_brick(line):
    return Brick(*map(parse_coord, line.rstrip().split('~')))

def parse_tower(lines):
    return Tower(map(parse_brick, lines))

tower = parse_tower(fileinput.input())

print(f'Part 1: {tower.solve_part1()}')
print(f'Part 2: {tower.solve_part2()}')
