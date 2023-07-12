from vectors import Vector
from tileMap import TileMap
from tile import Tile, Type

# this moduel contains functions for collision detection and resolution with tiles and points (as Vectors)

def isPosCollidingTile(pos: Vector, tile: Tile) -> bool:
    return tile.rect.collidepoint(pos.x, pos.y)

# check if a point is colliding with a boundary tile, if so resolve by displacing the point
def resolveBoundaryCollision(pos: Vector, tileMap: TileMap) -> Vector:
    # get the tile that the point is colliding with
    tile = tileMap.getTileByPos(pos)

    # if the tile is a boundary tile
    if tile.type == Type.BOUNDARY:
        # if the point is colliding with the left side of the tile
        if pos.x < tile.pos.x:
            # resolve by displacing the point to the right
            pos.x = tile.pos.x + tile.size
        # if the point is colliding with the right side of the tile
        elif pos.x > tile.pos.x + tile.size:
            # resolve by displacing the point to the left
            pos.x = tile.pos.x
        # if the point is colliding with the top side of the tile
        elif pos.y < tile.pos.y:
            # resolve by displacing the point to the bottom
            pos.y = tile.pos.y + tile.size
        # if the point is colliding with the bottom side of the tile
        elif pos.y > tile.pos.y + tile.size:
            # resolve by displacing the point to the top
            pos.y = tile.pos.y

    return pos

# prevent collisions with a boundary tile by keeping the distance between the point and the tile greater than the minimum distance
def preventBoundaryCollision(pos: Vector, tileMap: TileMap, minDistance: int = 10) -> Vector:
    # get the tile that the point is colliding with
    tile = tileMap.getTileByPos(pos)

    # if the tile is a boundary tile
    if tile.type == Type.BOUNDARY:
        # if the point is colliding with the left side of the tile
        if pos.x < tile.pos.x:
            # prevent collision by displacing the point to the right
            pos.x = tile.pos.x + tile.size + minDistance
        # if the point is colliding with the right side of the tile
        elif pos.x > tile.pos.x + tile.size:
            # prevent collision by displacing the point to the left
            pos.x = tile.pos.x - minDistance
        # if the point is colliding with the top side of the tile
        elif pos.y < tile.pos.y:
            # prevent collision by displacing the point to the bottom
            pos.y = tile.pos.y + tile.size + minDistance
        # if the point is colliding with the bottom side of the tile
        elif pos.y > tile.pos.y + tile.size:
            # prevent collision by displacing the point to the top
            pos.y = tile.pos.y - minDistance

    return pos
    