from card import Card
from typing import List
import random


class Player:
    def __init__(self, id: int):
        self.id = id
        self.hand: List[Card] = []
        self.heads = 0

    def pick_card(self, rows: List[List[Card]], players: List["Player"]) -> Card:
        return random.choice(self.hand)

    def pick_row(self, rows: List[List[Card]]) -> int:
        # count the heads for each row
        heads = [sum(card.heads for card in row) for row in rows]
        # return the index of the row with the least heads
        return heads.index(min(heads))

    def add_heads(self, heads: int):
        self.heads += heads
