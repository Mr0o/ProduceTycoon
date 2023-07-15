import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type

id = 0

class PlacableObject():
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, width: int, height: int, rows: int = 1, cols: int = 1):
        self.screen = screen
        self.pos = pos
        self.tileMap = tileMap
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols

        size = self.tileMap.zoom // self.tileMap.col

        self.isPlaced = False
        self.objectRect = pygame.Rect(self.pos.x, self.pos.y, size * self.rows, size * self.cols)

    def events(self):
        if self.isPlaced:
            return
        for tile in self.tileMap.tileMapGrid:
            # changes center of object object to center of current tile
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                self.pos.x = tile.pos.x + tile.size / 2
                self.pos.y = tile.pos.y + tile.size / 2

            # changes tile type to object if objectRect collides with tile and mouse is clicked
            if self.objectRect.colliderect(tile.rect):
                rect = tile.rect
                pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
                if False:
                    tile.type = Type.INTERACTABLE
                    self.tileMap.staticSurface = createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)
                    self.isPlaced = True

    def update(self):
        if self.isPlaced:
            return
        
        self.objectRect.center = (self.pos.x, self.pos.y)
        createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)

    def draw(self):
        if self.isPlaced:
            pygame.draw.rect(self.screen, (240, 180, 212), self.objectRect)
        else:
            pygame.draw.rect(self.screen, (240, 180, 212, 0.1), self.objectRect)
