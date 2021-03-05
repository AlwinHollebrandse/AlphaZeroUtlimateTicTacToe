import numpy as np

"""
Random and Human-ineracting players for the game of Ultimate TicTacToe.

Author: Alwin Hollebrandse, github.com/AlwinHollebrandse
Date: March 5, 2021.

Based on the OthelloPlayers by Surag Nair.

"""
class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanTicTacToePlayer():
    def __init__(self, game, n, numberOfLocalBoards):
        self.game = game
        self.n = n
        self.numberOfLocalBoards = numberOfLocalBoards

    def play(self, board):
        # display(board)
        valid = self.game.getValidMoves(board, 1)
        for i in range(len(valid)):
            if valid[i]:
                print(int(i/self.game.n), int(i%self.game.n))
        while True: 
            # Python 3.x
            a = input()
            # Python 2.x 
            # a = raw_input()

            localBoardIndex, localRow, localCol = [int(x) for x in a.split(' ')]
            boardvalues = np.arange(self.numberOfLocalBoards*self.n*self.n).reshape(self.numberOfLocalBoards,self.n,self.n)
            a = boardvalues[localBoardIndex][localRow][localCol]
            if valid[a]:
                break
            else:
                print('Invalid')

        return a
