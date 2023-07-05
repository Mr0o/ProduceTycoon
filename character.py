import pygame

class Character:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 20
        self.height = 45
        self.animation_images = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (120, 120, 120)]
        self.animation_count = 0
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def events(self):
        self.keys = pygame.key.get_pressed()
        # Each key moves the background the oposite direction that we want our character to move.
        # Scroll left
        if self.keys[pygame.K_a]:
            self.x -= 20
        # Scroll right
        if self.keys[pygame.K_d]:
            self.x += 20
        # Scroll down
        if self.keys[pygame.K_w]:
            self.y -= 20
        # Scroll Up
        if self.keys[pygame.K_s]:
            self.y += 20
        
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