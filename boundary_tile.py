import pygame

from tile import Tile

class Boundary_Tile(Tile):
    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int, tile_img: pygame.Surface ):
        super().__init__(screen, x, y, size)
        # scale image
        self.tile_img = pygame.transform.scale(tile_img, (self.size, self.size))
    def draw(self):
        self.screen.blit(self.tile_img, (self.x, self.y))