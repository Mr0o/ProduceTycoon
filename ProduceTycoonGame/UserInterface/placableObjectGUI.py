import pygame

from ProduceTycoonGame.vectors import Vector
from enum import Enum
from ProduceTycoonGame.UserInterface.slider import Slider
from ProduceTycoonGame.UserInterface.textInputBox import TextInputBox
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.UserInterface.dropdownButton import DropdownButton

class TypeObject(Enum):
    EMPTY = 0
    WATERMELON = 1
    BANANAS = 2
    APPLES = 3
    TOMATOES = 4

class PlacableObjectGUI():
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (200, 150, 170)):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

        self.type = TypeObject.EMPTY
        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.textBox = TextInputBox(self.screen, Vector(self.pos.x + 5, self.pos.y + self.height / 2 - 20), self.width - 10, 18, (230, 120, 140))
        self.slider = Slider(self.screen, Vector(self.pos.x + 5, self.pos.y + self.height / 2 - 3), self.width - 10, 6)

        self.hidden = True

        self.typeButtonDropdown = DropdownButton(self.screen, Vector(self.pos.x + 5, self.pos.y + 5), 'Type', 50, 20, (255, 255, 255))
        self.setTypeButtons = []
        self.createButtons()
        

    def createButtons(self):
        self.setTypeButtons.append(Button(self.screen, Vector(self.pos.x + 5 - self.typeButtonDropdown.width, self.pos.y + 30), 'Watermelon', 50, 20, (255, 255, 255)))
        self.setTypeButtons.append(Button(self.screen, Vector(self.pos.x + 5 - self.typeButtonDropdown.width, self.pos.y + 50), 'Bananas', 50, 20, (255, 255, 255)))
        self.setTypeButtons.append(Button(self.screen, Vector(self.pos.x + 5 - self.typeButtonDropdown.width, self.pos.y + 70), 'Apples', 50, 20, (255, 255, 255)))
        self.setTypeButtons.append(Button(self.screen, Vector(self.pos.x + 5 - self.typeButtonDropdown.width, self.pos.y + 90), 'Tomatoes', 50, 20, (255, 255, 255)))

    def events(self, mouseClicked: bool = False, events: list = []):
        if self.hidden:
            return

        self.textBox.events(events)
        self.slider.events(mouseClicked)

        if self.typeButtonDropdown.events(mouseClicked):
            for button in self.setTypeButtons:
                if button.events(mouseClicked):
                    match button.text:
                        case 'Watermelon':
                            self.type = TypeObject.WATERMELON
                            #print("Watermelon")
                        case 'Bananas':
                            self.type = TypeObject.BANANAS
                            #print("Bananas")
                        case 'Apples':
                            self.type = TypeObject.APPLES
                            #print("Apples")
                        case 'Tomatoes':
                            self.type = TypeObject.TOMATOES
                            #print("Tomatoes")
                        case _:
                            self.type = TypeObject.EMPTY

    
    def update(self):
        if self.hidden:
            self.typeButtonDropdown.isSelected = False
            return
        
        self.textBox.update()
        self.slider.update()

    def draw(self):
        if self.hidden:
            return

        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)

        self.textBox.draw()
        self.slider.draw()
        self.typeButtonDropdown.draw()
        if self.typeButtonDropdown.isSelected:
            for button in self.setTypeButtons:
                button.draw()
        