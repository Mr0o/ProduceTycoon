from random import randint
import pygame

# local imports
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.objectRegister import ObjectRegister
from ProduceTycoonGame.UserInterface.clock import Clock
from ProduceTycoonGame.UserInterface.shopMenu import ShopMenu
from ProduceTycoonGame.pathfinding import Pathfinder
from ProduceTycoonGame.valueHandler import ValueHandler
from ProduceTycoonGame.events import postEvent, clearEventList, eventOccured, Event

# this is the main game loop (events, update, draw)
class Game():
    def __init__(self, WIDTH: int = 800, HEIGHT: int = 600):
        pygame.init()
        #random.seed(100)

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.running = True
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
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

        self.tileMap = TileMap(self.screen, Vector(0, 0))

        # pathfinding (Vector Fields)
        self.pathfinder = Pathfinder(self.tileMap)

        self.playerValues = ValueHandler.getStaticValues()

        # buttons
        self.buttons = []
        self.button4x4 = Button(Vector(0, 0), "4x4 Tile", 60, 20)
        self.buttons.append(self.button4x4)
        self.button1x1 = Button(Vector(60, 0), "1x1 Tile", 60, 20)
        self.buttons.append(self.button1x1)
        self.moveObjects = Button(Vector(120, 0), "Move Objects", 120, 20)
        self.buttons.append(self.moveObjects)
        self.buttonShop = Button(Vector(240, 0), "Shop", 60, 20)
        self.buttons.append(self.buttonShop)

        # placed objects
        self.objects: list[ObjectRegister] = []

        self.guests: list[Guest] = []

        self.displayClock = Clock(self.clock, self.screen, Vector(WIDTH - 100, 0))

        self.shopMenu = ShopMenu(self.screen, Vector(WIDTH / 4, HEIGHT / 4), WIDTH / 2, HEIGHT / 2, self.playerValues)

        self.hideGUI = False
        self.moveObject = False

        self.elements = []
        Button.setScreen(self.screen)

    def events(self):
        for event in pygame.event.get():
            # will stop running and exit
            if event.type == pygame.QUIT:
                postEvent(Event("quit"))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    postEvent(Event("quit"))
                # press '1' to toggle debug
                if event.key == pygame.K_1:
                    self.debug = not self.debug
                # press '2' to toggle debugPlaceableObjects
                if event.key == pygame.K_2:
                    self.debugPlaceableObjects = not self.debugPlaceableObjects
                if event.key == pygame.K_BACKSPACE:
                    postEvent(Event("backspace_pressed"))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    postEvent(Event("left_mouse_clicked"))
                if event.button == 3:
                    postEvent(Event("right_mouse_clicked"))

        if len(self.objects):
            self.hideGUI = not self.objects[len(self.objects) - 1].info.placed
        else:
            self.hideGUI = False

        self.tileMap.events()

        ObjectRegister.setElementRectangles(self.elements)

        if not self.hideGUI:
            if self.button4x4.events():
                ObjectRegister(self.screen, Vector(0, 0), 4, 4, self.tileMap.tileSize)
            if self.button1x1.events():
                ObjectRegister(self.screen, Vector(0, 0), 1, 1, self.tileMap.tileSize)
            if self.moveObjects.events():
                self.hideGUI = True
                self.moveObject = True
            if self.buttonShop.events():
                self.hideGUI = True
                self.shopMenu.hidden = False

        self.objects = ObjectRegister.objects

        self.setHiddenUI()

        objectPlaced = False

        for currentObject in self.objects:
            currentObject.events()

            if not currentObject.info.placed:
                Exit = currentObject.info.objectGUI.exitButton.events()
                if Exit:
                    self.objects.remove(currentObject)
                continue

            self.elements.append(currentObject.rectangle)
            #if self.moveObject:
            #    if eventOccured("left_mouse_clicked"):
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
        if eventOccured("right_mouse_clicked") and len(self.objects):
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

        self.shopMenu.events()
        self.elements = []

        # check for quit event
        if eventOccured("quit"):
            self.running = False

        # clear the eventList every frame
        clearEventList()

    # set every element's hidden variable to the value of self.hideGUI
    def setHiddenUI(self):
        for button in self.buttons:
            self.elements.append(button.rect)
            button.hidden = self.hideGUI

        self.displayClock.hidden = self.hideGUI
        self.elements.append(self.displayClock.rect)

    def update(self):
        self.tileMap.update(self.objects)

        for guest in self.guests:
            guest.update()

        # pathfinder update will check for any changes and update the vector fields
        self.pathfinder.update()

        self.shopMenu.update()
        
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

        self.shopMenu.draw()

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

            # draw the highlighted tile id
            if self.tileMap.highlightedTile is not None:
                text = self.debugFont.render("Tile ID: " + str(self.tileMap.highlightedTile.id), True, (255, 255, 0))
                self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, 0))

            # draw the selected tile id
            if self.tileMap.selectedTile is not None:
                text = self.debugFont.render("Selected ID: " + str(self.tileMap.selectedTile.id), True, (255, 0, 255))
                self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, text.get_height()))

            # draw the size of the pathfinder vector fields list
            text = self.debugFont.render("Vector Fields: " + str(len(self.pathfinder.vectorFields)), True, (255, 255, 255))
            self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, text.get_height() * 2))
            
            # debug placeable objects
            if self.debugPlaceableObjects:
                for currentObject in self.objects:
                        if currentObject.info.placed:
                            # get the tiles that fall within the currentObject's rect
                            placedObjectTiles = self.tileMap.getTilesInRect(currentObject.createRectangle())
                            for tile in placedObjectTiles:
                                pygame.draw.rect(self.screen, (255, 255, 255), tile.rect, 2)
                        

                # draw a red square over the front tiles of the placeable objects
                for currentObject in self.objects:
                        if currentObject.info.placed:
                            for frontTileID in currentObject.getFrontTiles():
                                frontTile = self.tileMap.getTileByID(frontTileID)
                                pygame.draw.rect(self.screen, (255, 0, 0), frontTile.rect, 2)

                # draw a green square over the main tiles of the placeable objects
                for currentObject in self.objects:
                        if currentObject.info.placed:
                            mainTile = self.tileMap.getTileByID(currentObject.mainTileID)
                            pygame.draw.rect(self.screen, (0, 255, 0), mainTile.rect, 2)

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

        # exit pygame gracefully
        pygame.quit()