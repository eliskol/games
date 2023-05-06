import random


class NearPerfectPlayer:
    def choose_move(self, board) -> int:
        roll = random.random()
        if roll < 0.1:
            move = random.randrange(0, 9)
            while board[move] != 0:
                move = random.randrange(0, 9)
            return move
        else:
            for i in range(9):
                board[i] = 2
                if self.determine_winner(board) == 2:
                    return i
                board[i] = 0
            for i in range(9):
                board[i] = 1
                if self.determine_winner(board) == 1:
                    return i
                board[i] = 0
            horizontals = [board[i : i + 3] for i in range(3)]
            verticals = [board[i::3] for i in range(3)]
            diagonals = [[0, 4, 8], [2, 4, 6]]
            lines = horizontals + verticals + diagonals
            for line in lines:
                spaces = [board[line[i]] for i in range(3)]
                if spaces.count(1) == 1 and spaces.count(0) == 2:
                    move = line[round(3 * random.random())]
                    while board[move] != 0:
                        move = line[round(3 * random.random())]
                    return move
        move = random.randrange(0, 9)
        while board[move] != 0:
            move = random.randrange(0, 9)
        return move

    def determine_winner(self, board):
        for j in range(3):
            i = 3 * j
            if board[j] == board[j + 3] == board[j + 6] != 0:  # columns
                return board[j]
            elif board[i] == board[i + 1] == board[i + 2] != 0:  # rows
                return board[i]

        if board[0] == board[4] == board[8] != 0:  # diagonal
            return board[4]
        elif board[2] == board[4] == board[6] != 0:  # anti-diagonal
            return board[4]
        elif 0 not in board:
            return "Tie"

        return None
