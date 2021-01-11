"""
My recreation of the classic game of minesweeper, implementing different levels, reseting the game
and a main menu.
Author: Alastair McNeill
Started: 6th January 2021
Finished: 11th January 2021
"""
import pygame

from minesweeper.Constants import (BACKGROUND, LIGHT_GREY, MENU_IMG,
                                   SCREEN_WIDTH, WHITE, WIN_HIEGHT, WIN_WIDTH)
from minesweeper.Game import Game
from minesweeper.MainMenu import Menu

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HIEGHT))
pygame.display.set_caption("Minesweeper")
CLOCK = pygame.time.Clock()

def quit_app():
    """
    Function to quit everything to pass into menu class
    """
    pygame.quit()
    quit()

def start_app():
    """
    Placeholder function to pass into menu class
    """
    pass

def get_row_col_from_pos(game, pos):
    """
    Determine the row and col in the game that was clicked

    Arguments:
        game {Game} -- Game object that we are playing in to determine the size of a tile
        pos {tuple (x,y)} -- Mouse click position in the for of x, y to

    Returns:
        tuple (row, col) -- The row and col that were clicked upon
    """
    row = pos[1] // game.tile_size
    col = (pos[0] - 200) // game.tile_size
    return row, col


difficulties = ["EASY", "MEDIUM", "HARD"]
menu = Menu(WIN, MENU_IMG)
menu.add_slider(difficulties,(WIN_WIDTH//2 - 75, 300, 150, 50), LIGHT_GREY, WHITE, BACKGROUND)
menu.add_button("START", (WIN_WIDTH//2 - 75, 360, 150, 50), LIGHT_GREY, WHITE, BACKGROUND, start_app)
menu.add_button("QUIT", (WIN_WIDTH//2 - 75, 420, 150, 50), LIGHT_GREY, WHITE, BACKGROUND, quit_app)

def main():
    """
    Main loop for the game that runs the menu class, executes the game and handles the user interaction
    """
    indexes = menu.run()

    run = True
    game = Game(difficulties[indexes[0]])

    while run:
        CLOCK.tick(20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < WIN_WIDTH - SCREEN_WIDTH:
                    if pos[0] > 60 and pos[0] < 185 and pos[1] > 550 and pos[1] < 580:
                        game.reset()
                    elif pos[0] > 15 and pos[0] < 45 and pos[1] > 550 and pos[1] < 580:
                        main()

                else:
                    row, col =  get_row_col_from_pos(game, pos)
                    if event.button == 1:
                        game.select(row, col)
                    if event.button == 3:
                        game.flag(row, col)

        game.draw(WIN)


if __name__ == '__main__':
    main()
