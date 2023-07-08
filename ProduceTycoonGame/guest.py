import pygame
import random

from ProduceTycoonGame.functions import changeTile
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.tile import Tile, Type

class Guest():
    def __init__(self, screen: pygame.Surface, tile: Tile, tileMap: TileMap):
        self.screen = screen
        self.tile = tile
        self.tileMap = tileMap

        self.previousTile = self.tile
        self.size = self.tile.size
        self.movements = ["right", "right", "right", "down", "down"]
        self.movementCount = 0
        self.animation_images = [(0, 50, 0), (0, 100, 0), (0, 150, 0), (0, 200, 0), (0, 255, 0)]
        self.animation_count = 0
        self.rect = pygame.Rect((self.tile.x, self.tile.y), (self.size, self.size))

    def events(self):
        # counting the frames once we get to 49 we reset to 0 back to the first image in out animation
        if self.animation_count >= 49:
            self.animation_count = 0
        self.animation_count += 1
        if self.movementCount >= 299:
            self.movementCount = 0
        self.movementCount += 1
        

        #saves the previous tile you were on
        self.previousTile = self.tile

        # changing tile
        self.tile = changeTile(self, self.movements[self.movementCount//60])
        self.movements[self.movementCount//60] = "moved"

        # checks if the tile you move to is a boundary tile if it is you move back to previous tile
        if self.tile.type == Type.BOUNDARY:
            self.tile = self.previousTile
        #self.x, self.y = inputMovement(self.x, self.y)
        

        # Add flipping to images to show which direction we are moving

    
    def update(self):   
        # Updating guest
        self.rect = pygame.Rect((self.tile.x, self.tile.y), (self.size, self.size))

    def draw(self):
        # Drawling guest
        pygame.draw.rect(self.screen, self.animation_images[self.animation_count//10], self.rect)
    
