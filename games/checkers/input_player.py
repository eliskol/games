class InputPlayer:
    def choose_move(self, board):
        for row in board:
            print(row)
        print("Please input your move:")
        move = input()
        return int(move)
