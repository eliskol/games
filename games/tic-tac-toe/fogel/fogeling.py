import sys
import pickle
import time
import numpy as np
import pandas as pd

sys.path.insert(1, sys.path[0].removesuffix("fogel"))
from tic_tac_toe import Game
from neural_net import NeuralNet
from input_player import InputPlayer
from near_perfect import NearPerfectPlayer
from neural_net_player import NeuralNetPlayer, sigmoid, sigmoid_prime

# bruh = Game(InputPlayer(), NearPerfectPlayer())
# bruh.run()
rng = np.random.default_rng()

activation_functions_and_derivatives = [[sigmoid, sigmoid_prime] for _ in range(2)]


class FogelTrial:
    def __init__(self, num_players) -> None:
        self.num_players = num_players
        self.neural_net_players = [
            NeuralNetPlayer(rng.integers(low=1, high=10, endpoint=True))
            for _ in range(num_players)
        ]
        self.set_initial_nn_player_ids()
        self.max_payoffs = []
        self.current_generation = 0

    def set_initial_nn_player_ids(self):
        for i in range(self.num_players):
            self.neural_net_players[i].id = i + 1

    def set_child_player_ids(self):
        for i in range(self.num_players):
            self.neural_net_players[i + self.num_players].id = (
                self.current_generation * self.num_players + i + 1
            )

    def reset_nn_players(self):
        for nn_player in self.neural_net_players:
            nn_player.payoff = 0
            nn_player.score = 0
            nn_player.record = [0, 0, 0]
            nn_player.opponents = [[], [], []]
            nn_player.is_parent = True
            nn_player.selected = False

    def run_games(self):
        for nn_player in self.neural_net_players:
            for i in range(32):
                game = Game(nn_player, NearPerfectPlayer())
                game.run()
                nn_player.payoff += {1: 1, 2: -10, "Tie": 0}[game.winner]
                nn_player.record[{1: 0, 2: 1, "Tie": 2}[game.winner]] += 1

    def score_players(self):
        for nn_player in self.neural_net_players:
            other_network_indexes = [i for i in range(2 * self.num_players)]
            other_network_indexes.remove(self.neural_net_players.index(nn_player))
            random_network_indexes = rng.choice(other_network_indexes, 10)
            for i in random_network_indexes:
                opponent_player = self.neural_net_players[i]
                if nn_player.payoff > opponent_player.payoff:
                    nn_player.opponents[0].append(opponent_player.id)
                    nn_player.score += 1
                elif nn_player.payoff < opponent_player.payoff:
                    nn_player.opponents[1].append(opponent_player.id)
                elif nn_player.payoff == opponent_player.payoff:
                    nn_player.opponents[2].append(opponent_player.id)

    def identify_best_players(self):
        self.score_players()

        neural_net_players_by_score = sorted(
            self.neural_net_players, key=lambda player: player.score
        )
        # print("getting rid of player with score", min(neural_net_players_by_score))
        for nn_player in neural_net_players_by_score[self.num_players :]:
            nn_player.selected = True

    def create_next_gen(self):
        self.neural_net_players += [
            nn_player.replicate() for nn_player in self.neural_net_players
        ]

    def save_in_progress(self):
        print("saving trial in progress")
        neural_net_params = []
        for nn_player in self.neural_net_players:
            neural_net_params.append(
                (
                    list(nn_player.neural_net.A),
                    list(nn_player.neural_net.b),
                    # list(
                    #     neural_net_player.neural_net.activation_functions_and_derivatives
                    # ),
                    None,
                    float(nn_player.neural_net.learning_rate),
                )
            )
        with open("in_prog_trial.pickle", "wb") as f:
            pickle.dump(
                (self.max_payoffs, list(neural_net_params)),
                f,
                pickle.HIGHEST_PROTOCOL,
            )

    def resume_in_progress(self):
        try:
            with open("in_prog_trial.pickle", "rb") as f:
                self.max_payoffs = pickle.load(f)[0]
                if pickle.load(f)[1] != []:
                    neural_net_params = pickle.load(f)[1]
                    self.neural_net_players = [
                        NeuralNetPlayer.from_neural_net(
                            NeuralNet(
                                *neural_net_params.insert(
                                    2, activation_functions_and_derivatives
                                )[i]
                            )
                        )
                        for i in range(self.num_players)
                    ]
        except FileNotFoundError:
            pass
        except EOFError:
            pass

    def print_log_key(self):
        print("HYPERPARAMETERS")
        print(f"Networks per generation: {self.num_players}")
        print("ABBREVIATIONS")
        print("star (*) if selected")
        print("H = number of non-bias neurons in the hidden layer")
        print("[min weight, mean weight, max weight]")
        print("(wins : losses : ties)")
        print("(IDs won against | IDs lost against | IDs tied against)")

    def print_log_info(self):
        print(f"GENERATION {self.current_generation}")
        for nn_player in self.neural_net_players:
            print(
                f"{'*' if nn_player.selected else ' '} NN {nn_player.id} ({'parent' if nn_player.is_parent else f'child of {nn_player.parent_id}'}, H={nn_player.H}, {[round(weight, 2) for weight in nn_player.weight_info]})"
            )
            print(
                f"payoff {nn_player.payoff} {str(nn_player.record).replace('[', '(').replace(']', ')')}"
            )
            print(f"score={nn_player.score} {nn_player.opponents}")

            print()

        print(
            f"Highest payoff was {max([nn_player.payoff for nn_player in self.neural_net_players])}"
        )
        print(
            f"Average payoff was {sum([nn_player.payoff for nn_player in self.neural_net_players]) / (2 * self.num_players)}"
        )
        print()

    def run(self, num_generations_to_run, log=False):
        self.resume_in_progress()
        for i in range(len(self.max_payoffs), num_generations_to_run):
            start = time.time()
            self.current_generation += 1

            if not log:
                print(f"Generation {self.current_generation}")

            self.reset_nn_players()

            print("adding next gen")
            self.create_next_gen()

            self.set_child_player_ids()

            print("running games")
            self.run_games()

            self.identify_best_players()

            if log:
                self.print_log_info()

            max_payoff = max(
                [nn_player.payoff for nn_player in self.neural_net_players]
            )
            self.max_payoffs.append(max_payoff)
            self.former_best_player = self.neural_net_players[
                [nn_player.payoff for nn_player in self.neural_net_players].index(
                    max_payoff
                )
            ]

            # sort in order of score, then take upper half
            self.neural_net_players.sort(key=lambda player: player.score)
            self.neural_net_players = self.neural_net_players[self.num_players :]

            # resort by id (which players are oldest)
            self.neural_net_players.sort(key=lambda player: player.id)

            # print(
            #     f"Average payoff after pruning is {sum([nn_player.payoff for nn_player in self.neural_net_players]) / self.num_players}"
            # )

            print(time.time() - start)

            if (i + 1) % 10 == 0:
                self.save_in_progress()

            print()
        with open("in_prog_trial.pickle", "wb") as f:
            pickle.dump(([], []), f, pickle.HIGHEST_PROTOCOL)


