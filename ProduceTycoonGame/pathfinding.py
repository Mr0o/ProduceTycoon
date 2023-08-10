from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.tile import Tile, Type
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.collision import isGuestTouchingTile, resolveCollision

# the pathfinding algorithm of choice will be Goal Based Vector Field Pathfinding (VFP)

# create a heatmap of the tilemap
def createHeatmap(tileMap: TileMap, target: Tile) -> list[Tile]:
    # reset the cost and parent attributes of each tile
    for tile in tileMap.tileMapGrid:
        tile.cost = 0
        tile.parent = None
        tile.vector = Vector(0, 0)

    # list of open tiles
    openTiles: list[Tile] = []
    
    # list of closed tiles
    closedTiles: list[Tile] = []

    # add the target to the open tiles
    openTiles.append(target)

    # while there are still open tiles
    while len(openTiles) > 0:
        # get the current tile
        currentTile = openTiles[0]

        # for each tile in the open tiles
        for tile in openTiles:
            # if the tile has a lower cost than the current tile
            if tile.cost < currentTile.cost:
                # set the current tile to the tile
                currentTile = tile

        # remove the current tile from the open tiles
        openTiles.remove(currentTile)

        # add the current tile to the closed tiles
        closedTiles.append(currentTile)

        # get the neighbors of the current tile
        neighbors = tileMap.getNeighbors(currentTile)

        # for each neighbor of the current tile
        for neighbor in neighbors:
            # if the neighbor is not a boundary tile
            if neighbor.type != Type.BOUNDARY:
                # if the neighbor is not in the closed tiles
                if neighbor not in closedTiles:
                    # if the neighbor is not in the open tiles
                    if neighbor not in openTiles:
                       # add the neighbor to the open tiles
                        openTiles.append(neighbor)
                        # set the cost of the neighbor to the cost of the current tile plus 1
                        neighbor.cost = currentTile.cost + 1
                        # set the parent of the neighbor to the current tile
                        neighbor.parent = currentTile

    # return the closed tiles
    return closedTiles

# get the vector from neighboring tiles using kernel convolution
def getVector(tileMap: TileMap, tile: Tile) -> Vector:
    # get the neighbors of the tile
    neighbors = tileMap.getNeighbors(tile)

    vector = Vector(0, 0)

    neighboringVecs: list[Vector] = []
    
    # for each neighbor of the tile
    for neighbor in neighbors:
        if neighbor.type != Type.BOUNDARY:
            # if the neighbor has a parent
            if neighbor.parent != None:
                # get the vector from the neighbor to the parent using the centers of the tiles
                vec = Vector(neighbor.parent.pos.x + neighbor.parent.size - neighbor.pos.x - neighbor.size, neighbor.parent.pos.y + neighbor.parent.size - neighbor.pos.y - neighbor.size)
                vec.setMag(neighbor.cost)
                neighboringVecs.append(vec)

    # for each neighboring vector
    for neighboringVec in neighboringVecs:
        # add the neighboring vector to the vector
        vector.add(neighboringVec)

    vector.setMag(10)

    # return the vector
    return vector

# create a vector field of the tilemap
def createVectorField(tileMap: TileMap, heatmap: list[Tile]) -> list[Vector]:
    # create a list of tiles that will be returned
    vectorField: list[Vector] = []

    # for each tile in the heatmap
    for tile in heatmap:
        # get the vector from neighboring tiles using kernel convolution
        vector = getVector(tileMap, tile)

        tile.vector = vector

    # return the vector field
    return vectorField


# used to store the vector field of each placed object
# a guest will aquire the vector field for tile they are targeting
class VectorFields():
    def __init__(self, tileMap: TileMap):
        self.updateVectorFields(tileMap)


    def updateVectorFields(self, tileMap: TileMap):
        # create a vector field for each tile in the tileMap
        self.vectorFields: list[list[Vector]] = []
        for tile in tileMap.tileMapGrid:
            self.vectorFields.append(self.createVectorField(tileMap, tile))