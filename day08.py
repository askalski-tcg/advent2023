#! /usr/bin/env python3

import fileinput
import re
import math

class Network:
    def __init__(self, moves):
        self.moves = moves
        self.succ = { }

    def add_node(self, node, left, right):
        self.succ[node] = (left, right)

    def a_nodes(self):
        return (node for node in self.succ if node[-1] == 'A')

    def first_z(self, node):
        return next(steps for (steps, node) in enumerate(self.successors(node), 1) if node[-1] == 'Z')

    def successors(self, node):
        while True:
            for move in self.moves:
                node = self.succ[node][move]
                yield node

def ends_with(char):
    return lambda node: node[-1] == char

def solve_part1(network):
    return network.first_z('AAA')

def solve_part2(network):
    # the input was special: this is not a general solution
    return math.lcm(*(network.first_z(node) for node in network.a_nodes()))

def parse_network(text):
    moves, nodes = text.split('\n\n')
    network = Network([ 'LR'.index(move) for move in moves ])
    for node in nodes.rstrip().split('\n'):
        network.add_node(*re.findall(r'\w+', node))
    return network

network = parse_network(''.join(fileinput.input()))

print(f'Part 1: {solve_part1(network)}')
print(f'Part 2: {solve_part2(network)}')
