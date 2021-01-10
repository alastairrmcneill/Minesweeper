import pygame
from minesweeper.Game import Game
from minesweeper.Constants import WIN_HIEGHT, WIN_WIDTH, SCREEN_WIDTH

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HIEGHT))
pygame.display.set_caption("Minesweeper")
CLOCK = pygame.time.Clock()

def get_row_col_from_pos(game, pos):
    row = pos[1] // game.tile_size
    col = (pos[0] - 200) // game.tile_size
    return row, col


def main():
    run = True
    game = Game("Easy")

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
                        game.reset("Hard")
                    elif pos[0] > 15 and pos[0] < 45 and pos[1] > 550 and pos[1] < 580:
                        print("Home")

                else:
                    row, col =  get_row_col_from_pos(game, pos)
                    if event.button == 1:
                        game.select(row, col)
                    if event.button == 3:
                        game.flag(row, col)

        game.draw(WIN)


if __name__ == '__main__':
    main()
