from deck import Deck
from card import Card
from players import Player, MCTSPlayer
from typing import List


class Game:
    def __init__(self, num_cards: int, verbose: bool = True):
        self.players: List[Player] = []
        self.num_cards = num_cards
        self.verbose = verbose

    def setup(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.rows: List[List[Card]] = [[], [], [], []]

    def add_player(self, player: Player):
        self.players.append(player)

    def deal(self):
        for i in range(self.num_cards):
            for player in self.players:
                player.hand.append(self.deck.draw())

        for i in range(4):
            self.rows[i].append(self.deck.draw())

    def place_card(self, player: Player, card: Card):
        if self.verbose:
            print(f"Player {player.id} played {card}")
            print(f"Player {player.id} has {player.heads} heads")
        # remove the card from the player's hand
        player.hand.remove(card)
        valid_rows = [row for row in self.rows if card > row[-1]]
        if not valid_rows:
            row_index = player.pick_row(self.rows)
            row = self.rows[row_index]
            for c in row:
                player.add_heads(c.heads)
            row.clear()
            row.append(card)
        else:
            row = min(valid_rows, key=lambda x: card.value - x[-1].value)
            if len(row) == 5:
                for c in row:
                    player.add_heads(c.heads)
                row.clear()
                row.append(card)
            else:
                row.append(card)

    def play_round(self):
        # print the current rows
        for i, row in enumerate(self.rows):
            # print all cards in the row in the same line
            if self.verbose:
                print(f"Row {i}: {' '.join(str(card) for card in row)}")
        cards_played = {
            player: player.pick_card(self.rows, self.players) for player in self.players
        }
        sorted_cards = sorted(cards_played.items(), key=lambda x: x[1].value)
        for player, card in sorted_cards:
            self.place_card(player, card)

    def play_game(self):
        self.setup()
        self.deal()
        while all(player.heads < 66 for player in self.players):
            cnt = 1
            while any(player.hand for player in self.players):
                if self.verbose:
                    print("*" * 20)
                    print(f"Round {cnt}")
                self.play_round()
                cnt += 1
            self.setup()
            self.deal()
        # get min heads
        min_heads = min(player.heads for player in self.players)
        # get the winner
        winner = [player.id for player in self.players if player.heads == min_heads]
        if len(winner) > 1:
            winner = -1  # tie
        else:
            winner = winner[0]

        return winner


if __name__ == "__main__":
    g = Game(num_cards=10)
    p1 = MCTSPlayer(1, verbose=False)
    p2 = Player(2)
    g.add_player(p1)
    g.add_player(p2)
    winner = g.play_game()
    print(f"Monte Carlo AI: {p1.heads} heads")
    print(f"Naive AI: {p2.heads} heads")
    if len(winner) == 1:
        print(f"Player {winner[0]} wins!")
    else:
        print("It's a tie!")
