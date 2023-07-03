import pygame
from random import randint

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Game')

        self.background_rgb = (randint(0, 255), randint(0, 255), randint(0, 255))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.background_rgb = (randint(0, 255), randint(0, 255), randint(0, 255))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.background_rgb = (randint(0, 255), randint(0, 255), randint(0, 255))

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.background_rgb)

        # load font
        font = pygame.font.SysFont('Arial', 30)

        # draw text
        text = font.render('Hello World', True, (0, 0, 0))
        self.screen.blit(text, (0, 0))

        # draw fps
        text = font.render("FPS: " + str(int(self.clock.get_fps())), True, (0, 0, 0))
        self.screen.blit(text, (0, 30))

        # draw background color
        text = font.render("Background Color: " + str(self.background_rgb), True, (0, 0, 0))
        self.screen.blit(text, (0, 60))

        # draw help text
        text = font.render("Press SPACE to change background color", True, (0, 0, 0))
        self.screen.blit(text, (0, 150))

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