"""
The main game loop for Produce Tycoon
\n --
\n Usage:
\n\t`from ProduceTycoonGame.game import Game`
\n\t`game = Game()`
\n\t`game.run()`
\n --
\nThis is where the game is initialized and run
\nThe game loop calls these three methods every frame:
\n\t`events()` - handles events
\n\t`update()` - updates the game logic
\n\t`draw()` - draws the game to the screen
"""

from random import randint
import pygame

# local imports
from ProduceTycoonGame.events import postEvent, eventOccured, clearEventList
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, updateTileMap
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.objectRegister import Object, ObjectRegister
from ProduceTycoonGame.pathfinding import Pathfinder
from ProduceTycoonGame.UserInterface.GUI import GUI

# this is the main game loop (events, update, draw)
class Game:
    running = True
    screen: pygame.Surface

    def __init__(self, WIDTH: int = 800, HEIGHT: int = 600):
        pygame.init()

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)
        Game.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Produce Tycoon')

        # set the game icon
        icon = pygame.image.load('./Resources/Images/Produce/Tomato.png')
        pygame.display.set_icon(icon)

        # load font
        self.debugFont = pygame.font.SysFont('Arial', 15, bold=True)

        # debug variable that when true will enable debug features (fps, frametime, etc.)
        self.debug = False

        # debug variable that when true will draw the tiles that make up each currentObject (this could impact performance, therefore it is disabled by default)
        self.debugPlaceableObjects = False

        # set the screens
        ObjectRegister.setScreen(self.screen)
        TileMap.setScreen(self.screen)
        GUI.setScreen(self.screen)
        
        # create the tileMap
        self.tileMap = TileMap(Vector(0, 0))

        # init the GUI
        GUI.setTileMap(self.tileMap) # this is required by ObjectRegister (CAN WE DECOUPLE THIS?)
        GUI.WIDTH = self.WIDTH
        GUI.HEIGHT = self.HEIGHT
        self.GUI = GUI()

        # pathfinding (Vector Fields)
        self.pathfinder = Pathfinder(self.tileMap)

        self.guests: list[Guest] = []

    def events(self):
        clearEventList()

        for event in pygame.event.get():
            # will stop running and exit
            if event.type == pygame.QUIT:
                Game.running = False
            if event.type == pygame.KEYDOWN:
                # post the keydown event and include the event data
                postEvent("keyDown", eventData=event)

                if event.key == pygame.K_ESCAPE:
                    postEvent("escape")
                # press '1' to toggle debug
                elif event.key == pygame.K_1:
                    self.debug = not self.debug
                # press '2' to toggle debugPlaceableObjects
                elif event.key == pygame.K_2:
                    self.debugPlaceableObjects = not self.debugPlaceableObjects

                elif event.key == pygame.K_BACKSPACE:
                    postEvent("backspace", eventData=event)

                elif event.key == pygame.K_RETURN:
                    postEvent("enter", eventData=event)
            
            if event.type == pygame.KEYUP:
                postEvent("keyUp", eventData=event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    postEvent("leftMouseDown")
                if event.button == 3:
                    postEvent("rightMouseDown")

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    postEvent("leftMouseUp")
                if event.button == 3:
                    postEvent("rightMouseUp")

            # check for window resize
            if event.type == pygame.VIDEORESIZE:
                postEvent("windowResize", eventData=(event.w, event.h))
                self.WIDTH = event.w
                self.HEIGHT = event.h

        ### Place guests down on mouse click for testing (VERY HACKY, NEEDS TO BE REMOVED LATER) ###
        if eventOccured("rightMouseDown") and len(self.GUI.objects):
            # pick a random currentObject
            randomIndex = randint(0, len(self.GUI.objects) - 1)
            
            mousePos = pygame.mouse.get_pos()
            newGuest = Guest(self.screen, Vector(mousePos[0], mousePos[1]))
            targetTileID = self.GUI.objects[randomIndex].getFrontTiles()[0]
            newGuest.targetTile = self.tileMap.getTileByID(targetTileID)

            # make sure the guest is not None
            if newGuest.targetTile is not None:
                self.guests.append(newGuest)
        
        for guest in self.guests:
            self.GUI.elements.append(guest.rect)
            # guest events
            guest.events()

            # apply vector field of the current tile in the vector field list
            if guest.targetTile is not None:
                currentTile = self.tileMap.getTileByPos(guest.pos)
                force = self.pathfinder.getVector(currentTile, guest.targetTile)
                guest.applyForce(force)
            

            guest.update()
        ### END OF GUEST TESTING CODE ###

        # events for the GUI
        self.GUI.events()

    def update(self):
        for guest in self.guests:
            guest.update()

        # update the GUI
        self.GUI.update()

        # pathfinder update will check for any changes and update the vector fields
        self.pathfinder.update()
        
        if self.debug:
            pygame.display.set_caption('Produce Tycoon - ' + str(int(self.clock.get_fps())) + ' FPS')
        else:
            pygame.display.set_caption('Produce Tycoon')

    def draw(self):
        self.screen.fill((0, 0, 0))

        # drawing tileMap
        self.tileMap.draw()

        # if we are placing an object, draw the tile lines (feels like this if statement doesn't belong here..)
        if len(self.GUI.objects) and not self.GUI.objects[len(self.GUI.objects) - 1].info.placed:
            self.tileMap.drawTileLines()

        # drawing characters
        for guest in self.guests:
            guest.draw()

        # draw the GUI
        self.GUI.draw()

        ## DEBUG STUFF ##
        if self.debug:
            # draw raw frametime
            ft = int(self.clock.get_rawtime())
            # change color based on frametime to indicate performance (green = good, yellow = ok, red = bad)
            if ft > 16:
                ftColor = (255, 0, 0)
            elif ft > 8:
                ftColor = (255, 255, 0)
            else:
                ftColor = (0, 255, 0)
            text = self.debugFont.render(str(ft) + " ms", True, ftColor)
            self.screen.blit(text, (0, 20))

            # draw fps
            text = self.debugFont.render(str(int(self.clock.get_fps())) + " FPS ", True, (255, 255, 255))
            self.screen.blit(text, (0, text.get_height() + 20))

            # draw the size of the pathfinder vector fields list
            text = self.debugFont.render("Vector Fields: " + str(len(self.pathfinder.vectorFields)), True, (255, 255, 255))
            self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, text.get_height() * 2))

            # draw the current resolution WxH
            text = self.debugFont.render("Resolution: " + str(self.WIDTH) + " x " + str(self.HEIGHT), True, (255, 255, 255))
            self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, text.get_height() * 3))
            
            # debug placeable objects
            if self.debugPlaceableObjects:
                for currentObject in self.GUI.objects:
                    if currentObject.info.placed:
                        # get the tiles that fall within the currentObject's rect
                        placedObjectTiles = self.tileMap.getTilesInRect(currentObject.info.rect)
                        for tile in placedObjectTiles:
                            pygame.draw.rect(self.screen, (255, 255, 255), tile.rect, 2)
                        

                # draw a red square over the front tiles of the placeable objects
                for currentObject in self.GUI.objects:
                    if currentObject.info.placed:
                        for frontTileID in currentObject.getFrontTiles():
                            frontTile = self.tileMap.getTileByID(frontTileID)
                            pygame.draw.rect(self.screen, (255, 0, 0), frontTile.rect, 2)

                # draw a green square over the main tiles of the placeable objects
                for currentObject in self.GUI.objects:
                    if currentObject.info.placed:
                        mainTile = self.tileMap.getTileByID(currentObject.info.mainTileID)
                        pygame.draw.rect(self.screen, (0, 255, 0), mainTile.rect, 2)

        pygame.display.update()

    def run(self):
        while Game.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

        # exit pygame gracefully
        pygame.quit()
