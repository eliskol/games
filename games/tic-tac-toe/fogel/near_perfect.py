import random


class NearPerfectPlayer:
    def choose_move(self, board) -> int:
        roll = random.random
        if roll > 0.1:
            move = random.randrange(0, 9)
            while board[move] != 0:
                move = random.randrange(0, 9)
            return move
        else:
            for i in range(9):

    def check_winner(self, board):
        
