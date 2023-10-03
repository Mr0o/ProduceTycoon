"""Author: Owen Smith (Mr0)
\n Pathfinding module for Produce Tycoon
\n This module is used to handle pathfinding and is an implementation of the vector field pathfinding algorithm
\n --
\n To use it in the game, simply create one instance of the Pathfinder class in the game
\n \t`pathfinder = Pathfinder(tileMap)`
"""

import time
from ProduceTycoonGame.tileMap import TileMap, Tile, Type
from ProduceTycoonGame.vectors import Vector

# the pathfinding algorithm of choice will be Goal Based Vector Field Pathfinding (VFP)

def createHeatmap(tileMap: TileMap, target: Tile) -> list[Tile]:
    """Generate the 'heatmap' for the specified target tile.
    \n Sets the cost and parent attributes of each tile
    \n ### Parameters:
    \n `tileMap`: The tilemap to generate the heatmap for
    \n `target`: The target goal for the heatmap
    """

    # reset the cost and parent attributes of each tile
    for tile in tileMap.grid:
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
            if neighbor.typeTile != Type.BOUNDARY:
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

def calcVector(tileMap: TileMap, tile: Tile) -> Vector:
    """Calculate the vector for the specified tile using kernel convolution.
    \n ### Parameters:
    \n `tileMap`: The tilemap that contains the tile and its neighbors
    \n `tile`: The tile to calculate the vector for
    \n ### Returns:
    \n `vector`: The vector for the tile
    """

    # get the neighbors of the tile
    neighbors = tileMap.getNeighbors(tile)

    vector = Vector(0, 0)

    neighboringVecs: list[Vector] = []
    
    # for each neighbor of the tile
    for neighbor in neighbors:
        if neighbor.typeTile != Type.BOUNDARY:
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

def createVectorField(tileMap: TileMap, target: Tile) -> list[Vector]:
    """Create a field of vectors for each tile in the tileMap using the target tile.
    \n ### Parameters:
    \n `tileMap`: The tilemap to create the vector field for
    \n `target`: The target goal for the vector field pathfinding
    \n ### Returns:
    \n `vectorField`: The list of Vectors for each tile in the tileMap
    """
    # create a list of tiles that will be returned
    vectorField: list[Vector] = []

    # create a heatmap of the tilemap
    heatmap = createHeatmap(tileMap, target)

    # for each tile in the heatmap
    for tile in heatmap:
        # get the vector from neighboring tiles using kernel convolution
        vector = calcVector(tileMap, tile)

        tile.vector = vector

    # the heatmap is not necessarily in the same order as the tileMap, 
    # so we will loop throught the tileMap and get the vectors
    # Note: using the tile.vector attribute should be avoided because it will always be set to the last vector calculated
    # it is only used for the vectorField calculation, and should not be used for anything else
    for tile in tileMap.grid:
        vectorField.append(tile.vector)

    # return the vector field
    return vectorField


# used to store the vector field of each placed object
# a guest will aquire the vector field for tile they are targeting
class VectorField:
    """A class to store a vector field pointing to a single target tile.
    \n A vector field must be created for each target tile.
    \n It will also need to be updated any time the tilemap changes.
    \n ### Attributes:
    \n `tileMap`: The tilemap that the vector field is for
    \n `target`: The target tile that the vector field points to
    \n `vectors`: The list of vectors for each tile in the tilemap
    \n ### Methods:
    \n `update()`: Updates the vector field
    \n `getVector(tile)`: Returns the vector for the specified tile
    \n `getVectors()`: Returns the list of vectors for each tile in the tilemap
    """

    def __init__(self, tileMap: TileMap, target: Tile):
        self.tileMap = tileMap
        self.target = target
        self.vectors: list[Vector] = []
        self.update()

    def update(self):
        self.vectors = createVectorField(self.tileMap, self.target)

    def getVector(self, tile: Tile) -> Vector:
        if tile is None:
            print("WARN: VectorField.getVector() -> tile is None")
            return Vector(0, 0)
        
        return self.vectors[tile.id]

    def getVectors(self) -> list[Vector]:
        return self.vectors
    

class Pathfinder:
    """Pathfinder class to automatically manage all vector fields.
    \n To use it, simply create one instance in the game.
    \n \t`pathfinder = Pathfinder(tileMap)`
    \n To get a vector for a tile, use the `getVector()` method.
    \n \t`vector = pathfinder.getVector(tile, target)`
    \n The update method should be called any time the tilemap changes or simply on every frame.
    \n \t`pathfinder.update()`
    \n Everything else is handled internally and automatically.
    """
    def __init__(self, tileMap: TileMap):
        self.tileMap = tileMap
        self.vectorFields: list[VectorField] = []

    def createVectorField(self, target: Tile) -> None:
        """Creates a new vector field and appends to the vectorFields list"""

    def update(self) -> None:
        """Updates the pathfinder vector fields
        \n This should be called any time the tilemap changes
        \n Alternatively, it can simply be called every frame and will only update if changes are detected
        """
        # check for any changes in the tilemap and update the vector fields accordingly
        tileMapChanged = False
        for tile in self.tileMap.grid:
            if tile.changed:
                tileMapChanged = True
                tile.changed = False
        if tileMapChanged:
            #print("Updating vector fields")
            startTime = time.time()
            for vectorField in self.vectorFields:
                vectorField.update()
            #print("Vector fields updated in " + str(time.time() - startTime) + " seconds")

    def getVector(self, tile: Tile, target: Tile) -> Vector:
        """Returns the vector to get from the current tile to the target tile"""
        if tile is None:
            print("WARN: Pathfinder.getVector() -> tile is None")
            return Vector(0, 0)
        
        # get the vector field for the target
        vectorField = self.getVectorField(target)
        # get the vector from the vector field
        vector = vectorField.getVector(tile)

        return vector
    
    def getVectorField(self, target: Tile) -> VectorField:
        """Returns the vector field that matches the target"""
        if target is None:
            print("WARN: Pathfinder.getVectorField() -> target is None")
            return []
        # get the vector field for the target
        for vectorField in self.vectorFields:
            if vectorField.target == target:
                return vectorField
        
        # if the vector field does not exist, create it and return it
        self.createVectorField(target)
        return self.getVectorField(target)
    
    def clear(self) -> None:
        """Clears the vector fields list"""
        self.vectorFields.clear()