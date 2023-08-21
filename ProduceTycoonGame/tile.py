import pygame
from enum import Enum

from ProduceTycoonGame.vectors import Vector

WALKABLE_TILE_IMG = pygame.image.load('./Resources/Images/Tiles/FloorTile.png')
INTERACTABLE_TILE_IMG = pygame.image.load('./Resources/Images/Tiles/Interactable.jpg')
BOUNDARY_TILE_IMG = pygame.image.load('./Resources/Images/Tiles/Barrier.png')

class Type(Enum):
    WALKABLE = 1
    INTERACTABLE = 2
    BOUNDARY = 3
    EDGE = 4

class Tile():
    static_id = 0
    def __init__(self, screen: pygame.Surface, pos: Vector, size: int, type: Type = Type.WALKABLE):
        # create unique id for each tile
        self.id = Tile.static_id
        Tile.static_id += 1

        self.screen = screen

        self.pos = pos
        self.size = size
        
        self.type: Type = type

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.size, self.size))

        # when the mouse is hovering over the tile
        self.isHighlighted = False

        # when the mouse has clicked on the tile
        self.isSelected = False

        # when the tile type has changed
        self.changed = False

        # pathfinding variables
        self.cost: int = 0
        self.parent: Tile = None
        self.vector = Vector(0, 0)

        self.WALKABLE_TILE_IMG_SCALED = pygame.transform.scale(WALKABLE_TILE_IMG.copy(), (self.size, self.size))
        self.INTERACTABLE_TILE_IMG_SCALED = pygame.transform.scale(INTERACTABLE_TILE_IMG.copy(), (self.size, self.size))
        self.BOUNDARY_TILE_IMG_SCALED = pygame.transform.scale(BOUNDARY_TILE_IMG.copy(), (self.size, self.size))

    def update(self):
        pass
        # get the position of the tile in pymunk space
        # self.pos = Vector(self.body.position.x - self.size / 2, self.body.position.y - self.size / 2)
        # # update the rect
        # self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.size, self.size))

    def draw(self):
        self.tileImg = None
        match self.type:
            case Type.WALKABLE:
                self.screen.blit(self.WALKABLE_TILE_IMG_SCALED, (self.pos.x, self.pos.y))
            case Type.INTERACTABLE:
                self.screen.blit(self.INTERACTABLE_TILE_IMG_SCALED, (self.pos.x, self.pos.y))
            case Type.BOUNDARY:
                self.screen.blit(self.BOUNDARY_TILE_IMG_SCALED, (self.pos.x, self.pos.y))
            case Type.EDGE:
                # placeholder, this should be a wall tile img not a walkable tile img
                self.screen.blit(self.WALKABLE_TILE_IMG_SCALED, (self.pos.x, self.pos.y))


        # if self.isHighlighted:
        #     pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        # elif self.isSelected:
        #     pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)

    def setTileType(self, type: Type):
        self.type = type
        self.changed = True
        
            
            
            