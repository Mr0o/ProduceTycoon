import pygame
import json
import os

from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.UserInterface.text import Text
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.produce import Produce
from ProduceTycoonGame.playerData import PlayerData
from ProduceTycoonGame.objectRegister import ObjectRegister

from enum import Enum

class FilePath(Enum):
    PRODUCE = "produce.json"
    PLAYER_DATA = "playerData.json"
    OBJECTS = "objects.json"

class MainMenu:
    # Variables
    width: int
    height: int
    loadSave: Button
    newSave: Button
    active: bool = True
    saves: []

    currentSave = ""

    # Static Variables
    screen = pygame.Surface((0,0))
    SHOW_SAVES = False

    def __init__(self, width, height):
        self.width = width
        self.height = height

        MainMenu.screen = pygame.display.set_mode((self.width, self.height))
        MainMenu.screen.fill((0, 0, 0)) 

        self.background = pygame.Rect(0, 0, self.width, self.height)

        self.loadSave = Button(Vector(0, 0), "Load Save", 100, 50, lambda: self.showSaves())
        self.newSave = Button(Vector(0, 50), "New Save", 100, 50, lambda: self.newSave())

        self.saves = self.getSaves()

    def showSaves(self):
        MainMenu.SHOW_SAVES = not MainMenu.SHOW_SAVES
        print(MainMenu.SHOW_SAVES)

    def getSaves(self): 
        playerDataPath = "Resources\\PlayerData\\"
        saveDir = os.listdir(playerDataPath)

        saveButtons = []
        for save in saveDir:
            savePath = "./Resources/PlayerData/" + save + "/"
            saveButtons.append(Button(Vector(200, 150), save, 400, 50, lambda: self.load(savePath)))

        return saveButtons

    def load(self, filePath):
        MainMenu.currentSave = filePath
        objectsPath = filePath + FilePath.OBJECTS.value 
        ObjectRegister.load(objectsPath)

        playerDataPath = filePath + FilePath.PLAYER_DATA.value
        PlayerData.load(playerDataPath)

        producePath = filePath + FilePath.PRODUCE.value
        Produce.load(producePath)

        MainMenu.active = False

    def newSave(self):
        pass

    def events(self):
        self.loadSave.events()
        self.newSave.events()

        if MainMenu.SHOW_SAVES:
            for save in self.saves:
                save.events()

        Button.HAS_CLICKED = False

    def draw(self):
        pygame.draw.rect(MainMenu.screen, (239, 120, 178), self.background)

        self.loadSave.draw(MainMenu.screen)
        self.newSave.draw(MainMenu.screen)

        if MainMenu.SHOW_SAVES:
            for save in self.saves:
                save.draw(MainMenu.screen)

        pygame.display.update()


    

