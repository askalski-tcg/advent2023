#! /usr/bin/env python3

import fileinput
import networkx as nx
import random

class Graph:
    def __init__(self, g):
        self.g = g
        self.nodes = list(g.nodes)
        self.saved_edges = []

    def random_path(self):
        def sort(a, b):
            return (a, b) if a < b else (b, a)
        a = random.choice(self.nodes)
        b = random.choice(self.nodes)
        path = nx.shortest_path(self.g, a, b)
        return set(sort(a, b) for a, b in zip(path, path[1:]))

    def remove_temporarily(self, edge):
        self.saved_edges.append(edge)
        self.g.remove_edge(*edge)

    def restore(self):
        while len(self.saved_edges) != 0:
            edge = self.saved_edges.pop()
            self.g.add_edge(*edge)

    def try_cut(self):
        while True:
            common = self.random_path() & self.random_path()
            if len(common) == 1:
                return common.pop()

    def solve_part1(self):
        while True:
            for i in range(3):
                self.remove_temporarily(self.try_cut())
            if not nx.is_connected(self.g):
                break
            self.restore()

        a, b = list(nx.connected_components(self.g))
        return len(a) * len(b)

def parse_graph(lines):
    g = nx.Graph()
    for line in lines:
        src, *dsts = line.rstrip().split(' ')
        for dst in dsts:
            g.add_edge(src[:-1], dst)
    return Graph(g)

graph = parse_graph(fileinput.input())

print(f'Part 1: {graph.solve_part1()}')
