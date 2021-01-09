import pygame
from minesweeper.Game import Game
from minesweeper.Constants import WIN_HIEGHT, WIN_WIDTH, SQUARE_SIZE

WIN = pygame.display.set_mode((WIN_HIEGHT, WIN_WIDTH))
pygame.display.set_caption("Minesweeper")
CLOCK = pygame.time.Clock()

def get_row_col_from_pos(pos):
    row = pos[1] // SQUARE_SIZE
    col = pos[0] // SQUARE_SIZE
    return row, col


def main():
    run = True
    game = Game()

    while run:
        CLOCK.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col =  get_row_col_from_pos(pos)
                game.select(row, col)

        game.draw(WIN)


if __name__ == '__main__':
    main()
