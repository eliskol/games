class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.board = [0 for _ in range(9)]
        self.next_player = 1
        self.moves = 0

    def check_move_validity(self, move):
        if self.board[move] != 0:
            return False
        return True

    def print_board(self):
        print(f'{self.board[0]} {self.board[1]} {self.board[2]}\n{self.board[3]} {self.board[4]} {self.board[5]}\n{self.board[6]} {self.board[7]} {self.board[8]}')

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
            return 'Tie'

        return None

    def make_move(self):
        self.moves += 1
        current_player = self.players[self.next_player - 1]
        move_to_make = current_player.choose_move(self.board)
        validity_of_move = self.check_move_validity(move_to_make)
        if validity_of_move is True:
            self.board[move_to_make] = self.next_player
        if self.log is True:
            print('----------')
            self.print_board()
            print('Move #', self.moves)
            print('Move was', move_to_make if validity_of_move is True else f'invalid: {move_to_make}', ', made by', self.next_player)
            print('----------\n')
        self.next_player = [2, 1][self.next_player - 1]  # funky way to switch 1 and 2 because why not

    def run(self, log=False):
        self.log = log
        self.winner = self.determine_winner()
        while self.winner is None:
            self.make_move()
            self.winner = self.determine_winner()
