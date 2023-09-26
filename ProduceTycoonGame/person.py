import pygame

from ProduceTycoonGame.tileMap import Tile
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.timer import TimedEvent

def getImage(sheet: pygame.Surface, x: int, y: int, width: int, height: int, scale: int = 1):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((0, 0, 0))
    return image

# super class for guests and employees
class Person:
    def __init__(self, screen: pygame.Surface, pos: Vector, id: int, name: str = "Person"):
        self.screen = screen

        self.pos = pos
        self.vel = Vector(0, 0)
        self.acc = Vector(0, 0)
        self.size = 15
        self.movSpeed = 1.0

        # used to detect stuck condition
        self.prevPos = pos.copy()
        self.actualVel = Vector(0, 0)

        # stuck timer
        self.stuckTimer = TimedEvent()
        self.isStuck = False

        self.targetTile: Tile = None

        sheet = pygame.image.load("./Resources/Images/Characters/GenericGuest.png").convert_alpha()

        self.images = [getImage(sheet, 0, 0, 16, 16, 2), getImage(sheet, 16, 0, 16, 16, 2), getImage(sheet, 32, 0, 16, 16, 2), getImage(sheet, 48, 0, 16, 16, 2)]

        self.animationCount = 0
        self.rect = pygame.Rect(
            (self.pos.x, self.pos.y), (self.size, self.size))

        # person id
        self.id: int = id

        ## person variables
        self.name: str = name + str(id)
        # this is a percentage; 100% is happy, 0% is unhappy;
        self.happyScore: int = 100
        # this is a string that will reflect the person's most recent thought (e.g. "It's too crowded here" or "I want to buy some apples")
        self.thought: str = ""
        # this is a string that will reflect the person's current state (e.g. "idle" or "shopping") useful for changing the animation
        self.state: str

        # person task list
        # this is a list of strings that will reflect the person's current tasks (e.g. shopping list or job list)")
        self.tasks: list[str] = []

    def events(self):
        # counting the frames once we get to 49 we reset to 0 back to the first image in our animation
        if self.animationCount >= 39:
            self.animationCount = 0
        self.animationCount += 1

    def update(self):
        # set the previous position
        self.prevPos = self.pos.copy()

        # position is derived from the velocity and velocity is derived from the acceleration
        self.vel.add(self.acc)
        # force velocity to be a certain speed (magnitude)
        self.vel.setMag(self.movSpeed)
        self.pos.add(self.vel)
        self.acc.mult(0)
        # update the rect
        self.rect = pygame.Rect(
            (self.pos.x, self.pos.y), (self.size, self.size))
        
        self.checkIfStuck()
        if self.isStuck:
            print("stuck")
            self.isStuck = False
        
    def applyForce(self, force : Vector):
        fcopy = force.copy() # create a copy of the force
        self.vel.add(fcopy)

    def checkIfStuck(self):
        self.stuckTimer.update()
        # check if the person is stuck
        if self.actualVel.getMag() < 0.8 and not self.stuckTimer.isActive:
            self.stuckTimer.setTimer(1)
        
        # if the stuck timer is active then we check if it has reached the end
        if self.stuckTimer.isActive:
            if self.stuckTimer.isTriggered:
                # check if the person is still stuck
                if self.actualVel.getMag() < 0.8:
                    self.isStuck = True

    def scaleImages(self):
        images = []
        for image in self.images:
            images.append(pygame.transform.scale(image, (32, 32)))

        return images

    def draw(self):
        self.screen.blit(self.images[self.animationCount // 10], (self.pos.x, self.pos.y))