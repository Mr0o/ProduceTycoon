from math import sqrt

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.tile import Tile

def isGuestTouchingTile(guest: Guest, tile: Tile) -> bool:
    """
    Returns True if the guest is touching the tile
    """

    b1x = guest.pos.x + guest.size/2
    b1y = guest.pos.y + guest.size/2
    b2x = tile.pos.x + tile.size/2
    b2y = tile.pos.y + tile.size/2
    
    guestRadius = guest.size/2
    tileRadius = tile.size/2

    return ((b1x-b2x)*(b1x-b2x) + (b1y-b2y)*(b1y-b2y)) < (guestRadius+tileRadius)**2


def resolveCollision(guest: Guest, tile: Tile) -> Guest:
    """
    Resolves the collision between the guest and the tile\n
    Collisions are circle vs circle\n
    So the guest and tile are treated like circles\n
    Returns the guest with the new updated velocity and position
    """

    guestCenterX = guest.pos.x + guest.size/2
    guestCenterY = guest.pos.y + guest.size/2
    tileCenterX = tile.pos.x + tile.size/2
    tileCenterY = tile.pos.y + tile.size/2

    guestRadius = guest.size/2
    tileRadius = tile.size/2

    #find the distance between ball and peg centers
    distance = sqrt((guestCenterX - tileCenterX)**2 + (guestCenterY - tileCenterY)**2)
    #find the amount of overlap between the ball and peg
    overlap =  1.0 * (guestRadius + tileRadius - distance)

    #prevent division by zero
    if (distance == 0):
        distance = 0.0001  # arbitrary small number

    #displace the ball
    guest.pos.x += overlap * (guest.pos.x - tile.pos.x) / distance
    guest.pos.y += overlap * (guest.pos.y - tile.pos.y) / distance

    ## workout dynamic collisions
    #normal
    nx = (guest.pos.x - tile.pos.x) / distance
    ny = (guest.pos.y - tile.pos.y) / distance

    #tangent
    tx = -ny
    ty = nx

    #dot product tangent
    dpTan = guest.vel.x * tx + guest.vel.y * ty

    #dot product normal
    dpNorm1 = guest.vel.x * nx + guest.vel.y * ny

    # since we only are concerned with collision displacement, the momentum calculation is not useful, so we can ignore it
    #conservation of momentum in 1D
    # tileMass = 1
    # guestMass = 1
    # m = (dpNorm1 * (guestMass - tileMass) + 2.0 * tileMass * 0) / (guestMass + tileMass)

    #update velocity of the ball
    guest.vel.x = tx * dpTan + nx #* m
    guest.vel.y = ty * dpTan + ny #* m   

    return guest