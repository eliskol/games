class PredefinedPlayer:
    def __init__(self, moves: list) -> None:
        self.moves = moves

    def choose_move(self, board: list[list[int]]) -> int:
        if self.moves == []:
            return 0
        move = self.moves.pop(0)
        if self.check_move_validity(board, move):
            return move
        else:
            while not self.check_move_validity(board, move):
                move = self.moves.pop(0)
            return move

    def check_move_validity(self, board: list[list[int]], move: int) -> bool:
        column = [row[move] for row in board]
        if 0 in column:
            return True
        return False