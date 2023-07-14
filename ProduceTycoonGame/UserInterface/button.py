import pygame

from ProduceTycoonGame.vectors import Vector

class Button():
    def __init__(self, screen: pygame.Surface, pos: Vector, text: str, width: int, height: int):
        self.screen = screen
        self.pos = pos
        self.text = text
        self.width = width
        self.height = height

        self.isSelected = False
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))
    
    def events(self, mouseClicked: bool = False):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if mouseClicked and not self.isSelected:
                self.isSelected = True
                action = True
        
        if not mouseClicked:
            self.isSelected = False
            

        return action

    def draw(self):
        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        text = objectSize.render(self.text, True, (0, 0, 0))

        pygame.draw.rect(self.screen, (202, 228, 240), self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        self.screen.blit(text, (self.pos.x, self.pos.y))

        