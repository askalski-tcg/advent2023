#! /usr/bin/env python3

import fileinput
import re
import sympy as sp
import itertools

class Vector:
    def __init__(self, v):
        self.v = tuple(v)

    def __iter__(self):
        return iter(self.v)

    def __getitem__(self, idx):
        return self.v[idx]

    def __add__(self, other):
        return Vector(a + b for a, b in zip(self, other))

    def __sub__(self, other):
        return Vector(a - b for a, b in zip(self, other))

    def __mul__(self, other):
        if type(other) == Vector:
            return sum(a * b for a, b in zip(self, other))
        else:
            return Vector(n * other for n in self)

    def __truediv__(self, other):
        return Vector(n / other for n in self)

    def cross(self, other):
        return Vector([
            self.v[1] * other.v[2] - self.v[2] * other.v[1],
            self.v[2] * other.v[0] - self.v[0] * other.v[2],
            self.v[0] * other.v[1] - self.v[1] * other.v[0] ])

class Stone:
    def __init__(self, p, v):
        self.p = Vector(p)
        self.v = Vector(v)

    def __call__(self, t):
        return self.p + self.v * t

    def dist(self, other):
        return self.v.cross(other.v) * (other.p - self.p)

def solve_part1(stones):
    lo, hi = 200000000000000, 400000000000000
    count = 0

    for a, b in itertools.combinations(stones, 2):
        n = a.p[1] - b.p[1] + (b.p[0] - a.p[0]) * a.v[1] / a.v[0]
        d = b.v[1] - a.v[1] * b.v[0] / a.v[0]
        if d == 0:
            continue

        tb = n / d
        cx, cy, _ = b.p + b.v * tb
        ta = (cx - a.p[0]) / a.v[0]

        if ta > 0 and tb > 0 and lo <= cx <= hi and lo <= cy <= hi:
            count += 1

    return count

def solve_part2(stones):
    a, b, c, d, e = stones[:5]

    def try_intersect(s, ta, tb):
        return s.dist(Stone(a(ta), b(tb) - a(ta)))

    ta, tb = sp.symbols('ta tb')
    tb, = sp.solve(try_intersect(c, ta, tb), tb)
    for time_a in sp.solve(try_intersect(d, ta, tb), ta):
        time_b = tb.subs(ta, time_a)
        if try_intersect(e, time_a, time_b) == 0:
            rock_v = (b(time_b) - a(time_a)) / (time_b - time_a)
            rock_p = a.p + (a.v - rock_v) * time_a
            return sum(rock_p)

def parse_stone(line):
    px, py, pz, vx, vy, vz = map(int, re.findall(r'-?\d+', line))
    return Stone((px, py, pz), (vx, vy, vz))

stones = [ parse_stone(line) for line in fileinput.input() ]

print(f'Part 1: {solve_part1(stones)}')
print(f'Part 2: {solve_part2(stones)}')
