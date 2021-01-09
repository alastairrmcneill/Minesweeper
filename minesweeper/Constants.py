import pygame
import os

# Board constants
ROWS = 10
COLS = 10
NUM_BOMBS = 10
WIN_WIDTH = 400
WIN_HIEGHT = 400

SQUARE_SIZE = WIN_HIEGHT // ROWS

# Colours
DARK_GREY = (125, 125, 125)
LIGHT_GREY = (170, 170, 170)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
IMGS_PATH = os.path.join(BASE_PATH, "imgs")

BOMB_IMG = pygame.image.load(os.path.join(IMGS_PATH, "bomb.png"))
NUM_IMGS = [pygame.image.load(os.path.join(IMGS_PATH,str(x) + ".png")) for x in range(0,9)]
TILE_IMG = pygame.image.load(os.path.join(IMGS_PATH, "tile.png"))