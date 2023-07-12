import pygame

from ProduceTycoonGame.UserInterface.elements import Element
from ProduceTycoonGame.vectors import Vector

class MainUI():
    def __init__(self, screen: pygame.Surface, pos: Vector):
        self.screen = screen
        self.pos = pos
        pass



def createOverlay(width: int, height: int):
    surfaceUI = pygame.surface((width, height))
    pass



