import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type
from ProduceTycoonGame.vectors import Vector

class Element():
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap):
        self.screen = screen
        self.pos = pos
        self.tileMap = tileMap

        self.size = tileMap.zoom // tileMap.col

        
