class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.bomb = False
        self.shown = False
        self.surrounding_bombs = 0
        self.get_pos()

    def get_pos(self):
        pass

    def set_bomb(self):
        self.bomb = True

    def draw(self,win):
        pass