def start(num_trials, num_nets, num_gens, log=False):
    completed_trials_data = get_completed_trials_data()
    num_completed_trials = len(completed_trials_data)
    print(
        f"Number of trials completed: {num_completed_trials}; Number of trials to go: {num_trials - num_completed_trials}",
    )
    fogel_trials = [
        FogelTrial(num_nets) for _ in range(num_trials - num_completed_trials)
    ]
    for fogel_trial in fogel_trials:
        print(f"Trial number {fogel_trials.index(fogel_trial)}")
        fogel_trial.run(num_gens, log)
        completed_trials_data = get_completed_trials_data()
        completed_trials_data.append(fogel_trial.max_payoffs)
        dump_completed_trials_data(completed_trials_data)


def get_completed_trials_data():
    try:
        with open("completed_trials_data.pickle", "rb") as f:
            completed_trials_data = pickle.load(f)
    except (FileNotFoundError, EOFError):
        completed_trials_data = []
    # print(completed_trials_data)
    return completed_trials_data


def dump_completed_trials_data(completed_trials_data):
    with open("completed_trials_data.pickle", "wb") as f:
        pickle.dump(completed_trials_data, f, pickle.HIGHEST_PROTOCOL)


num_gens = 100
num_trials = 5

start(num_trials, 25, num_gens, True)

bruh = get_completed_trials_data()
# print(len(bruh[5]))
df = pd.DataFrame(
    {
        0: [i for i in range(num_gens)],
        1: [sum(trial[i] for trial in bruh) / num_trials for i in range(num_gens)],
    }
)
plot = df.plot(x=0, y=1, kind="line")
plot.figure.savefig("bruh.png")


#  todo
#  add log data to pickle file
