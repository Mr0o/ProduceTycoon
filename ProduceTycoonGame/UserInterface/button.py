import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.text import Text

class Button():
    def __init__(self, screen: pygame.Surface, pos: Vector, text: str, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (90, 140, 200)):
        self.screen = screen
        self.pos = pos
        self.text = text
        self.width = width
        self.height = height
        self.color = color
        
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))
        self.textRenderer = Text(self.screen, self.pos, self.width, self.height, self.text)

        self.isSelected = False
        self.hidden = False
    
    def events(self, mouseClicked: bool = False):
        if self.hidden:
            return

        # check if mouse position is on the button rect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # if mouse is clicked and the button is not already selected
            if mouseClicked and not self.isSelected:
                self.isSelected = True
        
        if not mouseClicked:
            self.isSelected = False

        return self.isSelected

    def draw(self):
        if self.hidden:
            return
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        self.textRenderer.draw()

        