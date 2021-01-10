import pygame
import json
import os
from datetime import datetime
from minesweeper.Board import Board
from minesweeper.Constants import BG_IMG, SMALL_FONT, WHITE, SCREEN_WIDTH, BASE_PATH

class Game:
    def __init__(self, difficulty):
        self.screen = pygame.Surface((600,600))
        self.rows = 0
        self.cols = 0
        self.num_bombs = 0
        self.reset(difficulty)


    def reset(self, difficulty):
        self.get_config(difficulty)
        self.tile_size = SCREEN_WIDTH // self.rows
        self.board = Board(self.rows, self.cols, self.num_bombs, self.tile_size)
        self.lost = False
        self.won = False
        self.shown_tiles = 0
        self.start_time = datetime.now().replace(microsecond = 0)
        self.end_time = None
        self.message = ""

    def get_config(self, difficulty):
        f = open(os.path.join(BASE_PATH, "config.JSON"))
        data = json.load(f)

        for level in data["difficulties"]:
            if level["Difficulty"] == difficulty:
                self.rows = level["ROWS"]
                self.cols = level["COLS"]
                self.num_bombs = level["NUM_BOMBS"]


    def flag(self, row, col):
        self.board.board[row][col].set_flag()

    def select(self, row, col):
        if not self.lost and not self.won:
            if not self.board.board[row][col].shown and not self.board.board[row][col].flagged:
                self.play(row, col)


    def play(self, row, col):
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
        self.board.show_flags()
        self.end_time = datetime.now().replace(microsecond = 0)
        total_time = str(self.end_time - self.start_time)
        index = total_time.index(":") + 1
        total_time = total_time[index:]
        self.message = "You won the game in a time of " + total_time + "."
        # Store the time taken?

    def lost_game(self):
        self.board.show_bombs()
        self.end_time = datetime.now().replace(microsecond = 0)
        self.message = "Game over. You lost."

    def draw_bomb_text(self, win):
        bomb_str = str(self.num_bombs - self.board.num_flagged())
        bomb_text = SMALL_FONT.render(bomb_str, True, WHITE)
        rect = bomb_text.get_rect(midleft=(105,112))
        win.blit(bomb_text, rect)

    def draw_time_text(self,win):
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
        win.blit(BG_IMG, (0,0))
        self.board.draw(self.screen)
        win.blit(self.screen, (200,0))
        self.draw_bomb_text(win)
        self.draw_time_text(win)
        self.draw_message(win)
        pygame.display.update()
