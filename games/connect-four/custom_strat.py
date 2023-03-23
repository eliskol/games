class CustomStrat:
    def choose_move(self, board):
        move = 3
        while 0 not in [board[i][move] for i in range(6)]:
            move = (move + 1) % 7
        return move
