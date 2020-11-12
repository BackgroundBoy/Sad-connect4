import copy
import numpy as np
from typing import List
# from game import Game
from functools import lru_cache
import pprint

INF = float('inf')
M_INF = -float('inf')


class AI_Unit:

    @lru_cache()
    def is_over(self, b, val) ->  bool:
        win = False 
        # count_3s = 0       
        # diagonal win, thre are 24 possible win position
        # print("over")
        board = np.array(b) 
        for j in range(7):
            if win:
                break
            # vertical 
            if j < 4:
                v_sum = board[:,j:j+4].sum(axis=1)
                if val*4 in v_sum:
                    win = True
                    break
            for i in range(3):
                # horizontal 
                h_sum = board[i:i+4,:].sum(axis=0)
                if val*4 in h_sum:
                    win = True
                    break

                # diagonal /
                if j <= 3:
                    diag_sum_1 = board[i,j] + board[i+1,j+1] + \
                                board[i+2,j+2] + board[i+3,j+3]
                    if diag_sum_1 == val*4:
                        win = True
                        break

                # diagonal \
                if j >= 3:
                    diag_sum_2 = board[i,j] + board[i+1,j-1] + \
                                board[i+2,j-2] + board[i+3,j-3]
                    if diag_sum_2 == val*4:
                        win = True
                        break
        # if win:
        #     print("over")
        #     print(board)
        return win
    
    @lru_cache()
    def eval(self, b, val):
        # like is_over but count group of 3 chips
        # score based on number of 3 group
        # if 0 socore but middle lane have empty slot then score + 1 
        # print("state")
        board = np.array(b)    
        count_3s = 0       
        # diagonal win, thre are 24 possible win position
        for j in range(7):
            # vertical 
            if j < 4:
                v_sum = board[:,j:j+4].sum(axis=1)
                if val*3 in v_sum:
                    count_3s += 1
            for i in range(3):
                # horizontal 
                h_sum = board[i:i+4,:].sum(axis=0)
                if val*3 in h_sum:
                    count_3s += 1

                # diagonal /
                if j <= 3:
                    diag_sum_1 = board[i,j] + board[i+1,j+1] + \
                                board[i+2,j+2] + board[i+3,j+3]
                    if diag_sum_1 == val*3:
                        count_3s += 1

                # diagonal \
                if j >= 3:
                    diag_sum_2 = board[i,j] + board[i+1,j-1] + \
                                board[i+2,j-2] + board[i+3,j-3]
                    if diag_sum_2 == val*3:
                        count_3s += 1
        if val == 1:
            count_3s *= -1
        return count_3s

    def apply_move(self, board:np.ndarray, col:int,
    horizontal_view:List[int], val) -> List:
        b = copy.deepcopy(board)
        h = copy.deepcopy(horizontal_view)
        row = horizontal_view[col]
        h[col] += 1
        b[row][col] = val # bot is number 9
        return b , h
    

    def alpha_beta_minimax(
        self, 
        board:np.ndarray, 
        horizontal_view:List[int], 
        alpha=M_INF,
        beta=INF,
        depth:int=5,
    ):
        moves = self.generate_moves(horizontal_view)
        best_score = M_INF
        best_move = -1
        for move in moves:
            b,h =self.apply_move(board,move,horizontal_view,9)
            move_score = self.min_move(b,h,alpha,beta,depth-1)
            print(move_score)
            if move_score > best_score:
                # print(move)
                best_move = move
                best_score = move_score
        return best_move

    def max_move(
        self, 
        board:np.ndarray, 
        horizontal_view:List[int], 
        alpha,
        beta,
        depth:int
    ) -> int:
        """
            Function for maximizing player
        """
        if self.is_over(tuple(map(tuple,board)), val=1):
            return -1000
        elif depth == 0:
            return self.eval(tuple(map(tuple,board)),9)
        else:
            best_score = M_INF
            moves = self.generate_moves(horizontal_view)
            for move in moves:
                b,h =self.apply_move(board,move,horizontal_view,9)
                move_score = self.min_move(b,h,alpha,beta,depth-1)
                best_score = max(move_score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    

    def min_move(
        self, 
        board:np.ndarray, 
        horizontal_view:List[int], 
        alpha,
        beta,
        depth:int
    ) -> int:
        """
            Function for minimizing player(opponent)
        """
        if self.is_over(tuple(map(tuple,board)), val=9):
            return 1000
        elif depth == 0:
            return self.eval(tuple(map(tuple,board)),9)
        best_score = INF
        moves = self.generate_moves(horizontal_view)
        for move in moves:
            b,h =self.apply_move(board,move,horizontal_view,1)
            move_score = self.max_move(b,h,alpha,beta,depth-1)
            # print("minmove max", move_score)
            best_score = min(best_score, move_score)
            beta = min(beta, move_score)
            if beta <= alpha:
                break
        return best_score

    def generate_moves(self, horizontal_view:List[int]) -> List[int]:
        moves = [] # cols that can insert chip
        for col in range(7):
            if horizontal_view[col] >= 6:
                continue
            moves.append(col)
        return moves
        
# debug
# if __name__ == "__main__":
#     a = [[0, 0, 0, 0, 0, 0, 0], 
#          [0, 0, 0, 0, 0, 0, 0], 
#          [0, 0, 0, 0, 0, 0, 0], 
#          [0, 0, 0, 0, 0, 0, 0], 
#          [0, 0, 0, 0, 0, 0, 0], 
#          [0, 0, 0, 0, 0, 0, 0]]
#     horizontal = [0,0,0,0,0,0,0]
#     b = np.array(a) 
#     # print(b[0:4][:2])
#     ai = AI_Unit()
#     pp = pprint.PrettyPrinter()
#     pp.pprint(b[::-1,:])
#     print(ai.is_over(b,1))