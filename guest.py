import pygame
import random

from movement import Movement

class Guest(object):
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = 30
        self.height = 45
        self.moving_left = False
        self.moving_right = False
        self.animation_images = [(0, 50, 0), (0, 100, 0), (0, 150, 0), (0, 200, 0), (0, 255, 0)]
        self.animation_images_left = [(50, 0, 0), (100, 0, 0), (150, 0, 0), (200, 0, 0), (255, 0, 0)]
        self.animation_count = 0
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def events(self):
        # counting the frames once we get to 49 we reset to 0 back to the first image in out animation
        if (self.animation_count >= 49):
            self.animation_count = 0
        self.animation_count += 1

        self.x, self.y = Movement.check_if_move(self.x, self.y)
        

        # Add flipping to images to show which direction we are moving
    
    def update(self):
        # Updating guest
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

    def draw(self):
        # Drawling guest
        pygame.draw.rect(self.screen, self.animation_images[self.animation_count//10], self.rect)