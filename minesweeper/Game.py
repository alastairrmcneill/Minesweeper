import pygame
from minesweeper.Board import Board

class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = Board()

    def select(self, row, col):
        self.board.board[row][col].shown = True

    def draw(self, win):
        self.board.draw(win)
        pygame.display.update()
