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

        # selected tile
        self.selected_tile = None

    def createTileGrid(self, zoom: int, numRows: int, numCols: int, tileMap_starting_pos: tuple[int, int]):
        # create grid of tiles
        tile_size = zoom // numCols

        tileMap_grid: list[Tile] = []
        for i in range(numRows):
            for j in range(numCols):
                if i == 0 or j == 0 or i == numRows-1 or j == numCols-1:
                    tileMap_grid.append(Tile(self.screen, tileMap_starting_pos[0] + j * tile_size,
                               tileMap_starting_pos[0] + i * tile_size, tile_size, Type.BOUNDARY))
                elif (i + j) % 2 == 0:
                    tileMap_grid.append(Tile(self.screen, tileMap_starting_pos[0] + j * tile_size,
                               tileMap_starting_pos[0] + i * tile_size, tile_size, Type.INTERACTABLE))
                else:
                    tileMap_grid.append(Tile(self.screen, tileMap_starting_pos[0] + j * tile_size,
                               tileMap_starting_pos[0] + i * tile_size, tile_size, Type.WALKABLE))

        return tileMap_grid

    def events(self, mouseClicked: bool = False):
        # changing the x and y positions
        self.x_mov, self.y_mov = inputMovement(self.x, self.y)

        # checking if mouse is hovering over tile
        self.highlighted_tile = None
        for tile in self.tileMap_grid:
            tile.isHighlighted = False
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                self.highlighted_tile = tile
                tile.isHighlighted = True
                if mouseClicked:
                    if self.selected_tile is not None:
                        # deselecting selected tile
                        self.selected_tile.isSelected = False
                    if self.selected_tile == tile:
                        # deselecting tile
                        tile.isSelected = False
                        self.selected_tile = None
                    else:
                        # selecting tile
                        self.selected_tile = tile
                        self.selected_tile.isSelected = True

    def update(self):
        for tile in self.tileMap_grid:
            tile.update(self.x_mov, self.y_mov)
        # updating borders x and y positions
        self.rect.x += self.x_mov
        self.rect.y += self.y_mov

    def draw(self):
        # drawing tileMap
        for tile in self.tileMap_grid:
            tile.draw()

        # draws border
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)
