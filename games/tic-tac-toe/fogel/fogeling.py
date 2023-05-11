import sys
import pickle
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

    def save_in_progress(self):
        print("saving trial in progress")
        with open("in_prog_trial.pickle", "wb") as f:
            pickle.dump(
                (self.max_payoffs, self.neural_net_players), f, pickle.HIGHEST_PROTOCOL
            )

    def resume_in_progress(self):
        with open("in_prog_trial.pickle", "rb") as f:
            self.max_payoffs = pickle.load(f)[0]
            if pickle.load(f)[1] != []:
                self.neural_net_players = pickle.load(f)[1]

    def run(self, num_generations_to_run):
        self.num_generations_to_run = num_generations_to_run
        for i in range(num_generations_to_run - len(self.max_payoffs)):
            self.current_generation = i
            print(i)
            print("adding next gen")
            self.create_next_gen()
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
            if (i + 1) % 10 == 0:
                self.save_in_progress()
        with open("in_prog_trial.pickle", "wb") as f:
            pickle.dump(([], []), f, pickle.HIGHEST_PROTOCOL)


def start(num_trials, num_nets, num_gens):
    completed_trials_data = get_completed_trials_data()
    num_completed_trials = len(completed_trials_data)
    fogels = [Fogel(num_nets) for _ in range(num_trials - num_completed_trials)]
    for fogel in fogels:
        print("fogel numer", fogels.index(fogel))
        fogel.run(num_gens)
        completed_trials_data = get_completed_trials_data()
        completed_trials_data.append(fogel.max_payoffs)
        dump_completed_trials_data()


def get_completed_trials_data():
    try:
        with open("completed_trials_data.pickle", "rb") as f:
            completed_trials_data = pickle.load(f)
    except (FileNotFoundError, EOFError):
        completed_trials_data = []
    return completed_trials_data


def dump_completed_trials_data(completed_trials_data):
    with open("completed_trials_data.pickle", "wb") as f:
        pickle.dump(completed_trials_data, f, pickle.HIGHEST_PROTOCOL)


start(20, 10, 10)

print([sum([fogel.max_payoffs[i] for fogel in fogels]) / len(fogels) for i in range(1)])
