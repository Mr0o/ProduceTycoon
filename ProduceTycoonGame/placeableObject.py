import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tile import Type
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.UserInterface.placeableObjectGUI import PlaceableObjectGUI, TypeObject
from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class PlaceableObject():
    static_id = 0
    static_currentID = None
    def __init__(self, screen: pygame.Surface, pos: Vector, size: int, rows: int = 1, cols: int = 1, elements: list = [], image: str = './Resources/Images/WatermelonBin.png'):
        self.id = PlaceableObject.static_id
        PlaceableObject.static_id += 1
        self.screen = screen
        self.pos = pos
        self.size = size
        self.rows = rows
        self.cols = cols
        self.elements = elements

        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.rows * self.size, self.cols * self.size))

        self.isPlaced = False
        self.hasPlaced = False
        self.canPlace = False
        self.rect = self.image.get_rect()

        self.exitButton = Button(self.screen, Vector(0, 0), 'X', 20, 20, (255, 0, 0))

        self.gui = PlaceableObjectGUI(self.screen, Vector(self.screen.get_width() - 100, 25), 100, 100, (200, 150, 170))
        self.gui.type = TypeObject.WATERMELON

        self.mainTileID = -1
        self.frontTileIDs = []
        self.direction = Direction.NORTH

    def checkIfCanPlace(self):
        for element in self.elements:
            if element.rect.colliderect(self.rect):
                self.canPlace = False
                break
            else:
                self.canPlace = True

    # function looks like garbage fix later
    def moveToNewPos(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.isPlaced = False
            return self.isPlaced
        return self.isPlaced

    
    def setDirection(self):
        tileMapWidth = 32
        self.frontTileIDs = []
        if self.direction == Direction.NORTH:
            for i in range(self.rows):
                newTileID = self.mainTileID + i
                self.frontTileIDs.append(newTileID)
        elif self.direction == Direction.EAST:
            for i in range(self.cols):
                newTileID = self.mainTileID + i * tileMapWidth + self.rows - 1
                self.frontTileIDs.append(newTileID)
        elif self.direction == Direction.SOUTH:
            for i in range(self.rows):
                newTileID = self.mainTileID + i + (self.cols - 1) * tileMapWidth
                self.frontTileIDs.append(newTileID)
        elif self.direction == Direction.WEST:
            for i in range(self.cols):
                newTileID = self.mainTileID + i * tileMapWidth
                self.frontTileIDs.append(newTileID)

    def events(self, previousMouseClick: bool = False, mouseClicked: bool = False, events: list = []):
        if self.isPlaced:
            mouseClickedObject = mouseClicked and self.rect.collidepoint(pygame.mouse.get_pos())
            if mouseClickedObject:
                PlaceableObject.static_currentID = self.id
                self.gui.hidden = not self.gui.hidden
            if not PlaceableObject.static_currentID == self.id:
                self.gui.hidden = True
            self.gui.events(mouseClicked, events)
        self.checkIfCanPlace()

        mousePos = pygame.mouse.get_pos()
        #offset between next tile and mouse position for both x and y
        xOffset = self.size - mousePos[0] % self.size
        yOffset = self.size - mousePos[1] % self.size
        #new position for the object
        if self.cols % 2 == 0:
            newPosX = mousePos[0] + xOffset - self.cols * self.size // 2
        else:
            newPosX = mousePos[0] + xOffset - self.cols * self.size
        self.pos.x = newPosX
        if self.rows % 2 == 0:
            newPosY = mousePos[1] + yOffset - self.rows * self.size // 2
        else:
            newPosY = mousePos[1] + yOffset - self.rows * self.size
        self.pos.y = newPosY
            
        # changes tile type to object if rect collides with tile and mouse is clicked
        if self.canPlace and not mouseClicked and previousMouseClick:
            self.isPlaced = True
            self.hasPlaced = True

    def update(self):
        if self.isPlaced:
            self.gui.update()

            match self.gui.type:
                case TypeObject.WATERMELON:
                    self.image = pygame.image.load('./Resources/Images/WatermelonBin.png')
                    #print("Watermelon")
                case TypeObject.BANANAS:
                    self.image = pygame.image.load('./Resources/Images/Banana_ProduceTycoon.png')
                    #print("Bananas")
                case TypeObject.APPLES:
                    self.image = pygame.image.load('./Resources/Images/Apple_ProduceTycoon.png')
                    #print("Apples")
                case TypeObject.TOMATOES:
                    self.image = pygame.image.load('./Resources/Images/Tomato.png')
                    #print("Tomatoes")
                case _:
                    self.image = pygame.image.load('./Resources/Images/WatermelonBin.png')
            return
        # will figure out later works for now lol
        self.rect.topleft = (self.pos.x, self.pos.y)

    def draw(self):
        self.image = pygame.transform.scale(self.image, (self.rows * self.size, self.cols * self.size))
        self.screen.blit(self.image, self.rect.topleft)

        if not self.isPlaced:
            self.exitButton.draw()

        if not self.gui.hidden:
            self.gui.draw()

    def getPos(self):
        return self.pos

    def getPlaced(self):
        return self.isPlaced

    