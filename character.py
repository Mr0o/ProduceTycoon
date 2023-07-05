import pygame

class Character:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 30
        self.height = 45
        self.animation_images = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (120, 120, 120)]
        self.animation_count = 0
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def events(self):
        # counting the frames once we get to 15 we reset to 0 back to the first image in out animation
        if (self.animation_count >= 15):
            self.animation_count = 0
        self.animation_count += 1

        # Add flipping to images to show which direction we are moving
    
    def update(self):
        # Updating character
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def draw(self):
        # Drawling character
        pygame.draw.rect(self.screen, self.animation_images[self.animation_count//4], self.rect)