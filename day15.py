#! /usr/bin/env python3

import fileinput
from functools import reduce

class Box:
    def __init__(self):
        self.entries = []

    def lookup(self, label):
        for idx, (old_label, _) in enumerate(self.entries):
            if label == old_label:
                return idx
        return None

    def set(self, label, value):
        idx = self.lookup(label)
        if idx is not None:
            self.entries[idx] = (label, value)
        else:
            self.entries.append((label, value))

    def delete(self, label):
        idx = self.lookup(label)
        if idx is not None:
            self.entries.remove(self.entries[idx])

    def total_focusing_power(self):
        return sum(i * value for i, (_, value) in enumerate(self.entries, start=1))

class HashMap:
    def __init__(self):
        self.boxes = [ Box() for i in range(256) ]

    def set(self, label, value):
        h = HashMap.hash(label)
        self.boxes[h].set(label, value)

    def delete(self, label):
        h = HashMap.hash(label)
        self.boxes[h].delete(label)

    def total_focusing_power(self):
        return sum(i * box.total_focusing_power() for i, box in enumerate(self.boxes, 1))

    def hash(string):
        def hash_step(value, ch):
            return (value + ord(ch)) * 17 % 256
        return reduce(hash_step, string, 0)

def solve_part1(steps):
    return sum(HashMap.hash(s) for s in steps)

def solve_part2(steps):
    hashmap = HashMap()
    for step in steps:
        if step[-1] == '-':
            hashmap.delete(step[:-1])
        else:
            label, value = step.split('=')
            hashmap.set(label, int(value))
    return hashmap.total_focusing_power()

steps = next(fileinput.input()).rstrip().split(',')

print(f'Part 1: {solve_part1(steps)}')
print(f'Part 2: {solve_part2(steps)}')
