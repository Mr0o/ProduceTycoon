import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type

id = 0

class PlacableObject():
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, width: int, height: int):
        self.screen = screen
        self.pos = pos
        self.tileMap = tileMap
        self.width = width
        self.height = height

        self.showRect = False
        self.isPlaced = False

        self.objectRect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def updatePos(self, condition: bool, newX: int, newY: int):
        if condition:
            self.pos.x = newX
            self.pos.y = newY


    def events(self, mouseClicked: bool = False, collideBut: bool = False):
        if self.isPlaced or not self.showRect:
            return
        for tile in self.tileMap.tileMapGrid:
            # changes center of object object to center of current tile
            conditionMouse = tile.rect.collidepoint(pygame.mouse.get_pos())
            newX = tile.pos.x + tile.size / 2
            newY = tile.pos.y + tile.size / 2
            self.updatePos(conditionMouse, newX, newY)

            # changes tile type to object if objectRect collides with tile and mouse is clicked
            if self.objectRect.colliderect(tile.rect) and mouseClicked and not(collideBut):
                tile.type = Type.INTERACTABLE
                self.tileMap.staticSurface = createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)
                self.isPlaced = True

    def update(self):
        if self.isPlaced or not self.showRect:
            return
        
        self.objectRect.center = (self.pos.x, self.pos.y)
        createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)

    def draw(self):
        if not self.showRect:
            return
        pygame.draw.rect(self.screen, (200, 0, 40), self.objectRect)
