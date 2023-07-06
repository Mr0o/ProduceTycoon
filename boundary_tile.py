import pygame

from tile import Tile

class Boundary_Tile(Tile):
    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int, tile_img: pygame.Surface):
        