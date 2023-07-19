import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.tile import Type

id = 0

class PlacableObject():
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, rows: int = 1, cols: int = 1, elements: list = [], image: str = './Resources/Images/Banana_ProduceTycoon.png'):
        self.screen = screen
        self.pos = pos
        self.tileMap = tileMap
        self.rows = rows
        self.cols = cols
        self.elements = elements

        self.size = self.tileMap.tileMapGrid[0].size

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.rows * self.size, self.cols * self.size))

        self.isPlaced = False
        self.canPlace = True
        self.rect = self.image.get_rect()

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
                self.pos.x = tile.pos.x - self.rows * self.size // 4
                self.pos.y = tile.pos.y - self.cols * self.size // 4
                
            # changes tile type to object if rect collides with tile and mouse is clicked
            if self.rect.colliderect(tile.rect) and self.canPlace and not mouseClicked and previousMouseClick:
                tile.setTileType(Type.INTERACTABLE)
                self.isPlaced = True
            
        return True

    def update(self):
        if self.isPlaced:
            return
        if self.cols % 2 == 1 and self.rows % 2 == 1:
            self.pos.x += self.size * 3 // 4
            self.pos.y -= 1
        if self.cols % 2 == 1:
            self.pos.y += self.size * 3 / 4 - 1
        elif self.rows % 2 == 1:
            self.pos.x -= 1
            self.pos.x += self.size * 3 / 4
        self.rect.topleft = (self.pos.x, self.pos.y)

    def draw(self):
        pygame.draw.rect(self.screen, (240, 180, 212), self.rect)
        self.screen.blit(self.image, self.rect.topleft)

