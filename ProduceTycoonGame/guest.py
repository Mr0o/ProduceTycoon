import pygame
import random

from ProduceTycoonGame.functions import inputMovement
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.tile import Tile, Type

class Guest():
    def __init__(self, screen: pygame.Surface, tile: Tile):
        self.screen = screen
        self.tile = tile
        self.tileArr = []
        self.size = self.tile.size
        self.moving = False
        self.moving_left = False
        self.moving_right = False
        self.animation_images = [(0, 50, 0), (0, 100, 0), (0, 150, 0), (0, 200, 0), (0, 255, 0)]
        self.animation_images_left = [(50, 0, 0), (100, 0, 0), (150, 0, 0), (200, 0, 0), (255, 0, 0)]
        self.animation_count = 0
        self.rect = pygame.Rect((self.tile.x, self.tile.y), (self.size, self.size))

    def events(self):
        # counting the frames once we get to 49 we reset to 0 back to the first image in out animation
        if (self.animation_count >= 49):
            self.animation_count = 0
        self.animation_count += 1

        #self.x, self.y = inputMovement(self.x, self.y)
        

        # Add flipping to images to show which direction we are moving

    
    def update(self):   
        # Updating guest
        self.rect = pygame.Rect((self.tile.x, self.tile.y), (self.size, self.size))

    def draw(self):
        # Drawling guest
        pygame.draw.rect(self.screen, self.animation_images[self.animation_count//10], self.rect)
    
