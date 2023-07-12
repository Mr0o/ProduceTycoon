import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.elements import Element


class Button(Element):
    def __init__(self, screen: pygame.Surface, pos: Vector, text: str):
        super().__init__(screen, pos)
        self.text = text

        self.isSelected = False
        self.create = False
        self.width = 50
        self.height = 20
        self.isOn = False

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
    
    def events(self, mouseClicked: bool = False):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and mouseClicked:
            self.isSelected = True
            self.create = True

    def update(self):
        if self.isSelected:
            self.isOn = True
            self.isSelected = False

    def draw(self):
        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        text = objectSize.render(self.text, True, (0, 0, 0))

        pygame.draw.rect(self.screen, (100, 100, 100), self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        self.screen.blit(text, (self.pos.x, self.pos.y))

        