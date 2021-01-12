"""
The constants needed for the game
"""
import os

import pygame

pygame.font.init()

# Board constants
WIN_WIDTH = 800
WIN_HIEGHT = 600
SCREEN_WIDTH = SCREEN_HIEGHT = 600

# Colours
DARK_GREY = (125, 125, 125)
LIGHT_GREY = (170, 170, 170)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BACKGROUND = (51, 51, 51)

# Images
BASE_PATH = os.path.dirname(os.path.dirname(__file__))
IMGS_PATH = os.path.join(BASE_PATH, "imgs")

BOMB_IMG = pygame.image.load(os.path.join(IMGS_PATH, "bomb.png"))
NUM_IMGS = [pygame.image.load(os.path.join(IMGS_PATH,str(x) + ".png")) for x in range(0,9)]
TILE_IMG = pygame.image.load(os.path.join(IMGS_PATH, "tile.png"))
FLAG_IMG = pygame.image.load(os.path.join(IMGS_PATH, "flag.png"))
BG_IMG = pygame.image.load(os.path.join(IMGS_PATH, "background.png"))
MENU_IMG = pygame.image.load(os.path.join(IMGS_PATH, "main_menu.png"))

# Fonts
SMALL_FONT = pygame.font.SysFont('Arial BLACK', 25)
BUTTON_FONT = pygame.font.SysFont("Arial BLACK", 20)
TEXT_FONT = pygame.font.SysFont("Arial", 20)
