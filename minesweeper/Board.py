import random
import pygame
from minesweeper.Tile import Tile
from minesweeper.Constants import ROWS, COLS, NUM_BOMBS, LIGHT_GREY, DARK_GREY, SQUARE_SIZE, WIN_HIEGHT, WIN_WIDTH

class Board:
    def __init__(self):
        self.board = [[Tile(i,j) for j in range(ROWS)] for i in range(COLS)]
        self.generate_board()

    def generate_board(self):
        bomb_indexes = random.sample(range(0,ROWS * COLS), NUM_BOMBS)

        index = 0
        for i in range(ROWS):
            for j in range(COLS):
                if index in bomb_indexes:
                    self.board[i][j].set_bomb()
                    self.check_neighbours(i, j)
                index += 1

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

    def draw(self, win):
        self.draw_background(win)
        self.draw_tiles(win)

    def draw_tiles(self, win):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j].draw(win)

    def draw_background(self, win):
        win.fill(LIGHT_GREY)
        for i in range(len(self.board) + 1):
            for j in range(len(self.board[0]) + 1):
                pygame.draw.line(win, DARK_GREY, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, WIN_HIEGHT), 3)
                pygame.draw.line(win, DARK_GREY, (0, j * SQUARE_SIZE), (WIN_WIDTH, j * SQUARE_SIZE), 3)


