import pygame

from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.text import Text
from ProduceTycoonGame.playerData import PlayerData
from ProduceTycoonGame.produce import Produce, Watermelon, Bananas, Apples, Tomatoes

class ShopMenu():
    # Variables
    pos: Vector
    width: int
    height: int
    color: tuple
    active: bool = False
    rect: pygame.Rect
    
    # Static Variables
    buttons = []
    screen = pygame.Surface((0, 0))

    def openGUI(self):
        self.active = True

    def exitGUI(self):
        self.active = False

    def buyWatermelon(self):
        if PlayerData.money < 100:
            print("---- Insufficient funds ----")
            return
        PlayerData.money -= Watermelon.buy
        Watermelon.amount += 1
        print("---- Purchased watermelon ----")

    def buyBananas(self):
        if PlayerData.money < 100:
            print("---- Insufficient funds ----")
            return
        PlayerData.money -= Bananas.buy
        Bananas.amount += 1
        print("---- Purchased bananas ----")

    def buyApples(self):
        if PlayerData.money < 100:
            print("---- Insufficient funds ----")
            return
        PlayerData.money -= Apples.buy
        Apples.amount += 1
        print("---- Purchased apples ----")

    def buyTomatoes(self):
        if PlayerData.money < 100:
            print("---- Insufficient funds ----")
            return
        PlayerData.money -= Tomatoes.buy
        Tomatoes.amount += 1
        print("---- Purchased tomatoes ----")

    # Static methods
    @staticmethod
    def setScreen(screen):
        ShopMenu.screen = screen

    x = 0
    y = 0
    def defineXandY(self):
        ShopMenu.x = self.pos.x + 10
        ShopMenu.y = self.pos.y + 10

    def createButton(self, name: str, width: int, height: int, func: callable):
        button = Button(Vector(ShopMenu.x, ShopMenu.y), name, width, height, func)
        ShopMenu.x += 20 + width
        if ShopMenu.x + width > self.width + self.pos.x:
            ShopMenu.x = self.pos.x + 20
            ShopMenu.y += 20
        return button

    def createButtonWithPos(self, name: str, pos: Vector, width: int, height: int, func: callable):
        return Button(pos, name, width, height, func)

    def createButtons(self):
        size = 4
        offset = 20 * size
        buttonWidth = int((self.width - offset) / size)
        buttonHeight = int((self.height - offset) / size)
        return [
            self.createButton('Watermelon', buttonWidth, buttonHeight, self.buyWatermelon),
            self.createButton('Bananas', buttonWidth, buttonHeight, self.buyBananas),
            self.createButton('Apples', buttonWidth, buttonHeight, self.buyApples),
            self.createButton('Tomatoes', buttonWidth, buttonHeight, self.buyTomatoes),

            self.createButtonWithPos('X', self.pos, 20, 20, self.exitGUI)
        ]

    def __init__(self, pos: Vector, width: int, height: int):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = (122, 238, 186)

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        ShopMenu.defineXandY(self)

        ShopMenu.buttons = self.createButtons()

    # Main methods
    def events(self):
        if self.active:
            for button in reversed(ShopMenu.buttons):
                button.events()

    def draw(self):
        if self.active:
           pygame.draw.rect(self.screen, self.color, self.rect)
           pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
           for button in ShopMenu.buttons:
               button.draw()
      