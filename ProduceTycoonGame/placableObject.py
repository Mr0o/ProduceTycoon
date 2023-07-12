import pygame

from ProduceTycoonGame.vectors import Vector

class PlacableObject():
    def __init__(self, screen: pygame.Surface, pos: Vector):
        self.screen = screen
        self.pos = pos

    def events(self, mouseClicked: bool):
        pass

    def update(self):
        pass

    def draw(self):
        pass
