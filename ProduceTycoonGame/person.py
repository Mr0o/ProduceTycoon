import pygame

from ProduceTycoonGame.tile import Tile
from ProduceTycoonGame.vectors import Vector

# super class for guests and employees
class Person():
    def __init__(self, screen: pygame.Surface, pos: Vector, id: int, name: str = "Person"):
        self.screen = screen
        self.pos = pos
        self.size = 50

        self.mov = Vector(0, 0)
        self.targetTile: Tile = None

        self.animationImages = [
            (0, 50, 0), (0, 100, 0), (0, 150, 0), (0, 200, 0), (0, 255, 0)]
        self.animationCount = 0
        self.rect = pygame.Rect(
            (self.pos.x, self.pos.y), (self.size, self.size))

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

        # pathfinding variables
        self.path: list = [Tile]
        self.pathIndex: int = 0

    def events(self):
        # counting the frames once we get to 49 we reset to 0 back to the first image in out animation
        if self.animationCount >= 49:
            self.animationCount = 0
        self.animationCount += 1

    def setTarget(self, targetTile: Tile):
        # set the target tile
        self.targetTile = targetTile
        self.pathIndex = 0

    def update(self):
        # move towards the next point in the path
        if self.path != None:
            # TODO: get the next tile in the path and set the mov vector to the direction of the next tile
            pass
                

        self.rect = pygame.Rect(
            (self.pos.x, self.pos.y), (self.size, self.size))

    def draw(self):
        pygame.draw.rect(
            self.screen, self.animationImages[self.animationCount//10], self.rect)