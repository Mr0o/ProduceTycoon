import pygame

# local imports
from character import Character

# this is the main game loop (events, update, draw)
class Game:
    def __init__(self, WIDTH: int = 800, HEIGHT: int = 600):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Produce Tycoon')

        self.character = Character(self.screen, WIDTH/2, HEIGHT/2)

    def events(self):
        for event in pygame.event.get():
            # will stop running and exit
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.character.update()

    def draw(self):
        self.screen.fill((100,100,100))

        # drawling charachters
        self.character.draw()

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
        text = font.render("(" + str(self.character.x) + ", " + str(self.character.y) + ")", True, (0, 0, 0))
        self.screen.blit(text, (0, 180))

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
