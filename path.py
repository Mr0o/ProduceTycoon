from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.tile import Tile, Type
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.vectors import Vector

def distanceBetweenTiles(tile1: Tile, tile2: Tile) -> int:
    return abs(tile1.pos.x - tile2.pos.x) + abs(tile1.pos.y - tile2.pos.y)

# use the A* algorithm to find the shortest path between two tiles
def findPath(tileMap: TileMap, startTile: Tile, endTile: Tile) -> list[Tile]:
    # create a list of tiles that have been visited
    visitedTiles: list[Tile] = []
    # create a list of tiles that have not been visited
    unvisitedTiles: list[Tile] = []
    # add the starting tile to the unvisited list
    unvisitedTiles.append(startTile)
    # create a dictionary of tiles that will be used to keep track of the tiles that have been visited and the tile that was visited before it
    previousTile: dict[Tile, Tile] = {}
    # create a dictionary of tiles that will be used to keep track of the distance from the starting tile to the current tile
    distanceFromStart: dict[Tile, int] = {}
    # set the distance from the starting tile to the starting tile to 0
    distanceFromStart[startTile] = 0
    # create a dictionary of tiles that will be used to keep track of the distance from the current tile to the end tile
    distanceToEnd: dict[Tile, int] = {}
    # set the distance from the current tile to the end tile to the distance between the starting tile and the end tile
    distanceToEnd[startTile] = distanceBetweenTiles(startTile, endTile)
    # while there are still tiles that have not been visited
    while len(unvisitedTiles) > 0:
        # set the current tile to the first tile in the unvisited list
        currentTile = unvisitedTiles[0]

        for tile in unvisitedTiles:
            if distanceFromStart[tile] < distanceFromStart[currentTile]:
                currentTile = tile

        if currentTile == endTile:
            path: list[Tile] = []
            # set the current tile to the end tile
            currentTile = endTile
            # while the current tile is not the starting tile
            while currentTile != startTile:
                path.append(currentTile)
                currentTile = previousTile[currentTile]

            path.reverse()
            return path

        # remove the current tile from the unvisited list
        unvisitedTiles.remove(currentTile)
        visitedTiles.append(currentTile)

        for neighbor in tileMap.getNeighbors(currentTile):
            # if the neighbor has not been visited
            if neighbor not in visitedTiles:
                distanceFromStart[neighbor] = distanceFromStart[currentTile] + distanceBetweenTiles(currentTile, neighbor)
                distanceToEnd[neighbor] = distanceBetweenTiles(neighbor, endTile)
                previousTile[neighbor] = currentTile

                if neighbor not in unvisitedTiles:
                    unvisitedTiles.append(neighbor)
            
    # return an empty list if no path was found
    return []

    
# test the findPath function
if __name__ == "__main__":
    import pygame
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # create a tile map
    tileMap = TileMap(screen, Vector(0, 0))
    # create a start tile
    startTile = tileMap.getTileByPos(Vector(30, 30))
    # create an end tile
    endTile = tileMap.getTileByPos(Vector(250, 250))

    # create a guest
    guest = Guest(screen, startTile.pos, "Test")

    # create a path
    path = None

    running = True
    while(running):
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if the mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # get the tile that the mouse is hovering over
                    tile = tileMap.getTileByPos(Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                    # if the tile is not None
                    if tile != None:
                        # set the start tile to the tile
                        startTile = tile
                        # set the guest's position to the tile's position
                        guest.pos = tile.pos
            
                # if the mouse is right clicked, set the tile that the mouse is hovering over to a boundary tile
                elif event.button == 3:
                    tile = tileMap.getTileByPos(Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                    if tile != None:
                        if tile.type == Type.BOUNDARY:
                            tile.type = Type.WALKABLE
                        else:
                            tile.type = Type.BOUNDARY

                
                # find the path from the start tile to the end tile
                path = findPath(tileMap, startTile, endTile)
                # if the path is not empty
                if len(path) > 0:
                    # set the guest's path to the path
                    guest.path = path
                    # set the guest's path index to 0
                    guest.pathIndex = 0
                    # set the guest's target tile to the first tile in the path
                    guest.targetTile = path[0]


        # update
        tileMap.update()
        guest.update()

        # draw
        screen.fill((0, 0, 0))
        tileMap.draw()
        guest.draw()

        # draw the path
        if path != None:
            for i in range(len(path) - 1):
                pygame.draw.line(screen, (255, 0, 0), (path[i].pos.x + path[i].size // 2, path[i].pos.y + path[i].size // 2), (path[i + 1].pos.x + path[i + 1].size // 2, path[i + 1].pos.y + path[i + 1].size // 2), 5)
                pygame.draw.circle(screen, (255, 0, 0), (path[i].pos.x + path[i].size // 2, path[i].pos.y + path[i].size // 2), 5)


        # draw the start tile
        pygame.draw.rect(screen, (255, 0, 0), (startTile.pos.x, startTile.pos.y, startTile.size, startTile.size))

        # draw the end tile
        pygame.draw.rect(screen, (0, 255, 0), (endTile.pos.x, endTile.pos.y, endTile.size, endTile.size))

        # draw the neighbor tiles of the start tile
        # for neighbor in tileMap.getNeighbors(startTile):
        #     pygame.draw.rect(screen, (0, 0, 255), (neighbor.pos.x, neighbor.pos.y, neighbor.size, neighbor.size))

        pygame.display.flip()  
        clock.tick(60)