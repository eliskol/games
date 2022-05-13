class Game:
    def __init__(self, player1, player2):
        # self.player1 = player1
        # self.player2 = player2
        self.players = [player1, player2]
        self.next_player = 1
        self.moves = 0
        self.board = [[0 for _ in range(7)] for _ in range(6)]


    def check_move_validity(self, move):
        for row in self.board:
            if row[move] == 0:
                return True
        return False

    def print_board(self):
        for row in reversed(self.board):
            print(row)

    def check_move_validity(self, move):
        for row in self.board:
            if row[move] == 0:
                return True
        return False

    def determine_winner(self):
        if self.board == [[0 for _ in range(7)] for _ in range(6)]:
            return None

        player_that_made_move = self.previous_player

        for i in range(0, 6):
            for j in range(0, 4):
                print(j)
                if self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] != 0:
                    return self.board[i][j]


        for i in range(0, 3):
            for j in range(0, 7):
                if self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j] != 0:
                    return self.board[i][j]

        for i in range(0, 3):
            for j in range(0, 4):
                if self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3] != 0:
                    return self.board[i][j]

                elif self.board[5 - i][j] == self.board[5 - (i + 1)][j + 1] == self.board[5 - (i + 2)][j + 2] == self.board[5 - (i + 3)][j + 3] != 0:
                    return self.board[i][j]

        
        if any(0 in row for row in self.board):
            pass
        else:
            return 'Tie'
        
        return None

    
    def drop_token(self, player, column):
        for row in range(6):
            if self.board[row][column] == 0:
                self.board[row][column] = player
                break

    def make_move(self):
        self.moves += 1
        current_player = self.players[self.next_player - 1]
        move_to_make = current_player.choose_move(self.board)
        validity_of_move = self.check_move_validity(move_to_make)
        if validity_of_move is True:
            self.drop_token(self.next_player, move_to_make)
            self.previous_player = self.next_player
        if self.log is True:
            print('----------')
            self.print_board()
            print('Move #', self.moves)
            print(
                'Move was', move_to_make if validity_of_move is True else f'invalid: {move_to_make}', ', made by', self.next_player)
            print('----------\n')
        # funky way to switch 1 and 2 because why not
        self.next_player = [2, 1][self.next_player - 1]

    def run(self, log=False):
        self.log = log
        self.winner = self.determine_winner()
        while self.winner is None:
            # input()
            # print(self.next_player)
            self.make_move()
            self.winner = self.determine_winner()



from random_player import RandomPlayer


class InputPlayer:
    def choose_move(self, board):
        for row in reversed(board):
            print(row)
        print("Which column would you like to drop down?")
        move = input()
        return int(move)

a = InputPlayer()
b = InputPlayer()

bruh = Game(a, b)
bruh.run(log=True)
print('winner: ', bruh.winner)
# bruh.print_board()x