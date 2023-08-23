from random import randint
import pygame

# local imports
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.placeableObject import PlaceableObject
from ProduceTycoonGame.UserInterface.clock import Clock
from ProduceTycoonGame.UserInterface.shopMenu import ShopMenu
from ProduceTycoonGame.pathfinding import Pathfinder, VectorField

# this is the main game loop (events, update, draw)
class Game():
    def __init__(self, WIDTH: int = 800, HEIGHT: int = 600):
        pygame.init()
        #random.seed(100)

        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
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

        # player values
        self.playerValues = {
            "currency": 1000,
            "watermelon-amount": 1,
            "watermelon-price": 5,
            "watermelon-sell-price": 5,
            "banana-amount": 1,
            "banana-price": 5,
            "banana-sell-price": 5,
            "apple-amount": 1,
            "apple-price": 5,
            "apple-sell-price": 5,
            "tomato-amount": 1,
            "tomato-price": 5,
            "tomato-sell-price": 5
        }

        self.tileMap = TileMap(self.screen, Vector(0, 0))

        # pathfinding (Vector Fields)
        self.pathfinder = Pathfinder(self.tileMap)

        # buttons
        self.buttons = []
        self.button4x4 = Button(self.screen, Vector(0, 0), "4x4 Tile", 60, 20)
        self.buttons.append(self.button4x4)
        self.button1x1 = Button(self.screen, Vector(60, 0), "1x1 Tile", 60, 20)
        self.buttons.append(self.button1x1)
        self.moveplaceableObjects = Button(self.screen, Vector(120, 0), "Move Objects", 120, 20)
        self.buttons.append(self.moveplaceableObjects)
        self.buttonShop = Button(self.screen, Vector(240, 0), "Shop", 60, 20)
        self.buttons.append(self.buttonShop)

        # placed objects
        self.placeableObjects: list[PlaceableObject] = []

        self.guests: list[Guest] = []

        self.displayClock = Clock(self.clock, self.screen, Vector(WIDTH - 100, 0))

        self.shopMenu = ShopMenu(self.screen, Vector(WIDTH / 4, HEIGHT / 4), WIDTH / 2, HEIGHT / 2, self.playerValues)

        self.hideGUI = False
        self.mouseClicked = False
        self.backspacePressed = False
        self.previousMouseClicked = False
        self.moveObject = False

    def events(self):
        self.previousMouseClicked = self.mouseClicked
        self.mouseClicked = False
        self.rightMouseClicked = False
        currency = self.shopMenu.getCurrency()

        if len(self.placeableObjects):
            self.hideGUI = not self.placeableObjects[len(self.placeableObjects) - 1].getPlaced()
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
                if event.key == pygame.K_BACKSPACE:
                    self.backspacePressed = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouseClicked = True
                if event.button == 3:
                    self.rightMouseClicked = True

        
        self.tileMap.events(self.mouseClicked)

        if not self.hideGUI:
            if self.button4x4.events(self.mouseClicked):
                self.placeableObjects.append(PlaceableObject(self.screen, Vector(0, 0), self.tileMap.tileSize, 4, 4, self.elements, './Resources/Images/WatermelonBin.png'))
            if self.button1x1.events(self.mouseClicked):
                self.placeableObjects.append(PlaceableObject(self.screen, Vector(0, 0), self.tileMap.tileSize, 1, 1, self.elements, './Resources/Images/Tomato.png'))
            if self.moveplaceableObjects.events(self.mouseClicked):
                self.hideGUI = True
                self.moveObject = True
            if self.buttonShop.events(self.mouseClicked):
                self.hideGUI = True
                self.shopMenu.hidden = False

        self.setHiddenUI()

        for placeableObject in self.placeableObjects:
            placeableObject.events(self.previousMouseClicked, self.mouseClicked, events)

            placeableObject.setDirection()

            #exitButton = placeableObject.exitButton.events(self.mouseClicked)
            #if exitButton and not placeableObject.isPlaced:
            #    self.placeableObjects.remove(placeableObject)

            if self.moveObject:
                if self.mouseClicked and self.previousMouseClicked:
                    self.moveObject = placeableObject.moveToNewPos()
                # elif exitButton:
                #     self.moveObject = False
            
            # do some stuff when the object is placed (only once on the frame the object is placed)
            if placeableObject.isPlaced and placeableObject.hasPlaced:
                placeableObject.hasPlaced = False
                
                # set the placeableObject's mainTile to changed (important for detecting changes in the tileMap)
                placedTileIDs = placeableObject.mainTileID
                placedTile = self.tileMap.getTileByID(placedTileIDs)

                if placedTile is not None:
                    placedTile.changed = True


        # place guests down on mouse click (testing, remove this later)
        if self.rightMouseClicked and len(self.placeableObjects):
            # pick a random placeableObject
            randomIndex = randint(0, len(self.placeableObjects) - 1)
            
            mousePos = pygame.mouse.get_pos()
            newGuest = Guest(self.screen, Vector(mousePos[0], mousePos[1]))
            targetTileID = self.placeableObjects[randomIndex].frontTileIDs[0]
            newGuest.targetTile = self.tileMap.getTileByID(targetTileID)

            # make sure the guest is not None
            if newGuest.targetTile is not None:
                self.guests.append(newGuest)
        
        for guest in self.guests:
            # guest events
            guest.events()

            # apply vector field of the current tile in the vector field list
            if guest.targetTile is not None:
                currentTile = self.tileMap.getTileByPos(guest.pos)
                force = self.pathfinder.getVector(currentTile, guest.targetTile)
                guest.applyForce(force)
            

            guest.update()

        self.displayClock.events()

        self.shopMenu.events(self.mouseClicked)

        self.elements = []
        self.elements.extend(self.buttons)
        self.elements.extend(self.placeableObjects)
        self.elements.extend(self.guests)
        self.elements.append(self.displayClock)

    # set every element's hidden variable to the value of self.hideGUI
    def setHiddenUI(self):
        for button in self.buttons:
            button.hidden = self.hideGUI

        self.displayClock.hidden = self.hideGUI

    def update(self):
        self.tileMap.update(self.placeableObjects)

        for guest in self.guests:
            guest.update()

        for placeableObject in self.placeableObjects:
            placeableObject.update()

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
        if len(self.placeableObjects) and not self.placeableObjects[len(self.placeableObjects) - 1].getPlaced():
            self.tileMap.drawTileLines()

        for button in self.buttons:
            button.draw()

        for placeableObject in self.placeableObjects:
            placeableObject.draw()

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

            # draw a red square over the front tiles of the placeable objects
            for placeableObject in self.placeableObjects:
                if placeableObject.isPlaced:
                    for frontTileID in placeableObject.frontTileIDs:
                        frontTile = self.tileMap.getTileByID(frontTileID)
                        pygame.draw.rect(self.screen, (255, 0, 0), frontTile.rect, 2)

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

        # exit pygame gracefully
        pygame.quit()