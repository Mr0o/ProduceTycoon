import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.text import Text

#class Button():
#    static_screen = pygame.Surface((0, 0))
#    def __init__(self, pos: Vector, name: str, width: int, height: int, color: tuple[int, int, int]= (200, 110, #110)):
#        self.pos = pos
#        self.name = name
#        self.width = width
#        self.height = height
#        self.color = color
#        
#        self.textRenderer = Text(Button.static_screen, self.pos, self.width, self.height, self.name)
#        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))
#
#        self.isSelected = False
#        self.hidden = False
#
#    
#    
#    def events(self, mouseClicked: bool):
#        
#
#    def draw(self):
#        if self.hidden:
#            return
#        pygame.draw.rect(Button.static_screen, self.color, self.rect)
#        pygame.draw.rect(Button.static_screen, (0, 0, 0), self.rect, 2)
#        self.textRenderer.draw()



class ButtonInfo():
    pos: Vector
    name: str
    width: int
    height: int
    func: callable
    color: tuple[int, int, int]= (110, 190, 210)
    active: bool = False
    isSelected: bool = False

    def __init__(self, pos, name, width, height, func, active = True, isSelected = False):
        self.pos = pos
        self.name = name
        self.width = width
        self.height = height
        self.func = func

        self.active = active
        self.isSelected = isSelected

class Button():
    text: Text
    rect: pygame.Rect
    info: ButtonInfo

    # static variables
    screen = pygame.Surface((0, 0))

    #static methods
    @staticmethod
    def setScreen(screen: pygame.Surface):
        Button.screen = screen

    # instance methods
    def __init__(self, pos: Vector, name: str, width: int, height: int, func: callable):
        self.text = createText(pos, width, height, name)
        self.rect = createRect(pos, width, height)
        self.info = createInfo(pos, name, width, height, func)

    # main methods
    def events(self, mouseClicked: bool):
        if not self.info.active:
            return
        # check if mouse position is on the button rect
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # if mouse is clicked and the button is not already selected
            if mouseClicked and not self.info.isSelected:
                self.info.isSelected = True
                # call the function
                self.info.func()
        if not mouseClicked:
            self.info.isSelected = False
    
    def draw(self):
        if not self.info.active:
            return
        pygame.draw.rect(Button.screen, self.info.color, self.rect)
        pygame.draw.rect(Button.screen, (0, 0, 0), self.rect, 2)
        self.text.draw()

def createText(pos, width, height, name):
    return Text(Button.screen, pos, width, height, name)

def createRect(pos, width, height):
    return pygame.Rect((pos.x, pos.y), (width, height))

def createInfo(pos, name, width, height, func):
    return ButtonInfo(pos, name, width, height, func)


        

        


        