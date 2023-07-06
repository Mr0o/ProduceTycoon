import pygame

from functions import inputMovement
from tile import Tile
from graphic_tile import Graphic_Tile

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
                if (i + j) % 2 == 0:
                    col.append(Tile(self.screen, self.background_starting_pos + j * self.tile_size, self.background_starting_pos + i * self.tile_size, self.tile_size))
                else:
                    col.append(Graphic_Tile(self.screen, self.background_starting_pos + j * self.tile_size, self.background_starting_pos + i * self.tile_size, self.tile_size, pygame.image.load('./bg.jpg')))
            self.background_grid.append(col)

        self.rect = pygame.Rect((0, 0), (self.screen.get_width(), self.screen.get_height()))

    def events(self):
        for i in range(self.rows):
            for j in range(self.col):
                self.background_grid[i][j].x, self.background_grid[i][j].y = inputMovement(self.background_grid[i][j].x, self.background_grid[i][j].y)
        self.rect.x, self.rect.y = inputMovement(self.rect.x, self.rect.y)

    def update(self):
        for i in range(self.rows):
            for j in range(self.col):
                self.background_grid[i][j].update(self.background_grid[i][j].x, self.background_grid[i][j].y)
    def draw(self):
        # drawing background
        for i in range(self.rows):
            for j in range(self.col):
                self.background_grid[i][j].draw()
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)

        

