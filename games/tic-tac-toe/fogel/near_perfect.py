import random


class NearPerfectPlayer:
    def choose_move(self, board) -> int:
        empty_spaces = self.find_empty_spaces(board)
        board_copy = list(board)
        roll = random.random()
        if roll < 0.1:
            return random.choice(empty_spaces)
        else:
            for i in empty_spaces:
                board_copy[i] = 2
                if self.determine_winner(board_copy) == 2:
                    return i
                board_copy[i] = 0
            for i in empty_spaces:
                board_copy[i] = 1
                if self.determine_winner(board_copy) == 1:
                    return i
                board_copy[i] = 0
            horizontals = [[i for i in range(9)][i : i + 3] for i in range(3)]
            verticals = [[i for i in range(9)][i::3] for i in range(3)]
            diagonals = [[0, 4, 8], [2, 4, 6]]
            lines = horizontals + verticals + diagonals
            for line in lines:
                spaces = [board_copy[line[i]] for i in range(3)]
                if spaces.count(1) == 1 and spaces.count(0) == 2:
                    empty_spaces_in_line = self.find_empty_spaces(spaces)
                    return line[random.choice(empty_spaces_in_line)]
        return random.choice(empty_spaces)

    def find_empty_spaces(self, board):
        empty_spaces = []
        for i in range(len(board)):
            if board[i] == 0:
                empty_spaces.append(i)
        return empty_spaces

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
