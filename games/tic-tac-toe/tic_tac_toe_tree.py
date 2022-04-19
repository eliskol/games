from tic_tac_toe import Game
# class TicTacToeTree:
#     def __init__(self):


class Node:
    def __init__(self, board_state):
        self.state = board_state
        self.winner = self.determine_winner()
        if self.winner == None:
            self.turn = 1 if self.state.count(1) == self.state.count(2) else 2
        else:
            self.turn = None

    def determine_winner(self):

        for j in range(3):
            i = 3 * j
            if self.state[j] == self.state[j + 3] == self.state[j + 6] != 0:  # columns
                return self.state[j]
            elif self.state[i] == self.state[i + 1] == self.state[i + 2] != 0:  # rows
                return self.state[i]

        if self.state[0] == self.state[4] == self.state[8] != 0:  # diagonal
            return self.state[4]
        elif self.state[2] == self.state[4] == self.state[6] != 0:  # anti-diagonal
            return self.state[4]
        elif 0 not in self.state:
            return 'Tie'

        return None
