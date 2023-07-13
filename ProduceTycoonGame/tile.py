import pygame
import pymunk
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

        # pymunk body and shape
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (self.pos.x + self.size / 2, self.pos.y + self.size / 2)
        self.shape = pymunk.Poly.create_box(self.body, (self.size, self.size))
        self.shape.friction = 1

        self.type: Type = type

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.size, self.size))

        # when the mouse is hovering over the tile
        self.isHighlighted = False

        # when the mouse has clicked on the tile
        self.isSelected = False

        self.WALKABLE_TILE_IMG_SCALED = pygame.transform.scale(WALKABLE_TILE_IMG.copy(), (self.size, self.size))
        self.INTERACTABLE_TILE_IMG_SCALED = pygame.transform.scale(INTERACTABLE_TILE_IMG.copy(), (self.size, self.size))
        self.BOUNDARY_TILE_IMG_SCALED = pygame.transform.scale(BOUNDARY_TILE_IMG.copy(), (self.size, self.size))

    def update(self):
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.size, self.size))

    def draw(self):
        self.tileImg = None
        match self.type:
            case Type.WALKABLE:
                self.screen.blit(self.WALKABLE_TILE_IMG_SCALED, (self.pos.x, self.pos.y))
            case Type.INTERACTABLE:
                self.screen.blit(self.INTERACTABLE_TILE_IMG_SCALED, (self.pos.x, self.pos.y))
            case Type.BOUNDARY:
                self.screen.blit(self.BOUNDARY_TILE_IMG_SCALED, (self.pos.x, self.pos.y))

        if self.isHighlighted:
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        elif self.isSelected:
            pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)
        
            
            
            