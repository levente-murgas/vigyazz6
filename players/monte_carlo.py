import numpy as np
from typing import List, Optional
from card import Card
from .player import Player  # Updated import statement
from copy import deepcopy
import random


class State:
    def __init__(self, rows: List[List[Card]], players: List[Player]):
        self.rows = rows
        self.players = players
        self.bot = players[0]

    @classmethod
    def from_state(cls, state: "State") -> "State":
        return cls(deepcopy(state.rows), deepcopy(state.players))

    def is_game_over(self):
        return len(self.bot.hand) == 0

    def get_legal_actions(self):
        return self.bot.hand if self.bot.hand else []

    def simulate_round(self, action: Card):
        current_state = State.from_state(self)
        cards_played = {
            player: player.pick_card(self.rows, self.players)
            for player in self.players
            if player != self.bot
        }
        cards_played[self.bot] = action
        sorted_cards = sorted(cards_played.items(), key=lambda x: x[1].value)
        for player, card in sorted_cards:
            self.rows = self.apply_action(player, card, self.rows)

        new_state = State.from_state(self)
        self.rows = current_state.rows
        self.players = current_state.players
        self.bot = current_state.bot
        return new_state

    def apply_action(self, player: Player, action: Card, new_rows: List[List[Card]]):
        player.hand.remove(action)
        valid_rows = [row for row in new_rows if action > row[-1]]
        if not valid_rows:
            row_index = np.random.randint(4)
            row = new_rows[row_index]
            for c in row:
                player.add_heads(c.heads)
            row.clear()
            row.append(action)
        else:
            row = min(valid_rows, key=lambda x: action.value - x[-1].value)
            if len(row) == 5:
                for c in row:
                    player.add_heads(c.heads)
                row.clear()
                row.append(action)
            else:
                row.append(action)
        return new_rows

    def game_result(self):
        return self.bot.heads


class MonteCarloTreeSearchNode:
    def __init__(
        self,
        state: State,
        parent=None,
        action: Optional[Card] = None,
    ):
        self.state = state
        self.parent: MonteCarloTreeSearchNode = parent
        self.children: List[MonteCarloTreeSearchNode] = []
        self._number_of_visits = 0.0
        self._result = 0.0
        self.action = action

    def n(self):
        return self._number_of_visits

    def v(self):
        return self._result

    def get_untried_actions(self):
        legal_actions = self.state.get_legal_actions()
        value_card_dict = {card.value: card for card in legal_actions}
        values = set(value_card_dict.keys())
        for child in self.children:
            child_legal_actions = child.state.get_legal_actions()
            child_values = set([card.value for card in child_legal_actions])
            values.intersection_update(child_values)

        untried_actions = [value_card_dict[value] for value in values]
        return untried_actions

    def expand(self):
        untried_actions = self.get_untried_actions()
        action = random.choice(untried_actions)
        next_state = self.state.simulate_round(action)
        child_node = MonteCarloTreeSearchNode(next_state, parent=self, action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self) -> float:
        current_rollout_state = self.state

        while not current_rollout_state.is_game_over():
            action = self.rollout_policy(current_rollout_state.get_legal_actions())
            current_rollout_state = current_rollout_state.simulate_round(action)
        return current_rollout_state.game_result()

    def backpropagate(self, result: float):
        self._number_of_visits += 1.0
        self._result += result
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        """Check if all moves have been expanded."""
        return len(self.children) == len(self.state.get_legal_actions())

    def best_child(self, c_param=0.1):
        choices_weights = [
            (c.v() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n()))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self, simulation_no=100, verbose=False):
        for i in range(1, simulation_no + 1):
            if verbose and i % 10 == 0:
                print(f"Simulation {i}/{simulation_no}")
            v = self._tree_policy()
            reward = -v.rollout()  # Negate reward if lower is better
            v.backpropagate(reward)
        return self.best_child(c_param=0.0)


class MCTSPlayer(Player):
    def __init__(self, id: int, verbose=False):
        super().__init__(id)
        self.verbose = verbose

    def pick_card(self, rows: List[List[Card]], players: List[Player]) -> Card:
        copy_rows = deepcopy(rows)
        copy_players = deepcopy(players)
        root = MonteCarloTreeSearchNode(State(copy_rows, copy_players))
        best_node = root.best_action(verbose=self.verbose)
        value = best_node.action.value
        for card in self.hand:
            if card.value == value:
                best_action = card
                break
        return best_action
