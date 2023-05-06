import sys
import numpy as np

sys.path.insert(1, sys.path[0].removesuffix("fogel"))
from tic_tac_toe import Game
from near_perfect import NearPerfectPlayer
from neural_net_player import NeuralNetPlayer

rng = np.random.default_rng()


class Fogel:
    def __init__(self, num_players) -> None:
        self.num_players = num_players
        self.neural_net_players = [
            NeuralNetPlayer(rng.integers(low=1, high=10, endpoint=True))
            for _ in range(num_players)
        ]
        self.max_payoffs = []

    def run_games(self):
        for neural_net_player in self.neural_net_players:
            neural_net_player.payoff = 0
        for i in range(32):
            for neural_net_player in self.neural_net_players:
                game = Game(neural_net_player, NearPerfectPlayer())
                game.run()
                neural_net_player.payoff += {1: 1, 2: -10, "Tie": 0}[game.winner]

    def select_best_players(self):
        for neural_net_player in self.neural_net_players:
            random_network_indexes = rng.integers(low=1, high=self.num_players, size=10)
            for i in random_network_indexes:
                neural_net_player.payoff += (
                    neural_net_player.payoff > self.neural_net_players[i].payoff
                )
        for i in range(int(self.num_players / 2)):
            neural_net_players_by_score = [
                neural_net_player.score for neural_net_player in self.neural_net_players
            ]
            del self.neural_net_players[
                neural_net_players_by_score.index(min(neural_net_players_by_score))
            ]

    def create_next_gen(self):
        for i in range(len(self.neural_net_players)):
            self.neural_net_players.append(self.neural_net_players[i].replicate())

    def run(self, iterations):
        for i in range(iterations):
            print(i)
            print("running games")
            self.run_games()
            self.max_payoffs.append(
                max(
                    [
                        neural_net_player.payoff
                        for neural_net_player in self.neural_net_players
                    ]
                )
            )
            print("pruning off players")
            self.select_best_players()
            print("adding next gen")
            self.create_next_gen()


fogels = [Fogel(50) for _ in range(20)]
for fogel in fogels:
    print("fogel numer", fogels.index(fogel))
    fogel.run(800)

print([sum([fogel.max_payoffs[i] for fogel in fogels]) / len(fogels) for i in range(800)])

