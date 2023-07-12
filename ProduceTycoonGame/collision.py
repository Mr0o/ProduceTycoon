from math import sqrt

# even though this game uses tiles and squares, the collision detection is being done in terms of circles
def isCircleTouchingCircle(b1x, b1y, b1r, b2x, b2y, b2r) -> bool:
    return ((b1x-b2x)*(b1x-b2x) + (b1y-b2y)*(b1y-b2y)) < (b1r+b2r)*(b1r+b2r)

# wrapper function for the collision detection
def isGuestTouchingTile(guest, tile) -> bool:
    b1x = guest.pos.x + guest.size / 2
    b1y = guest.pos.y + guest.size / 2
    b1r = guest.size / 2

    b2x = tile.pos.x + tile.size / 2
    b2y = tile.pos.y + tile.size / 2
    b2r = tile.size / 2

    return isCircleTouchingCircle(b1x, b1y, b1r, b2x, b2y, b2r)


def resolveCollision(person, tile):
    """
    Resolve collision between two tiles

    - person: Tile
    - tile: Tile

    Collison is resolved by displacing the tiles so that they are no longer touching
    \nReturns <person> with the updated position
    """

    #find the distance between person and tile centers
    distance = sqrt((person.pos.x + person.size / 2 - tile.pos.x - tile.size / 2)**2 + (person.pos.y + person.size / 2 - tile.pos.y - tile.size / 2)**2)
    #find the amount of overlap between the person and tile
    overlap =  person.size / 2 + tile.size / 2 - distance

    #prevent division by zero
    if (distance == 0):
        distance = 0.0001  # arbitrary small number

    #displace the person
    person.pos.x -= overlap * (person.pos.x - tile.pos.x) / distance
    person.pos.y -= overlap * (person.pos.y - tile.pos.y) / distance

    return person
    