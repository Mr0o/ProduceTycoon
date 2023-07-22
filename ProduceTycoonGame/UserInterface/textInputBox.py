import pygame

from ProduceTycoonGame.vectors import Vector

class TextInputBox():
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (200, 150, 170)):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.active = False
        self.base_font = pygame.font.Font(None, 32)
        self.text = ''
    
    def events(self, mouseClicked: bool = False, backspacePressed: bool = False):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if mouseClicked:
                self.active = True
            else:
                self.active = False

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)