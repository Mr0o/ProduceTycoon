from random import randint
import pygame

# local imports
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.objectRegister import ObjectRegister
from ProduceTycoonGame.UserInterface.clock import Clock
from ProduceTycoonGame.pathfinding import Pathfinder
from ProduceTycoonGame.valueHandler import ValueHandler

# Helper Functions
def createObject(screen: pygame.Surface, pos: Vector, width: int, height: int, tileSize: int):
    return ObjectRegister(screen, pos, width, height, tileSize)

# this is the main game loop (events, update, draw)
class Game():
    def __init__(self, WIDTH: int = 800, HEIGHT: int = 600):
        pygame.init()
        #random.seed(100)

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        TileMap.setScreen(self.screen)
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Produce Tycoon')

        # set the game icon
        icon = pygame.image.load('./Resources/Images/Tomato.png')
        pygame.display.set_icon(icon)

        # load font
        self.debugFont = pygame.font.SysFont('Arial', 15, bold=True)

        # debug variable that when true will enable debug features (fps, frametime, etc.)
        self.debug = False

        # debug variable that when true will draw the tiles that make up each currentObject (this could impact performance, therefore it is disabled by default)
        self.debugPlaceableObjects = False

        self.tileMap = TileMap(Vector(0, 0))

        # pathfinding (Vector Fields)
        self.pathfinder = Pathfinder(self.tileMap)

        self.playerValues = ValueHandler.getStaticValues()

        # buttons
        object4x4Args = (self.screen, Vector(0, 0), 4, 4, self.tileMap.info.tileSize)
        object1x1Args = (self.screen, Vector(0, 0), 1, 1, self.tileMap.info.tileSize)
        self.buttons = []
        Button.setScreen(self.screen)
        self.button4x4 = Button(Vector(0, 0), "4x4 Tile", 60, 20, lambda: createObject(*object4x4Args))
        self.buttons.append(self.button4x4)
        self.button1x1 = Button(Vector(60, 0), "1x1 Tile", 60, 20, lambda: createObject(*object1x1Args))
        self.buttons.append(self.button1x1)
        #self.moveObjects = Button(Vector(120, 0), "Move Objects", 120, 20)
        #self.buttonShop = Button(Vector(240, 0), "Shop", 60, 20)

        # placed objects
        self.objects: list[ObjectRegister] = []

        self.guests: list[Guest] = []

        self.displayClock = Clock(self.clock, self.screen, Vector(WIDTH - 100, 0))

        #self.shopMenu = ShopMenu(self.screen, Vector(WIDTH / 4, HEIGHT / 4), WIDTH / 2, HEIGHT / 2, self.playerValues)

        self.hideGUI = False
        self.mouseClicked = False
        self.backspacePressed = False
        self.previousMouseClicked = False
        self.moveObject = False

        self.elements = []

    def events(self):
        self.previousMouseClicked = self.mouseClicked
        self.mouseClicked = False
        self.rightMouseClicked = False
        #currency = self.shopMenu.getCurrency()

        if len(self.objects):
            self.hideGUI = not self.objects[len(self.objects) - 1].info.placed
        else:
            self.hideGUI = False

        events = []
        for event in pygame.event.get():
            events.append(event)
            # will stop running and exit
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # press '1' to toggle debug
                if event.key == pygame.K_1:
                    self.debug = not self.debug
                # press '2' to toggle debugPlaceableObjects
                if event.key == pygame.K_2:
                    self.debugPlaceableObjects = not self.debugPlaceableObjects
                if event.key == pygame.K_BACKSPACE:
                    self.backspacePressed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouseClicked = True
                if event.button == 3:
                    self.rightMouseClicked = True

        
        self.tileMap.events(self.mouseClicked)

        ObjectRegister.setElementRectangles(self.elements)

        if not self.hideGUI:
            for button in self.buttons:
                button.events(self.mouseClicked)
            #if self.moveObjects.events(self.mouseClicked):
            #    self.hideGUI = True
            #    self.moveObject = True
            #if self.buttonShop.events(self.mouseClicked):
            #    self.hideGUI = True
            #    self.shopMenu.hidden = False

        self.objects = ObjectRegister.objects

        self.setHiddenUI()

        objectPlaced = False

        for currentObject in self.objects:
            currentObject.events(self.previousMouseClicked, self.mouseClicked, events)

            #if not currentObject.info.placed:
                #Exit = currentObject.info.objectGUI.exitButton.events(self.mouseClicked)
                #if Exit:
                #    self.objects.remove(currentObject)
                #continue

            self.elements.append(currentObject.rectangle)
            #if self.moveObject:
            #    if self.mouseClicked and self.previousMouseClicked:
            #        self.moveObject = currentObject.moveToNewPos()
            
            # do some stuff when the object is placed (only once on the frame the object is placed)
            if currentObject.info.hasPlaced:
                currentObject.info.hasPlaced = False
                
                # set the currentObject's mainTile to changed (important for detecting changes in the tileMap)
                placedTileID = currentObject.mainTileID
                placedTile = self.tileMap.getTileByID(placedTileID)

                if placedTile is not None:
                    placedTile.changed = True
                    
                    objectPlaced = True

        if objectPlaced:
            # get the tiles that fall within the currentObject's rect
            placedObjectTiles = self.tileMap.getTilesInRect(self.objects[len(self.objects) - 1].rectangle)

            # remove the main tile from the list
            for tile in placedObjectTiles:
                if tile.id == self.objects[len(self.objects) - 1].mainTileID:
                    placedObjectTiles.remove(tile)
                    break
        
            self.pathfinder.update()

        # place guests down on mouse click (testing, remove this later)
        if self.rightMouseClicked and len(self.objects):
            # pick a random currentObject
            randomIndex = randint(0, len(self.objects) - 1)
            
            mousePos = pygame.mouse.get_pos()
            newGuest = Guest(self.screen, Vector(mousePos[0], mousePos[1]))
            targetTileID = self.objects[randomIndex].getFrontTiles()[0]
            newGuest.targetTile = self.tileMap.getTileByID(targetTileID)

            # make sure the guest is not None
            if newGuest.targetTile is not None:
                self.guests.append(newGuest)
        
        for guest in self.guests:
            self.elements.append(guest.rect)
            # guest events
            guest.events()

            # apply vector field of the current tile in the vector field list
            if guest.targetTile is not None:
                currentTile = self.tileMap.getTileByPos(guest.pos)
                force = self.pathfinder.getVector(currentTile, guest.targetTile)
                guest.applyForce(force)
            

            guest.update()

        self.displayClock.events()

        #self.shopMenu.events(self.mouseClicked)
        self.elements = []

    # set every element's hidden variable to the value of self.hideGUI
    def setHiddenUI(self):
        for button in self.buttons:
            self.elements.append(button.rect)
            button.active = self.hideGUI

        self.displayClock.hidden = self.hideGUI
        self.elements.append(self.displayClock.rect)

    def update(self):
        for guest in self.guests:
            guest.update()

        # pathfinder update will check for any changes and update the vector fields
        self.pathfinder.update()

        #self.shopMenu.update()
        
        if self.debug:
            pygame.display.set_caption('Produce Tycoon - ' + str(int(self.clock.get_fps())) + ' FPS')
        else:
            pygame.display.set_caption('Produce Tycoon')

    def draw(self):
        self.screen.fill((0, 0, 0))

        # drawing tileMap
        self.tileMap.draw()

        # if we are placing an object, draw the tile lines
        if len(self.objects) and not self.objects[len(self.objects) - 1].info.placed:
            self.tileMap.drawTileLines()

        for button in self.buttons:
            button.draw()

        for currentObject in self.objects:
            currentObject.draw()

        # drawing charachters
        for guest in self.guests:
            guest.draw()

        self.displayClock.draw()

        #self.shopMenu.draw()

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

            ## draw the highlighted tile id
            #if self.tileMap.highlightedTile is not None:
            #    text = self.debugFont.render("Tile ID: " + str(self.tileMap.highlightedTile.id), True, (255, 255, #0))
            #    self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, 0))
            #
            ## draw the selected tile id
            #if self.tileMap.selectedTile is not None:
            #    text = self.debugFont.render("Selected ID: " + str(self.tileMap.selectedTile.id), True, (255, 0, #255))
            #    self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, text.get_height()))

            # draw the size of the pathfinder vector fields list
            text = self.debugFont.render("Vector Fields: " + str(len(self.pathfinder.vectorFields)), True, (255, 255, 255))
            self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, text.get_height() * 2))
            
            # debug placeable objects
            if self.debugPlaceableObjects:
                for currentObject in self.objects:
                    if currentObject.placed:
                        # get the tiles that fall within the currentObject's rect
                        placedObjectTiles = self.tileMap.getTilesInRect(currentObject.rect)
                        for tile in placedObjectTiles:
                            pygame.draw.rect(self.screen, (255, 255, 255), tile.rect, 2)
                        

                # draw a red square over the front tiles of the placeable objects
                for currentObject in self.objects:
                    if currentObject.placed:
                        for frontTileID in currentObject.frontTileIDs:
                            frontTile = self.tileMap.getTileByID(frontTileID)
                            pygame.draw.rect(self.screen, (255, 0, 0), frontTile.rect, 2)

                # draw a green square over the main tiles of the placeable objects
                for currentObject in self.objects:
                    if currentObject.placed:
                        mainTile = self.tileMap.getTileByID(currentObject.mainTileID)
                        pygame.draw.rect(self.screen, (0, 255, 0), mainTile.rect, 2)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

        # exit pygame gracefully
        pygame.quit()

# Code that shouldgo in here
#def getMainTile(self, tile: Tile, currentObject: Object):
#        ifTileCollidesWithRect = tile.info.rect.colliderect(currentObject.rectangle)
#        ifObjectIsPlaced = currentObject.info.placed
#        if ifTileCollidesWithRect and currentObject.mainTileID == -1 and ifObjectIsPlaced:
#            currentObject.setMainTileID(tile.id)
#def changeTileType(self, tile: Tile, currentObject: Object):
#    if currentObject.info.placed and tile.info.rect.colliderect(currentObject.rectangle):
#        if tile.info.typeTile == Type.WALKABLE:
#            tile.info.typeTile = Type.BOUNDARY
#if currentObjects is not None:
#    for currentObject in currentObjects:
#        for tile in self.tileMapGrid:  
#            self.getMainTile(tile, currentObject)
#            self.changeTileType(tile, currentObject)
