import pygame

from ProduceTycoonGame.functions import inputMovement
from ProduceTycoonGame.tile import Tile, Type


class TileMap():
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.x_mov = 0
        self.y_mov = 0

        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        self.zoom = self.screen.get_width()

        self.rows = self.screen.get_height() // 20
        self.col = self.screen.get_width() // 20
        self.tileMap_starting_pos = (self.x, self.y)
        
        # create the grid of tiles
        self.tileMap_grid = self.createTileGrid(self.zoom, self.rows, self.col, self.tileMap_starting_pos) 

        # creates rectangle size of screen for border
        self.rect = pygame.Rect((0, 0), (self.width, self.height))

        # highlighted tile
        self.highlighted_tile = None

    def createTileGrid(self, zoom: int, numRows: int, numCols: int, tileMap_starting_pos: tuple[int, int]):
        # create grid of tiles
        tile_size = zoom // numCols
        tileMap_grid: list[list[Tile]] = []
        for i in range(numRows):
            col: list[Tile] = []
            for j in range(numCols):
                if i == 0 or j == 0 or i == numRows-1 or j == numCols-1:
                    col.append(Tile(self.screen, tileMap_starting_pos[0] + j * tile_size,
                               tileMap_starting_pos[0] + i * tile_size, tile_size, Type.BOUNDARY))
                elif (i + j) % 2 == 0:
                    col.append(Tile(self.screen, tileMap_starting_pos[0] + j * tile_size,
                               tileMap_starting_pos[0] + i * tile_size, tile_size, Type.INTERACTABLE))
                else:
                    col.append(Tile(self.screen, tileMap_starting_pos[0] + j * tile_size,
                               tileMap_starting_pos[0] + i * tile_size, tile_size, Type.WALKABLE))
            tileMap_grid.append(col)

        return tileMap_grid

    def events(self):
        # changing the x and y positions
        self.x_mov, self.y_mov = inputMovement(self.x, self.y)

        # checking if mouse is hovering over tile
        self.highlighted_tile = None
        for i in range(self.rows):
            for j in range(self.col):
                if self.tileMap_grid[i][j].rect.collidepoint(pygame.mouse.get_pos()):
                    self.tileMap_grid[i][j].isHighlighted = True
                    self.highlighted_tile = self.tileMap_grid[i][j]
                else:
                    self.tileMap_grid[i][j].isHighlighted = False

    def update(self):
        for i in range(self.rows):
            for j in range(self.col):
                # updates each tiles x and y positions
                self.tileMap_grid[i][j].update(self.x_mov, self.y_mov)
        # updating borders x and y positions
        self.rect.x += self.x_mov
        self.rect.y += self.y_mov

    def draw(self):
        # drawing tileMap
        for i in range(self.rows):
            for j in range(self.col):
                self.tileMap_grid[i][j].draw()

        # draws border
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)
    def getTile(self, tileID: int):
        for i in range(self.rows):
            for j in range(self.col):
                if i + j == tileID:
                    return self.tileMap_grid[i][j]
                else:
                    return self.tileMap_grid[10][10]

