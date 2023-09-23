import pygame
import json

from ProduceTycoonGame.events import eventOccured
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.playerData import PlayerData
from ProduceTycoonGame.produce import Produce

from enum import Enum, IntEnum

# ---------- Enums ----------
class TypeObject(IntEnum):
    WALL = 0
    PRODUCE_CASE = 1
    REGISTER = 2

class TypeProduceCase(Enum):
    EMPTY = None
    WATERMELON = 'Watermelon'
    BANANAS = 'Bananas'
    APPLES = 'Apples'
    TOMATOES = 'Tomatoes'

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
    active: bool = False

    # Positions
    x = 700; y = 30

    # ---------- Constructor ----------
    def __init__(self):
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
    pos: Vector
    gui: ObjectGUI
    rows: int
    columns: int
    placed: bool = False
    hasPlaced: bool = False
    mainTileID: int = -1
    image: pygame.Surface
    rect: pygame.Rect
    direction = Direction = Direction.NORTH
    typeCase = TypeProduceCase = TypeProduceCase.EMPTY
    amount: int = 0

    elementRectangles = []
    screen = pygame.Surface((0, 0))
    tileSize = 0

    # ---------- Constructor ----------  
    def __init__(self, pos, gui, rows, columns):
        self.pos = pos
        self.gui = gui
        self.rows = rows
        self.columns = columns
        self.setImage()

    # ---------- Setters ----------
    def setImage(self):
        match self.typeCase:
            case TypeProduceCase.WATERMELON:
                image = pygame.image.load('./Resources/Images/Produce/WatermelonBin.png')
            case TypeProduceCase.BANANAS:
                image = pygame.image.load('./Resources/Images/Produce/Banana_ProduceTycoon.png')
            case TypeProduceCase.APPLES:
                image = pygame.image.load('./Resources/Images/Produce/Apple.png')
            case TypeProduceCase.TOMATOES:
                image = pygame.image.load('./Resources/Images/Produce/Tomato.png')
            case TypeProduceCase.EMPTY:
                image = pygame.image.load('./Resources/Images/Produce/WatermelonBin.png')
        self.configureImage(image)

    def configureImage(self, image):
        self.image = pygame.transform.scale(image, (ObjectInfo.tileSize * self.columns, ObjectInfo.tileSize * self.rows))
        self.image = pygame.transform.rotate(self.image, self.direction * -90)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos.x, self.pos.y)

    def save(self):
        return {
            'rows': self.rows,
            'columns': self.columns,
            'tileSize': ObjectInfo.tileSize,
            'placed': self.placed,
            'hasPlaced': self.hasPlaced,
            'mainTileID': self.mainTileID,
            'direction': self.direction,
            'typeCase': self.typeCase.value,
            'amount': self.amount
        }

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
        tileSize = ObjectInfo.tileSize

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
        if self.info.typeCase is not TypeProduceCase.EMPTY:
            TYPE = self.info.typeCase.value
            PRODUCE = Produce.data[TYPE]
            # Adds the produce from the case back into the player data to be used again
            PRODUCE['amount'] += self.info.amount
            # Set amount back to 0 to add the new type of produce too it
            self.info.amount = 0
        # Return nothing if the type is the same
        if self.info.typeCase is typeCase:
            return
        self.info.typeCase = typeCase

    def setDirection(self):
        self.info.direction = getNextDirection(self.info.direction)

    # ---------- Getters ----------
    def getOffset(self, mousePos):
        return ObjectInfo.tileSize - mousePos % ObjectInfo.tileSize

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
        if self.info.typeCase is TypeProduceCase.EMPTY:
            print("---- Cannot add produce to EMPTY case ----")
            return
        TYPE = self.info.typeCase.value
        PRODUCE = Produce.data[TYPE]
        if PRODUCE['amount'] == 0:
            print("---- Insufficient produce ----")
            return
        self.info.amount += 1
        print(f"{PRODUCE['name']}: {self.info.amount}")
        PRODUCE['amount'] -= 1

    def removeProduce(self):
        if self.info.typeCase is TypeProduceCase.EMPTY:
            print("---- Cannot remove produce from EMPTY case ----")
            return
        TYPE = self.info.typeCase.value
        PRODUCE = Produce.data[TYPE]
        if self.info.amount == 0:
            print("---- Insufficient produce ----")
            return
        self.info.amount -= 1
        print(f"{PRODUCE['name']}: {self.info.amount}")
        PRODUCE['amount'] += 1

    def sellProduce(self):
        TYPE = self.info.typeCase.value
        PRODUCE = Produce.data[TYPE]
        if self.info.typeCase is TypeProduceCase.EMPTY:
            print("---- Cannot sell produce from EMPTY case ----")
            return
        if self.info.amount == 0:
            print("---- Insufficient produce ----")
            return
        PlayerData.data['money'] += PRODUCE.get('sell')
        self.info.amount -= 1
        print(f"{PRODUCE['name']}: {self.info.amount}")
        print(f"Money: {PlayerData.data['money']}")

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
        ObjectInfo.screen.blit(self.info.image, (self.info.pos.x, self.info.pos.y))
        if self.info.gui.active:
            self.info.gui.draw()

    def load(objectID, pos, rows, columns, placed, hasPlaced, mainTileID, direction, typeCase, amount): 
        gui = ObjectGUI()    
        info = ObjectInfo(pos, gui, rows, columns)
        info.mainTileID = mainTileID
        info.direction = direction
        info.typeCase = TypeProduceCase(typeCase)
        info.amount = amount
        info.placed = placed
        info.hasPlaced = hasPlaced
        return Object(objectID, info)

    def save(self):
        return {
            'objectID': self.objectID,
            'pos': {
                'x': self.info.pos.x,
                'y': self.info.pos.y
            },
            'info': self.info.save()
        }

