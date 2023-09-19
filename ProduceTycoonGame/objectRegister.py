import pygame

from ProduceTycoonGame.events import eventOccured
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.playerData import PlayerData
from ProduceTycoonGame.produce import Produce, Watermelon, Bananas, Apples, Tomatoes

from enum import Enum, IntEnum

# These should all be in the object class
#   - Add an addproduce method that takes a produce from player data and adds it into the case quantity.
#   - Add a removeproduce method that takes a produce from player data and removes it from the case quantity.
#   - Add a sellproduce method that takes a produce from player data and sells it for money.

# Add a rotate method that rotates the object.

# ---------- Enums ----------
class TypeObject(IntEnum):
    WALL = 0
    PRODUCE_CASE = 1
    REGISTER = 2

class TypeProduceCase(Enum):
    EMPTY = Produce
    WATERMELON = Watermelon
    BANANAS = Bananas
    APPLES = Apples
    TOMATOES = Tomatoes

class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

# ---------- Helper Functions ----------
def getNextDirection(direction: Direction):
    return direction + 1 if direction + 1 < 4 else direction - 3

class ObjectGUI:
    currentObject: object
    buttons: []
    active: bool

    # Positions
    x = 700; y = 30

    # ---------- Constructor ----------
    def __init__(self, active = False, direction = Direction.NORTH, typeCase = TypeProduceCase.WATERMELON):
        self.active = active
        self.buttons = self.createButtons()

    # ---------- Setters ----------
    def setObject(self, newObject: object):
        self.currentObject = newObject

    # ---------- Helpers ----------
    def createButton(self, nameButton: str, func: callable):
        x = ObjectGUI.x
        y = ObjectGUI.y
        ObjectGUI.y += 20
        return Button(Vector(x, y), nameButton, 100, 20, func)

    def createButtons(self):
        # Resets poss back to (700, 30) for the next object
        ObjectGUI.x = 700; ObjectGUI.y = 30

        # Create each button with a lambda function that calls the setTypeCase method with the correct type
        return [
            self.createButton('Watermelon', lambda: self.currentObject.setTypeCase(TypeProduceCase.WATERMELON)),
            self.createButton('Bananas', lambda: self.currentObject.setTypeCase(TypeProduceCase.BANANAS)),
            self.createButton('Apples', lambda: self.currentObject.setTypeCase(TypeProduceCase.APPLES)),
            self.createButton('Tomatoes', lambda: self.currentObject.setTypeCase(TypeProduceCase.TOMATOES)),
            self.createButton('Empty', lambda: self.currentObject.setTypeCase(TypeProduceCase.EMPTY)),
            self.createButton('X', lambda: self.exitGUI()),
            self.createButton('Rotate', lambda: self.currentObject.setDirection()),
            self.createButton('Add Produce', lambda: self.currentObject.addProduce()),
            self.createButton('Remove Produce', lambda: self.currentObject.removeProduce()),
            self.createButton('Sell Produce', lambda: self.currentObject.sellProduce()),
        ]

    def exitGUI(self):
        self.active = False
        Object.currentID = -1

    # ---------- Main ----------
    def events(self):
        for button in reversed(self.buttons):
            button.events()

    def draw(self):
        for button in self.buttons:
            button.draw()

class ObjectInfo:
    screen: pygame.Surface
    pos: Vector
    gui: ObjectGUI
    rows: int
    columns: int
    tileSize: int
    placed: bool = False
    hasPlaced: bool = False
    mainTileID: int = -1
    image: pygame.Surface
    rect: pygame.Rect
    direction = Direction = Direction.NORTH
    typeCase = TypeProduceCase = TypeProduceCase.EMPTY
    amount: int = 0

    elementRectangles = []

    # ---------- Constructor ----------  
    def __init__(self, screen, pos, gui, rows, columns, tileSize):
        self.screen = screen
        self.pos = pos
        self.gui = gui
        self.rows = rows
        self.columns = columns
        self.tileSize = tileSize
        self.setImage() 
        self.rect = self.image.get_rect()

    # ---------- Setters ----------
    def setImage(self):
        match self.typeCase:
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

    # ---------- Helpers ----------
    def configureImage(self, image: pygame.Surface):
        self.image = pygame.transform.scale(image, (self.rows * self.tileSize, self.columns * self.tileSize))
        #self.image.rotate(self.direction * 90) 

