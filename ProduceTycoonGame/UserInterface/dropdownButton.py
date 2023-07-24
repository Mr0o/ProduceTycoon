import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button

class DropdownButton(Button):
    def __init__(self, screen: pygame.Surface, pos: Vector, text: str, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (90, 140, 200)):
        super().__init__(screen, pos, text, width, height, color)

        self.isSelected = False
        self.hidden = False
    
    def events(self, mouseClicked: bool = False):
        if self.hidden:
            return

        # check if mouse position is on the button rect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # if mouse is clicked and the button is not already selecte
            if mouseClicked:
                self.isSelected = not self.isSelected

        return self.isSelected

    def draw(self):
        if self.hidden:
            return
        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        text = objectSize.render(self.text, True, (0, 0, 0))

        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        # center the text using the width and height of the text rect
        self.screen.blit(text, (self.pos.x + (self.width/2 - text.get_width()/2), self.pos.y + (self.height/2 - text.get_height()/2)))

        