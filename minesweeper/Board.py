"""
Board class that holds all the tiles for and generation functions
"""

import random

import pygame

from minesweeper.Constants import DARK_GREY, LIGHT_GREY, WIN_HIEGHT, WIN_WIDTH
from minesweeper.Tile import Tile


class Board:
    def __init__(self, rows, cols, num_bombs, tile_size):
        """
        Init function for the board clas

        Arguments:
            rows {int} -- Number of rows in the game board
            cols {int} -- Number of columbs in the game board
            num_bombs {int} -- Number of bombs to place on the board
            tile_size {int} -- Width and height of the square tile
        """
        self.rows = rows
        self.cols = cols
        self.num_bombs = num_bombs
        self.tile_size = tile_size
        self.board = [[Tile(i,j, tile_size) for j in range(rows)] for i in range(cols)]
        self.generate_board()

    def generate_board(self):
        """
        Generates the board from the given parameters in the init method
        """
        bomb_indexes = random.sample(range(0,self.rows * self.cols), self.num_bombs)

        index = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if index in bomb_indexes:
                    self.board[i][j].set_bomb()
                    self.check_neighbours(i, j)
                index += 1

    def check_neighbours(self, i, j):
        """
        Checks all the tiles surrounding the current tile at i,j

        Arguments:
            i {int} -- Row of the current selected tile
            j {int} -- Column of the current selected tile
        """
        for x in range(-1,2):
            for y in range(-1,2):
                if not (x == 0 and y == 0):
                    if i+x >= 0 and i+x < self.rows and j+y >= 0 and j+y < self.cols:
                        self.board[i+x][j+y].surrounding_bombs += 1

    def num_flagged(self):
        """
        Checks the number of tiles that are currently flagged

        Returns:
            int -- The count of the number of tiles in the board currently flagged
        """
        count = 0
        for row in self.board:
            for tile in row:
                if tile.flagged:
                    count += 1
        return count

    def show_bombs(self):
        """
        Shows al the bomb tiles in the board
        """
        for row in self.board:
            for tile in row:
                tile.flagged = False
                if tile.bomb:
                    tile.shown = True


    def show_flags(self):
        """
        Shows all the flags on the bomb tiles in the board
        """
        for row in self.board:
            for tile in row:
                if tile.bomb:
                    tile.flagged = True

    def print_board(self):
        """
        Prints board to the command line
        """
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
        """
        Draws current board to the screen

        Arguments:
            win {surface} -- Pygame window to draw to
        """
        self.draw_background(win)
        self.draw_tiles(win)

    def draw_tiles(self, win):
        """
        Draws all the tiles to the screen

        Arguments:
            win {surface} -- Pygame window to draw to
        """
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j].draw(win)

    def draw_background(self, win):
        """
        Draws the background behind the tiles

        Arguments:
            win {surface} -- Pygame window to draw to
        """
        win.fill(LIGHT_GREY)
        for i in range(len(self.board) + 1):
            for j in range(len(self.board[0]) + 1):
                pygame.draw.line(win, DARK_GREY, (i * self.tile_size, 0), (i * self.tile_size, WIN_HIEGHT), 3)
                pygame.draw.line(win, DARK_GREY, (0, j * self.tile_size), (WIN_WIDTH, j * self.tile_size), 3)


