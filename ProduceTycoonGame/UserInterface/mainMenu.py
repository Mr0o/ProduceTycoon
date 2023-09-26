import pygame
import os

from ProduceTycoonGame.events import eventOccured
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.UserInterface.text import Text
from ProduceTycoonGame.UserInterface.textInputBox import TextInputBox
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.produce import Produce
from ProduceTycoonGame.playerData import PlayerData
from ProduceTycoonGame.objectRegister import ObjectRegister

from enum import Enum

PlayerDataFilePath = "./Resources/Playerdata/"

# ---------- Helper Functions ---------- #
def load(filePath):
    MainMenu.currentSave = filePath

    if not os.path.exists(filePath):
        os.mkdir(filePath)
        createInitialSave(filePath)

    ObjectRegister.load(filePath)
    PlayerData.load(filePath)
    Produce.load(filePath)

    MainMenu.active = False

def createInitialSave(filePath) -> None:
    Produce.save(filePath)
    PlayerData.save(filePath)
    ObjectRegister.save(filePath)

def getSaves() -> list[Button]: 
    playerdataPath = PlayerDataFilePath
    if not os.path.exists(playerdataPath):
        os.mkdir(playerdataPath)

    saveDir = os.listdir(playerdataPath)

    # sort the saveDir alphabetically
    saveDir.sort()

    saveButtons = []
    x = 150
    for save in saveDir:
        savePath = PlayerDataFilePath + save + "/"
        saveButtons.append(Button(Vector(200, x), save, 400, 50, lambda save=savePath: load(save)))
        x += 50

    return saveButtons

class MainMenu:
    # Variables
    width: int
    height: int
    loadSave: Button
    newSave: Button
    active: bool = True
    saveButtons: list[Button]
    
    # ---------- Save Prompt ---------- #
    savePrompt: pygame.Rect
    savePromptText: Text
    savePromptTextInput: TextInputBox
    savePromptSaveButton: Button
    savePath: str

    # ---------- Static Variables ---------- #
    screen = pygame.Surface((0,0))
    currentSave = ""
    SHOW_SAVES = False
    CREATE_SAVE = False

    # ---------- Instance Methods ---------- #
    def __init__(self, width, height):
        self.width = width
        self.height = height

        MainMenu.screen = pygame.display.set_mode((self.width, self.height))
        MainMenu.screen.fill((0, 0, 0)) 

        self.background = pygame.Rect(0, 0, self.width, self.height)

        self.loadSave = Button(Vector(0, 0), "Load Save", 100, 50, lambda: self.showSaves())
        self.newSave = Button(Vector(0, 50), "New Save", 100, 50, lambda: self.promptNewSave())

        self.saveButtons = getSaves()

        self.createSavePrompt()

    # ---------- Helpers ---------- #
    def promptNewSave(self):
        MainMenu.CREATE_SAVE = not MainMenu.CREATE_SAVE

    def showSaves(self):
        MainMenu.SHOW_SAVES = not MainMenu.SHOW_SAVES

    def createSavePrompt(self):
        self.savePrompt = pygame.Rect(200, 200, 400, 200)

        self.savePromptText = Text(Vector(self.savePrompt.x, self.savePrompt.y), 400, 50, "Save Name:")
        self.savePromptTextInput = TextInputBox(MainMenu.screen, Vector(self.savePrompt.x, self.savePrompt.y + 50), 400, 50)

        self.savePath = PlayerDataFilePath + self.savePromptTextInput.getText() + "/"

        self.savePromptSaveButton = Button(Vector(self.savePrompt.x, self.savePrompt.y + 100), "Save", 400, 50, lambda: load(self.savePath))
        self.cancelSaveButton = Button(Vector(self.savePrompt.x, self.savePrompt.y + 150), "Cancel", 400, 50, lambda: self.newSave())

    # ---------- Main Methods ---------- #
    def events(self):
        self.loadSave.events()
        self.newSave.events()

        if MainMenu.SHOW_SAVES:
            for save in self.saveButtons:
                save.events()

        if MainMenu.CREATE_SAVE:
            self.savePromptTextInput.events()
            self.savePath = PlayerDataFilePath + self.savePromptTextInput.getText() + "/"
            self.savePromptSaveButton.events()

        Button.HAS_CLICKED = False

    def draw(self):
        pygame.draw.rect(MainMenu.screen, (247, 120, 98), self.background)

        self.loadSave.draw(MainMenu.screen)
        self.newSave.draw(MainMenu.screen)

        if MainMenu.SHOW_SAVES:
            for save in self.saveButtons:
                save.draw(MainMenu.screen)

        if MainMenu.CREATE_SAVE:
            pygame.draw.rect(MainMenu.screen, (130, 40, 160), self.savePrompt)
            self.savePromptText.draw()
            self.savePromptTextInput.draw()
            self.savePromptSaveButton.draw()

        pygame.display.update()


    

