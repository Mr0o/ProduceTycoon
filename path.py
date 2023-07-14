from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.tile import Tile, Type
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.physics import Physics

# add cost and parent attributes to the tile class (temporarily)
Tile.cost: int = 0
Tile.parent: Tile = None
Tile.vector: Vector = Vector(0, 0)

# the pathfinding algorithm of choice will be Goal Based Vector Field Pathfinding (VFP)
# NOTE: There is a high performance cost when creating the heatmap and vector field, so this needs to be done as few times as possible
# We could either design the game around this or try to speed things up with optimizations, perhaps by using c++ ???

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
        # if the neighbor is not a boundary tile
        if neighbor.type != Type.BOUNDARY:
            # if the neighbor has a parent
            if neighbor.parent != None:
                # get the vector from the neighbor to the parent
                neighboringVecs.append(Vector(neighbor.parent.pos.x - neighbor.pos.x, neighbor.parent.pos.y - neighbor.pos.y))

    # for each neighboring vector
    for neighboringVec in neighboringVecs:
        # add the neighboring vector to the vector
        vector.add(neighboringVec)

    vector.setMag(10)

    # return the vector
    return vector

# create a vector field of the tilemap
def createVectorField(tileMap: TileMap, heatmap: list[Tile]) -> list[Tile]:
    # create a list of tiles that will be returned
    vectorField: list[Vector] = []

    # for each tile in the heatmap
    for tile in heatmap:
        # get the vector from neighboring tiles using kernel convolution
        vector = getVector(tileMap, tile)

        tile.vector = vector

    # return the vector field
    return vectorField


# test the pathfinding algorithm
if __name__ == "__main__":
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Vector Field Pathfinding Testing')
    clock = pygame.time.Clock()

    # create a tilemap
    tileMap = TileMap(screen, Vector(0, 0))

    # create a guest
    guest = Guest(screen, Vector(25, 25))

    # target tile
    targetTile = tileMap.getTileByID(150)

    # create a heatmap
    print("Creating heatmap...")
    heatmap = createHeatmap(tileMap, targetTile)

    # create a vector field
    print("Creating vector field...")
    vectorField = createVectorField(tileMap, heatmap)

    physics = Physics(tileMap.getNonWalkableTiles(), [guest])

    # main game loop
    running = True
    while running:
        # events
        mouseClicked = False
        for event in pygame.event.get():
            # will stop running and exit
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    print("Creating new tilemap...")
                    # reset the tilemap (clears boundary tiles)
                    tileMap = TileMap(screen, Vector(0, 0))

                    # create a heatmap
                    print("Creating heatmap...")
                    heatmap = createHeatmap(tileMap, targetTile)

                    # create a vector field
                    print("Creating vector field...")
                    vectorField = createVectorField(tileMap, heatmap)

                    # reset the physics
                    physics = Physics(tileMap.getNonWalkableTiles(), [guest])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClicked = True

        # set the target tile at the mouse position
        if mouseClicked:
            targetTile = tileMap.getTileByPos(Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            # create a heatmap
            print("Creating heatmap...")
            heatmap = createHeatmap(tileMap, targetTile)

            # create a vector field
            print("Creating vector field...")
            vectorField = createVectorField(tileMap, heatmap)
        
        # right click to set boundary tiles
        if pygame.mouse.get_pressed()[2]:
            tileAtPos = tileMap.getTileByPos(Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            if tileAtPos != None and tileAtPos.type != Type.BOUNDARY:
                tileAtPos.type = Type.BOUNDARY
                # add tile to physics
                physics.addTile(tileAtPos)

        # middle click to place guests
        if pygame.mouse.get_pressed()[1]:
            guest.pos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


        tileMap.events(pygame.mouse.get_pressed()[2])

        # guest events
        guest.events()

        # set the force for the guest using the tile they reside on
        currentTile = tileMap.getTileByPos(guest.pos)
        if currentTile != None:
            # apply the force to the guest in pymunk space
            physics.applyForce(guest, currentTile.vector)

        # update
        tileMap.update()

        # physics update
        physics.update(clock.get_time())

        # draw
        screen.fill((0, 0, 0))

        # draw the heatmap and vector
        for tile in heatmap:
            # use cost to calculate color'
            # red value must be between 0 and 255
            rValue = (tile.cost / 50) * 255
            if rValue > 255:
                rValue = 255
            color = (rValue, 0, 0)
            pygame.draw.rect(screen, color, tile.rect)

            # draw the vector
            pygame.draw.line(screen, (100, 100, 100), (tile.pos.x + tile.size / 2, tile.pos.y + tile.size / 2), (tile.pos.x + tile.size / 2 + tile.vector.x, tile.pos.y + tile.size / 2 + tile.vector.y), 2)


        # draw boundary tiles on top of heatmap
        for tile in tileMap.tileMapGrid:
            if tile.type == Type.BOUNDARY:
                screen.blit(tile.BOUNDARY_TILE_IMG_SCALED, (tile.pos.x, tile.pos.y))

        # draw the guest
        guest.draw()

        # draw the target tile
        pygame.draw.rect(screen, (0, 255, 0), targetTile.rect)

        # update the caption to show fps
        pygame.display.set_caption('Vector Field Pathfinding Testing | FPS: ' + str(int(clock.get_fps())) + ' | ' + str(clock.get_rawtime()) + ' ms')

        # update the display
        pygame.display.update()

        # set the fps
        clock.tick(60)