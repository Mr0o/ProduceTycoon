import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.elements import Element


class Button(Element):
    def __init__(self, screen: pygame.Surface, pos: Vector, text: str, isSelected: bool = False):
        super().__init__(screen, pos)
        self.text = text
        self.isSelected = isSelected

        self.width = 50
        self.height = 20
        self.color = (40, 120, 180)
        self.previousMouseClick = False

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        
    
    def events(self, mouseClicked: bool):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and mouseClicked:
            self.isSelected != self.isSelected
            self.showRect = True
        
        if self.isSelected:
            self.color = (200, 120, 180)
        
        self.previousMouseClick = mouseClicked
        


    def update(self):
        pass
        

    def draw(self):
        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        text = objectSize.render(self.text, True, (0, 0, 0))

        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        self.screen.blit(text, (self.pos.x, self.pos.y))

        