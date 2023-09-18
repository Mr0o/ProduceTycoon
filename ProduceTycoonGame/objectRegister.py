import pygame

from ProduceTycoonGame.events import eventOccured
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button

from enum import Enum, IntEnum

class TypeObject(IntEnum):
    WALL = 0
    PRODUCE_CASE = 1
    REGISTER = 2

class TypeProduceCase(Enum):
    EMPTY = 'Empty'
    WATERMELON = 'Watermelon'
    BANANAS = 'Bananas'
    APPLES = 'Apples'
    TOMATOES = 'Tomatoes'

class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

# Helder functions
def getNextDirection(direction: Direction):
    return direction + 1 if direction + 1 < 4 else direction - 3

class ObjectGUI:
    typeButtons = []
    active: bool
    direction: Direction
    typeCase: TypeProduceCase

    # Positions
    x = 700; y = 30
    def __init__(self, active = False, direction = Direction.NORTH, typeCase = TypeProduceCase.WATERMELON):
        self.active = active
        self.direction = direction
        self.typeCase = typeCase

        self.changeDirectionButton = self.createButton('Rotate', lambda: self.setDirection(self.direction))
        self.exitButton = self.createButton('X', lambda: self.exitGUI())

        self.typeButtons = self.createButtons()

        # Resets positions back to (700, 30) fbsr;jbwr
        ObjectGUI.x = 700; ObjectGUI.y = 30

    # Helper methods
    def createButton(self, nameButton: str, func: callable):
        x = ObjectGUI.x
        y = ObjectGUI.y
        ObjectGUI.y += 20
        return Button(Vector(x, y), nameButton, 100, 20, func)

    def createButtons(self):
        # Create each button with a lambda function that calls the setTypeCase method with the correct type
        return [
            self.createButton('Watermelon', lambda: self.setTypeCase(TypeProduceCase.WATERMELON)),
            self.createButton('Bananas', lambda: self.setTypeCase(TypeProduceCase.BANANAS)),
            self.createButton('Apples', lambda: self.setTypeCase(TypeProduceCase.APPLES)),
            self.createButton('Tomatoes', lambda: self.setTypeCase(TypeProduceCase.TOMATOES)),
            self.createButton('Empty', lambda: self.setTypeCase(TypeProduceCase.EMPTY))
        ]
    
    def setDirection(self, direction: Direction):
        self.direction = getNextDirection(direction)

    def setTypeCase(self, typeCase: TypeProduceCase):
        self.typeCase = typeCase

    def exitGUI(self):
        self.active = False
        Object.currentID = -1

    # Main methods
    def events(self):
        for button in self.typeButtons:
            button.events()
        self.changeDirectionButton.events()
        self.exitButton.events()

    def draw(self):
        for button in self.typeButtons:
            button.draw()
        self.changeDirectionButton.draw()
        self.exitButton.draw()

class ObjectInfo:
    screen: pygame.Surface
    position: Vector
    gui: ObjectGUI
    rows: int
    colums: int
    tileSize: int
    placed: bool
    hasPlaced: bool

    elementRectangles = []

    def __init__(self, screen, position, gui, rows, colums, tileSize, placed = False, hasPlaced = False):
        self.screen = screen
        self.position = position
        self.gui = gui
        self.rows = rows
        self.colums = colums
        self.tileSize = tileSize
        self.placed = placed
        self.hasPlaced = hasPlaced

    def canPlace(self, objectRectangle: pygame.Rect):
        for rectangle in ObjectInfo.elementRectangles:
            if objectRectangle.colliderect(rectangle):
                return False
        return True

    @staticmethod
    def setElementRectangles(elementRectangles):
        ObjectInfo.elementRectangles = elementRectangles     
    
