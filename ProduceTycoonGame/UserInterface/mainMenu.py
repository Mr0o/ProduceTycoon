import pygame
import os

from ProduceTycoonGame.events import eventOccured, postEvent
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.UserInterface.text import Text
from ProduceTycoonGame.UserInterface.textInputBox import TextInputBox
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.produce import Produce
from ProduceTycoonGame.playerData import PlayerData
from ProduceTycoonGame.objectRegister import ObjectRegister
from ProduceTycoonGame.UserInterface.messageBox import MessageBox

from enum import Enum

PlayerDataFilePath = "./Resources/Playerdata/"

# ---------- Helper Functions ---------- #
def createInitialSave(filePath) -> None:
    Produce.save(filePath)
    PlayerData.save(filePath)
    ObjectRegister.save(filePath)

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
    messageBox: MessageBox

    # ---------- Static Variables ---------- #
    screen = pygame.Surface((0,0))
    currentSave = ""
    SHOW_SAVES = False
    CREATE_SAVE = False

    @staticmethod
    def setScreen(screen: pygame.Surface):
        MainMenu.screen = screen

    # ---------- Instance Methods ---------- #
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.background = pygame.Rect(0, 0, self.width, self.height)

        self.loadSave = Button(Vector(0, 0), "Load Save", 100, 50, lambda: self.showSaves())
        self.newSave = Button(Vector(0, 50), "New Save", 100, 50, lambda: self.promptNewSave())

        self.saveButtons = self.getSaves()

        self.createSavePrompt()

        self.messageBox = MessageBox(MainMenu.screen)

    # ---------- Getters ---------- #
    def getSaves(self,) -> list[Button]: 
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
            saveButtons.append(Button(Vector(200, x), save, 400, 50, lambda save=savePath: self.load(save)))
            x += 50

        return saveButtons

    # ---------- Helpers ---------- #
    def promptNewSave(self):
        MainMenu.CREATE_SAVE = not MainMenu.CREATE_SAVE
        MainMenu.SHOW_SAVES = False

    def showSaves(self):
        MainMenu.SHOW_SAVES = not MainMenu.SHOW_SAVES
        MainMenu.CREATE_SAVE = False

    def load(self, filePath):
        MainMenu.currentSave = filePath

        if MainMenu.CREATE_SAVE:
            MainMenu.CREATE_SAVE = False
            if not os.path.exists(filePath):
                os.mkdir(filePath)
                createInitialSave(filePath)
            else:
                print("Save already exists")
                postEvent("postMessage", eventData="Save already exists")
                print(eventOccured("postMessage"))
                return

        ObjectRegister.load(filePath)
        PlayerData.load(filePath)
        Produce.load(filePath)

        MainMenu.active = False

    def createSavePrompt(self):
        self.savePrompt = pygame.Rect(200, 200, 400, 200)

        self.savePromptText = Text(Vector(self.savePrompt.x, self.savePrompt.y), 400, 50, "Save Name:")
        self.savePromptTextInput = TextInputBox(MainMenu.screen, Vector(self.savePrompt.x, self.savePrompt.y + 50), 400, 50)

        self.savePath = PlayerDataFilePath + self.savePromptTextInput.getText() + "/"

        self.savePromptSaveButton = Button(Vector(self.savePrompt.x, self.savePrompt.y + 100), "Save", 400, 50, lambda: self.load(self.savePath))
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

        self.messageBox.events()

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

        self.messageBox.draw()

        pygame.display.update()


    

