from minesweeper.Constants import SQUARE_SIZE, WHITE, RED, BLUE, BOMB_IMG, TILE_IMG, NUM_IMGS
import pygame

class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.bomb = False
        self.shown = False
        self.surrounding_bombs = 0
        self.flag = False
        self.img = None
        self.scaled_img = None
        self.get_pos(row, col)

    def get_pos(self, row, col):
        self.x = col * SQUARE_SIZE
        self.y = row * SQUARE_SIZE

    def get_img(self):
        if not self.shown:
            self.img = TILE_IMG
        else:
            if self.bomb:
                self.img = BOMB_IMG
            else:
                self.img = NUM_IMGS[self.surrounding_bombs]

    def scale_img(self):
        self.scaled_img = pygame.transform.scale(self.img, (SQUARE_SIZE, SQUARE_SIZE))


    def set_bomb(self):
        self.bomb = True

    def draw(self, win):
        self.get_img()
        self.scale_img()
        win.blit(self.scaled_img, (self.x, self.y))
