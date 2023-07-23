import pygame

from ProduceTycoonGame.vectors import Vector

class Slider():
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (200, 150, 170)):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.slider = pygame.Rect((self.pos.x + 5, self.pos.y + self.height / 2 - 3), (4, 6))

        self.isSelected = False

    def events(self, mouseClicked: bool = False):
        if self.slider.collidepoint(pygame.mouse.get_pos()):
            if mouseClicked:
                self.isSelected = not self.isSelected

        return self.isSelected
    
    def update(self):
        if self.isSelected:
            self.slider.x = pygame.mouse.get_pos()[0]
            if self.slider.x < self.pos.x + 5:
                self.slider.x = self.pos.x + 5
            elif self.slider.x > self.pos.x + self.width - 10:
                self.slider.x = self.pos.x + self.width - 10
            
    
    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)
        pygame.draw.rect(self.screen, (0, 0, 0), self.slider)