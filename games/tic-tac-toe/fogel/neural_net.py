import time
import math
import numpy as np

# refactor this whole thing (lol, lmao)


class NeuralNet:
    def __init__(
        self,
        A,
        b,
        activation_functions_and_derivatives: list[np.vectorize],
        datapoints,
        learning_rate,
    ):
        self.A = A
        self.b = b
        self.activation_functions_and_derivatives = activation_functions_and_derivatives
        # should be [[activation func for 1st layer, derivative], [2nd layer, derivative], .. etc]; currently can't do diff activation functions for diff neurons on same layer
        self.datapoints = datapoints
        self.learning_rate = learning_rate
        self.mutation_rate = None
        self.number_of_weights = sum(
            [matrix.shape[0] * matrix.shape[1] for matrix in self.A]
        ) + sum([matrix.shape[0] * matrix.shape[1] for matrix in self.b])
        self.num_nodes_by_layer = [
            weight_matrix.shape[1] for weight_matrix in self.A
        ] + [
            self.A[-1].shape[0]
        ]  # using weight matrix shapes to find num nodes by layer

    @classmethod
    def random(
        cls,
        num_nodes_by_layer,
        bounds,
        activation_functions_and_derivatives,
        datapoints,
        learning_rate,
    ):
        rng = np.random.default_rng()

        A_weight_matrix_shapes = [
            (num_nodes_by_layer[i + 1], num_nodes_by_layer[i])
            for i in range(len(num_nodes_by_layer) - 1)
        ]
        b_weight_matrix_shapes = [
            (num_nodes_by_layer[i + 1], 1) for i in range(len(num_nodes_by_layer) - 1)
        ]

        A = []
        b = []
        for shape in A_weight_matrix_shapes:
            A.append(np.matrix(rng.uniform(low=bounds[0], high=bounds[1], size=shape)))
        for shape in b_weight_matrix_shapes:
            b.append(np.matrix(rng.uniform(low=bounds[0], high=bounds[1], size=shape)))

        return cls(
            A, b, activation_functions_and_derivatives, datapoints, learning_rate
        )

    def propagate_forward(self, A, b, x, y):
        Sigma = [None]
        h = [np.matrix(x)]
        for i in range(len(A)):
            activation_function = self.activation_functions_and_derivatives[i][0]
            Sigma.append(A[i] * h[i] + b[i])
            h.append(activation_function(Sigma[i + 1]))
        return Sigma, h

    def propagate_backward(
        self, A: list[np.matrix], b, x, y, Sigma: list[np.matrix], h: list[np.matrix]
    ):
        dRSS_dh = []
        dRSS_dh.append(2 * (h[-1] - y))
        for l, A_l in enumerate(reversed(A[1:])):
            activation_function_derivative = self.activation_functions_and_derivatives[
                l
            ][1]
            dRSS_dh.append(
                A_l.transpose()
                @ (
                    np.multiply(
                        dRSS_dh[-1], activation_function_derivative(Sigma[-l - 1])
                    )
                )
            )
        return dRSS_dh[::-1]

    def expand_neuron_gradients_to_weight_gradients(self, dRSS_dh, Sigma, h):
        dRSS_db = []
        dRSS_da = []
        for l in range(0, len(h) - 1):
            activation_function_derivative = self.activation_functions_and_derivatives[
                l
            ][1]
            dRSS_db.append(
                np.multiply(dRSS_dh[l], activation_function_derivative(Sigma[l + 1]))
            )
            dRSS_da.append(np.matrix(np.outer(dRSS_db[l], h[l])))
        return dRSS_db, dRSS_da

    def sum_weight_gradients(self):
        self.dRSS_da = [np.zeros(matrix.shape) for matrix in self.A]
        self.dRSS_db = [np.zeros(matrix.shape) for matrix in self.b]
        for [x, y] in self.datapoints:
            Sigma, h = self.propagate_forward(self.A, self.b, x, y)
            dRSS_dh = self.propagate_backward(self.A, self.b, x, y, Sigma, h)
            dRSS_db, dRSS_da = self.expand_neuron_gradients_to_weight_gradients(
                dRSS_dh, Sigma, h
            )
            for l in range(len(self.dRSS_da)):
                self.dRSS_da[l] += dRSS_da[l]
                self.dRSS_db[l] += dRSS_db[l]

    def descend_gradient_to_new_weights(self):
        for l in range(len(self.A)):
            self.A[l] = self.A[l] - self.learning_rate * self.dRSS_da[l]
            self.b[l] = self.b[l] - self.learning_rate * self.dRSS_db[l]

    def train(self, iterations):
        beginning = time.time()
        data = [beginning, 0]
        for i in range(iterations):
            self.sum_weight_gradients()
            self.descend_gradient_to_new_weights()
            # if time.time() - data[0] > 3:
            #     print(i, 'completed;', (i - data[1]) / (time.time() - data[0]), 'per second in last interval;', (i + 1) / (time.time() - beginning), 'iter/s overall')
            #     data = [time.time(), i]
        print("training completed!")

    def predict(self, x):
        return self.propagate_forward(self.A, self.b, x, None)[1][-1]

    def compute_RSS(self):
        return sum([(self.predict(x) - y) ** 2 for x, y in self.datapoints])
