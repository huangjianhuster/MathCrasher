from game2dboard import Board
import game2dboard
from tkinter import messagebox
import copy
import numpy as np

# GLOBAL consts
BOARD_LENGTH = 20
BLOCK_SIZE = 30
game2dboard.Cell._text_color = 'red'

board = Board(BOARD_LENGTH, BOARD_LENGTH)
board.cell_size = BLOCK_SIZE
board.cell_color = "lightgreen"
board.spacing = 5
board.title = "Stepping Stone"

# initial configuration
center = int(BOARD_LENGTH / 2)
board[center][center] = 1
board[center-2][center-2] = 1
current_board = board
current_max = 1
arr0 = np.array(current_board.copy(), dtype=np.float64)

# initial configuration
def setup():
    global board, current_board, current_max, arr0
    board.fill(None)
    board[center][center] = 1
    board[center-2][center-2] = 1
    current_board = board
    current_max = 1
    arr0 = np.array(current_board.copy(), dtype=np.float64)
    # print(current_board)
    current_board.start_timer(300)

# functions
def mouse_click(btn, r, c):
    """
    click on a block; 
    calculation neigboring sum;
    if it is sequential, fill the number
    """
    global current_board
    global current_max
    global arr0

    block_num = sum_neighbors(arr0, r, c)
    if (current_max + 1) == block_num:
        # the only place to change global variables
        current_board[r][c] = block_num
        arr0 =  np.array(current_board.copy(), dtype=np.float64)
        # update max 
        current_max = block_num

    if not find_solutions():
        current_board.stop_timer()
        if messagebox.askyesno("Stepping stone", "Game over!\nRestart?"):
            setup()
            return
    
    return None


# neighbor sum
def sum_neighbors(arr, i, j):
    sum_arr = arr[i,j]
    if np.isnan(arr[i,j]):
        sum_arr = int(np.nansum(arr[i-1:i+2, j-1:j+2]))
    return sum_arr

# evaluation whether there is a solution
def find_solutions():
    """
    To check if there is any place to put the next sequential number in the current board.
    if there is, return True
    it there is not, return False [Game end!]
    """
    global current_board, arr0, current_max
    exists = False
    for row in range(current_board.nrows):
        for col in range(current_board.ncols):
            dat = sum_neighbors(arr0, row, col)
            if dat == (current_max + 1):
                exists = True
    return exists

current_board.on_mouse_click = mouse_click
current_board.show()
