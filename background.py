import pygame

from movement import Movement

class Background:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = 20
        self.background_img = pygame.transform.scale(pygame.image.load('./bg.jpg'), (self.size, self.size))

    def events(self):
        self.x, self.y = Movement.check_if_move(self.x, self.y)
            
    def update(self):
        # Updatig background and border
        pass

    def draw(self):
        # Drawling background and a border
       self.screen.blit(self.background_img, (self.x, self.y))
