import sys
sys.path.insert(1, sys.path[0].replace('tests', 'games/tic-tac-toe'))


from random_tic_tac_toe_player import RandomPlayer
from tic_tac_toe import Game

player1 = RandomPlayer()
player2 = RandomPlayer()
outcomes = {'Tie': 0, 1: 0, 2: 0}
for i in range(10000):
    game = Game(player2, player1)
    game.run(log=False)
    # print(game.winner)
    outcomes[game.winner] += 1
    if i % 1000 == 0:
        print(i)
print(outcomes)