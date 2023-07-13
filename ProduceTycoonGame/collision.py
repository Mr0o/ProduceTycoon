from math import sqrt

import pygame

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

    #find the distance between the closest points on the two rects
    distance = sqrt((person.pos.x - person.size / 2 - tile.pos.x - tile.size / 2) ** 2 + (person.pos.y - person.size / 2 - tile.pos.y - tile.size / 2) ** 2)
    #find the amount of overlap between the person and tile
    overlap =  person.size / 2 + tile.size / 2 - distance

    #prevent division by zero
    if (distance == 0):
        distance = 0.0001  # arbitrary small number

    #displace the person
    person.pos.x += (person.pos.x - tile.pos.x) / distance * overlap
    person.pos.y += (person.pos.y - tile.pos.y) / distance * overlap

    return person
    