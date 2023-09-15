import pygame

from ProduceTycoonGame.events import eventOccured
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button

class DropdownButton(Button):
    def __init__(self, screen: pygame.Surface, pos: Vector, text: str, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (90, 140, 200)):
        super().__init__(screen, pos, text, width, height, color)

        self.isSelected = False
        self.hidden = False
    
    def events(self):
        if self.hidden:
            return

        # check if mouse position is on the button rect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # if mouse is clicked and the button is not already selecte
            if eventOccured("leftMouseDown"):
                self.isSelected = not self.isSelected

        return self.isSelected

    def draw(self):
       super().draw()

        