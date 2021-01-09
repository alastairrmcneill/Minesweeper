import random
import pygame
from minesweeper.Tile import Tile
from minesweeper.Constants import LIGHT_GREY, DARK_GREY, SQUARE_SIZE, WIN_HIEGHT, WIN_WIDTH

class Board:
    def __init__(self, rows, cols, num_bombs):
        self.rows = rows
        self.cols = cols
        self.num_bombs = num_bombs
        self.board = [[Tile(i,j) for j in range(rows)] for i in range(cols)]
        # self.generate_board()
        self.test_board()

    def test_board(self):
        self.board[0][0].set_bomb()
        self.check_neighbours(0,0)
        self.board[2][0].set_bomb()
        self.check_neighbours(2,0)

    def generate_board(self):
        bomb_indexes = random.sample(range(0,self.rows * self.cols), self.num_bombs)

        index = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if index in bomb_indexes:
                    self.board[i][j].set_bomb()
                    self.check_neighbours(i, j)
                index += 1

    def check_neighbours(self, i, j):
        for x in range(-1,2):
            for y in range(-1,2):
                if not (x == 0 and y == 0):
                    if i+x >= 0 and i+x < self.rows and j+y >= 0 and j+y < self.cols:
                        self.board[i+x][j+y].surrounding_bombs += 1

    def num_flagged(self):
        count = 0
        for row in self.board:
            for tile in row:
                if tile.flagged:
                    count += 1
        return count

    def show_bombs(self):
        for row in self.board:
            for tile in row:
                if tile.bomb:
                    tile.shown = True

    def show_flags(self):
        for row in self.board:
            for tile in row:
                if tile.bomb:
                    tile.flagged = True

    def print_board(self):
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
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


