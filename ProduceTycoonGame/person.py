import pygame
import pymunk

from ProduceTycoonGame.tile import Tile
from ProduceTycoonGame.vectors import Vector

# super class for guests and employees
class Person():
    def __init__(self, screen: pygame.Surface, pos: Vector, id: int, name: str = "Person"):
        self.screen = screen
        self.pos = pos
        self.size = 15
        self.maxForceMag = 2

        self.mov = Vector(0, 0)
        self.targetTile: Tile = None

        self.animationImages = [
            (0, 50, 0), (0, 100, 0), (0, 150, 0), (0, 200, 0), (0, 255, 0)]
        self.animationCount = 0
        self.rect = pygame.Rect(
            (self.pos.x, self.pos.y), (self.size, self.size))
        
        # pymunk body and shape
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (self.pos.x + self.size / 2, self.pos.y + self.size / 2)
        self.shape = pymunk.Poly.create_box(self.body, (self.size, self.size))
        self.shape.friction = 1

        # person id
        self.id: int = id

        # person variables
        self.name: str = name + str(id)
        # this is a percentage; 100% is happy, 0% is unhappy;
        self.happyScore: int = 100
        # this is a string that will reflect the person's most recent thought (e.g. "It's too crowded here" or "I want to buy some apples")
        self.thought: str = ""
        # this is a string that will reflect the person's current state (e.g. "idle" or "shopping") usefule for changing the animation
        self.state: str

        # person task list
        # this is a list of strings that will reflect the person's current tasks (e.g. shopping list or job list)")
        self.tasks: list[str] = []

    def events(self):
        # counting the frames once we get to 49 we reset to 0 back to the first image in our animation
        if self.animationCount >= 49:
            self.animationCount = 0
        self.animationCount += 1

    def update(self):
        # get the position of the person in pymunk space
        self.pos = Vector(self.body.position.x - self.size / 2, self.body.position.y - self.size / 2)
        self.rect = pygame.Rect(
            (self.pos.x, self.pos.y), (self.size, self.size))

    def draw(self):
        pygame.draw.rect(
            self.screen, self.animationImages[self.animationCount//10], self.rect)