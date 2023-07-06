import pygame

from functions import inputMovement
from tile import Tile

class Background:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y

        # create grid of tiles
        self.rows = screen.get_height() // 50
        self.col = screen.get_width() // 50
        self.background_grid: list[list[Tile]] = []
        self.background_starting_pos = 0
        self.tile_size = screen.get_width() // self.col
        for i in range(self.rows):
            col: list[Tile] = []
            for j in range(self.col):
                col.append(Tile(self.screen, self.background_starting_pos + j * self.tile_size, self.background_starting_pos + i * self.tile_size, self.tile_size, pygame.image.load('./bg.jpg')))
            self.background_grid.append(col)

    def events(self):
        self.x, self.y = inputMovement(self.x, self.y)

    def update(self):
        pass

    def draw(self):
        # drawing background
        for i in range(self.rows):
            for j in range(self.col):
                self.screen.blit(self.background_grid[i][j].tile_img, (self.background_grid[i][j].x + self.x, self.background_grid[i][j].y + self.y))

        

