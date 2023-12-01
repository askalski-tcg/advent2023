#! /usr/bin/env python3

import fileinput

WORDS = [
    'zero', 'one', 'two', 'three', 'four',
    'five', 'six', 'seven', 'eight', 'nine' ]

def digit(s):
    return int(s[0]) if s[0].isdigit() else None

def word(s):
    return next((n for n, word in enumerate(WORDS) if s.startswith(word)), None)

def digit_or_word(s):
    return digit(s) or word(s)

def calibration_value(line, convert):
    conversions = (convert(line[i:]) for i in range(len(line)))
    digits = [ d for d in conversions if d is not None ]
    return digits[0] * 10 + digits[-1]

def solve(lines, convert):
    return sum(calibration_value(line, convert) for line in lines)

lines = [ line.strip() for line in fileinput.input() ]

print(f'Part 1: {solve(lines, digit)}')
print(f'Part 2: {solve(lines, digit_or_word)}')
