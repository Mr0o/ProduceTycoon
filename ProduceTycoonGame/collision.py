from math import sqrt

import pygame
from ProduceTycoonGame.vectors import Vector

# detect collision between two pygame rects
def isGuestTouchingTile(guest, tile) -> bool:
    return guest.rect.colliderect(tile.rect)


def resolveCollision(person, tile):
    """
    Resolve collision between two tiles

    - person: Tile
    - tile: Tile

    Collison is resolved by displacing the tiles so that they are no longer touching
    \nReturns <person> with the updated position
    """

    # get the distance between the two tiles
    distance = sqrt((person.pos.x - tile.pos.x)**2 + (person.pos.y - tile.pos.y)**2)

    # get the direction of the collision
    direction = Vector(tile.pos.x - person.pos.x, tile.pos.y - person.pos.y)
    direction.normalize()

    # get the displacement
    displacement = direction * distance

    # apply the displacement to the person
    person.pos -= Vector(displacement.x, displacement.y)

    return person
    