class Object:
    # Variables
    objectID: int
    info: ObjectInfo

    # Static variables
    currentID = -1

    # ---------- Constructor ----------
    def __init__(self, objectID, info):
        self.objectID = objectID
        self.info = info
        self.info.gui.setObject(self)

    # ---------- Setters ----------
    def setPosition(self):
        mousePos = pygame.mouse.get_pos()
        tileSize = self.info.tileSize

        xOffset = self.getOffset(mousePos[0])
        yOffset = self.getOffset(mousePos[1])

        # X Position 
        if self.info.columns % 2 == 0:
            x = mousePos[0] + xOffset - self.info.columns * tileSize // 2
        else:
            x = mousePos[0] + xOffset - self.info.columns * tileSize

        # Y Position
        if self.info.rows % 2 == 0:
            y = mousePos[1] + yOffset - self.info.rows * tileSize // 2
        else:
            y = mousePos[1] + yOffset - self.info.rows * tileSize

        self.info.pos = Vector(x, y)
        self.info.rect.topleft = (x, y)

    def setTypeCase(self, typeCase: TypeProduceCase):
        # Return nothing if the type is the same
        if self.info.typeCase is typeCase:
            return
        if self.info.typeCase is not TypeProduceCase.EMPTY:
            # Adds the produce from the case back into the player data to be used again
            self.info.typeCase.value.amount += self.info.amount
            # Set amount back to 0 to add the new type of produce too it
            self.info.amount = 0
        self.info.typeCase = typeCase

    def setDirection(self):
        self.info.direction = getNextDirection(self.info.direction)

    # ---------- Getters ----------
    def getOffset(self, mousePos):
        return self.info.tileSize - mousePos % self.info.tileSize

    def getFrontTiles(self):
        tileMapWidth = 32
        frontTileIDs = []
        match self.info.direction:
            case Direction.NORTH:
                for i in range(self.info.columns):
                    newTileID = self.info.mainTileID + i
                    frontTileIDs.append(newTileID)
            case Direction.EAST:
                for i in range(self.info.rows):
                    newTileID = self.info.mainTileID + i * tileMapWidth + self.info.rows - 1
                    frontTileIDs.append(newTileID)
            case Direction.SOUTH:
                for i in range(self.info.columns):
                    newTileID = self.info.mainTileID + i + (self.info.columns - 1) * tileMapWidth
                    frontTileIDs.append(newTileID)
            case Direction.WEST:
                for i in range(self.info.rows):
                    newTileID = self.info.mainTileID + i * tileMapWidth
                    frontTileIDs.append(newTileID)
        return frontTileIDs

    def setMainTileID(self, ID):
        self.info.mainTileID = ID

    # ---------- Validators ----------
    def canPlace(self):
        for rect in ObjectInfo.elementRectangles:
            if self.info.rect.colliderect(rect):
                return False
        return True

    # ---------- Helpers ----------
    def addProduce(self):
        PRODUCE = self.info.typeCase.value
        if self.info.typeCase is TypeProduceCase.EMPTY:
            print("---- Cannot add produce to EMPTY case ----")
            return
        if PRODUCE.amount == 0:
            print("---- Insufficient produce ----")
            return
        self.info.amount += 1
        print(f"{PRODUCE.name}: {self.info.amount}")
        PRODUCE.amount -= 1

    def removeProduce(self):
        PRODUCE = self.info.typeCase.value
        if self.info.typeCase is TypeProduceCase.EMPTY:
            print("---- Cannot remove produce from EMPTY case ----")
            return
        if self.info.amount == 0:
            print("---- Insufficient produce ----")
            return
        self.info.amount -= 1
        print(f"{PRODUCE.name}: {self.info.amount}")
        PRODUCE.amount += 1

    def sellProduce(self):
        PRODUCE = self.info.typeCase.value
        if self.info.typeCase is TypeProduceCase.EMPTY:
            print("---- Cannot sell produce from EMPTY case ----")
            return
        if self.info.amount == 0:
            print("---- Insufficient produce ----")
            return
        PlayerData.money += PRODUCE.sell
        self.info.amount -= 1
        print(f"{PRODUCE.name}: {self.info.amount}")
        print(f"Money: {PlayerData.money}")

    def openGUI(self):
        # If clicked happen on object
        mouseClickedObject = eventOccured("leftMouseDown") and self.info.rect.collidepoint(pygame.mouse.get_pos())
        if mouseClickedObject:
            # Current ID is set to this object's ID
            Object.currentID = self.objectID
            # The first click on the object will open the GUI second click will close it
            self.info.gui.active = not self.info.gui.active
        if Object.currentID is not self.objectID :
            self.info.gui.active = False
        return self.info.gui.active

    def placeObject(self):
        if self.canPlace() and eventOccured("leftMouseDown"):
            self.info.placed = True
            self.info.hasPlaced = True
    
    # ---------- Main ----------
    def events(self):
        self.info.setImage()

        if self.info.placed:
            if self.openGUI():
                self.info.gui.events()
            return
 
        self.setPosition()
        self.placeObject()

    def draw(self):
        self.info.screen.blit(self.info.image, (self.info.pos.x, self.info.pos.y))
        if self.info.gui.active:
            self.info.gui.draw()

class ObjectRegister:
    # Variables
    objectID = 0
    # Static Variables
    objects = []

    # ---------- Static ----------
    @staticmethod
    def setElementRectangles(elementRectangles):
        ObjectInfo.elementRectangles = elementRectangles

    # ---------- Constructor ----------
    def __init__(self, screen, pos, rows, columns, tileSize):
        self.objects.append(self.generateObject(screen, pos, rows, columns, tileSize))

    # ---------- Helpers ----------
    def generateObjectID(self):
        objectID = ObjectRegister.objectID
        ObjectRegister.objectID += 1
        return objectID

    def generateObject(self, screen, pos, rows, columns, tileSize):
        objectID = self.generateObjectID()    
        gui = ObjectGUI()    
        objectInfo = ObjectInfo(screen, pos, gui, rows, columns, tileSize)
        return Object(objectID, objectInfo)
    