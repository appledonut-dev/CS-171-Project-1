from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
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
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move

    def leaf_heuristic(self):
        state = self.board.is_win(self.color)
        if state:
            if state == self.color:
                return self.col * self.row
            return -1 * self.col * self.row
        score = 0
        for checker in self.board.board:
            if checker.get_color == self.color:
                if checker.is_king:
                    score += 2
                else:
                    score += 1
            elif checker.get_color == self.opponent[self.color]:
                if checker.is_king:
                    score -= 2
                else:
                    score -= 1
        return score