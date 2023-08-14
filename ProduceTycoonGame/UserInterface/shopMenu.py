import pygame

from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.vectors import Vector

class ShopMenu():
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (90, 140, 200)):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

        self.hidden = True
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.buttons = []
        self.exitButton = Button(self.screen, Vector(self.pos.x, self.pos.y), 'X', 20, 20, (255, 0, 0))


    def events(self, mouseClicked: bool = False):
        self.hidden = self.exitButton.events(mouseClicked)

    def update(self):
        pass

    def draw(self):
        if not self.hidden:
           pygame.draw.rect(self.screen, self.color, self.rect)
           pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
           self.exitButton.draw()