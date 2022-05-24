class InputPlayer:
    def choose_move(self, board):
        for row in reversed(board):
            print(row)
        print("Which column would you like to drop down?")
        move = input()
        return int(move)