import time
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
            if neighbor.type != Type.BOUNDARY and neighbor.type != Type.EDGE:
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

    # get the nu,ber of boundary tiles in the neighbors
    boundaryTiles = 0
    for neighbor in neighbors:
        if neighbor.type == Type.BOUNDARY or neighbor.type == Type.EDGE:
            boundaryTiles += 1
    
    # for each neighbor of the tile
    for neighbor in neighbors:
        # check that its not a boundary tile or an edge tile
        if neighbor.type != Type.BOUNDARY and neighbor.type != Type.EDGE:
            # if the neighbor has a parent
            if neighbor.parent != None:
                # get the vector from the neighbor to the parent using the centers of the tiles
                vec = Vector(neighbor.parent.pos.x + neighbor.parent.size - neighbor.pos.x - neighbor.size, neighbor.parent.pos.y + neighbor.parent.size - neighbor.pos.y - neighbor.size)
                vec.setMag(neighbor.cost)
                neighboringVecs.append(vec)
        else:
            # pretend that boundary tiles have a vector pointing to the center of the current tile (this will make the guest avoid boundary tiles)
            vec = Vector(tile.pos.x + tile.size - neighbor.pos.x - neighbor.size, tile.pos.y + tile.size - neighbor.pos.y - neighbor.size)
            vec.setMag(8)
            neighboringVecs.append(vec)

    # for each neighboring vector
    for neighboringVec in neighboringVecs:
        # add the neighboring vector to the vector
        vector.add(neighboringVec)

    vector.setMag(10)

    # check if the vector is 0
    if vector.getMag() == 0:
        # set the vector to a random vector
        vector = Vector(1, 0)
        vector.setMag(10)

    # return the vector
    return vector

# create a vector field of the tilemap
def createVectorField(tileMap: TileMap, target: Tile) -> list[Vector]:
    # create a list of tiles that will be returned
    vectorField: list[Vector] = []

    # create a heatmap of the tilemap
    heatmap = createHeatmap(tileMap, target)

    # for each tile in the heatmap
    for tile in heatmap:
        # get the vector from neighboring tiles using kernel convolution
        vector = getVector(tileMap, tile)

        tile.vector = vector

    # return the vector field
    return vectorField


# used to store the vector field of each placed object
# a guest will aquire the vector field for tile they are targeting
class VectorField():
    def __init__(self, tileMap: TileMap, target: Tile):
        self.tileMap = tileMap
        self.target = target
        self.vectorField: list[Vector] = []

    def update(self):
        self.vectorField = createVectorField(self.tileMap, self.target)

    def getVector(self, tile: Tile) -> Vector:
        vector: Vector = VectorField[tile.id]
        return vector

    def getVectorField(self) -> list[Vector]:
        return self.vectorField
    

# this will contain all vectorFields and contain methods to create, update, and get vector data from them
class Pathfinder():
    def __init__(self, tileMap: TileMap):
        self.tileMap = tileMap
        self.vectorFields: list[VectorField] = []

    def createVectorField(self, target: Tile) -> None:
        vectorField = VectorField(self.tileMap, target)
        vectorField.update()
        self.vectorFields.append(vectorField)

    def update(self) -> None:
        # check for any changes in the tilemap and update the vector fields accordingly
        tileMapChanged = False
        for tile in self.tileMap.tileMapGrid:
            if tile.changed:
                tileMapChanged = True
                break
        if tileMapChanged:
            print("Updating vector fields")
            startTime = time.time()
            for vectorField in self.vectorFields:
                vectorField.update()
            print("Vector fields updated in " + str(time.time() - startTime) + " seconds")

    def getVector(self, tile: Tile, target: Tile) -> Vector:
        # get the VectorField with the matching target
        targetVectorField = None
        for vectorField in self.vectorFields:
            if vectorField.target == target:
                targetVectorField = vectorField
                break
        
        # if there is no VectorField that matches the target
        if targetVectorField == None:
            print("No VectorField with the matching target")
            print("Creating VectorField ...")
            # create a VectorField with the matching target
            targetVectorField = VectorField(self.tileMap, target)
            self.vectorFields.append(targetVectorField)

        # get the vector from the VectorField
        vector = targetVectorField.getVector(tile)

        # return the vector
        return vector
    
    def clear(self) -> None:
        self.vectorFields.clear()