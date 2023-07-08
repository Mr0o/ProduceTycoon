import pygame
import random

from ProduceTycoonGame.functions import inputMovement
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.tile import Tile, Type

class Guest():
    def __init__(self, screen: pygame.Surface, tile: Tile):
        self.pos = tile.pos.copy()

        self.screen = screen
        self.tile = tile

        self.size = 25

        self.animationImages = [(0, 50, 0), (0, 100, 0), (0, 150, 0), (0, 200, 0), (0, 255, 0)]
        self.animationCount = 0
        self.rect = pygame.Rect((self.tile.pos.x, self.tile.pos.y), (self.size, self.size))

    def events(self):
        # counting the frames once we get to 49 we reset to 0 back to the first image in out animation
        if self.animationCount >= 49:
            self.animationCount = 0
        self.animationCount += 1

        self.pos = inputMovement(self.pos)

        # Add flipping to images to show which direction we are moving

    
    def update(self):   
        # Updating guest
        self.rect = pygame.Rect((self.tile.pos.x, self.tile.pos.y), (self.size, self.size))

    def draw(self):
        # Drawing guest
        pygame.draw.rect(self.screen, self.animationImages[self.animationCount//10], self.rect)

        
    
