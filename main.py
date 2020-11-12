from game import Game

if __name__ == '__main__':
    gg = False
    conn4 = Game()
    while not gg:
        if conn4.manage_turn():
            conn4.print_grame_state()
