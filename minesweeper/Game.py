import pygame
from datetime import datetime
from minesweeper.Board import Board
from minesweeper.Constants import ROWS, COLS, NUM_BOMBS, BG_IMG, SMALL_FONT, WHITE

class Game:
    def __init__(self):
        self.screen = pygame.Surface((600,600))
        self.reset()


    def reset(self):
        self.rows = ROWS
        self.cols = COLS
        self.num_bombs = NUM_BOMBS
        self.board = Board(self.rows, self.cols, self.num_bombs)
        self.lost = False
        self.won = False
        self.shown_tiles = 0
        self.start_time = datetime.now().replace(microsecond = 0)

    def select(self, row, col):
        if not self.lost and not self.won:
            if not self.board.board[row][col].shown:
                self.play(row, col)


    def play(self, row, col):
        self.board.board[row][col].shown = True
        self.shown_tiles += 1
        print(self.shown_tiles)


        if self.shown_tiles == self.rows * self.cols - self.num_bombs:
            self.won = True
            self.won_game()
            return

        if self.board.board[row][col].bomb:
            self.lost = True
            self.lost_game()
            return

        if self.board.board[row][col].surrounding_bombs == 0:
            for x in range(-1,2):
                for y in range(-1,2):
                    if not (x == 0 and y == 0):
                        if row+x >= 0 and row+x < self.rows and col+y >= 0 and col+y < self.cols:
                            if not self.board.board[row+x][col+y].shown:
                                self.select(row + x, col + y)

    def won_game(self):
        self.board.show_flags()
        # Show a winning message over the board
        # Store the time taken?

    def lost_game(self):
        self.board.show_bombs()

    def draw_bomb_text(self, win):
        bomb_str = str(self.num_bombs - self.board.num_flagged())
        bomb_text = SMALL_FONT.render(bomb_str, True, WHITE)
        rect = bomb_text.get_rect(midleft=(105,112))
        win.blit(bomb_text, rect)

    def draw_time_text(self,win):
        current_time = datetime.now().replace(microsecond = 0)
        game_time = current_time -  self.start_time
        game_time = str(game_time)
        index = game_time.index(":") + 1
        time_text = SMALL_FONT.render(game_time[index:], True, WHITE)
        rect = time_text.get_rect(center = (100, 50))
        win.blit(time_text, rect)

    def draw(self, win):
        win.blit(BG_IMG, (0,0))
        self.board.draw(self.screen)
        win.blit(self.screen, (200,0))
        self.draw_bomb_text(win)
        self.draw_time_text(win)
        pygame.display.update()
