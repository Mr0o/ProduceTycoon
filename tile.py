import pygame

class Tile():
    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.tile_img = pygame.Rect((self.x, self.y), (self.size, self.size))
        
    def draw(self):
        pygame.draw.rect(self.screen, (0, 0, 0), self.tile_img)
        #self.screen.blit(self.background_grid.tile_img, (self.x, self.y))