#! /usr/bin/env python3

import fileinput
from functools import reduce
from more_itertools import chunked

INFINITY = 9e99

class Interval:
    def __init__(self, lo, hi):
        self.lo, self.hi = lo, hi

    def __lt__(self, other):
        return self.hi < other.hi

    def empty(self):
        return self.lo == self.hi

    def contains(self, value):
        return self.lo <= value < self.hi

    def translate(self, delta):
        return Interval(self.lo + delta, self.hi + delta)

    def cut(self, value):
        left  = Interval(min(self.lo, value), min(self.hi, value))
        right = Interval(max(self.lo, value), max(self.hi, value))
        return left, right

class Mapping:
    def __init__(self, ranges):
        maps = ((Interval(src, src + length), dest - src) for dest, src, length in ranges)
        self.maps = self.fill_in_gaps(maps)

    def fill_in_gaps(self, maps):
        result = [ ]
        prev_hi = -INFINITY
        for src, delta in sorted(maps):
            left, right = Interval(prev_hi, src.hi).cut(src.lo)
            result.extend([ (left, 0), (right, delta) ])
            prev_hi = src.hi
        result.append((Interval(prev_hi, INFINITY), 0))
        return result

    def find_mapping(self, value):
        return next((src, delta) for src, delta in self.maps if src.contains(value))

    def map_interval(self, interval):
        result = [ ]
        while not interval.empty():
            src, delta = self.find_mapping(interval.lo)
            prefix, interval = interval.cut(src.hi)
            result.append(prefix.translate(delta))
        return result

    def map_intervals(self, intervals):
        return reduce(lambda acc, val: acc + self.map_interval(val), intervals, [])

def parse_seeds(text):
    return list(map(int, text.split()[1:]))

def parse_mapping(text):
    return Mapping(map(int, line.split()) for line in text.split('\n')[1:])

def map_intervals(mappings, intervals):
    return reduce(lambda acc, val: val.map_intervals(acc), mappings, intervals)

def min_mapped_value(mappings, intervals):
    return min(interval.lo for interval in map_intervals(mappings, intervals))

def solve_part1(mappings, seeds):
    intervals = (Interval(seed, seed + 1) for seed in seeds)
    return min_mapped_value(mappings, intervals)

def solve_part2(mappings, seeds):
    intervals = (Interval(lo, lo + length) for lo, length in chunked(seeds, 2))
    return min_mapped_value(mappings, intervals)

input_sections = ''.join(fileinput.input()).rstrip().split('\n\n')
seeds = parse_seeds(input_sections[0])
mappings = list(map(parse_mapping, input_sections[1:]))

print(f'Part 1: {solve_part1(mappings, seeds)}')
print(f'Part 2: {solve_part2(mappings, seeds)}')
