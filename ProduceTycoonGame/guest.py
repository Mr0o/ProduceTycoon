import pygame
import random

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tile import Tile
from ProduceTycoonGame.person import Person

# global
id = 0

class Guest(Person):
    def __init__(self, screen: pygame.Surface, pos: Vector, name: str = "Guest"):
        global id; id += 1
        super().__init__(screen, pos, id, name)

    def setTarget(self, targetTile: Tile):
        if targetTile != None:
            # create a vector from the guest to the target tile
            self.mov = Vector(targetTile.pos.x - self.pos.x, targetTile.pos.y - self.pos.y)
            self.mov.setMag(5)

        # set the target tile
        self.targetTile = targetTile

    # draw
    def draw(self):
        super().draw()
        
        # load font
        debugFont = pygame.font.SysFont('Arial', 15, bold=True)

        # draw name
        nameText = debugFont.render(self.name, True, (0, 255, 0))
        self.screen.blit(nameText, (self.pos.x, self.pos.y - nameText.get_height()))
