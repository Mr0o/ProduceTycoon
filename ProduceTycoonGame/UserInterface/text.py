import pygame

from ProduceTycoonGame.vectors import Vector

class Text():

    # Static variables
    screen = pygame.Surface((0, 0))

    # Static methods
    @staticmethod
    def setScreen(screen: pygame.Surface):
        Text.screen = screen

    def __init__(self, pos: Vector, width: int, height: int, text: str):
        self.pos = pos
        self.width = width
        self.height = height
        self.text = text

        self.objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        self.renderText = self.objectSize.render(self.text, True, (0, 0, 0))
        self.x = self.pos.x + (self.width/2 - self.renderText.get_width()/2)
        self.y = self.pos.y + (self.height/2 - self.renderText.get_height()/2)

    def update(self):
        self.renderText = self.objectSize.render(self.text, True, (0, 0, 0))

    def draw(self):
        Text.screen.blit(self.renderText, (self.x, self.y))

    def setText(self, text: str):
        self.text = text
        self.update()