import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.events import eventOccured
from ProduceTycoonGame.objectRegister import Object, ObjectRegister
from ProduceTycoonGame.playerData import PlayerData
from ProduceTycoonGame.produce import Produce
from ProduceTycoonGame.tileMap import TileMap # This is required by ObjectRegister (CAN WE DECOUPLE THIS?)

from ProduceTycoonGame.UserInterface.text import Text
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.UserInterface.clock import Clock
from ProduceTycoonGame.UserInterface.mainMenu import MainMenu
from ProduceTycoonGame.UserInterface.shopMenu import ShopMenu
from ProduceTycoonGame.UserInterface.messageBox import MessageBox

# Helper Functions
def createObject(pos: Vector, width: int, height: int):
    return ObjectRegister(pos, width, height)

def saveGame(save):
    ObjectRegister.save(save)
    PlayerData.save(save)
    Produce.save(save)

    #Game.running = False

def exitGame():
    #Game.running = False
    return

class GUI:
    """
    Contains all the GUI elements
    \n Intended to seperate the GUI specific logic from the game class
    """
    screen: pygame.Surface
    WIDTH: int
    HEIGHT: int

    savePrompt: pygame.Rect
    savePromptText: Text
    savePromptYesButton: Button
    savePromptNoButton: Button
    hideGUI: bool

    # tileMap - This is required by ObjectRegister (CAN WE DECOUPLE THIS?)
    tileMap: TileMap
    @staticmethod
    def setTileMap(tileMap: TileMap):
        GUI.tileMap = tileMap
        ObjectRegister.setTileSize(tileMap.tileSize)

    @staticmethod
    def setScreen(screen: pygame.Surface):
        """
        Set the screen for all the GUI elements
        """
        GUI.screen = screen
        Button.setScreen(GUI.screen)
        Text.setScreen(GUI.screen)
        MainMenu.setScreen(GUI.screen)
        ShopMenu.setScreen(GUI.screen)

    def createSavePrompt(self):
        self.savePrompt = pygame.Rect(self.WIDTH / 4, self.HEIGHT / 4, self.WIDTH / 2, self.HEIGHT / 2)
        self.savePromptText = Text(Vector(self.WIDTH / 4, self.HEIGHT / 4), 400, 150, "Would you like to save your game?")
        self.savePromptYesButton = Button(Vector(self.WIDTH / 4 + 80, self.HEIGHT / 4 + 220), "Yes", 40, 40, lambda: saveGame(MainMenu.currentSave))
        self.savePromptNoButton = Button(Vector(self.WIDTH / 4 + 280, self.HEIGHT / 4 + 220), "No", 40, 40, lambda: exitGame())

    def drawSavePrompt(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.savePrompt)
        pygame.draw.rect(self.screen, (0, 0, 0), self.savePrompt, 2)
        self.savePromptText.draw()
        self.savePromptYesButton.draw()
        self.savePromptNoButton.draw()

    def savePromptEvents(self):
        self.drawSavePrompt()
        self.savePromptYesButton.events()
        self.savePromptNoButton.events()

    def __init__(self):
        # buttons
        object4x4Args = (Vector(0, 0), 4, 4)
        object1x1Args = (Vector(0, 0), 1, 1)
        self.buttons: list[Button] = []
        self.button4x4 = Button(Vector(0, 0), "4x4 Tile", 60, 20, lambda: createObject(*object4x4Args))
        self.buttons.append(self.button4x4)
        self.button1x1 = Button(Vector(60, 0), "1x1 Tile", 60, 20, lambda: createObject(*object1x1Args))
        self.buttons.append(self.button1x1)
        #self.moveObjects = Button(Vector(120, 0), "Move Objects", 120, 20)
        self.shopMenu = ShopMenu(Vector(GUI.WIDTH / 4, GUI.HEIGHT / 4), GUI.WIDTH / 2, GUI.HEIGHT / 2)
        self.openShop = Button(Vector(240, 0), "Shop", 60, 20, self.shopMenu.openGUI)
        self.buttons.append(self.openShop)

        self.mainMenu = MainMenu(self.WIDTH, self.HEIGHT)

        self.hideGUI = False
        self.moveObject = False

        ### placed objects (CAN WE DECOUPLE THIS FROM THE GUI?) ###
        self.objects: list[Object] = []
        self.elements: list[pygame.Rect] = []

        # money box
        moneyBoxWidth = 40
        moneyBoxHeight = 20
        moneyBoxX = 0
        moneyBoxY = self.HEIGHT - moneyBoxHeight
        self.moneyBox = pygame.Rect((moneyBoxX, moneyBoxY), (moneyBoxWidth, moneyBoxHeight))

        self.textRenderer = Text(Vector(moneyBoxX, moneyBoxY), moneyBoxWidth, moneyBoxHeight, str(PlayerData.data['money']))

        self.promptSaveGame = False
        self.createSavePrompt()

        # clock instance
        self.displayClock = Clock(pygame.time.Clock(), self.screen, Vector(self.WIDTH - 100, 0))

        # message box instance
        self.messageBox = MessageBox(self.screen)

    def events(self):
        if MainMenu.active:
            self.mainMenu.events()
            return
        
        self.messageBox.events()

        if not self.hideGUI:
            for button in self.buttons:
                button.events()

        self.setHiddenUI()

        self.shopMenu.events()

        self.displayClock.events()

        if eventOccured("escape"):
            self.promptSaveGame = True

        if self.promptSaveGame:
            self.savePromptEvents()

        ### Object event stuff (CAN WE DECOUPLE THIS FROM THE GUI?) ###
        ObjectRegister.setElementRectangles(self.elements)

        self.objects = ObjectRegister.objects

        objectPlaced = False

        for currentObject in self.objects:
            currentObject.events()

            #if not currentObject.info.placed:
                #Exit = currentObject.info.objectGUI.exitButton.events(eventOccured("leftMouseDown"))
                #if Exit:
                #    self.objects.remove(currentObject)
                #continue

            self.elements.append(currentObject.info.rect)
            #if self.moveObject:
            #    if eventOccured("leftMouseDown") and self.previousMouseClicked:
            #        self.moveObject = currentObject.moveToNewPos()
            
            # do some stuff when the object is placed (only once on the frame the object is placed)
            if currentObject.info.hasPlaced:
                currentObject.info.hasPlaced = False
                
                # set the currentObject's mainTile to changed (important for detecting changes in the tileMap)
                placedTileID = currentObject.info.mainTileID
                placedTile = self.tileMap.getTileByID(placedTileID)

                if placedTile is not None:
                    placedTile.changed = True
                    
                    objectPlaced = True

        if objectPlaced:
            # get the tiles that fall within the currentObject's rect
            placedObjectTiles = self.tileMap.getTilesInRect(self.objects[len(self.objects) - 1].info.rect)

            # remove the main tile from the list
            for tile in placedObjectTiles:
                if tile.id == self.objects[len(self.objects) - 1].info.mainTileID:
                    placedObjectTiles.remove(tile)
                    break
        self.elements = []
        ### END OF OBJECT/OBJECTREGISTER EVENTS CODE ###

        Button.HAS_CLICKED = False
        

    def update(self):
        pass

    def draw(self):
        if MainMenu.active:
            self.mainMenu.draw()
            return
        
        for currentObject in self.objects:
            currentObject.draw()
        
        for button in self.buttons:
            button.draw()

        self.displayMoney()

        self.shopMenu.draw()

        if self.promptSaveGame:
            self.drawSavePrompt()

        self.displayClock.draw()

        self.messageBox.draw()

    def displayMoney(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.moneyBox)
        pygame.draw.rect(self.screen, (0, 0, 0), self.moneyBox, 2)
        self.textRenderer.setText(str(PlayerData.data['money']))
        self.textRenderer.draw() 

    # set every element's hidden variable to the value of self.hideGUI
    def setHiddenUI(self):
        for button in self.buttons:
            self.elements.append(button.rect)
            button.active = self.hideGUI

        self.displayClock.hidden = self.hideGUI
        self.elements.append(self.displayClock.rect)
