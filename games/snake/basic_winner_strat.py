import time

class Winner:
    def choose_move(self, board):
        time.sleep(0.0001)
        for row in board:
            if 'e' in row:
                self.head_coords = (board.index(row), row.index('e'))
        
        if (self.head_coords[1] == 0 and self.head_coords[0] in range(0, 9)) or (self.head_coords[1] % 2 == 0 and self.head_coords[0] in range(1, 9)):
            return 'w'
        elif (self.head_coords[0] == 0 and self.head_coords[1] in range(1, 10)) or self.head_coords == (0, 9):
            return 'a'
        elif (self.head_coords[1] % 2 == 1 and self.head_coords[0] in range(2, 10)) or self.head_coords == (1, 9):
            return 's'
        elif (self.head_coords[0] == 9 and self.head_coords[1] % 2 == 0) or (self.head_coords[0] == 1 and self.head_coords[1] in range(0, 9)):
            return 'd'