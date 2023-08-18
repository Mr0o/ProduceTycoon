import pygame

from ProduceTycoonGame.vectors import Vector

class Button():
    def __init__(self, screen: pygame.Surface, pos: Vector, text: str, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (90, 140, 200)):
        self.screen = screen
        self.pos = pos
        self.text = text
        self.width = width
        self.height = height
        self.color = color
        
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))
        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        self.renderText = objectSize.render(self.text, True, (0, 0, 0))
        self.xPos = self.pos.x + (self.width/2 - self.renderText.get_width()/2)
        self.yPos = self.pos.y + (self.height/2 - self.renderText.get_height()/2)

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
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        self.drawText()

    def drawText(self):
        self.screen.blit(self.renderText, (self.xPos, self.yPos))

        