#! /usr/bin/env python3

import fileinput
import re
from queue import Queue
from math import lcm

class Module:
    def __init__(self, glyph, outputs):
        self.glyph = glyph
        self.inputs = dict()
        self.outputs = outputs
        self.state = False

    def add_input(self, source):
        self.inputs[source] = False

    def reset(self):
        self.state = False
        for sender in self.inputs:
            self.inputs[sender] = False

    def receive(self, sender, level):
        if self.glyph is None:
            return level
        elif self.glyph == '&':
            self.inputs[sender] = level
            inv_output = True
            for value in self.inputs.values():
                inv_output &= value
            return not inv_output
        elif self.glyph == '%':
            if not level:
                self.state = not self.state
                return self.state
        return None

class Network:
    def __init__(self, modules):
        self.modules = dict(modules)
        self.connect_outputs()

    def connect_outputs(self):
        for sender in self.modules:
            for target in self.modules[sender].outputs:
                if target in self.modules:
                    self.modules[target].add_input(sender)

    def reset(self):
        for module in self.modules.values():
            module.reset()

    def backtrace(self, receiver):
        for sender, module in self.modules.items():
            if receiver in module.outputs:
                return sender, module

    def push_button(self, callback=None):
        queue = Queue()
        queue.put(('button', 'broadcaster', False))
        while not queue.empty():
            sender, receiver, level = queue.get()
            if callback is not None:
                callback(sender, receiver, level)
            if receiver in self.modules:
                module = self.modules[receiver]
                output = module.receive(sender, level)
                if output is not None:
                    for target in module.outputs:
                        queue.put((receiver, target, output))

def solve_part1(network):
    counts = { False: 0, True: 0 }

    def count_pulse(sender, receiver, level):
        nonlocal counts
        counts[level] += 1

    network.reset()
    for i in range(1000):
        network.push_button(count_pulse)

    return counts[False] * counts[True]

def solve_part2(network):
    # Note: Relies on an assumption about the network (but does not verify as per YAGNI)
    feeder, module = network.backtrace('rx')

    unseen = set(module.inputs)
    pushes, cycle = 0, 1

    def detect_cycles(sender, receiver, level):
        nonlocal cycle
        if level and receiver == feeder and sender in unseen:
            unseen.remove(sender)
            cycle = lcm(cycle, pushes)

    network.reset()
    while len(unseen) != 0:
        pushes += 1
        network.push_button(detect_cycles)

    return cycle

def parse_module(line):
    name, outputs = line.split(' -> ')
    glyph, name = (name[0], name[1:]) if name[0] in '%&' else (None, name)
    return name, Module(glyph, outputs.split(', '))

def parse_network(lines):
    return Network(map(parse_module, lines))

network = parse_network(line.rstrip() for line in fileinput.input())

print(f'Part 1: {solve_part1(network)}')
print(f'Part 2: {solve_part2(network)}')
