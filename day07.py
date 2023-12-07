#! /usr/bin/env python3

import fileinput
from collections import Counter

class Hand:
    def __init__(self, cards):
        self.ranks = [ Hand.rank_of(card) for card in cards ]
        self.strength = Hand.get_strength(self.ranks)

    def __lt__(self, other):
        return (self.strength, self.ranks) < (other.strength, other.ranks)

    def rank_of(card):
        return '23456789TJQKA'.index(card)

    def get_strength(ranks):
        return sorted(Counter(ranks).values(), reverse=True)

class JokerHand(Hand):
    def __init__(self, hand):
        joker_rank = Hand.rank_of('J')
        self.ranks = [ -1 if rank == joker_rank else rank for rank in hand.ranks ]
        self.strength = JokerHand.upgrade_strength(hand.strength, hand.ranks.count(joker_rank))

    def upgrade_strength(strength, joker_count):
        if 1 <= joker_count <= 4:
            strength = strength.copy()
            strength.remove(joker_count)
            strength[0] += joker_count
        return strength

def total_winnings(hands):
    return sum(rank * bid for rank, (hand, bid) in enumerate(sorted(hands), start=1))

def solve_part1(hands):
    return total_winnings(hands)

def solve_part2(hands):
    return total_winnings((JokerHand(hand), bid) for hand, bid in hands)

hands = [ (Hand(cards), int(bid)) for cards, bid in map(str.split, fileinput.input()) ]

print(f'Part 1: {solve_part1(hands)}')
print(f'Part 2: {solve_part2(hands)}')
