import pygame

from ProduceTycoonGame.vectors import Vector

class Slider():
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (202, 228, 240)):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.slider = pygame.Rect((self.pos.x + 5, self.pos.y + self.height / 2 - 3), (6, 4))

        self.isSelected = False
        self.hidden = True
    def events(self, mouseClicked: bool = False):
        if self.hidden:
            return

        # check if mouse position is on the button rect
        if self.slider.collidepoint(pygame.mouse.get_pos()):
            # if mouse is clicked and the button is not already selected
            if mouseClicked:
                self.isSelected = not self.isSelected
                print(self.isSelected)
        
            
        return self.isSelected
    
    def update(self):
        if self.hidden:
            return

        if self.isSelected:
            self.slider.x = pygame.mouse.get_pos()[0]
            if self.slider.x < self.pos.x + 5:
                self.slider.x = self.pos.x + 5
            elif self.slider.x > self.pos.x + self.width - 5:
                self.slider.x = self.pos.x + self.width - 5
    
    def draw(self):
        if self.hidden:
            return
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        pygame.draw.rect(self.screen, (0, 0, 0), self.slider)