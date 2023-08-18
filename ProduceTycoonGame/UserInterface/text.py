import pygame

from ProduceTycoonGame.vectors import Vector

class Text():
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, text: str):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.text = text

        self.objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        self.renderText = self.objectSize.render(self.text, True, (0, 0, 0))
        self.xPos = self.pos.x + (self.width/2 - self.renderText.get_width()/2)
        self.yPos = self.pos.y + (self.height/2 - self.renderText.get_height()/2)

    def update(self):
        self.renderText = self.objectSize.render(self.text, True, (0, 0, 0))

    def draw(self):
        self.screen.blit(self.renderText, (self.xPos, self.yPos))

    def setText(self, text: str):
        self.text = text
        self.update()