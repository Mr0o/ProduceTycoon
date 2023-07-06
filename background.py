import pygame

from movement import check_if_move
from tile import Tile

class Background:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y

        # create grid of tiles
        self.rows = 20
        self.col = 20
        self.background_grid: list[list[Tile]] = []
        self.background_starting_pos = 0
        self.tile_size = 20
        for i in range(self.rows):
            col: list[Tile] = []
            for j in range(self.col):
                col.append(Tile(self.screen, self.background_starting_pos - 20 * i,self.background_starting_pos - 20 * i, self.tile_size))
                self.background_grid.append(col)

    def events(self):
        # get relative mouse position
        rel_mouse_pos = pygame.mouse.get_rel()
        # get mouse buttons
        mouse_buttons = pygame.mouse.get_pressed()
        # if left mouse button is pressed
        if mouse_buttons[0]:
            # scroll background
            self.x += rel_mouse_pos[0]
            self.y += rel_mouse_pos[1]
        
        for i in range(self.rows):
            for j in range(self.col):
                self.background_grid[i][j].events()

    def update(self):
        pass

    def draw(self):
        # drawing background
        for i in range(self.rows):
            for j in range(self.col):
                self.background_grid[i][j].draw()

        

