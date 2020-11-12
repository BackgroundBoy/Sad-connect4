import pprint
import numpy as np
from ai import AI_Unit
import sys

class Game:
    pp = pprint.PrettyPrinter()
    board = np.array([
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
    ])

    horizontal_state = [0,0,0,0,0,0,0]

    player_state = 0

    player = []
    ai = AI_Unit()

    def __init__(self):
        first = input("Player go first?[y/n]").lower()
        if first == 'y':
            self.player = [1,9]
        else:
            self.player = [9,1]
    
    def is_over(self) -> (bool,int):
        win = False 
        p1,p2 = 1,9
        win_player = -1 
        for j in range(7):
            if win:
                break
            # vertical 
            if j < 4:
                v_sum = self.board[:,j:j+4].sum(axis=1)
                if p1*4 in v_sum:
                    win = True
                    win_player = p1
                elif p2*4 in v_sum:
                    win = True
                    win_player = p2
            for i in range(3):
                if win:
                    break
                # horizontal 
                h_sum = self.board[i:i+4,:].sum(axis=0)
                if p1*4 in h_sum:
                    win = True
                elif p2*4 in h_sum:
                    win = True
                    win_player = p2     
                
                # diagonal /
                if j <= 3:
                    diag_sum_1 = self.board[i,j] + self.board[i+1,j+1] + \
                                self.board[i+2,j+2] + self.board[i+3,j+3]
                    if diag_sum_1 == p1*4:
                        win = True
                        win_player = p1
                    if diag_sum_1 == p1*4:
                        win = True
                        win_player = p1
                
                # diagonal \
                if j >= 3:
                    diag_sum_2 = self.board[i,j] + self.board[i+1,j-1] + \
                                self.board[i+2,j-2] + self.board[i+3,j-3]
                    if diag_sum_2 == p1*4:
                        win = True
                        win_player = p1
                    elif diag_sum_2 == p2*4:
                        win = True
                        win_player = p2
        return win, win_player

    def insert_coin(self, col:int, val:int=1):
        print(val, col) #
        if col > 6: 
            return False
        if self.horizontal_state[col] >=6:
            return False
        row = self.horizontal_state[col]
        self.horizontal_state[col] += 1
        self.board[row][col] = val
        return True

    def manage_turn(self):
        over, player = self.is_over()
        if over:
            print(f'Player #%d win' % player)
            sys.exit()
        if self.player[self.player_state] == 1:
            print("player turn!, please input move")
            col = int(input("select column(0-6): "))

        else:
            print("AI turn")
            col = self.ai.alpha_beta_minimax(self.board, self.horizontal_state,\
                                             depth=7)
            print(col)
            # col = 0

        if self.insert_coin(col, self.player[self.player_state]):
            self.player_state = (self.player_state+1)%2
            return True
        return False
        

    def print_grame_state(self):
        self.pp.pprint(self.board[::-1][:])