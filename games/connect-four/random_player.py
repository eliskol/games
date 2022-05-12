import random


class RandomPlayer:
    def choose_move(self, board):
        move = random.randrange(0, 7)
        return move