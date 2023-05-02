import random


class RandomPlayer:
    def choose_move(self, board):
        move = random.randrange(0, 9)
        while board[move] != 0:
            move = random.randrange(0, 9)
        return move
