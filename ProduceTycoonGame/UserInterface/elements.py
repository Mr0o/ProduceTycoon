import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type
from ProduceTycoonGame.vectors import Vector

class Element():
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, isSelected: bool):
        self.screen = screen
        self.pos = pos
        self.tileMap = tileMap
        self.isSelected = isSelected

        self.size = tileMap.zoom // tileMap.col

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
