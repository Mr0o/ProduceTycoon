import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tile import Type
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.valueHandler import ValueHandler
from ProduceTycoonGame.UserInterface.slider import Slider
from ProduceTycoonGame.UserInterface.textInputBox import TextInputBox
from ProduceTycoonGame.UserInterface.dropdownButton import DropdownButton
from ProduceTycoonGame.UserInterface.text import Text

from enum import Enum

class TypeObject(Enum):
    WALL = 0
    PRODUCE_CASE = 1
    REGISTER = 2

class TypeProduceCase(Enum):
    EMPTY = 'Empty'
    WATERMELON = 'Watermelon'
    BANANAS = 'Bananas'
    APPLES = 'Apples'
    TOMATOES = 'Tomatoes'

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

# Helder functions

def getNextDirection(direction):
    return direction + 1 if direction + 1 < 4 else direction - 3

def getMouseClick():
    return pygame.mouse.get_pressed()[0]

class ObjectGUI:
    typeDict: dict[str, TypeProduceCase]
    typeButtons: list[Button] = []
    activeGUI: bool

    # Positions
    x = 700; y = 3
    def __init__(self, activeGUI = False):
        
        self.typeDict = {
            'Watermelon': TypeProduceCase.WATERMELON,
            'Tomatoes': TypeProduceCase.TOMATOES,
            'Bananas':  TypeProduceCase.BANANAS,
            'Apples': TypeProduceCase.APPLES,
            'Empty': TypeProduceCase.EMPTY 
        }

        self.changeDirectionButton = self.createButton('Rotate')
        self.exitButton = self.createButton('X')

        self.typeButtons = [
            self.createButton('Watermelon'),
            self.createButton('Tomatoes'),
            self.createButton('Bananas'),
            self.createButton('Apples'),
            self.createButton('Empty')
        ]

        
        self.activeGUI = activeGUI

        ObjectGUI.x = 700; ObjectGUI.y = 3

    # Helper methods
    def createButton(self, nameButton: str):
        x = ObjectGUI.x
        y = ObjectGUI.y
        ObjectGUI.y += 20
        return Button(Vector(x, y), nameButton, 100, 20)

    # Main methods
    def events(self):
        pass
    def draw(self):
        for button in self.typeButtons:
            button.draw()

class ObjectInfo:
    screen: pygame.Surface
    position: Vector
    objectGUI: ObjectGUI
    rows: int
    colums: int
    tileSize: int
    direction: Direction
    typeCase: TypeProduceCase
    placed: bool
    hasPlaced: bool

    elementRectangles = []

    def __init__(self, screen, position, objectGUI, rows, colums, tileSize, direction = Direction.NORTH, typeCase = TypeProduceCase.WATERMELON, placed = False, hasPlaced = False):
        self.screen = screen
        self.position = position
        self.objectGUI = objectGUI
        self.rows = rows
        self.colums = colums
        self.tileSize = tileSize
        self.direction = direction
        self.typeCase = typeCase
        self.placed = placed
        self.hasPlaced = hasPlaced
        
    # Some method for changing type
    def setType(self):
        typeButtons = self.objectGUI.typeButtons
        for button in typeButtons:
            # If button is clicked
            if button.events(getMouseClick()):
                # Return type of button
                self.typeCase = self.objectGUI.typeDict[button.name]

    def setDirection(self):
        # If button is clicked
        if self.objectGUI.changeDirectionButton.events(getMouseClick()):
            self.direction = self.getNextDirection(self.direction)

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

    s_currentID = -1

    def __init__(self, objectID, info, mainTileID = -1):
        self.objectID = objectID
        self.info = info
        self.mainTileID = mainTileID
        self.setImage()
        self.configureImage(self.image)
        self.rectangle = self.createRectangle()

    # Helper methods
    def configureImage(self, image: pygame.Surface):
        self.image = pygame.transform.scale(image, (self.info.rows * self.info.tileSize, self.info.colums * self.info.tileSize))
        #self.image.rotate(self.info.direction * 90)

    def createRectangle(self):
        return self.image.get_rect()

    def updateRectangle(self, x, y):
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
        self.updateRectangle(posX, posY)

    def getOffset(self, mousePos):
        return self.info.tileSize - mousePos % self.info.tileSize

    def setImage(self):
        match self.info.typeCase:
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

    def getFrontTiles(self):
        tileMapWidth = 32
        frontTileIDs = []
        match self.info.direction:
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
    
    def openGUI(self, mouseClicked):
        # If clicked happen on object
        mouseClickedObject = mouseClicked and self.rectangle.collidepoint(pygame.mouse.get_pos())
        if mouseClickedObject:
            # Current ID is set to this object's ID
            Object.s_currentID = self.objectID
            # The first click on the object will open the GUI
            self.info.objectGUI.activeGUI = not self.info.objectGUI.activeGUI
        if Object.s_currentID is not self.objectID :
            self.info.objectGUI.activeGUI = False
        return self.info.objectGUI.activeGUI

    def placeObject(self, mouseClicked, previousMouseClick):
        if self.info.canPlace(self.rectangle) and mouseClicked and not previousMouseClick:
            self.info.placed = True
            self.info.hasPlaced = True
    
    # Main methods
    def events(self, previousMouseClick: bool = False, mouseClicked: bool = False, events: list = []):
        self.setImage()
        
        if self.info.placed:
            self.info.setType()
            self.info.setDirection()
            if self.openGUI(mouseClicked):
                self.info.objectGUI.events()
            return
 
        self.setPosition()
        self.placeObject(mouseClicked, previousMouseClick)

    def draw(self):
        self.info.screen.blit(self.image, (self.info.position.x, self.info.position.y))
        if self.info.placed and self.info.objectGUI.activeGUI:
            self.info.objectGUI.draw()
        

