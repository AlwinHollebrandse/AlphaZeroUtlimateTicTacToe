'''
Board class for the game of TicTacToe.
Default board size is 9x9. In this game, the board is made of 9 3x3 localBoards
Board data:
  1=white(O), -1=black(X), 0=empty, 2=unavailable TODO idk if a 2 is acceptable
  first dim is localBoardIndex, 2nd is column within said subBoard, and 3rd is row within the localBoard
     globalBoard[0][0][0] is the top left square within the top left board,
     globalBoard[0][2][0] is the bottom left square within the top left board,
Squares are stored and manipulated as (x,y,z) tuples.

Author: Alwin Hollebrandse, github.com/AlwinHollebrandse
Date: March 5, 2021.

Based on the board for the game of 3D TicTacToe by Adam Lawson.
'''

import numpy as np

# TODO check what functions are actually used
class GlobalBoard():

    players = [-1, 1] # ['X', 'O']

    def __init__(self, n=3, numberOfLocalBoards=9):
        '''Set up initial board configuration.'''

        self.n = n
        self.numberOfLocalBoards = numberOfLocalBoards # NOTE this code only works if n==3 and numberOfLocalBoards==9
        self.validLocalBoardIndex = [x for x in range(numberOfLocalBoards)]
        # Create the empty board array.
        self.globalBoard = np.zeros((numberOfLocalBoards, n, n))

    # # add [][] indexer syntax to the Board # TODO needed? - does this convert 0-81 to the [][][] format
    # def __getitem__(self, index): 
    #     return self.globalBoard[index]

    def get_legal_moves(self, player):
        '''Returns all the legal moves for the given player.
        @param player (1=O,-1=X)
        '''
        allLegalMoves = set()  # stores the legal moves.

        # Get all the empty squares (color==0)
        for localBoardIndex in self.validLocalBoardIndex: 
            for row in range(self.n):
                for col in range(self.n):
                    if self.globalBoard[localBoardIndex][row][col] == 0:
                        newmove = (localBoardIndex, row, col)
                        allLegalMoves.add(newmove)
        return list(allLegalMoves)

    def has_legal_moves(self):
        '''checks if there is a legal move available'''
        for localBoardIndex in self.validLocalBoardIndex: 
            for row in range(self.n): # TODO correct row vs col ordering?
                for col in range(self.n):
                    if self.globalBoard[localBoardIndex][row][col] == 0:
                        return True
        return False

    def get_global_winner(self):
        '''Returns the winner of the global game if there is one'''
        tempGlobalBoard = self.compute_global_state()
        return self.check_current_state(tempGlobalBoard)

    def is_global_win(self, player):
        '''Check whether the given player has won the global game 
        @param player (1=O,-1=X)
        '''
        tempGlobalBoard = self.compute_global_state()
        if self.check_current_state(tempGlobalBoard) == player:
            return True
        return False

    def is_local_win(self, player, localBoardIndex):
        '''Check whether the given player has cwon the local game 
        @param player (1=O,-1=X)
        '''
        if self.check_current_state(self.globalBoard[localBoardIndex]) == player:
            return True
        return False

    def check_current_state(self, board):
        '''Returns the winner of the given board and None if there isnt a winner yet 
        @param board a 3x3 array that represents a normal TicTacToe game
        '''
        # Check horizontals
        if (board[0][0] == board[0][1] and board[0][1] == board[0][2] and board[0][0] in self.players):
            return board[0][0]
        if (board[1][0] == board[1][1] and board[1][1] == board[1][2] and board[1][0] in self.players):
            return board[1][0]
        if (board[2][0] == board[2][1] and board[2][1] == board[2][2] and board[2][0] in self.players):
            return board[2][0]

        # Check verticals
        if (board[0][0] == board[1][0] and board[1][0] == board[2][0] and board[0][0] in self.players):
            return board[0][0]
        if (board[0][1] == board[1][1] and board[1][1] == board[2][1] and board[0][1] in self.players):
            return board[0][1]
        if (board[0][2] == board[1][2] and board[1][2] == board[2][2] and board[0][2] in self.players):
            return board[0][2]

        # Check diagonals
        if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] in self.players):
            return board[1][1]
        if (board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[2][0] in self.players):
            return board[1][1]

        # Check if draw
        isDraw = True
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    isDraw = False
                    break
        if isDraw:
            return 2

        return None

    def compute_global_state(self):
        '''Returns a 3x3 array representing the localWinners of the global game'''
        tempGlobalBoard = np.zeros((self.n, self.n))

        for i in range(self.numberOfLocalBoards):
            localWinner = self.check_current_state(self.globalBoard[i])
            if localWinner != None:
                tempGlobalBoard[int(i/3)][i%3] = localWinner

        return tempGlobalBoard

    def execute_move(self, move, player):
        '''Perform the given move on the board 
        @param move (a 3-tuple that holds the localBoardIndex, row, and col of the desired move)
        @param player (1=O,-1=X)
        '''
        (localBoardIndex, row, col) = move

        # Add the piece to the empty square.
        assert self.globalBoard[localBoardIndex][row][col] == 0
        self.globalBoard[localBoardIndex][row][col] = player
        
        # fill the local board with 'unavailable' (value=2) if a local winner was found
        if self.check_current_state(self.globalBoard[localBoardIndex]) != None:
            self.fill_all_local_empty_spaces(self.globalBoard[localBoardIndex])
        
        # get the next localBoardIndex list
        potentialNextLocalBoardIndex = (self.n * row) + col
        if self.check_current_state(self.globalBoard[potentialNextLocalBoardIndex]) == None:
            self.validLocalBoardIndex = potentialNextLocalBoardIndex
        else:
            self.validLocalBoardIndex = []
            for i in range(self.numberOfLocalBoards):
                if self.check_current_state(self.globalBoard[i]) == None:
                    self.validLocalBoardIndex.append(i)

    def fill_all_local_empty_spaces(self, board):
        '''sets all empty spaces (value=0) to unavailable (value=2)'''
        for i in range(self.n):
            for j in range(self.n):
                if board[i][j] == 0:
                    board[i][j] = 2
