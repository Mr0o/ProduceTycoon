import pygame
import random

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tile import Tile
from ProduceTycoonGame.person import Person

class Guest(Person):
    def setTarget(self, targetTile: Tile):
        if targetTile != None:
            # create a vector from the guest to the target tile
            self.mov = Vector(targetTile.pos.x - self.pos.x, targetTile.pos.y - self.pos.y)
            self.mov.setMag(5)

        # set the target tile
        self.targetTile = targetTile
