import pygame

class Tile():
    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int, tile_img: pygame.Surface):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.tile_img = tile_img
        
        # scale image
        self.tile_img = pygame.transform.scale(self.tile_img, (self.size, self.size))