import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.events import eventOccured, getEvent

class TextInputBox:
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (200, 150, 170)):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.active = False
        self.textFont = pygame.font.Font(None, 32)
        self.text = ''
    
    def events(self):
        if eventOccured("leftMouseDown"):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True
            else:
                self.active = False
        if self.active:
            if eventOccured("backspace"):
                self.text = self.text[:-1]
            elif eventOccured("keyDown"):
                self.text += getEvent("keyDown").getData().unicode

    def getText(self):
        return self.text

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)
        self.screen.blit(self.textFont.render(self.text, True, (0, 0, 0)), (self.pos.x + 5, self.pos.y))