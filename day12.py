#! /usr/bin/env python3

import fileinput
from functools import lru_cache

def count_matches(springs, groups):
    @lru_cache
    def count_matches(springs, groups):
        length = groups[0]
        if length == 0:
            return 0 if '#' in springs else 1
        elif len(springs) < length + 1:
            return 0

        count = 0
        if springs[0] != '#':
            count += count_matches(springs[1:], groups)
        if '.' not in springs[:length] and springs[length] != '#':
            count += count_matches(springs[length + 1:], groups[1:])
        return count

    return count_matches(springs + '.', groups + (0,))

def solve_part1(records):
    return sum(count_matches(springs, groups) for springs, groups in records)

def solve_part2(records):
    return solve_part1(('?'.join([springs] * 5), groups * 5) for springs, groups in records)

def parse_numbers(numbers):
    return tuple(int(number) for number in numbers.split(','))

def parse_record(line):
    springs, groups = line.split(' ')
    return springs, parse_numbers(groups)

records = [ parse_record(line.rstrip()) for line in fileinput.input() ]

print(f'Part 1: {solve_part1(records)}')
print(f'Part 2: {solve_part2(records)}')
