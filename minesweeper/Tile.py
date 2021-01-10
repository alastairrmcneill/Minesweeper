from minesweeper.Constants import WHITE, RED, BLUE, BOMB_IMG, TILE_IMG, NUM_IMGS, FLAG_IMG
import pygame

class Tile:
    def __init__(self, row, col, tile_size):
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
        self.x = col * self.tile_size
        self.y = row * self.tile_size

    def get_img(self):
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
        self.scaled_img = pygame.transform.scale(self.img, (self.tile_size, self.tile_size))

    def set_bomb(self):
        self.bomb = True

    def set_flag(self):
        self.flagged = not self.flagged

    def show(self):
        self.shown = True
        self.flagged = False

    def draw(self, win):
        self.get_img()
        self.scale_img()
        win.blit(self.scaled_img, (self.x, self.y))
