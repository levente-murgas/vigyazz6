from card import Card
import random


class Deck:
    def __init__(self):
        self.cards = [Card(i) for i in range(1, 105)]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)
