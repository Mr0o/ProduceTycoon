import pygame

from ProduceTycoonGame.vectors import Vector

class Button():
    def __init__(self, screen: pygame.Surface, pos: Vector, text = "3x3"):
        self.screen = screen
        self.pos = pos
        self.text = text

        self.width = 21
        self.height = 20
        self.color = (0, 0, 255)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        
    
    def events(self, mouseClicked: bool):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and mouseClicked:
            self.color = (0, 123, 255)
        else:
            self.color = (0, 0, 255)

    def draw(self):

        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        text = objectSize.render(self.text, True, (0, 0, 0))

        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(text, (self.pos.x, self.pos.y))