class ObjectRegister:
    # Variables
    objects = []
    objectID = 0

    # ---------- Static ----------
    @staticmethod
    def setElementRectangles(elementRectangles):
        ObjectInfo.elementRectangles = elementRectangles
    
    @staticmethod
    def setScreen(screen):
        ObjectInfo.screen = screen

    @staticmethod
    def setTileSize(tileSize):
        ObjectInfo.tileSize = tileSize

    @staticmethod
    def load():
        with open ('./Resources/Playerdata/objects.json', 'r') as savefile:
            for currentObject in json.load(savefile):
                objectID = currentObject['objectID']
                pos = Vector(currentObject['pos']['x'], currentObject['pos']['y'])
                rows = currentObject['info']['rows']
                columns = currentObject['info']['columns']
                placed = currentObject['info']['placed']
                hasPlaced = currentObject['info']['hasPlaced']
                mainTileID = currentObject['info']['mainTileID']
                direction = currentObject['info']['direction']
                typeCase = currentObject['info']['typeCase']
                amount = currentObject['info']['amount']
                ObjectRegister.objects.append(Object.load(objectID, pos, rows, columns, placed, hasPlaced, mainTileID,  direction, typeCase, amount))

                ObjectRegister.objectID = objectID + 1

    @staticmethod
    def save():
        objectList = []
        for currentObject in ObjectRegister.objects:
            objectList.append(currentObject.save())
        with open ('./Resources/Playerdata/objects.json', 'w') as savefile:
            json.dump(objectList, savefile, indent=4)

    # ---------- Constructor ----------
    def __init__(self, pos, rows, columns):
        self.objects.append(self.generateObject(pos, rows, columns))

    # ---------- Helpers ----------
    def generateObjectID(self):
        objectID = ObjectRegister.objectID
        ObjectRegister.objectID += 1
        return objectID

    def generateObject(self, pos, rows, columns):
        objectID = self.generateObjectID()    
        gui = ObjectGUI()    
        info = ObjectInfo(pos, gui, rows, columns)
        return Object(objectID, info)
    