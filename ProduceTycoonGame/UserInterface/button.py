import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.text import Text
from ProduceTycoonGame.events import eventOccured, Event

class Button():
    static_screen = pygame.Surface((0, 0))
    def __init__(self, pos: Vector, name: str, width: int, height: int, color: tuple[int, int, int]= (200, 110, 110)):
        self.pos = pos
        self.name = name
        self.width = width
        self.height = height
        self.color = color
        
        self.textRenderer = Text(Button.static_screen, self.pos, self.width, self.height, self.name)
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.isSelected = False
        self.hidden = False

    @staticmethod
    def setScreen(screen: pygame.Surface):
        Button.static_screen = screen
    
    def events(self):
        if self.hidden:
            return False

        # check if mouse position is on the button rect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # if mouse is clicked and the button is not already selected
            if eventOccured('left_mouse_clicked') and not self.isSelected:
                self.isSelected = True
        
        if not eventOccured('left_mouse_clicked'):
            self.isSelected = False
        self.textRenderer = Text(Button.static_screen, self.pos, self.width, self.height, self.name)

        return self.isSelected

    def draw(self):
        if self.hidden:
            return
        pygame.draw.rect(Button.static_screen, self.color, self.rect)
        pygame.draw.rect(Button.static_screen, (0, 0, 0), self.rect, 2)
        self.textRenderer.draw()

        