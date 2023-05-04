import random


class NearPerfectPlayer:
    def choose_move(self, board) -> int:
        roll = random.random
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

    def determine_winner(self):
        for j in range(3):
            i = 3 * j
            if self.board[j] == self.board[j + 3] == self.board[j + 6] != 0:  # columns
                return self.board[j]
            elif self.board[i] == self.board[i + 1] == self.board[i + 2] != 0:  # rows
                return self.board[i]

        if self.board[0] == self.board[4] == self.board[8] != 0:  # diagonal
            return self.board[4]
        elif self.board[2] == self.board[4] == self.board[6] != 0:  # anti-diagonal
            return self.board[4]
        elif 0 not in self.board:
            return "Tie"

        return None
