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
    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        
        moves = self.board.get_all_possible_moves(self.color)
        best_score = float(-1 * self.col * self.row)
        best_move = moves[0][0]
    
        depth_limit = 3
    
        for checker_moves in moves:
            for move in checker_moves:
                self.board.make_move(move, self.color)
                score = self.dfs(self.opponent[self.color], depth_limit - 1)
                self.board.undo()

                if score > best_score:
                    best_score = score
                    best_move = move
                
        self.board.make_move(best_move, self.color)
        return best_move

        

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
    
    def dfs(self, turn, depth_limit):
        #Base Case
        if depth_limit == 0 or self.board.is_win(turn) != 0:
            return self.leaf_heuristic()
            
        moves = self.board.get_all_possible_moves(turn)
        if len(moves) == 0:
            if turn == self.color:
                return -1 * self.col * self.row # return loss
            else:
                return self.col * self.row # return win
        
        if turn == self.color: # my turn (MAX)
            score = float(-1 * self.col * self.row) # lowest possible score
            for checker_moves in moves:
                for move in checker_moves:
                    self.board.make_move(move, turn)
                    score = max(score, self.dfs(self.opponent[turn], depth_limit -1))
                    self.board.undo()
                    # pass max value
        else: # opponent's turn (MIN)
            score = float(self.col * self.row) # largest possible score
            for checker_moves in moves:
                for move in checker_moves:
                    self.board.make_move(move, turn)
                    score = min(score, self.dfs(self.opponent[turn], depth_limit - 1))
                    self.board.undo()
                    # pass min value
        return score

    def leaf_heuristic(self):
            state = self.board.is_win(self.color)
            if state:
                if state == self.color:
                    return self.col * self.row
                return -1 * self.col * self.row
                
            score = 0
            
            color_map = {1: "B", 2: "W"}
            my_color = color_map[self.color]
            opp_color = color_map[self.opponent[self.color]]
            
            for row in range(self.row):
                for col in range(self.col):
                    checker = self.board.board[row][col]
                    
                    if checker.color == my_color:
                        if checker.is_king:
                            score += 2
                        else:
                            score += 1
                    elif checker.color == opp_color:
                        if checker.is_king:
                            score -= 2
                        else:
                            score -= 1
                            
            return score