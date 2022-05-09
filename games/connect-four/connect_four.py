class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.next_player = 1
        self.moves = 0
        self.board = [[0 for _ in range(7)] for _ in range(6)]

    def check_move_validity(self, move):
        skip

    def print_board(self):
        for row in self.board:
            print(row)

    def check_move_validity(self, move):
        for row in self.board:
            if row[move] == 0:
                return True
        return False

    def determine_winner(self):
        player_that_made_move = self.next_player = [2, 1][self.next_player - 1]
        previous_column_move = self.previous_move
        for row in reversed(range(6)):
            if self.board[row][column] == player_that_made_move:
                row_that_token_dropped_to = row
        
    
    def drop_token(self, player, column):
        for row in range(6):
            if self.board[row][column] == 0:
                self.board[row][column] = player

    def make_move(self):
        self.moves += 1
        current_player = self.players[self.next_player - 1]
        move_to_make = current_player.choose_move(self.board)
        validity_of_move = self.check_move_validity(move_to_make)
        if validity_of_move is True:
            self.drop_token(self.next_player, move_to_make)
            self.previous_move = move_to_make
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
            self.make_move()
            self.winner = self.determine_winner()


bruh = Game('a', 'a')
bruh.print_board()
