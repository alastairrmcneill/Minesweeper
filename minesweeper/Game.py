import pygame
from minesweeper.Board import Board
from minesweeper.Constants import ROWS, COLS, NUM_BOMBS

class Game:
    def __init__(self):
        self.reset()


    def reset(self):
        self.rows = ROWS
        self.cols = COLS
        self.num_bombs = NUM_BOMBS
        self.board = Board(self.rows, self.cols, self.num_bombs)
        self.lost = False
        self.won = False
        self.shown_tiles = 0

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

    def draw(self, win):
        self.board.draw(win)
        pygame.display.update()
