import pprint
import numpy as np
from ai import AI_Unit


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
        if self.player[self.player_state] == 1:
            print("player turn!, please input move")
            col = int(input("select column(0-6): "))

        else:
            print("AI turn")
            col = self.ai.alpha_beta_minimax(self.board, self.horizontal_state,\
                                             depth=10)
            print(col)
            # col = 0

        if self.insert_coin(col, self.player[self.player_state]):
            self.player_state = (self.player_state+1)%2
            return True
        return False
        

    def print_grame_state(self):
        self.pp.pprint(self.board[::-1][:])