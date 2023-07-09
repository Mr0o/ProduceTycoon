import pygame
import random

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.functions import inputMovement
from ProduceTycoonGame.tile import Tile

class Guest():
    def __init__(self, screen: pygame.Surface, pos: Vector):
        self.screen = screen
        self.pos = pos
        self.size = 50

        self.mov = Vector(0, 0)
        self.targetTile: Tile = None

        self.animationImages = [
            (0, 50, 0), (0, 100, 0), (0, 150, 0), (0, 200, 0), (0, 255, 0)]
        self.animationCount = 0
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.size, self.size))

    def events(self):
        # counting the frames once we get to 49 we reset to 0 back to the first image in out animation
        if self.animationCount >= 49:
            self.animationCount = 0
        self.animationCount += 1

        self.pos = inputMovement(self.pos)

        # Add flipping to images to show which direction we are moving

    def update(self):
        # Updating guest
        # move towards target tile
        if self.targetTile != None:
            # check if rects are colliding
            if self.rect.colliderect(self.targetTile.rect):
                self.targetTile = None
                self.mov = Vector(0, 0)
            else:
                self.pos.add(self.mov)

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.size, self.size))


    def draw(self):
        # Drawing guest
        pygame.draw.rect(
            self.screen, self.animationImages[self.animationCount//10], self.rect)

    def setTarget(self, targetTile: Tile):
        if targetTile != None:
            # create a vector from the guest to the target tile
            self.mov = Vector(targetTile.pos.x - self.pos.x, targetTile.pos.y - self.pos.y)
            self.mov.setMag(5)

        # set the target tile
        self.targetTile = targetTile
