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
    
    def events(self, events: list = []):
        print()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    print(self.text)


    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)
        self.screen.blit(self.base_font.render(self.text, True, (0, 0, 0)), (self.pos.x + 5, self.pos.y + 5))