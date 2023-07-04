import pygame

class Character:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 20
        self.height = 45
        self.animation_images = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (120, 120, 120)]
        self.animation_count = 0
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
    def events(self):
        if (self.animation_count >= 15):
            self.animation_count = 0
        self.animation_count += 1

        #pygame.draw.rect(self.screen, self.animation_images[self.animation_count//4][0], pygame.transform.scale((self.character_rect), (self.width * self.animation_images[self.animation_count//4][1], self.height * self.animation_images[self.animation_count//4][1])))
    def draw(self):
        pygame.draw.rect(self.screen, self.animation_images[self.animation_count//4], self.rect)