from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .UltimateTicTacToeLogic import GlobalBoard
import numpy as np

'''
Game class implementation for the game of Ultimate TicTacToe

Author: Alwin Hollebrandse, github.com/AlwinHollebrandse
Date: March 5, 2021.

Based on the TicTacToe by Adam Lawson.
'''

class UltimateTicTacToeGame(Game):
    def __init__(self, n=3, numberOfLocalBoards=9):
        self.n = n
        self.numberOfLocalBoards = numberOfLocalBoards
        self.b = GlobalBoard(self.n, self.numberOfLocalBoards)

    def getInitBoard(self):
        '''return initial board (numpy board)'''
        # b = GlobalBoard(self.n, self.numberOfLocalBoards)
        return np.array(self.b.globalBoard)

    def getBoardSize(self):
        '''return (a,b,c) tuple'''
        return (self.numberOfLocalBoards, self.n, self.n)

    def getActionSize(self):
        '''return number of actions'''
        return self.numberOfLocalBoards * self.n * self.n  + 1 # per Othello getSym, the +1 is for "1 for pass"

    def getNextState(self, board, player, action): # TODO need to recall prev local/curr localboard, while only returnung the tuple
        '''if player takes action on board, return next (board,player)
        action must be a valid move
        '''
        if action == self.numberOfLocalBoards * self.n * self.n: # TODO why allow for a skip?
            return (board, -player)
        # b = GlobalBoard(self.n, self.numberOfLocalBoards)
        self.b.globalBoard = np.copy(board)

        # TODO the 3d version had this, NOTE it basically is option 2 of the below TODO
        # boardvalues = np.arange(0,(self.n*self.n*self.n)).reshape(self.n,self.n,self.n)
        # move = np.argwhere(boardvalues==action)[0]
        # b.execute_move(move, player)

        # move is int that is 0-getActionSize
        # TODO is 0-8 first localboard values, or the top 9 vlaues of the global board?
        localBoardIndex = int(action / self.numberOfLocalBoards) # NOTE this uses the option 1 in above TODO
        actionModLocalBoards = int(action % self.numberOfLocalBoards)
        localRow = int(actionModLocalBoards / self.n)
        localCol = int(actionModLocalBoards % self.n)
        move = (localBoardIndex, localRow, localCol)
        # self.display(self.b.globalBoard)
        self.b.execute_move(move, player)
        return (self.b.globalBoard, -player)

    def getValidMoves(self, board, player):
        '''return a fixed size binary vector'''
        valids = [0]*self.getActionSize()
        # b = GlobalBoard(self.n, self.numberOfLocalBoards) # TODO why cant this just be global? and reset on the init func?
        self.b.globalBoard = np.copy(board)
        legalMoves = self.b.get_legal_moves(player)
        if len(legalMoves) == 0:
            valids[-1] = 1 # TODO is this why theres a plus 1 in aciton size
            return np.array(valids)
        for localBoardIndex, localRow, localCol in legalMoves:
            valids[(self.numberOfLocalBoards * localBoardIndex) + (self.n * localRow) + localCol] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        '''return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        '''
        # b = GlobalBoard(self.n, self.numberOfLocalBoards)
        self.b.globalBoard = np.copy(board)

        globalWinner = self.b.get_global_winner()
        if globalWinner == player:
            return 1
        elif globalWinner == -player:
            return -1
        elif globalWinner == None:
            return 0

        # draw has a very little value 
        return 1e-4

    # TODO does this work with the unavailable 2 value?
    def getCanonicalForm(self, board, player):
        '''return state if player==1, else return -state if player==-1'''
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        board = np.arange(81).reshape(self.n, self.n, self.n, self.n)
        pi_board = np.reshape(pi[:-1], (self.n, self.n, self.n, self.n))
        l = []
        for i in range(1,5):
            for j in [True, False]:
                if j:
                    newB = np.rot90(board, k=i, axes=(3,2)) # inner boards rotations
                    newB = np.rot90(newB, k=i, axes=(1,0)) # outer board rotations
                    newPi = np.rot90(pi_board, k=i, axes=(3,2)) # inner boards rotations
                    newPi = np.rot90(newPi, k=i, axes=(1,0)) # outer board rotations
                else:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                
                newB = np.reshape(newB, (self.numberOfLocalBoards, self.n, self.n))
                newPi = np.reshape(newPi, (self.numberOfLocalBoards, self.n, self.n))
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        '''8x8 numpy array (canonical board)'''
        return board.tostring()

    @staticmethod
    def display(board):
        print('\n')
        localBoardIndexes = [[0,1,2],[3,4,5],[6,7,8]]
        for layer in localBoardIndexes:
            print('----------------------------------------------------------------------------------')
            print('| ' + str(board[layer[0]][0][0]) + ' | ' + str(board[layer[0]][0][1]) + ' | ' + str(board[layer[0]][0][2]) + ' ||| ' +
                str(board[layer[1]][0][0]) + ' | ' + str(board[layer[1]][0][1]) + ' | ' + str(board[layer[1]][0][2]) + ' ||| ' +
                str(board[layer[2]][0][0]) + ' | ' + str(board[layer[2]][0][1]) + ' | ' + str(board[layer[2]][0][2]) + ' |')
            print('----------------------------------------------------------------------------------')
            print('| ' + str(board[layer[0]][1][0]) + ' | ' + str(board[layer[0]][1][1]) + ' | ' + str(board[layer[0]][1][2]) + ' ||| ' +
                str(board[layer[1]][1][0]) + ' | ' + str(board[layer[1]][1][1]) + ' | ' + str(board[layer[1]][1][2]) + ' ||| ' +
                str(board[layer[2]][1][0]) + ' | ' + str(board[layer[2]][1][1]) + ' | ' + str(board[layer[2]][1][2]) + ' |')
            print('----------------------------------------------------------------------------------')
            print('| ' + str(board[layer[0]][2][0]) + ' | ' + str(board[layer[0]][2][1]) + ' | ' + str(board[layer[0]][2][2]) + ' ||| ' +
                str(board[layer[1]][2][0]) + ' | ' + str(board[layer[1]][2][1]) + ' | ' + str(board[layer[1]][2][2]) + ' ||| ' +
                str(board[layer[2]][2][0]) + ' | ' + str(board[layer[2]][2][1]) + ' | ' + str(board[layer[2]][2][2]) + ' |')    
            print('----------------------------------------------------------------------------------')
        print('\n')
