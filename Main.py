import pygame
from minesweeper.Game import Game
from minesweeper.MainMenu import Menu
from minesweeper.Constants import WIN_HIEGHT, WIN_WIDTH, SCREEN_WIDTH, MENU_IMG, WHITE, LIGHT_GREY, BACKGROUND

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HIEGHT))
pygame.display.set_caption("Minesweeper")
CLOCK = pygame.time.Clock()

def quit_app():
    pygame.quit()
    quit()

def start_app():
    pass

def get_row_col_from_pos(game, pos):
    row = pos[1] // game.tile_size
    col = (pos[0] - 200) // game.tile_size
    return row, col


difficulties = ["EASY", "MEDIUM", "HARD"]
menu = Menu(WIN, MENU_IMG)
menu.add_slider(difficulties,(WIN_WIDTH//2 - 75, 300, 150, 50), LIGHT_GREY, WHITE, BACKGROUND)
menu.add_button("START", (WIN_WIDTH//2 - 75, 360, 150, 50), LIGHT_GREY, WHITE, BACKGROUND, start_app)
menu.add_button("QUIT", (WIN_WIDTH//2 - 75, 420, 150, 50), LIGHT_GREY, WHITE, BACKGROUND, quit_app)

def main():
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
