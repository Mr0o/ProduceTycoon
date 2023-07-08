import pygame
import random

from ProduceTycoonGame.functions import inputMovement
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.tile import Tile, Type

class Guest():
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.tile_id = 0
        self.tileArr = []
        self.width = 30
        self.height = 45
        self.moving = False
        self.moving_left = False
        self.moving_right = False
        self.animation_images = [(0, 50, 0), (0, 100, 0), (0, 150, 0), (0, 200, 0), (0, 255, 0)]
        self.animation_images_left = [(50, 0, 0), (100, 0, 0), (150, 0, 0), (200, 0, 0), (255, 0, 0)]
        self.animation_count = 0
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def events(self):
        # counting the frames once we get to 49 we reset to 0 back to the first image in out animation
        if (self.animation_count >= 49):
            self.animation_count = 0
        self.animation_count += 1

        self.x, self.y = inputMovement(self.x, self.y)

        if self.moving:
            self.x += 20
            self.y += 20
            self.moving = False
        

        # Add flipping to images to show which direction we are moving

    
    def update(self):
        # Updating guest
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def draw(self):
        # Drawling guest
        pygame.draw.rect(self.screen, self.animation_images[self.animation_count//10], self.rect)
    
    def bestPath(currentTile: Tile, targetTile: int):
        self.tiles = tiles
        self.currentTile = currentTile
        self.targetTile = targetTile
        self.tileArr = []
        self.shortestPath = 10000

        # if tile is a boundary tile or interactable tile you will not move onto it
        if self.currentTile.type == BOUNDARY or self.currentTile.type == INTERACTABLE:
            return []

        # if tile is the tile you are looking for return the array you are looking for.
        if self.currentTile.id == self.targetTile:
            if self.shortestPath < self.tileArr.length:
                return []
            else:
                self.shortestPath = self.tileArr
                return self.tileArr

        self.tileArr = bestPath(self.guest, self.tiles, tiles.getTile(self.currentTile.id + 1), self.targetTile)
        self.tileArr = bestPath(self.guest, self.tiles, tiles.getTile(self.currentTile.id - 1), self.targetTile)
        self.tileArr = bestPath(self.guest, self.tiles, tiles.getTile(self.currentTile.id + 10), self.targetTile)
        self.tileArr = bestPath(self.guest, self.tiles, tiles.getTile(self.currentTile.id - 10), self.targetTile)

        print(self.tileArr)
        return self.tileArr