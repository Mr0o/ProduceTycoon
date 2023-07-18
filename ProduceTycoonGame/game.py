import pygame

# local imports
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.placableObject import PlacableObject
from ProduceTycoonGame.clock import Clock

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

        # load font
        self.debugFont = pygame.font.SysFont('Arial', 15, bold=True)

        self.tileMap = TileMap(self.screen, Vector(0, 0))

        # buttons
        self.buttons = []
        self.button3x3 = Button(self.screen, Vector(100, 100), "3x3 Tile", 60, 20)
        self.buttons.append(self.button3x3)
        self.button1x1 = Button(self.screen, Vector(100, 123), "1x1 Tile", 60, 20)
        self.buttons.append(self.button1x1)
        self.movePlacableObjects = Button(self.screen, Vector(100, 146), "Move Objects", 60, 20)
        self.buttons.append(self.movePlacableObjects)

        # placed objects
        self.placedObjects: list[PlacableObject] = []

        self.guests: list[Guest] = []
        self.guests.append(Guest(self.screen, Vector(WIDTH/2, HEIGHT/2)))

        self.displayClock = Clock(self.clock, self.screen, Vector(WIDTH - 100, 0))

        self.hideGUI = False
        self.mouseClicked = False
        self.previousMouseClicked = False

    def events(self):
        self.previousMouseClicked = self.mouseClicked
        self.mouseClicked = False
        
        for event in pygame.event.get():
            # will stop running and exit
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouseClicked = True

        
        self.tileMap.events(self.mouseClicked)
        if not self.hideGUI:
            if self.button3x3.events(self.mouseClicked):
                self.placedObjects.append(PlacableObject(self.screen, Vector(0, 0), self.tileMap, 60, 60, 3, 3, self.elements))
            if self.button1x1.events(self.mouseClicked):
                self.placedObjects.append(PlacableObject(self.screen, Vector(0, 0), self.tileMap, 20, 20, 1, 1, self.elements))
            if self.movePlacableObjects.events(self.mouseClicked):
                self.hideGUI = True
                for placedObject in self.placedObjects:
                    placedObject.moveToNewPos()
                    print(placedObject.isPlaced)
            
        for button in self.buttons:
            if self.hideGUI:
                button.hide = True
            else:
                button.hide = False

        for placedObject in self.placedObjects:
            placedObject.events(self.mouseClicked, self.previousMouseClicked)

            self.hideGUI = not placedObject.isPlaced

        # set target for guests (this is just for testing, not final implementation)
        # if self.mouseClicked:
        #     for guest in self.guests:
        #         pass
        
        for guest in self.guests:
            guest.events()

        self.displayClock.events()

        self.elements = []
        self.elements.extend(self.buttons)
        self.elements.extend(self.placedObjects)
        self.elements.extend(self.guests)
        self.elements.append(self.displayClock)

    def update(self):
        self.tileMap.update()

        for guest in self.guests:
            guest.update()

        for placedObject in self.placedObjects:
            placedObject.update()
        
        pygame.display.set_caption('Produce Tycoon - ' + str(int(self.clock.get_fps())) + ' FPS')

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

        if not self.hideGUI:
            self.displayClock.draw()

        ## DEBUG STUFF ##
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
        self.screen.blit(text, (0, 0))

        # draw fps
        text = self.debugFont.render(str(int(self.clock.get_fps())) + " FPS ", True, (255, 255, 255))
        self.screen.blit(text, (0, text.get_height()))

        # draw the highlighted tile id
        if self.tileMap.highlightedTile is not None:
            text = self.debugFont.render("Tile ID: " + str(self.tileMap.highlightedTile.id), True, (255, 255, 0))
            self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, 0))

        # draw the selected tile id
        if self.tileMap.selectedTile is not None:
            text = self.debugFont.render("Selected ID: " + str(self.tileMap.selectedTile.id), True, (255, 0, 255))
            self.screen.blit(text, (self.WIDTH/2 - text.get_width()/2, text.get_height()))

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

        # exit pygame gracefully
        pygame.quit()