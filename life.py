from platform import system
from random import randint
from copy import deepcopy
import sys
import os

grid_n = None
grid_n_1 = None

NEIGHBORS = (
    (-1,0),
    (1,0),
    (0,-1),
    (0,1),
    (-1,-1),
    (-1,1),
    (1,-1),
    (1,1)
)


if system() == 'Windows':
    def clear_screen():
        os.system('cls')
else:
    def clear_screen():
        os.system('clear')


def pause_game():
    input('\033[97mEnter to continue =>')


def init_grid(rows, cols):
    global grid_n
    global grid_n_1

    grid_n = [[randint(0,1) for _ in range(cols)] for j in range(rows)]
    grid_n_1 = deepcopy(grid_n)
    print('\n=============== Generation 0 ===============')
    print(*grid_n_1, sep='\n')
    pause_game()
    clear_screen()


def start_game(pause=0, max_iter=1000):
    global grid_n
    global grid_n_1
    neighbors_live = 0

    print("Starting game...")
    iteration = 0
    while iteration < max_iter:
        row_len = len(grid_n)
        col_len = len(grid_n[0]) # Will not be ragged so this is fine
        for i in range(0, row_len):
            for j in range(0, col_len):
                neighbors_live = 0
                for row in NEIGHBORS:
                    m = i + row[0]
                    n = j + row[1]
                    if (m >= 0 and m < row_len and n >= 0 and n < col_len
                        and grid_n[m][n] == 1):
                        neighbors_live += 1
                # Birth:
                if grid_n[i][j] == 0 and neighbors_live == 3:
                    grid_n_1[i][j] = 1
                # Death:
                elif grid_n[i][j] == 1 and (neighbors_live < 2 or neighbors_live > 3):
                    grid_n_1[i][j] = 0
    
        grid_n = deepcopy(grid_n_1)
        iteration += 1
        print(f'=============== Generation {iteration} ===============')
        for i in range(len(grid_n)):
            for j in range(len(grid_n[0])):
                if grid_n[i][j] == 1:
                    print("\033[91m" + str(grid_n[i][j]), end=' ')
                else:
                    print("\033[97m" + str(grid_n[i][j]), end=' ',)
            print()
        if pause == 1:
            pause_game()
        clear_screen()


def main():
    args = sys.argv[1:]
    rows = cols = pause = 0
    gen = 1000

    if len(args) > 3:
        if args[0] == '-rows' and args[2] == '-cols':
            try:
                rows = int(args[1])
                cols = int(args[3])
                if len(args) > 5:
                    if args[4] == '-pause':
                        try:
                            pause = int(args[5])
                        except ValueError as e:
                            print(e)
                            exit(1)
                    else:
                        print("\n3rd arg ignored...",)
                        print("-pause expected as 3rd arg", end="\n\n")
                if len(args) == 8:
                    if args[6] == '-gen':
                        try:
                            gen = int(args[7])
                        except ValueError as e:
                            print(e)
                            exit(1)
                    else:
                        print("\n4th arg ignored...")
                        print("-gen expected as 4th arg", end="\n\n")
            except ValueError as e:
                print(e)
                exit(1)
    elif len(args) == 0: # Default value
        rows = 20
        cols = 20
    elif len(args) == 1:
        white = str.format('\033[97m')
        yellow = str.format('\033[93m')
        print(f"\n{white}                  Options")
        print("_____________________________________________")
        print(f"{yellow}-h      ", end="")
        print(f"{white}Help (this menu)")
        print(f"{yellow}-rows   ", end="")
        print(f"{white}Specify the number of rows")
        print(f"{yellow}-cols   ", end="")
        print(f"{white}Specify the number of columns")
        print(f"{yellow}-pause  ", end="")
        print(f"{white}Choose to pause after each step: 0=false, 1=true")
        print(f"{yellow}-gen    ", end="")
        print(f"{white}Specify the number of generations")

        print("\n                  Examples")
        print("_____________________________________________")
        print("Ex a: python life.py")
        print("Ex b: python life.py -rows 20 -cols 20")
        print("Ex c: python life.py -rows 20 -cols 20 -pause 1")
        print("Ex d: python life.py -rows 20 -cols 20 -pause 0")
        print("Ex e: python life.py -rows 20 -cols 20 -pause 0 -gen 100")
        exit(0)
    else:
        print("\nInvalid args supplied...")
        print("Ex a: python life.py")
        print("Ex b: python life.py -rows 20 -cols 20", end="\n\n")
        print("Ex c: python life.py -rows 20 -cols 20 -pause 1", end="\n\n")
        print("Ex d: python life.py -rows 20 -cols 20 -pause 0", end="\n\n")
        print("Ex e: python life.py -rows 20 -cols 20 -pause 0 -gen 100", end="\n\n")
        exit(1)
    
    init_grid(rows, cols)
    start_game(pause=pause, max_iter=gen)

main()
