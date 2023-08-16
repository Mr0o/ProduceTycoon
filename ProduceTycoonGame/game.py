import pygame

# local imports
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.placableObject import PlacableObject
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

        self.tileMap = TileMap(self.screen, Vector(0, 0))
        self.size = self.tileMap.tileMapGrid[0].size

        # pathfinding (Vector Fields)
        self.pathfinder = Pathfinder(self.tileMap)

        # buttons
        self.buttons = []
        self.button3x3 = Button(self.screen, Vector(0, 0), "3x3 Tile", 60, 20)
        self.buttons.append(self.button3x3)
        self.button1x1 = Button(self.screen, Vector(60, 0), "1x1 Tile", 60, 20)
        self.buttons.append(self.button1x1)
        self.movePlacableObjects = Button(self.screen, Vector(120, 0), "Move Objects", 120, 20)
        self.buttons.append(self.movePlacableObjects)
        self.buttonShop = Button(self.screen, Vector(240, 0), "Shop", 60, 20)
        self.buttons.append(self.buttonShop)

        # placed objects
        self.placedObjects: list[PlacableObject] = []

        self.guests: list[Guest] = []
        self.guests.append(Guest(self.screen, Vector(WIDTH/2, HEIGHT/2)))

        self.displayClock = Clock(self.clock, self.screen, Vector(WIDTH - 100, 0))

        self.shopMenu = ShopMenu(self.screen, Vector(WIDTH / 4, HEIGHT / 4), WIDTH / 2, HEIGHT / 2)

        self.hideGUI = False
        self.mouseClicked = False
        self.backspacePressed = False
        self.previousMouseClicked = False
        self.moveObject = False

    def events(self):
        self.previousMouseClicked = self.mouseClicked
        self.mouseClicked = False
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

        
        self.tileMap.events(self.mouseClicked)

        if not self.hideGUI:
            if self.button3x3.events(self.mouseClicked):
                self.placedObjects.append(PlacableObject(self.screen, Vector(0, 0), self.size, 4, 4, self.elements, './Resources/Images/WatermelonBin.png'))
            if self.button1x1.events(self.mouseClicked):
                self.placedObjects.append(PlacableObject(self.screen, Vector(0, 0), self.size, 1, 1, self.elements, './Resources/Images/Tomato.png'))
            if self.movePlacableObjects.events(self.mouseClicked):
                self.hideGUI = True
                self.moveObject = True
            if self.buttonShop.events(self.mouseClicked):
                self.hideGUI = True
                self.shopMenu.hidden = False
            
        self.checkIfHidden()

        for placedObject in self.placedObjects:
            self.hideGUI = placedObject.events(self.previousMouseClicked, self.mouseClicked, events)
            if placedObject.exitButton.events(self.mouseClicked) and not placedObject.isPlaced:
                self.placedObjects.remove(placedObject)

            if self.moveObject and not self.mouseClicked and self.previousMouseClicked:
                self.moveObject = placedObject.moveToNewPos()

        if not self.shopMenu.hidden:
            self.shopMenu.exitButton.events(self.mouseClicked)
        
        for guest in self.guests:
            guest.events()

        self.displayClock.events()

        self.elements = []
        self.elements.extend(self.buttons)
        self.elements.extend(self.placedObjects)
        self.elements.extend(self.guests)
        self.elements.append(self.displayClock)

    def checkIfHidden(self):
        for button in self.buttons:
            button.hidden = self.hideGUI

        self.displayClock.hidden = self.hideGUI


    def update(self):
        self.tileMap.update(self.placedObjects)

        for guest in self.guests:
            guest.update()

        for placedObject in self.placedObjects:
            placedObject.update()

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

        # drawing charachters
        for guest in self.guests:
            guest.draw()
        

        for button in self.buttons:
            button.draw()

        for placedObject in self.placedObjects:
            placedObject.draw()

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

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

        # exit pygame gracefully
        pygame.quit()