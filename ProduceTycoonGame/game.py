import pygame

# local imports
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.guest import Guest
from ProduceTycoonGame.UserInterface.button import Button

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

        self.guests: list[Guest] = []
        self.guests.append(Guest(self.screen, Vector(WIDTH/2, HEIGHT/2)))

        self.button = Button(self.screen, Vector(100, 100), self.tileMap)

    def events(self):
        mouseClicked = False
        zeroClicked = False
        for event in pygame.event.get():
            # will stop running and exit
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseClicked = True

        
        self.tileMap.events(mouseClicked)
        self.button.events(mouseClicked)

        # set target for guests (this is just for testing, not final implementation)
        if mouseClicked:
            for guest in self.guests:
                guest.setTarget(self.tileMap.selectedTile)

        
        for guest in self.guests:
            guest.events()

    def update(self):
        self.tileMap.update()

        for guest in self.guests:
            guest.update()

        self.button.update()
        
        pygame.display.set_caption('Produce Tycoon - ' + str(int(self.clock.get_fps())) + ' FPS')

    def draw(self):
        self.screen.fill((0, 0, 0))

        # drawing tileMap
        self.tileMap.draw()

        # drawing charachters
        for guest in self.guests:
            guest.draw()
        
        self.button.draw()

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