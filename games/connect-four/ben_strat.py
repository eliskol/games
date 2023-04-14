import random


class player:
    def __init__(self, strategy):
        self.strategy = strategy

    def choose_move(self, board):
        return self.strategy(board)


def random_strat(board):
    moves = []
    for i in range(0, len(board[0])):
        if board[0][i] == 0:
            moves.append(i)
    move = randint(0, len(moves) - 1)
    return move
