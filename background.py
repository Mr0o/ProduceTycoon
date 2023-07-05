import pygame

from movement import Movement

class Background:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = 2001
        self.width = 2001
        self.background_box = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.background_img = pygame.image.load('./bg.jpg')
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))

    def events(self):
        self.x, self.y = Movement.check_if_move(self.x, self.y)
            
    def update(self):
        # Updatig background and border
        self.background_box = pygame.Rect((self.x, self.y), (self.width, self.height))

    def draw(self):
        # Drawling background and a border
        self.screen.blit(self.background_img, (self.x, self.y))
        pygame.draw.rect(self.screen, (255, 0, 0), self.background_box, 2)
