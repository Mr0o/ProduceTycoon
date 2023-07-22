import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.slider import Slider

class PlacableObjectGUI():
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (200, 150, 170)):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.slider = Slider(self.screen, Vector(self.pos.x + 5, self.pos.y + self.height / 2 - 3), self.width - 10, 6)

        self.hidden = True

    def events(self, mouseClicked: bool = False):
        if self.hidden:
            return
        
        self.slider.events(mouseClicked)

    
    def update(self):
        if self.hidden:
            return
        
        self.slider.update()

    def draw(self):
        if self.hidden:
            return

        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)

        self.slider.draw()