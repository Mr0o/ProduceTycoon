import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type
from ProduceTycoonGame.vectors import Vector

class Element():
    def __init__(self, screen: pygame.Surface, pos: Vector):
        self.screen = screen
        self.pos = pos

    def events(self, mouseClicked: bool):
        pass

        