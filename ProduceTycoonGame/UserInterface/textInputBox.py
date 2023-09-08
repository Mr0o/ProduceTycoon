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
        self.textFont = pygame.font.Font(None, 32)
        self.text = ''
    
    def events(self):
        return
        ###### TODO: get rid of this lmao, or at least switch to events
        #print()
        # for event in events:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if self.rect.collidepoint(event.pos):
        #             self.active = True
        #         else:
        #             self.active = False
        #     if event.type == pygame.KEYDOWN:
        #         if self.active:
        #             if event.key == pygame.K_BACKSPACE:
        #                 self.text = self.text[:-1]
        #             elif   (event.key == pygame.K_0 or event.key == pygame.K_1 
        #                  or event.key == pygame.K_2 or event.key == pygame.K_3 
        #                  or event.key == pygame.K_4 or event.key == pygame.K_5 
        #                  or event.key == pygame.K_6 or event.key == pygame.K_7 
        #                  or event.key == pygame.K_8 or event.key == pygame.K_9):

        #                 self.text += event.unicode

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)
        self.screen.blit(self.textFont.render(self.text, True, (0, 0, 0)), (self.pos.x + 5, self.pos.y))