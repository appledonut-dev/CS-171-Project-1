from random import randint
from BoardClasses import Move
from BoardClasses import Board
from math import sqrt, log
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

class MCTSNode():
    def __init__(self, color, parent):
        self.color = color
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def uct_value(self, c):
        return self.wins/self.visits + c*math.sqrt(math.log(self.parent.visits)/self.visits)


class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1  # if no enemy move, that means we're first (color = 1)





