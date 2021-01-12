"""
Game class that holds the main game mechanics for the Minesweeper game
"""

import json
import os
from datetime import datetime

import pygame

from minesweeper.Board import Board
from minesweeper.Constants import (BASE_PATH, BG_IMG, SCREEN_WIDTH, SMALL_FONT,
                                   WHITE)


class Game:
    def __init__(self, difficulty):
        """
        Init method for Game class

        Arguments:
            difficulty {string} -- The difficulty we want to play this game on. Used to find game data from config file
        """
        self.screen = pygame.Surface((600,600))
        self.rows = 0
        self.cols = 0
        self.num_bombs = 0
        self.difficulty = difficulty
        self.get_config()
        self.reset()


    def reset(self):
        """
        Sets a lot of the parameters for the game. Can be used to reset the game when appropriate button pressed
        """
        self.tile_size = SCREEN_WIDTH // self.rows
        self.board = Board(self.rows, self.cols, self.num_bombs, self.tile_size)
        self.lost = False
        self.won = False
        self.shown_tiles = 0
        self.start_time = datetime.now().replace(microsecond = 0)
        self.end_time = None
        self.message = ""

    def get_config(self):
        """
        Get game confgiuration from config file
        """
        f = open(os.path.join(BASE_PATH, "config.JSON"))
        data = json.load(f)

        for level in data["difficulties"]:
            if level["Difficulty"] == self.difficulty:
                self.rows = level["ROWS"]
                self.cols = level["COLS"]
                self.num_bombs = level["NUM_BOMBS"]
                self.best_time = level["BEST_TIME"]


    def flag(self, row, col):
        """
        Flags the square on the board that was clicked

        Arguments:
            row {int} -- Row of the tile to flag
            col {int} -- Col of the tile to flag
        """
        self.board.board[row][col].set_flag()

    def select(self, row, col):
        """
        Try to click the tile

        Arguments:
            row {int} -- Row of the tile to check
            col {int} -- Col of the tile to check
        """
        if not self.lost and not self.won:
            if not self.board.board[row][col].shown and not self.board.board[row][col].flagged:
                self.play(row, col)


    def play(self, row, col):
        """
        Click and reveal the tile at the row and column. If bomb lose game

        Arguments:
            row {int} -- Row of the tile to reveal
            col {int} -- Col of the tile to reveal
        """
        self.board.board[row][col].show()

        if self.board.board[row][col].bomb:
            self.lost = True
            self.lost_game()
            return

        self.shown_tiles += 1

        if self.shown_tiles == self.rows * self.cols - self.num_bombs:
            self.won = True
            self.won_game()
            return

        if self.board.board[row][col].surrounding_bombs == 0:
            for x in range(-1,2):
                for y in range(-1,2):
                    if not (x == 0 and y == 0):
                        if row+x >= 0 and row+x < self.rows and col+y >= 0 and col+y < self.cols:
                            if not self.board.board[row+x][col+y].shown:
                                self.select(row + x, col + y)

    def won_game(self):
        """
        Function to run when you win the game
        """
        self.board.show_flags()
        self.end_time = datetime.now().replace(microsecond = 0)
        difference = self.end_time - self.start_time
        total_time = str(difference)
        index = total_time.index(":") + 1
        total_time = total_time[index:]
        self.message = "You won the game in a time of " + total_time + "."
        # Store the time taken?

        if difference.total_seconds() < self.best_time or self.best_time == 0:
            self.message = "You won the game in a new best time of " + total_time + "."
            self.best_time = difference.total_seconds()
            self.write_best_score(difference.total_seconds())

    def write_best_score(self, time):
        """
        Write the best time to the config file for that difficulty

        Arguments:
            time {float} -- Time to write to file
        """
        with open(os.path.join(BASE_PATH, "config.JSON"), "r") as f:
            data = json.load(f)

        for level in data["difficulties"]:
            if level["Difficulty"] == self.difficulty:
                level["BEST_TIME"] = int(time)

        with open(os.path.join(BASE_PATH, "config.JSON"), "w") as f:
            json.dump(data, f, indent=4)



    def lost_game(self):
        """
        Function to run when you lose the game
        """
        self.board.show_bombs()
        self.end_time = datetime.now().replace(microsecond = 0)
        self.message = "Game over. You lost."

    def draw_bomb_text(self, win):
        """
        Show the number of bombs remaining unflagged

        Arguments:
            win {surface} -- Pygame window to draw to
        """
        bomb_str = str(self.num_bombs - self.board.num_flagged())
        bomb_text = SMALL_FONT.render(bomb_str, True, WHITE)
        rect = bomb_text.get_rect(midleft=(105,112))
        win.blit(bomb_text, rect)

    def draw_time_text(self,win):
        """
        Function to draw the time taken so far to the screen

        Arguments:
            win {surface} -- Pygame window to draw to
        """
        if self.won or self.lost:
            game_time = self.end_time - self.start_time
        else:
            current_time = datetime.now().replace(microsecond = 0)
            game_time = current_time -  self.start_time

        game_time = str(game_time)
        index = game_time.index(":") + 1

        time_text = SMALL_FONT.render(game_time[index:], True, WHITE)
        rect = time_text.get_rect(center = (100, 50))
        win.blit(time_text, rect)

    def draw_message(self, win):
        """
        Function to draw a message to the screen

        Arguments:
            win {surface} -- Pygame window to draw to
        """
        allowed_width = 180

        words = self.message.split()

        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = SMALL_FONT.size(' '.join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            # add a line consisting of those words
            line = ' '.join(line_words)
            lines.append(line)

        y = 200
        for line in lines:
            text = SMALL_FONT.render(line, True, WHITE)
            rect = text.get_rect(midtop = (100, y))
            win.blit(text, rect)

            y = y + text.get_height() + 5

    def draw(self, win):
        """
        Function to draw the window each iteration of the game

        Arguments:
            win {surface} -- Pygame window to draw to
        """
        win.blit(BG_IMG, (0,0))
        self.board.draw(self.screen)
        win.blit(self.screen, (200,0))
        self.draw_bomb_text(win)
        self.draw_time_text(win)
        self.draw_message(win)
        pygame.display.update()
