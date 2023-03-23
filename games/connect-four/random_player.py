import random


class RandomPlayer:
    def choose_move(self, board):
        move = random.randrange(0, 7)
        while 0 not in [board[i][move] for i in range(6)]:
            move = random.randrange(0, 7)
        return move