import pygame
from minesweeper.Game import Game
from minesweeper.Constants import WIN_HIEGHT, WIN_WIDTH, SCREEN_WIDTH, SQUARE_SIZE

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HIEGHT))
pygame.display.set_caption("Minesweeper")
CLOCK = pygame.time.Clock()

def get_row_col_from_pos(pos):
    row = pos[1] // SQUARE_SIZE
    col = (pos[0] - 200) // SQUARE_SIZE
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
                if pos[0] < WIN_WIDTH - SCREEN_WIDTH:
                    if pos[0] > 60 and pos[0] < 185 and pos[1] > 550 and pos[1] < 580:
                        game.reset()
                    elif pos[0] > 15 and pos[0] < 45 and pos[1] > 550 and pos[1] < 580:
                        print("Home")
                    else:
                        print(pos)
                else:
                    row, col =  get_row_col_from_pos(pos)
                    game.select(row, col)

        game.draw(WIN)


if __name__ == '__main__':
    main()
