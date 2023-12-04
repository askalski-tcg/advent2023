#! /usr/bin/env python3

import fileinput
import re
from collections import defaultdict

class Card:
    def __init__(self, card_id, my_numbers, winning_numbers):
        self.card_id = card_id
        self.matches = len(set(my_numbers) & set(winning_numbers))

    def point_value(self):
        return 0 if self.matches == 0 else 2**(self.matches - 1)

def parse_numbers(numbers):
    return (int(n) for n in numbers.split())

def parse_card(line):
    match = re.match(r'Card *(\d+): (.*?) \| (.*)', line)
    card_id, my_numbers, winning_numbers = match.groups()
    return Card(int(card_id), parse_numbers(my_numbers), parse_numbers(winning_numbers))

def solve_part1(cards):
    return sum(card.point_value() for card in cards)

def solve_part2(cards):
    stack_delta = defaultdict(int)
    this_stack = 1
    total_cards = 0

    for i, card in enumerate(cards):
        this_stack += stack_delta[i]
        total_cards += this_stack
        stack_delta[i + 1] += this_stack
        stack_delta[i + 1 + card.matches] -= this_stack

    return total_cards

cards = [ parse_card(line) for line in fileinput.input() ]

print(f'Part 1: {solve_part1(cards)}')
print(f'Part 2: {solve_part2(cards)}')
