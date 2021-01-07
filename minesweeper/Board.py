import random
from minesweeper.Tile import Tile
from minesweeper.Constants import ROWS, COLS, NUM_BOMBS

class Board:
    def __init__(self):
        self.board = [[Tile(i,j) for j in range(ROWS)] for i in range(COLS)]
        self.generate_board()
        self.print_board()

    def generate_board(self):
        bomb_indexes = random.sample(range(1,ROWS * COLS), NUM_BOMBS)

        index = 0
        for i in range(ROWS):
            for j in range(COLS):
                index += 1
                if index in bomb_indexes:
                    self.board[i][j].set_bomb()
                    self.check_neighbours(i, j)

    def check_neighbours(self, i, j):
        for x in range(-1,2):
            for y in range(-1,2):
                if not (x == 0 and y == 0):
                    if i+x >= 0 and i+x < ROWS and j+y >= 0 and j+y < COLS:
                        self.board[i+x][j+y].surrounding_bombs += 1

    def print_board(self):
        for i in range(ROWS):
            row = []
            for j in range(COLS):
                if self.board[i][j].bomb:
                    row.append("[O]")
                else:
                    x = self.board[i][j].surrounding_bombs
                    if x != 0:
                        row.append("[" + str(x) + "]")
                    else:
                        row.append("[ ]")
            print(row)

    def draw(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j].draw()