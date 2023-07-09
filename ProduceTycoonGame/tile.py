import pygame
from enum import Enum

from ProduceTycoonGame.vectors import Vector

WALKABLE_TILE_IMG = pygame.image.load('./Resources/Images/Tiles/Walkable.jpg')
INTERACTABLE_TILE_IMG = pygame.image.load('./Resources/Images/Tiles/Interactable.jpg')
BOUNDARY_TILE_IMG = pygame.image.load('./Resources/Images/Tiles/Barrier.png')

class Type(Enum):
    WALKABLE = 1
    INTERACTABLE = 2
    BOUNDARY = 3

# global
id = 0

class Tile():
    def __init__(self, screen: pygame.Surface, pos: Vector, size: int, type: Type = Type.WALKABLE):
        # create unique id for each tile
        global id; self.id = id; id += 1

        self.screen = screen

        self.pos = pos
        self.size = size

        self.type = type
        
        self.tileImg = None
        match self.type:
            case Type.WALKABLE:
                self.tileImg = WALKABLE_TILE_IMG
            case Type.INTERACTABLE:
                self.tileImg = INTERACTABLE_TILE_IMG
            case Type.BOUNDARY:
                self.tileImg = BOUNDARY_TILE_IMG
            # default case
            case _:
                raise Exception("Invalid tile type: " + str(self.type) + " for tile: " + str(self.id))
        
        # scale image to size
        self.tileImg = pygame.transform.scale(self.tileImg, (self.size, self.size))

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.size, self.size))

        # when the mouse is hovering over the tile
        self.isHighlighted = False

        # when the mouse has clicked on the tile
        self.isSelected = False

    def update(self):
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.size, self.size))
        
    def draw(self):
        if self.isHighlighted:
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
        elif self.isSelected:
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect)
        else:
            self.screen.blit(self.tileImg, (self.pos.x, self.pos.y))