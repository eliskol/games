import math
import random
import numpy as np
from tic_tac_toe import Game
from neural_net import NeuralNet
from near_perfect import NearPerfectPlayer

sigmoid = np.vectorize(lambda x: 1 / (1 + math.e ** -x))
sigmoid_prime = np.vectorize(lambda x: (
    math.e ** -x) / (1 + math.e ** -x) ** 2)

for i in range(50):
    H = (10 * random.random()) + 1
    num_nodes_by_layer = [9, H, 9]
    activation_functions_and_derivatives = [[sigmoid, sigmoid_prime] for _ in range(2)]
    