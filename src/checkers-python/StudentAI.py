from random import randint, choice
from BoardClasses import Move
from BoardClasses import Board
from math import sqrt, log
from time import time
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

class MCTSNode():
    def __init__(self, board, move = None, color = None, parent = None):
        self.board = board
        self.move = move
        self.counter = len(self.board.saved_move)
        self.color = color
        self.opponent = {1:2,2:1}
        self.parent = parent
        self.children = []
        self.unexplored = []
        self.wins = 0
        self.visits = 0
        self.winner = 0

    def uct_value(self, c):
        return self.wins/self.visits + c*sqrt(log(self.parent.visits)/self.visits)

    def reset(self):
        offset = len(self.board.saved_move) - self.counter
        for i in range(offset):
            self.board.undo()
        
    def select(self, c):
        if self.winner != 0: # reached terminal state
            self.backpropagate(self.winner)
    
        if not self.children and not self.unexplored:
            # fill movelist
            moves_2d = self.board.get_all_possible_moves(self.color)
            self.unexplored = [m for checker_moves in moves_2d for m in checker_moves]

            if not self.unexplored:
                self.winner = self.opponent[self.color]
                self.backpropagate(self.winner)
                return
            
        if self.unexplored:
            self.expand()
            return
        else:
            max_child = max(self.children, key=lambda child: child.uct_value(c)) # chooses the first max
            self.board.make_move(max_child.move, self.color)
            max_child.select(c)
    
    def expand(self):
        move = self.unexplored.pop()
        self.board.make_move(move, self.color)
        # we make move before initializing child node to give child node correct turn
        child = MCTSNode(self.board, move, self.opponent[self.color], self)
        self.children.append(child)
        # set winner flag for child
        child.winner = child.board.is_win(self.color)
        if child.winner == 0:
            child.backpropagate(child.simulate())
        else:
            child.backpropagate(child.winner)

    def simulate(self, turn_limit = 100):
        turn_counter = 0
        winner = 0
        turn = self.color
        while turn_counter < turn_limit and not winner:
            moves_2d = self.board.get_all_possible_moves(turn)
            moves = [m for checker_moves in moves_2d for m in checker_moves]
            rand_move = choice(moves)
            self.board.make_move(rand_move, turn)
            winner = self.board.is_win(turn)
            turn = self.opponent[turn]
            turn_counter += 1
        if winner == 0: winner = -1 # default to tie
        return winner
    
    def backpropagate(self, winner):
        node = self
        while node is not None:
            node.visits += 1
            if node.parent is not None:
                turn = node.parent.color
                if winner == turn:
                    node.wins += 1
                elif winner == -1:
                    node.wins += 0.5
            node = node.parent
        
    def return_best_child(self):
        for child in self.children:
            return max(self.children, key=lambda child: (child.visits, child.wins / child.visits))

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
        
        self.root = MCTSNode(self.board, None, 2, None)
        
    def get_move(self, move):
        if len(move) == 0:
            self.color = 1  # if no enemy move, that means we're first (color = 1)
            self.root.color = 1
        else:
            self.board.make_move(move, self.opponent[self.color])
            match = None
            for child in self.root.children:
                if child.move == move:
                    match = child
                    break
            if match is not None:
                match.parent = None
                self.root = match # move root to matching board
            else:
                self.root = MCTSNode(self.board, None, self.color, None)
        self.build_tree(sqrt(2), 2)
        
        self.root = self.root.return_best_child() # move best move child to root
        self.root.parent = None
        self.board.make_move(self.root.move, self.color)
        return self.root.move
            
    def build_tree(self, c, time_limit):
        start_time = time()
        while time() - start_time < time_limit:
            self.root.select(c)
            self.root.reset() # undo moves


