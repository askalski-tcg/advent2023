#! /usr/bin/env python3

import fileinput

def forward_difference(history):
    return [ b - a for a, b in zip(history, history[1:]) ]

def extrapolate(history):
    if any(history):
        return history[-1] + extrapolate(forward_difference(history))
    return 0

def solve_part1(histories):
    return sum(map(extrapolate, histories))

def solve_part2(histories):
    return solve_part1(history[::-1] for history in histories)

def parse_numbers(line):
    return [ int(n) for n in line.split() ]

histories = [ parse_numbers(line) for line in fileinput.input() ]

print(f'Part 1: {solve_part1(histories)}')
print(f'Part 2: {solve_part2(histories)}')
