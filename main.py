import pygame
import sys
from random import randint

pygame.init()

class Character:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 20
        self.height = 45
        self.animation_images = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (120, 120, 120)]
        self.animation_count = 0
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
    def events(self):
        if (self.animation_count >= 15):
            self.animation_count = 0
        self.animation_count += 1

        #pygame.draw.rect(self.screen, self.animation_images[self.animation_count//4][0], pygame.transform.scale((self.character_rect), (self.width * self.animation_images[self.animation_count//4][1], self.height * self.animation_images[self.animation_count//4][1])))
    def draw(self):
        pygame.draw.rect(self.screen, self.animation_images[self.animation_count//4], self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
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

        self.character = Character(self.screen, 0, 0)

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


if __name__ == '__main__':
    game = Game()
    game.run()