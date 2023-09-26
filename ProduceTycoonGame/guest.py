import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.person import Person

# global
id = 0

def resetIDguest():
    global id; id = 0

class Guest(Person):
    def __init__(self, screen: pygame.Surface, pos: Vector, name: str = "Guest"):
        global id; id += 1
        super().__init__(screen, pos, id, name)