from ProduceTycoonGame.collision import isGuestTouchingTile, resolveCollision
from ProduceTycoonGame.pathfinding import Pathfinder, VectorField
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.tile import Type
from ProduceTycoonGame.tileMap import TileMap

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

    # create pathfinder instance
    pathfinder = Pathfinder(tileMap)

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
                    for tile in tileMap.tileMapGrid:
                        if tile.type != Type.EDGE:
                            tile.type = Type.WALKABLE

                    # clear the pathfinder
                    pathfinder.clear()

                    # update the pathfinder
                    pathfinder.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClicked = True

        # set the target tile at the mouse position
        if mouseClicked:
            targetTile = tileMap.getTileByPos(Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

            # clear the old vector fields
            pathfinder.clear()

            # update the pathfinder
            pathfinder.update()
        
        # right click to set boundary tiles
        if pygame.mouse.get_pressed()[2]:
            tileAtPos = tileMap.getTileByPos(Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
            if tileAtPos != None and tileAtPos.type != Type.BOUNDARY and tileAtPos.type != Type.EDGE:
                tileAtPos.setTileType(Type.BOUNDARY)


        # if the tileMap has changed, update the pathfinder
        for tile in tileMap.tileMapGrid:
            if tile.changed:
                # update the pathfinder
                pathfinder.update()
                break

        # middle click to place guests
        if pygame.mouse.get_pressed()[1]:
            guest.pos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            guest.vel = Vector(0, 0)
            guest.acc = Vector(0, 0)

        tileMap.events(pygame.mouse.get_pressed()[2])

        # guest events
        guest.events()

        # set the force for the guest using the tile they reside on
        currentTile = tileMap.getTileByPos(guest.pos)
        if currentTile != None:
            # apply the force to the guest
            force = pathfinder.getVector(currentTile, targetTile)
            guest.applyForce(force)

        guest.update()

        # check for collisions
        for tile in tileMap.tileMapGrid:
            if tile.type == Type.BOUNDARY or tile == targetTile:
                if isGuestTouchingTile(guest, tile):
                    guest = resolveCollision(guest, tile)

        # get the actual velocity of the guest after collision check
        guest.actualVel = guest.vel.copy()
        # get the difference between the current pos and the previous pos
        posDelta = guest.pos - guest.prevPos

        guest.actualVel = posDelta

        # check if the guest is stuck (velocity is less than 0.9)
        if guest.isStuck:
            # get untsuck
            guest.vel = Vector(0, 0)
            guest.acc = Vector(0, 0)
            # find a neighboring tile that is not a boundary tile and teleport the guest to that tile
            neighbors = tileMap.getNeighbors(currentTile)
            for neighbor in neighbors:
                if neighbor.type != Type.BOUNDARY:
                    guest.pos = neighbor.pos.copy()
                    break

        # update
        tileMap.update()

        # draw
        screen.fill((0, 0, 0))

        # draw the heatmap and vector
        for tile in tileMap.tileMapGrid:
            # use cost to calculate color'
            # red value must be between 0 and 255
            rValue = (tile.cost / 50) * 255
            if rValue > 255:
                rValue = 255
            color = (rValue, 150, 60)
            pygame.draw.rect(screen, color, tile.rect)

            # draw the vector from the pathfinder vectors list
            vector = pathfinder.getVector(tile, targetTile)
            pygame.draw.line(screen, (100, 100, 100), (tile.pos.x + tile.size / 2, tile.pos.y + tile.size / 2), (tile.pos.x + tile.size / 2 + vector.x, tile.pos.y + tile.size / 2 + vector.y), 2)

            # draw the vector from the tile
            # pygame.draw.line(screen, (100, 100, 100), (tile.pos.x + tile.size / 2, tile.pos.y + tile.size / 2), (tile.pos.x + tile.size / 2 + tile.vector.x, tile.pos.y + tile.size / 2 + tile.vector.y), 2)


        # draw boundary tiles on top of heatmap
        for tile in tileMap.tileMapGrid:
            if tile.type == Type.BOUNDARY or tile.type == Type.EDGE or tile == targetTile:
                screen.blit(tile.BOUNDARY_TILE_IMG_SCALED, (tile.pos.x, tile.pos.y))

        # draw the guest
        guest.draw()

        # print the guest velocity
        text = pygame.font.SysFont('Arial', 15, bold=True).render("Guest Velocity: " + str(guest.vel.getMag()), True, (255, 255, 255))
        screen.blit(text, (0, 0))

        # print the guest actual velocity
        text = pygame.font.SysFont('Arial', 15, bold=True).render("Guest Actual Velocity: " + str(guest.actualVel.getMag()), True, (255, 255, 255))
        screen.blit(text, (0, 60))

        # print the guest stuck timer
        if guest.stuckTimer.isActive:
            text = pygame.font.SysFont('Arial', 15, bold=True).render("Stuck: " + str(guest.stuckTimer.timeRemaining), True, (255, 255, 255))
            screen.blit(text, (0, 20))

        # print the size of the vector fields list in pathfinder
        text = pygame.font.SysFont('Arial', 15, bold=True).render("Vector Fields: " + str(len(pathfinder.vectorFields)), True, (255, 255, 255))
        screen.blit(text, (0, 40))

        # print the tile id of the tile the guest is in
        if currentTile != None:
            text = pygame.font.SysFont('Arial', 15, bold=True).render("Tile ID: " + str(currentTile.id), True, (255, 255, 255))
            screen.blit(text, (0, 80))

        # draw the target tile
        pygame.draw.rect(screen, (0, 255, 0), targetTile.rect)

        # update the caption to show fps
        pygame.display.set_caption('Vector Field Pathfinding Testing | FPS: ' + str(int(clock.get_fps())) + ' | ' + str(clock.get_rawtime()) + ' ms')

        # update the display
        pygame.display.update()

        # set the fps
        clock.tick(60)