class ObjectRegister:
    objectID = 0
    objects = []

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
        objectGUI = ObjectGUI()    
        objectInfo = ObjectInfo(screen, position, objectGUI, rows, colums, tileSize)
        return Object(objectID, objectInfo)







#class PlaceableObjectGUI:
#    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, color: tuple[int, int, int] | #pygame.Color = (200, 150, 170)):
#        self.screen = screen
#        self.pos = pos
#        self.width = width
#        self.height = height
#        self.color = color
#
#        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))
#
#        textBoxX = self.pos.x + 5
#        textBoxY = self.pos.y + self.height / 2 - 20
#        self.textBox = TextInputBox(self.screen, Vector(textBoxX, textBoxY), self.width - 10, 18, (230, 120, 140))
#        sliderX = self.pos.x + 5
#        sliderY = self.pos.y + self.height / 2 - 3
#        self.slider = Slider(self.screen, Vector(sliderX, sliderY), self.width - 10, 6)
#
#        self.hidden = True
#        self.type = ""
#
#        self.typeButtonDropdown = DropdownButton(self.screen, Vector(self.pos.x + 5, self.pos.y + 5), 'Type', 50, #20, (255, 255, 255))
#        self.setTypeButtons = []
#        self.createButtons()
#        self.objectValues = {}
#        
#
#    def createButtons(self):
#        xPos = self.pos.x + 5 - self.typeButtonDropdown.width
#        yPos += self.pos.y + 30
#        self.setTypeButtons.append(Button(self.screen, Vector(xPos, yPos), 'Watermelon', 50, 20, (255, 255, 255)))
#        yPos += 20
#        self.setTypeButtons.append(Button(self.screen, Vector(xPos, yPos), 'Bananas', 50, 20, (255, 255, 255)))
#        yPos += 20
#        self.setTypeButtons.append(Button(self.screen, Vector(xPos, yPos), 'Apples', 50, 20, (255, 255, 255)))
#        yPos += 20
#        self.setTypeButtons.append(Button(self.screen, Vector(xPos, yPos), 'Tomatoes', 50, 20, (255, 255, 255)))
#
#    def events(self, mouseClicked: bool = False, events: list = []):
#        if self.hidden:
#            return
#
#        self.textBox.events(events)
#        self.slider.events(mouseClicked)
#
#        if self.typeButtonDropdown.events(mouseClicked):
#            for button in self.setTypeButtons:
#                if button.events(mouseClicked):
#                    self.type = button.text
#    
#    def update(self, objectValues: dict[str, int] = {}):
#        if self.hidden:
#            self.typeButtonDropdown.isSelected = False
#            return
#        self.objectValues = objectValues
#        
#        self.textBox.update()
#        self.slider.update()
#
#    def draw(self, printValues: str = ""):
#        if self.hidden:
#            return
#
#        pygame.draw.rect(self.screen, self.color, self.rect)
#        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)
#
#        valuesText = Text(self.screen, Vector(self.pos.x + 5, self.pos.y + 105), self.width - 10, 20, printValues)
#        valuesText.draw()
#
#        self.textBox.draw()
#        self.slider.draw()
#        self.typeButtonDropdown.draw()
#        if self.typeButtonDropdown.isSelected:
#            for button in self.setTypeButtons:
#                button.draw()
#
#    def getType(self) -> str:
#        return self.type
#        
#
#class PlaceableObject:
#    static_id = 0
#    static_currentID = None
#
#    def __init__(self, screen: pygame.Surface, pos: Vector, size: int, rows: int = 1, cols: int = 1, elements: list #= [], image: str = './Resources/Images/WatermelonBin.png'):
#        self.id = PlaceableObject.static_id
#        PlaceableObject.static_id += 1
#        self.screen = screen
#        self.pos = pos
#        self.size = size
#        self.rows = rows
#        self.cols = cols
#        self.elements = elements
#
#        self.image = pygame.image.load(image)
#        self.image = pygame.transform.scale(self.image, (self.rows * self.size, self.cols * self.size))
#
#        self.isPlaced = False
#        self.hasPlaced = False
#        self.canPlace = False
#        self.rect = self.image.get_rect()
#
#        self.exitButton = Button(self.screen, Vector(0, 0), 'X', 20, 20, (255, 0, 0))
#
#        self.gui = PlaceableObjectGUI(self.screen, Vector(self.screen.get_width() - 100, 25), 100, 100, (200, 150, #170))
#        self.type = typeCase.WATERMELON
#
#        self.mainTileID = -1
#        self.frontTileIDs = []
#        self.direction = Direction.NORTH
#
#        self.amount = 0
#        self.price = 0
#        self.printValues = ''
#
#
#    def checkIfCanPlace(self):
#        for element in self.elements:
#            if element.rect.colliderect(self.rect):
#                self.canPlace = False
#                break
#            else:
#                self.canPlace = True
#
#    # function looks like garbage fix later
#    def moveToNewPos(self):
#        if self.rect.collidepoint(pygame.mouse.get_pos()):
#            self.isPlaced = False
#            return self.isPlaced
#        return self.isPlaced
#    
#    def setDirection(self):
#        
#
#    def events(self):
#        
#        self.checkIfCanPlace()
#
#        mousePos = pygame.mouse.get_pos()
#        #offset between next tile and mouse position for both x and y
#        
#        #new position for the object
#        
#            
#        # changes tile type to object if rect collides with tile and mouse is clicked
#        if self.canPlace and not mouseClicked and previousMouseClick:
#            self.isPlaced = True
#            self.hasPlaced = True
#
#    def update(self):
#        if self.isPlaced:
#            self.gui.update()
#
#            # self.printValues = (self.type.value + ': ' + 
#            #                     str(self.objectValues.getValue('quantity')) + '\n\t' + 
#            #                     str(self.objectValues.getValue('price')))
#
#            match self.gui.getType():
#                case TypeObject.WATERMELON.value:
#                    self.image = pygame.image.load('./Resources/Images/WatermelonBin.png')
#                    self.type = TypeObject.WATERMELON
#                case TypeObject.BANANAS.value:
#                    self.image = pygame.image.load('./Resources/Images/Banana_ProduceTycoon.png')
#                    self.type = TypeObject.BANANAS
#                case TypeObject.APPLES.value:
#                    self.image = pygame.image.load('./Resources/Images/Apple_ProduceTycoon.png')
#                    
#                case TypeObject.TOMATOES.value:
#                    self.image = pygame.image.load('./Resources/Images/Tomato.png')
#                    self.type = TypeObject.TOMATOES
#                case _:
#                    self.image = pygame.image.load('./Resources/Images/WatermelonBin.png')
#                    self.type = TypeObject.EMPTY
#            return
#
#        
#
#    def draw(self):
#        
#        self.screen.blit(self.image, self.rect.topleft)
#
#        if not self.isPlaced:
#            self.exitButton.draw()
#
#        self.gui.draw(self.printValues)
#
#    def getPos(self):
#        return self.pos
#
#    def getPlaced(self):
#        return self.isPlaced

    