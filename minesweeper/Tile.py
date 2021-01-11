"""
Tile class that contains the information for each square in the game
"""

import pygame

from minesweeper.Constants import (BLUE, BOMB_IMG, FLAG_IMG, NUM_IMGS, RED,
                                   TILE_IMG, WHITE)


class Tile:
    def __init__(self, row, col, tile_size):
        """
        Init method for the tile class

        Arguments:
            row {int} -- Row to place this tile at
            col {int} -- Columb to place this tile at
            tile_size {int} -- Width and height of the square tile
        """
        self.row = row
        self.col = col
        self.tile_size = tile_size
        self.x = 0
        self.y = 0
        self.bomb = False
        self.flagged = False
        self.shown = False
        self.surrounding_bombs = 0
        self.flag = False
        self.img = None
        self.scaled_img = None
        self.get_pos(row, col)

    def get_pos(self, row, col):
        """
        Sets the x and y position fo the current tile

        Arguments:
            row {int} -- Row of the current tile
            col {int} -- Column of the current tile
        """
        self.x = col * self.tile_size
        self.y = row * self.tile_size

    def get_img(self):
        """
        Determines what image to show when drawing
        """
        if not self.shown:
            self.img = TILE_IMG
            if self.flagged:
                self.img = FLAG_IMG
        else:
            if self.bomb:
                self.img = BOMB_IMG
            else:
                self.img = NUM_IMGS[self.surrounding_bombs]

    def scale_img(self):
        """
        Scales the determined image to fit the size of the tile
        """
        self.scaled_img = pygame.transform.scale(self.img, (self.tile_size, self.tile_size))

    def set_bomb(self):
        """
        Set this tile to be a bomb
        """
        self.bomb = True

    def set_flag(self):
        """
        Set this tile to be flagged or not
        """
        self.flagged = not self.flagged

    def show(self):
        """
        Set the current tile to be shown and deflags
        """
        self.shown = True
        self.flagged = False

    def draw(self, win):
        """
        Draws the current tile to the screen

        Arguments:
            win {surface} -- Pygame window to draw to
        """
        self.get_img()
        self.scale_img()
        win.blit(self.scaled_img, (self.x, self.y))
