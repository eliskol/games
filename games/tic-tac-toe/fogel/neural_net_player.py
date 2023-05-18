# make neural net player; just need to configure num hidden nodes; methods for replicating nn
import math
import numpy as np
from numpy.random import normal as N
from neural_net import NeuralNet


sigmoid = np.vectorize(lambda x: 1 / (1 + math.e**-x))
sigmoid_prime = np.vectorize(lambda x: (math.e**-x) / (1 + math.e**-x) ** 2)


class NeuralNetPlayer:
    def __init__(self, H) -> None:
        self.H = H
        self.activation_functions_and_derivatives = [
            [sigmoid, sigmoid_prime] for _ in range(2)
        ]
        self.neural_net = NeuralNet.random(
            [9, self.H, 9],
            [-0.5, 0.5],
            self.activation_functions_and_derivatives,
            None,
            0.01,
        )
        self.payoff = 0
        self.score = 0
        self.id = None
        self.parent_id = None

    @classmethod
    def from_neural_net(cls, neural_net):
        H = neural_net.num_nodes_by_layer[1]
        neural_net_player = cls(H)
        neural_net_player.neural_net = neural_net
        return neural_net_player

    def choose_move(self, board):
        input_board = self.convert_board_to_input(board)
        output = self.neural_net.predict(input_board)
        move = output.argmax()
        while board[move] != 0:
            output[move] = -99999
            move = output.argmax()
        return move

    def convert_board_to_input(self, board):
        return [[-1] if board[i] == 2 else [board[i]] for i in range(9)]

    def replicate(self):
        rng = np.random.default_rng()
        new_A = []
        new_b = []
        for weight_matrix in self.neural_net.A:
            new_A.append(
                weight_matrix + np.matrix(rng.normal(0, 0.05, size=weight_matrix.shape))
            )
        for weight_matrix in self.neural_net.b:
            new_b.append(
                weight_matrix + np.matrix(rng.normal(0, 0.05, size=weight_matrix.shape))
            )
        roll = rng.random()
        if roll > 0.5:
            second_roll = rng.random()
            if second_roll < 0.5 and self.H > 1:
                new_A[0] = np.delete(new_A[0], -1, 0)
                new_A[1] = np.delete(new_A[1], -1, 1)
                new_b[0] = np.delete(new_b[0], -1, 0)

            elif second_roll > 0.5 and self.H < 10:
                new_A[0] = np.vstack([new_A[0], np.matrix([0 for _ in range(9)])])
                new_A[1] = np.hstack([new_A[1], np.matrix([[0] for _ in range(9)])])
                new_b[0] = np.vstack([new_b[0], np.matrix(0)])
        neural_net = NeuralNet(
            new_A, new_b, self.activation_functions_and_derivatives, None, 0.01
        )
        # print(self.H, neural_net.num_nodes_by_layer[1])
        nn_player = self.from_neural_net(neural_net)
        nn_player.parent_id = self.id
        return nn_player
