import pygame
from enum import Enum

WALKABLE_TILE_IMG = pygame.image.load('./Walkable.jpg')
INTERACTABLE_TILE_IMG = pygame.image.load('./Interactable.jpg')
BOUNDARY_TILE_IMG = pygame.image.load('./Barrier.png')

class Type(Enum):
    WALKABLE = 1
    INTERACTABLE = 2
    BOUNDARY = 3

class Tile():
    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int, type: Type = Type.WALKABLE):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size

        self.type = type
        
        self.tile_img = None
        if self.type == Type.WALKABLE:
            self.tile_img = WALKABLE_TILE_IMG
        elif self.type == Type.INTERACTABLE:
            self.tile_img = INTERACTABLE_TILE_IMG
        elif self.type == Type.BOUNDARY:
            self.tile_img = BOUNDARY_TILE_IMG
        else:
            raise Exception("Invalid tile type")
        
        # scale image to size
        self.tile_img = pygame.transform.scale(self.tile_img, (self.size, self.size))

        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))

    def update(self, x:int, y:int):
        self.x += x
        self.y += y
        self.rect = pygame.Rect((self.x, self.y), (self.size, self.size))
        
    def draw(self):
        self.screen.blit(self.tile_img, (self.x, self.y))