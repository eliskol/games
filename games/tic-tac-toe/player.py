class Player:
    def __init__(self, strategy):
        self.strategy = strategy

    def choose_move(self, board):
        return self.strategy(board)
