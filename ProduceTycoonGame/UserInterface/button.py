import pygame

from ProduceTycoonGame.vectors import Vector


class Button():
    def __init__(self, screen: pygame.Surface, pos: Vector, text: str, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (202, 228, 240)):

        self.screen = screen
        self.pos = pos
        self.text = text
        self.width = width
        self.height = height
        self.color = color
        
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

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
        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        text = objectSize.render(self.text, True, (0, 0, 0))

        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        # center the text using the width and height of the text rect
        self.screen.blit(text, (self.pos.x + (self.width/2 - text.get_width()/2), self.pos.y + (self.height/2 - text.get_height()/2)))

        