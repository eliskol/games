class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.next_player = player1
        self.moves = 0
        self.board = [[0 for _ in range(7)] for _ in range(6)]
    
    def check_move_validity(self, move):
        skip 

    def print_board(self):
        for row in self.board:
            print(row)

    def determine_winner(self):
        

bruh = Game('a', 'a')
bruh.print_board()