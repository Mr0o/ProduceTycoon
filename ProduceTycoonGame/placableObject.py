import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type

id = 0

class PlacableObject():
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, width: int, height: int, rows: int = 1, cols: int = 1, elements: list = []):
        self.screen = screen
        self.pos = pos
        self.tileMap = tileMap
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.elements = elements


        self.size = self.tileMap.zoom // self.tileMap.col - 1

        self.isPlaced = False
        self.canPlace = True
        self.rect = pygame.Rect(self.pos.x - 1000, self.pos.y - 1000, self.size * self.rows, self.size * self.cols)

    def checkIfCanPlace(self):
        for element in self.elements:
            if element.rect.colliderect(self.rect):
                self.canPlace = False
                break
            else:
                self.canPlace = True

    def events(self, mouseClicked: bool = False):
        if self.isPlaced:
            return

        self.checkIfCanPlace()
        for tile in self.tileMap.tileMapGrid:
            # changes center of object object to center of current tile
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                self.pos.x = tile.pos.x + tile.size / 2
                self.pos.y = tile.pos.y + tile.size / 2
            # changes tile type to object if rect collides with tile and mouse is clicked
            if self.rect.colliderect(tile.rect) and self.canPlace and mouseClicked:
                tile.setTileType(Type.INTERACTABLE)
                self.isPlaced = True

    def update(self):
        if self.isPlaced:
            return
        self.rect.center = (self.pos.x, self.pos.y)

    def draw(self):
        pygame.draw.rect(self.screen, (240, 180, 212), self.rect)
