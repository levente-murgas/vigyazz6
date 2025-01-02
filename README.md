# Vigyazz6 Monte Carlo Tree Search

This project implements a Monte Carlo Tree Search (MCTS) algorithm for the card game Vigyazz6. The goal is to create an AI player that can effectively play the game using MCTS. The efficiency of the AI player is evaluated through simulations of the game with different numbers of players and cards. The analysis of the results is shown in the notebook `analysis.ipynb`.

## Project Structure

- `players/monte_carlo.py`: Contains the implementation of the MCTS algorithm and the MCTSPlayer class.
- `players/player.py`: Contains the base Player class and its methods.
- `simulation.py`: Script to run simulations of the game with different numbers of players and cards.
- `game.py`: Contains the Game class that manages the game logic.
- `card.py`: Contains the Card class that represents a card in the game.
- `data/`: Directory to store the results of the simulations.

## How to Run

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/vigyazz6.git
    cd vigyazz6
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the simulation script:
    ```sh
    python simulation.py
    ```

## Monte Carlo Tree Search (MCTS)

MCTS is a heuristic search algorithm for decision processes, most notably employed in game playing. The algorithm performs simulations of the game to build a search tree and uses the results of these simulations to make decisions.

### Key Components

- **State**: Represents the current state of the game, including the rows of cards and the players.
- **MonteCarloTreeSearchNode**: Represents a node in the MCTS tree, containing the state, parent node, children nodes, and methods for expansion, simulation, and backpropagation.
- **MCTSPlayer**: A player that uses MCTS to pick the best card to play.

## Simulation

The `simulation.py` script runs multiple simulations of the game with varying numbers of players and cards. The results are saved in CSV files in the `data/` directory.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.
