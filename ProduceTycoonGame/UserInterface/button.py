import pygame

from ProduceTycoonGame.events import eventOccured
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.text import Text

class ButtonInfo():
    pos: Vector
    name: str
    width: int
    height: int
    func: callable
    baseImage: pygame.Surface
    selectedImage: pygame.Surface
    color: tuple[int, int, int]= (110, 190, 210)
    active: bool = True
    isSelected: bool = False

    def __init__(self, pos, name, width, height, func, baseImage, selectedImage):
        self.pos = pos
        self.name = name
        self.width = width
        self.height = height
        self.func = func
        self.baseImage = baseImage
        self.selectedImage = selectedImage

class Button():
    text: Text
    rect: pygame.Rect
    info: ButtonInfo

    # Static variables
    screen = pygame.Surface((0, 0))
    HAS_CLICKED = False

    # Static methods
    @staticmethod
    def setScreen(screen: pygame.Surface):
        Button.screen = screen

    # Instance methods
    def __init__(self, pos, name, width, height, func, baseImage = None, selectedImage = None):
        self.text = createText(pos, width, height, name)
        self.rect = createRect(pos, width, height)
        self.info = createInfo(pos, name, width, height, func, baseImage, selectedImage)


    # main methods
    def events(self):
        if not self.info.active or Button.HAS_CLICKED:
            return
        # Check if mouse position is on the button rect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # if mouse is clicked and the button is not already selected
            if eventOccured("leftMouseDown") and not self.info.isSelected:
                self.info.isSelected = True
                Button.HAS_CLICKED = True
                self.info.func()
        if not eventOccured("leftMouseDown"):
            self.info.isSelected = False
    
    def draw(self):
        if not self.info.active:
            return

        if self.info.baseImage != None and self.info.selectedImage != None:
            if self.info.isSelected:
                Button.screen.blit(self.info.selectedImage, (self.info.pos.x, self.info.pos.y))
            else:
                Button.screen.blit(self.info.baseImage, (self.info.pos.x, self.info.pos.y))
        else:
            pygame.draw.rect(Button.screen, self.info.color, self.rect)
            pygame.draw.rect(Button.screen, (0, 0, 0), self.rect, 2)
            self.text.draw()

def createText(pos, width, height, name):
    return Text(Button.screen, pos, width, height, name)

def createRect(pos, width, height):
    return pygame.Rect((pos.x, pos.y), (width, height))

def createInfo(pos, name, width, height, func, baseImage, selectedImage):
    return ButtonInfo(pos, name, width, height, func, baseImage, selectedImage)


        

        


        