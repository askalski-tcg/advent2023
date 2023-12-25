#! /usr/bin/env python3

import fileinput
from collections import defaultdict
import networkx as nx

class Grid:
    def __init__(self, rows):
        self.dim = len(rows)
        assert self.dim == len(rows[0]), 'unimplemented non-square grid'
        self.grid = rows
        assert self.grid[0][1] == self.grid[-1][-2] == '.'

    def __contains__(self, coord):
        r, c = coord
        return 0 <= r < self.dim and 0 <= c < self.dim

    def __getitem__(self, coord):
        r, c = coord
        return self.grid[r][c]

    def neighbors(self, coord, prev):
        r, c = coord
        for neighbor in [ (r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c) ]:
            if neighbor not in self or neighbor == prev or self[neighbor] == '#':
                continue
            if self[neighbor] == '>' and neighbor[1] < c:
                continue
            if self[neighbor] == 'v' and neighbor[0] < r:
                continue
            yield neighbor

    def to_digraph(self):
        start = (0, 1)
        goal = (self.dim - 1, self.dim - 2)

        G = nx.DiGraph()

        visited = set()
        stack = [ (start, start, (1, 1), 1) ]
        while len(stack) != 0:
            node0, prev, node, distance = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            for neighbor in self.neighbors(node, prev):
                if (self[node] in '>v' and distance > 1) or neighbor == goal:
                    G.add_edge(node0, neighbor, weight=distance + 1)
                    stack.append((neighbor, node, neighbor, 0))
                else:
                    stack.append((node0, node, neighbor, distance + 1))

        return G, start, goal

def border_paths(G, start, goal):
    border_paths = []
    visited = set()
    path = []
    def dfs(node):
        if node == goal:
            border_paths.append(list(path))
        visited.add(node)
        for neighbor in G.neighbors(node):
            if neighbor not in visited and G.degree(neighbor) < 4:
                path.append(neighbor)
                dfs(neighbor)
                path.pop()
        visited.remove(node)
    dfs(start)
    return border_paths

def weight(G, a, b):
    return G.get_edge_data(a, b)['weight']

def solve_part1(G, start, goal):
    max_weight = 0
    for path in nx.simple_paths.all_simple_paths(G, start, goal):
        total_weight = 0
        for edge in zip(path, path[1:]):
            total_weight += weight(G, *edge)
        max_weight = max(max_weight, total_weight)
    return max_weight

def solve_part2(G, start, goal):
    base_cost = 0

    # combine start node with its only successor
    node, = G.successors(start)
    base_cost += G.get_edge_data(start, node)['weight']
    G.remove_node(start)
    start = node

    # combine goal node with its only predecessor
    node, = G.predecessors(goal)
    base_cost += G.get_edge_data(node, goal)['weight']
    G.remove_node(goal)
    goal = node

    heuristic = defaultdict(int)
    for a, b in G.edges():
        w = weight(G, a, b)
        heuristic[a] = max(heuristic[a], w)
        heuristic[b] = max(heuristic[b], w)

    potential = sum(heuristic[n] for n in G.nodes() if n != start)

    G = nx.Graph(G)

    visited = set()

    # Backtracking along the graph border always leads to a dead end
    forbidden_successors = defaultdict(list)
    for path in border_paths(G, start, goal):
        for a, b in zip(path, path[1:]):
            forbidden_successors[b].append(a)
    def prune(node, neighbor):
        return neighbor in forbidden_successors[node]

    def dfs(node, cost, best=0):
        nonlocal potential
        if node == goal:
            return max(best, cost)
        # prune if we can't improve on the max
        if cost + potential <= best:
            return best
        potential -= heuristic[node]
        visited.add(node)
        for neighbor in G.neighbors(node):
            if neighbor in visited or prune(node, neighbor):
                continue
            w = weight(G, node, neighbor)
            best = max(best, dfs(neighbor, cost + w, best))
        visited.remove(node)
        potential += heuristic[node]
        return best

    return base_cost + dfs(start, 0)

grid = Grid([ line.rstrip() for line in fileinput.input() ])
G, start, goal = grid.to_digraph()

print(f'Part 1: {solve_part1(G, start, goal)}')
print(f'Part 2: {solve_part2(G, start, goal)}')
