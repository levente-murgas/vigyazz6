from game import Game
from players import Player, MCTSPlayer
from tqdm import tqdm

number_of_simulations = 1000

# p represents the number of players
for p in range(1, 5):
    with open(f"./data/results_p{p}.csv", "w") as f:
        header = "num_cards,mcts_heads,"
        header += ",".join(f"player_{i}_heads" for i in range(p))
        header += ",winner\n"
        f.write(header)
        # n represents the number of cards dealt to each player
        for n in range(5, 11):
            for x in tqdm(
                range(1, number_of_simulations),
                total=number_of_simulations,
                desc=f"Num cards:{n}, Num players:{p}",
            ):
                g = Game(num_cards=n, verbose=False)
                # generate a list of players
                bot = MCTSPlayer(0, verbose=False)
                players = [bot] + [Player(i + 1) for i in range(p)]
                for player in players:
                    g.add_player(player)
                winner = g.play_game()

                row = (
                    str(n)
                    + ","
                    + ",".join(str(player.heads) for player in players)
                    + ","
                    + str(winner)
                    + "\n"
                )
                f.write(row)