class Object:
    objectID: int
    info: ObjectInfo
    mainTileID: int
    image: pygame.Surface
    rectangle: pygame.Rect

    currentID = -1

    def __init__(self, objectID, info, mainTileID = -1):
        self.objectID = objectID
        self.info = info
        self.mainTileID = mainTileID
        self.setImage()
        self.configureImage(self.image)
        self.rectangle = self.createRectangle()

    # Instance methods
    def configureImage(self, image: pygame.Surface):
        self.image = pygame.transform.scale(image, (self.info.rows * self.info.tileSize, self.info.colums * self.info.tileSize))
        #self.image.rotate(self.info.direction * 90)

    def createRectangle(self):
        return self.image.get_rect()

    def setRectanglePos(self, x, y):
        self.rectangle.topleft = (x, y)

    def setPosition(self):
        mousePos = pygame.mouse.get_pos()
        tileSize = self.info.tileSize

        xOffset = self.getOffset(mousePos[0])
        yOffset = self.getOffset(mousePos[1])

        # X Position 
        if self.info.colums % 2 == 0:
            posX = mousePos[0] + xOffset - self.info.colums * tileSize // 2
        else:
            posX = mousePos[0] + xOffset - self.info.colums * tileSize
        # Y Position
        if self.info.rows % 2 == 0:
            posY = mousePos[1] + yOffset - self.info.rows * tileSize // 2
        else:
            posY = mousePos[1] + yOffset - self.info.rows * tileSize

        self.info.position = Vector(posX, posY)
        self.setRectanglePos(posX, posY)

    def getOffset(self, mousePos):
        return self.info.tileSize - mousePos % self.info.tileSize

    def setImage(self):
        match self.info.gui.typeCase:
            case TypeProduceCase.WATERMELON:
                image = pygame.image.load('./Resources/Images/WatermelonBin.png')
            case TypeProduceCase.BANANAS:
                image = pygame.image.load('./Resources/Images/Banana_ProduceTycoon.png')
            case TypeProduceCase.APPLES:
                image = pygame.image.load('./Resources/Images/WatermelonBin.png')
            case TypeProduceCase.TOMATOES:
                image = pygame.image.load('./Resources/Images/Tomato.png')
            case TypeProduceCase.EMPTY:
                image = pygame.image.load('./Resources/Images/WatermelonBin.png')
        self.configureImage(image)

    def setMainTileID(self, ID):
        self.mainTileID = ID

    def getFrontTiles(self):
        tileMapWidth = 32
        frontTileIDs = []
        match self.info.gui.direction:
            case Direction.NORTH:
                for i in range(self.info.rows):
                    newTileID = self.mainTileID + i
                    frontTileIDs.append(newTileID)
            case Direction.EAST:
                for i in range(self.info.colums):
                    newTileID = self.mainTileID + i * tileMapWidth + self.info.rows - 1
                    frontTileIDs.append(newTileID)
            case Direction.SOUTH:
                for i in range(self.info.rows):
                    newTileID = self.mainTileID + i + (self.info.colums - 1) * tileMapWidth
                    frontTileIDs.append(newTileID)
            case Direction.WEST:
                for i in range(self.info.colums):
                    newTileID = self.mainTileID + i * tileMapWidth
                    frontTileIDs.append(newTileID)
        return frontTileIDs
    
    def openGUI(self):
        # If clicked happen on object
        mouseClickedObject = eventOccured("leftMouseDown") and self.rectangle.collidepoint(pygame.mouse.get_pos())
        if mouseClickedObject:
            # Current ID is set to this object's ID
            Object.currentID = self.objectID
            # The first click on the object will open the GUI second click will close it
            self.info.gui.active = not self.info.gui.active
        if Object.currentID is not self.objectID :
            self.info.gui.active = False
        return self.info.gui.active

    def placeObject(self):
        if self.info.canPlace(self.rectangle) and eventOccured("leftMouseDown"):
            self.info.placed = True
            self.info.hasPlaced = True
    
    # Main methods
    def events(self):
        self.setImage()

        if self.info.placed:
            if self.openGUI():
                self.info.gui.events()
            return
 
        self.setPosition()
        self.placeObject()

    def draw(self):
        self.info.screen.blit(self.image, (self.info.position.x, self.info.position.y))
        if self.info.placed and self.info.gui.active:
            self.info.gui.draw()
        

class ObjectRegister:
    objectID = 0
    objects = []

    # fix code __init__ or generateObject moethod they should not both take in the same arguments basically
    def __init__(self, screen, position, rows, colums, tileSize):
        self.objects.append(self.generateObject(screen, position, rows, colums, tileSize))

    def generateObjectID(self):
        objectID = ObjectRegister.objectID
        ObjectRegister.objectID += 1
        return objectID

    @staticmethod
    def setElementRectangles(elementRectangles):
        ObjectInfo.setElementRectangles(elementRectangles)

    def generateObject(self, screen, position, rows, colums, tileSize):
        objectID = self.generateObjectID()    
        gui = ObjectGUI()    
        objectInfo = ObjectInfo(screen, position, gui, rows, colums, tileSize)
        return Object(objectID, objectInfo)
    