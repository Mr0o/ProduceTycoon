from random import randint
import pygame
from ProduceTycoonGame.UserInterface.messageBox import MessageBox

# local imports
from ProduceTycoonGame.events import postEvent, eventOccured, getEvent, clearEventList
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, Tile, Type, updateTileMap
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.objectRegister import ObjectRegister
from ProduceTycoonGame.UserInterface.clock import Clock
from ProduceTycoonGame.pathfinding import Pathfinder
from ProduceTycoonGame.UserInterface.shopMenu import ShopMenu
from ProduceTycoonGame.produce import Produce
from ProduceTycoonGame.playerData import PlayerData
from ProduceTycoonGame.UserInterface.text import Text

# Helper Functions
def createObject(screen: pygame.Surface, pos: Vector, width: int, height: int, tileSize: int):
    return ObjectRegister(screen, pos, width, height, tileSize)

def loadGame():
    Produce.load()

def saveGame():
    Produce.save()

# this is the main game loop (events, update, draw)
class Game():
    def __init__(self, WIDTH: int = 800, HEIGHT: int = 600):
        pygame.init()

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Produce Tycoon')

        loadGame()

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
        ShopMenu.setScreen(self.screen)
        Button.setScreen(self.screen)
        TileMap.setScreen(self.screen)
        
        self.tileMap = TileMap(Vector(0, 0))

        # pathfinding (Vector Fields)
        self.pathfinder = Pathfinder(self.tileMap)


        # buttons
        object4x4Args = (self.screen, Vector(0, 0), 4, 4, self.tileMap.tileSize)
        object1x1Args = (self.screen, Vector(0, 0), 1, 1, self.tileMap.tileSize)
        self.buttons = []
        self.button4x4 = Button(Vector(0, 0), "4x4 Tile", 60, 20, lambda: createObject(*object4x4Args))
        self.buttons.append(self.button4x4)
        self.button1x1 = Button(Vector(60, 0), "1x1 Tile", 60, 20, lambda: createObject(*object1x1Args))
        self.buttons.append(self.button1x1)
        #self.moveObjects = Button(Vector(120, 0), "Move Objects", 120, 20)
        self.shopMenu = ShopMenu(Vector(WIDTH / 4, HEIGHT / 4), WIDTH / 2, HEIGHT / 2)
        self.openShop = Button(Vector(240, 0), "Shop", 60, 20, self.shopMenu.openGUI)
        self.buttons.append(self.openShop)

        # placed objects
        self.objects: list[ObjectRegister] = []

        self.guests: list[Guest] = []

        self.displayClock = Clock(self.clock, self.screen, Vector(WIDTH - 100, 0))

        #self.shopMenu = ShopMenu(self.screen, Vector(WIDTH / 4, HEIGHT / 4), WIDTH / 2, HEIGHT / 2, self.playerValues)

        self.hideGUI = False
        self.moveObject = False

        self.elements = []

        # money box
        moneyBoxWidth = 40
        moneyBoxHeight = 20
        moneyBoxX = 0
        moneyBoxY = self.HEIGHT - moneyBoxHeight
        self.moneyBox = pygame.Rect((moneyBoxX, moneyBoxY), (moneyBoxWidth, moneyBoxHeight))

        self.textRenderer = Text(ShopMenu.screen, Vector(moneyBoxX, moneyBoxY), moneyBoxWidth, moneyBoxHeight, str(PlayerData.money))

        # message box instance
        self.messageBox = MessageBox(self.screen)

    def events(self):
        clearEventList()

        for event in pygame.event.get():
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

                # press space to toggle a test message
                if event.key == pygame.K_SPACE:
                    postEvent("postMessage", eventData="This is a test message!")

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

        
        if len(self.objects):
            self.hideGUI = not self.objects[len(self.objects) - 1].info.placed
        else:
            self.hideGUI = False

        self.messageBox.events()

        ObjectRegister.setElementRectangles(self.elements)

        if not self.hideGUI:
            for button in self.buttons:
                button.events()

        self.objects = ObjectRegister.objects

        self.setHiddenUI()

        objectPlaced = False

        for currentObject in self.objects:
            currentObject.events()

            #if not currentObject.info.placed:
                #Exit = currentObject.info.objectGUI.exitButton.events(eventOccured("leftMouseDown"))
                #if Exit:
                #    self.objects.remove(currentObject)
                #continue

            self.elements.append(currentObject.info.rect)
            #if self.moveObject:
            #    if eventOccured("leftMouseDown") and self.previousMouseClicked:
            #        self.moveObject = currentObject.moveToNewPos()
            
            # do some stuff when the object is placed (only once on the frame the object is placed)
            if currentObject.info.hasPlaced:
                currentObject.info.hasPlaced = False
                
                # set the currentObject's mainTile to changed (important for detecting changes in the tileMap)
                placedTileID = currentObject.info.mainTileID
                placedTile = self.tileMap.getTileByID(placedTileID)

                if placedTile is not None:
                    placedTile.changed = True
                    
                    objectPlaced = True

        if objectPlaced:
            # get the tiles that fall within the currentObject's rect
            placedObjectTiles = self.tileMap.getTilesInRect(self.objects[len(self.objects) - 1].info.rect)

            # remove the main tile from the list
            for tile in placedObjectTiles:
                if tile.id == self.objects[len(self.objects) - 1].info.mainTileID:
                    placedObjectTiles.remove(tile)
                    break
        
            self.pathfinder.update()

        # place guests down on mouse click (testing, remove this later)
        if eventOccured("rightMouseDown") and len(self.objects):
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

        Button.HAS_CLICKED = False

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
        
        if len(self.objects) > 0:
            updateTileMap(self.tileMap, self.objects)

        # pathfinder update will check for any changes and update the vector fields
        self.pathfinder.update()

        #self.shopMenu.update()
        
        if self.debug:
            pygame.display.set_caption('Produce Tycoon - ' + str(int(self.clock.get_fps())) + ' FPS')
        else:
            pygame.display.set_caption('Produce Tycoon')

    def displayMoney(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.moneyBox)
        pygame.draw.rect(self.screen, (0, 0, 0), self.moneyBox, 2)
        self.textRenderer.setText(str(PlayerData.money))
        self.textRenderer.draw() 

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
        self.displayMoney()

        self.shopMenu.draw()

        self.messageBox.draw()

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
                    if currentObject.info.placed:
                        # get the tiles that fall within the currentObject's rect
                        placedObjectTiles = self.tileMap.getTilesInRect(currentObject.info.rect)
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
                        mainTile = self.tileMap.getTileByID(currentObject.info.mainTileID)
                        pygame.draw.rect(self.screen, (0, 255, 0), mainTile.rect, 2)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
        
        saveGame()

        # exit pygame gracefully
        pygame.quit()
