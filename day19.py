#! /usr/bin/env python3

import fileinput
import re

class Interval:
    def __init__(self, start, stop):
        self.start = min(start, stop)
        self.stop = stop

    def __and__(self, other):
        return Interval(max(self.start, other.start), min(self.stop, other.stop))

    def cut(self, n):
        return Interval(self.start, n), Interval(n, self.stop)

    def size(self):
        return self.stop - self.start

UNIVERSE = Interval(1, 4001)

class Part:
    def __init__(self, xmas):
        self.axes = xmas if type(xmas) == dict else dict(zip('xmas', xmas))

    def empty_part():
        return Part([ Interval(0, 0) ] * 4)

    def universal_part():
        return Part([ UNIVERSE ] * 4)

    def constrain(self, category, interval):
        return Part(self.axes | { category: self.axes[category] & interval })

    def volume(self):
        volume = 1
        for interval in self.axes.values():
            volume *= interval.size()
        return volume

    def rating(self):
        return sum(interval.start for interval in self.axes.values())

class Rule:
    def __init__(self, category=None, accept=None, reject=None):
        self.category = category
        self.accept = accept
        self.reject = reject

    def constrain(self, part):
        if self.category is None:
            return part, Part.empty_part()
        return (part.constrain(self.category, interval) for interval in (self.accept, self.reject))

class WorkflowTree:
    def __init__(self, workflows):
        self.workflows = dict(workflows)

    def accepted_volume(self, part, name='in'):
        volume = 0

        for rule, target in self.workflows[name]:
            match, part = rule.constrain(part)
            if target == 'A':
                volume += match.volume()
            elif target != 'R' and match.volume() != 0:
                volume += self.accepted_volume(match, target)

        return volume

def solve_part1(workflows, parts):
    return sum(part.rating() * workflows.accepted_volume(part) for part in parts)

def solve_part2(workflows):
    return workflows.accepted_volume(Part.universal_part())

def parse_inequality(relation, value):
    if relation == '<':
        accept, reject = UNIVERSE.cut(value)
    else:
        reject, accept = UNIVERSE.cut(value + 1)
    return accept, reject

def parse_rule(rule):
    match = re.match(r'(?:([xmas])([<>])(\d+):)?(A|R|[a-z]+)', rule)
    category, relation, value, target = match.groups()

    if category is None:
        return Rule(), target
    else:
        accept, reject = parse_inequality(relation, int(value))
        return Rule(category, accept, reject), target

def parse_workflow(line):
    name, rule_list = re.match(r'([a-z]+){(.+)}', line).groups()
    rules = [ parse_rule(rule) for rule in rule_list.split(',') ]
    return name, rules

def parse_workflow_tree(section):
    return WorkflowTree(parse_workflow(line) for line in section.split('\n'))

def parse_part(line):
    numbers = map(int, re.findall(r'\d+', line))
    return Part(Interval(n, n + 1) for n in numbers)

def parse_parts(section):
    return [ parse_part(line) for line in section.split('\n') ]

workflows_section, parts_section = ''.join(fileinput.input()).rstrip().split('\n\n')

workflows = parse_workflow_tree(workflows_section)
parts = parse_parts(parts_section)

print(f'Part 1: {solve_part1(workflows, parts)}')
print(f'Part 2: {solve_part2(workflows)}')
