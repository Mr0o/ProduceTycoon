import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.tile import Type

id = 0

class PlacableObject():
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, rows: int = 1, cols: int = 1, elements: list = []):
        self.screen = screen
        self.pos = pos
        self.tileMap = tileMap
        self.rows = rows
        self.cols = cols
        self.elements = elements

        self.size = self.tileMap.zoom // self.tileMap.col - 1

        self.imageBanana = pygame.image.load('./Resources/Images/Banana_ProduceTycoon.png')
        self.imageBanana = pygame.transform.scale(self.imageBanana, (self.rows * self.size, self.cols * self.size))

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

    def moveToNewPos(self, mouseClicked: bool = False, previousMouseClick: bool = False):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.isPlaced = False
            self.placeAgain = True
            for tile in self.tileMap.tileMapGrid:
                if tile.rect.colliderect(self.rect):
                    tile.setTileType(Type.WALKABLE)
            return False

        return True

    def events(self, mouseClicked: bool = False, previousMouseClick: bool = False):
        if self.isPlaced:
            return False

        self.checkIfCanPlace()
        self.pos.x, self.pos.y = pygame.mouse.get_pos()
        for tile in self.tileMap.tileMapGrid:
            # changes center of object object to center of current tile
            if tile.rect.collidepoint(pygame.mouse.get_pos()):
                self.pos.x = tile.pos.x + tile.size / 2
                self.pos.y = tile.pos.y + tile.size / 2
            # changes tile type to object if rect collides with tile and mouse is clicked
            if self.rect.colliderect(tile.rect) and self.canPlace and not mouseClicked and previousMouseClick:
                tile.setTileType(Type.INTERACTABLE)
                self.isPlaced = True
            
        return True

    def update(self):
        if self.isPlaced:
            return
        self.rect.center = (self.pos.x, self.pos.y)

    def draw(self):
        pygame.draw.rect(self.screen, (240, 180, 212), self.rect)
        self.screen.blit(self.imageBanana, (self.pos.x - self.imageBanana.get_width() / 2, self.pos.y - self.imageBanana.get_height() / 2))
