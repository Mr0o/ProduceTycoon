import pygame

from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.text import Text
from ProduceTycoonGame.playerData import PlayerData
from ProduceTycoonGame.produce import Produce

# ---------- Helper Functions ---------- 
def buy(PRODUCE: dict):
        if PlayerData.money < PRODUCE['buy']:
            print("---- Insufficient funds ----")
            return
        PlayerData.money -= PRODUCE['buy']
        PRODUCE['amount'] += 1
        print(f"---- Purchased {PRODUCE['name']} ----")

def getImage(sheet: pygame.Surface, x: int, y: int, width: int, height: int, scale: int = 1):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (x, y, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((0, 0, 0))
    return image

class ShopMenu():
    # Variables
    pos: Vector
    width: int
    height: int
    color: tuple
    active: bool = False
    rect: pygame.Rect
    image: pygame.Surface
    
    # Static Variables
    buttons = []
    screen = pygame.Surface((0, 0))
    x = 0
    y = 0

    # ---------- Static methods ---------- 
    @staticmethod
    def setScreen(screen):
        ShopMenu.screen = screen

    def defineXandY(self):
        ShopMenu.x = self.pos.x + 20
        ShopMenu.y = self.pos.y + 20

    # ---------- Constructor ----------
    def __init__(self, pos: Vector, width: int, height: int):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = (122, 238, 186)

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))
        self.image = pygame.image.load('./Resources/Images/GUI/ShopMenu.png').convert_alpha()
        self.image.set_colorkey((0, 0, 0))

        self.buttonImage = pygame.image.load('./Resources/Images/GUI/ShopMenuButtons.png').convert_alpha()

        self.buttonImages = [getImage(self.buttonImage, 0, 0, 75, 55), getImage(self.buttonImage, 75, 0, 75, 55), getImage(self.buttonImage, 150, 0, 75, 55), getImage(self.buttonImage, 225, 0, 75, 55), getImage(self.buttonImage, 0, 55, 75, 55), getImage(self.buttonImage, 75, 55, 75, 55), getImage(self.buttonImage, 150, 55, 75, 55), getImage(self.buttonImage, 225, 55, 75, 55)]

        ShopMenu.defineXandY(self)

        ShopMenu.buttons = self.createButtons()

    # ---------- Helpers ----------
    def openGUI(self):
        self.active = True

    def exitGUI(self):
        self.active = False

    def createButton(self, name: str, width: int, height: int, func: callable, baseImage: pygame.Surface, selectedImage: pygame.Surface):
        button = Button(Vector(ShopMenu.x, ShopMenu.y), name, width, height, func, baseImage, selectedImage)
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
        buttonWidth = 75 #int((self.width - offset) / size)
        buttonHeight = int((self.height - offset) / size)
        WATERMELON = Produce.data.get('Watermelon')
        BANANAS = Produce.data.get('Bananas')
        APPLES = Produce.data.get('Apples')
        TOMATOES = Produce.data.get('Tomatoes')
        return [
            self.createButton(WATERMELON['name'], buttonWidth, buttonHeight, lambda: buy(WATERMELON), self.buttonImages[0], self.buttonImages[4]),
            self.createButton(BANANAS['name'], buttonWidth, buttonHeight, lambda: buy(BANANAS), self.buttonImages[1], self.buttonImages[5]),
            self.createButton(APPLES['name'], buttonWidth, buttonHeight, lambda: buy(APPLES), self.buttonImages[2], self.buttonImages[6]),
            self.createButton(TOMATOES['name'], buttonWidth, buttonHeight, lambda: buy(TOMATOES), self.buttonImages[3], self.buttonImages[7]),

            self.createButtonWithPos('X', self.pos, 20, 20, self.exitGUI)
        ]

    # ---------- Main methods ---------- 
    def events(self):
        if self.active:
            for button in reversed(ShopMenu.buttons):
                button.events()

    def draw(self):
        if self.active:
           ShopMenu.screen.blit(self.image, (self.pos.x, self.pos.y))
           for button in ShopMenu.buttons:
               button.draw()
      