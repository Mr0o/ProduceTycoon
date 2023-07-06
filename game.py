import pygame
import random
import numpy as np

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

        self.rows, self.col = (20, 20)
        self.background_starting_pos = -2000
        self.background_grid = []

        #for i in range(self.rows):
            #self.background_grid.append(())
        for j in range(self.col):
            self.background_grid.append((0, 0))
        self.mat_vals = np.vstack(self.background_grid)

        #Background(self.screen, self.background_starting_pos - 20 * i,self.background_starting_pos - 20 * i

        self.guests: list[Guest] = []
        self.guests.append(Guest(self.screen, WIDTH/2, HEIGHT/2))

    def events(self):
        for event in pygame.event.get():
            # will stop running and exit
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        for i in range(self.rows):
            for j in range(self.col):
                self.background_grid[i][j].events()
        for guest in self.guests:
            guest.events()

    def update(self):

        #for i in range(self.rows):
        #    for j in range(self.col):    
        #        self.background_grid[i][j].update()
        for guest in self.guests:
            guest.update()

    def draw(self):
        self.screen.fill((0, 0, 0))

        # drawling background
        for i in range(self.rows):
            for j in range(self.col):
                self.background_grid[i][j].draw()
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
