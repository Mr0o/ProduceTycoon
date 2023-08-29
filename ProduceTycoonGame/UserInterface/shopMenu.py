import pygame

from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.text import Text
from ProduceTycoonGame.valueHandler import ValueHandler

class ShopMenu():
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, playerValues: dict, color: tuple[int, int, int] | pygame.Color = (90, 140, 200)):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.playerValues = playerValues
        self.color = color

        self.playerValues = ValueHandler.getStaticValues()

        self.hidden = True
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.buttons = []
        self.exitButton = Button(Vector(self.pos.x, self.pos.y), 'X', 20, 20, (255, 0, 0))
        self.watermelonButton = Button(Vector(self.pos.x + 20, self.pos.y + 20), 'Watermelon', 100, 100, (255, 0, 0))

        currencyBoxWidth = 40
        currencyBoxHeight = 20
        currencyBoxX = self.pos.x + width - currencyBoxWidth
        currencyBoxY = self.pos.y
        self.currencyBox = pygame.Rect((currencyBoxX, currencyBoxY), (currencyBoxWidth, currencyBoxHeight))

        self.currency = 'currency'
        self.textRenderer = Text(self.screen, Vector(currencyBoxX, currencyBoxY), currencyBoxWidth, 
        currencyBoxHeight, str(self.playerValues[self.currency]))


    def events(self, mouseClicked: bool = False):
        if self.exitButton.events(mouseClicked):
            self.hidden = True
        if self.watermelonButton.events(mouseClicked):
            self.playerValues[self.currency] -= 100
            self.playerValues["Watermelon-amount"] += 1

    def update(self):
        self.textRenderer.setText(str(self.playerValues[self.currency]))

    def draw(self):
        if not self.hidden:
           pygame.draw.rect(self.screen, self.color, self.rect)
           pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
           self.exitButton.draw()
           self.watermelonButton.draw()
           self.displayCurrency()

    def displayCurrency(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.currencyBox)
        pygame.draw.rect(self.screen, (0, 0, 0), self.currencyBox, 2)
        self.textRenderer.draw()    

    def getCurrency(self):
        return self.playerValues[self.currency]