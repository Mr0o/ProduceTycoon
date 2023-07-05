import pygame

# local imports
from character import Character

# this is the main game loop (events, update, draw)
class Game:
    def __init__(self):
        pygame.init()

        WIDTH = 800
        HEIGHT = 600

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Produce Tycoon')

        self.keys = []
        self.background_x = -1000
        self.background_y = -1000
        self.display_scroll = [0, 0]
        self.background_height = 2001
        self.background_width = 2001
        self.background_box = pygame.Rect((self.background_x, self.background_y), (self.background_width, self.background_height))

        self.character = Character(self.screen, WIDTH/2, HEIGHT/2)

    def events(self):
        for event in pygame.event.get():
            # will stop running and exit
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        self.keys = pygame.key.get_pressed()
        # Each key moves the background the oposite direction as we want our character to move.
        # Scroll left
        if self.keys[pygame.K_a]:
            self.display_scroll[0] -= 20
            self.character.x -= 20
        # Scroll right
        if self.keys[pygame.K_d]:
            self.display_scroll[0] += 20
            self.character.x += 20
        # Scroll down
        if self.keys[pygame.K_w]:
            self.display_scroll[1] -= 20
            self.character.y -= 20
        # Scroll Up
        if self.keys[pygame.K_s]:
            self.display_scroll[1] += 20
            self.character.y += 20
        
        # redrawling background image and border
        self.background_box = pygame.Rect((self.background_x - self.display_scroll[0], self.background_y - self.display_scroll[1]), (self.background_width, self.background_height))
        self.character.events()

        # updating character position
        self.character.rect = pygame.Rect((self.character.x - self.display_scroll[0], self.character.y - self.display_scroll[1]), (self.character.width, self.character.height))

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0,0,0))

        # Creating a background and a border
        pygame.draw.rect(self.screen, (0, 255, 0), self.background_box)
        pygame.draw.rect(self.screen, (255, 0, 0), self.background_box, 2)

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

        # draw help text
        text = font.render("Press SPACE to change background color", True, (0, 0, 0))
        self.screen.blit(text, (0, 150))
        
        # draw position (x, y)
        text = font.render("(" + str(self.background_box.x) + ", " + str(self.background_box.y) + ")", True, (0, 0, 0))
        self.screen.blit(text, (0, 180))

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
