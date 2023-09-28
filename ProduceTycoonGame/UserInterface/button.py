import pygame

from ProduceTycoonGame.events import eventOccured
from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.text import Text

from enum import Enum

# check for debug mode flag in args
import sys
debug = False
if len(sys.argv) > 1:
    if "--debug" in sys.argv or "-d" in sys.argv:
        debug = True

class ButtonState(Enum):
    HIDDEN = 0,
    DISABLED = 1,
    ENABLED = 2,
    #FOCUSED = 3,
    HOVERED = 4,
    CLICKED = 5,

class ButtonInfo:
    pos: Vector
    name: str
    width: int
    height: int
    func: callable
    baseImage: pygame.Surface
    selectedImage: pygame.Surface
    color: tuple[int, int, int]= (110, 190, 210)
    active: bool = True
    state: ButtonState = ButtonState.ENABLED

    def __init__(self, pos, name, width, height, func, baseImage, selectedImage):
        self.pos = pos
        self.name = name
        self.width = width
        self.height = height
        self.func = func
        self.baseImage = baseImage
        self.selectedImage = selectedImage

class Button:
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
    def __init__(self, pos: Vector, name: str, width: int, height: int, func: callable, baseImage = None, selectedImage = None):
        self.text = createText(pos, width, height, name)
        self.rect = createRect(pos, width, height)
        self.info = createInfo(pos, name, width, height, func, baseImage, selectedImage)


    # main methods
    def events(self):
        if not self.info.active or Button.HAS_CLICKED:
            self.into.state = ButtonState.HIDDEN
        match self.info.state:
            case ButtonState.DISABLED:
                return

        match self.info.state:
            case ButtonState.ENABLED:
                self.info.color = (110, 190, 210)
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.info.state = ButtonState.HOVERED

        match self.info.state:
            case ButtonState.HOVERED:
                self.info.color = (100, 170, 210)
                if eventOccured("leftMouseDown"):
                    self.info.state = ButtonState.CLICKED
                else:
                    self.info.state = ButtonState.ENABLED

        match self.info.state:
            case ButtonState.CLICKED:
                self.info.color = (240, 140, 180)
                if eventOccured("leftMouseUp"):
                    self.info.func()
                    self.info.state = ButtonState.ENABLED

        match self.info.state:
            case ButtonState.HIDDEN:
                return
    
    def draw(self, screen: pygame.Surface = Text.screen):
        if self.info.state is ButtonState.HIDDEN:
            return

        #if self.image is not None:
        #    Button.screen.blit(self.info.image, (self.info.pos.x, self.info.pos.y))
        pygame.draw.rect(Button.screen, self.info.color, self.rect)
        pygame.draw.rect(Button.screen, (0, 0, 0), self.rect, 2)
        self.text.draw()

        if debug:
            pygame.draw.rect(Button.screen, (255, 255, 0), self.rect, 1)

def createText(pos, width, height, name):
    return Text(pos, width, height, name)

def createRect(pos, width, height):
    return pygame.Rect((pos.x, pos.y), (width, height))

def createInfo(pos, name, width, height, func, baseImage, selectedImage):
    return ButtonInfo(pos, name, width, height, func, baseImage, selectedImage)


        

        


        