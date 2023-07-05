import pygame
import random

# local imports
from background import Background
from guest import Guest

# this is the main game loop (events, update, draw)
class Game:
    def __init__(self, WIDTH: int = 800, HEIGHT: int = 600):
        pygame.init()
        #random.seed(100)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Produce Tycoon')

        self.background = Background(self.screen, -1000,-1000)

        self.guests: list[Guest] = []
        self.guests.append(Guest(self.screen, WIDTH/2, HEIGHT/2, self.background.background_box))

    def events(self):
        for event in pygame.event.get():
            # will stop running and exit
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        self.background.events()
        for guest in self.guests:
            guest.events()

    def update(self):
        self.background.update()
        for guest in self.guests:
            guest.update()

    def draw(self):
        self.screen.fill((120,120,120))

        # drawling background
        self.background.draw()
        # drawling charachters
        for guest in self.guests:
            guest.draw()

        # load font
        font = pygame.font.SysFont('Arial', 30)

        # draw text
        text = font.render('Hello World', True, (0, 0, 0))
        self.screen.blit(text, (0, 0))

        # draw fps
        text = font.render("FPS: " + str(int(self.clock.get_fps())), True, (0, 0, 0))
        self.screen.blit(text, (0, 30))

        # draw position text
        text = font.render("Pos", True, (0, 0, 0))
        self.screen.blit(text, (0, 150))
        
        # draw position (x, y)
        text = font.render("(" + str(self.guests[0].x) + ", " + str(self.guests[0].y) + ")", True, (0, 0, 0))
        self.screen.blit(text, (0, 180))

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
