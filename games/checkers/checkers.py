class Game:
    def __init__(self, player1, player2) -> None:
        # self.player1 = player1
        # self.player1.player = 1
        # self.player2 = player2
        # self.player2.player = 2
        # self.players = [player1, player2]
        self.board = self.construct_starting_board()
        self.next_player = 1
        self.moves = 0
        self.p1_adjacency_matrix = [[]]

    def construct_starting_board(self) -> list:
        board = [[0 for _ in range(8)] for _ in range(8)]
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 0:
                    board[i][j] = 1
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    board[i][j] = 2
        return board

    def display_board(self) -> None:
        for row in self.board:
            print(row)

    def find_possible_moves_for_piece(self, coords):
        piece = self.board[coords[0]][coords[1]]
        # 1 = normal 1 piece, 2 = normal 2 piece
        # K1 = king for player1, K2 = king for player2
        # p1 moves in positive direction, 2 moves in negative direction
