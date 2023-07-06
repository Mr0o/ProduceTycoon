import pygame

class Tile():
    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        #self.tile_img = pygame.image.load('./bg.jpg')
        #self.tile_img = pygame.Rect((self.x, self.y), (self.size, self.size))

    def update(self, x:int, y:int):
        pass
        #self.tile_img = pygame.Rect((self.x, self.y), (self.size, self.size))
        
    def draw(self):
        pass
        #pygame.draw.rect(self.screen, (255, 255, 255), self.tile_img)
        #self.screen.blit(self.tile_img, (self.x, self.y))