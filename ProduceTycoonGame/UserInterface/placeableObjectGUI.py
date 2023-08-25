import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.slider import Slider
from ProduceTycoonGame.UserInterface.textInputBox import TextInputBox
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.UserInterface.dropdownButton import DropdownButton
from ProduceTycoonGame.UserInterface.text import Text

class PlaceableObjectGUI():
    def __init__(self, screen: pygame.Surface, pos: Vector, width: int, height: int, color: tuple[int, int, int] | pygame.Color = (200, 150, 170)):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

        self.rect = pygame.Rect((self.pos.x, self.pos.y), (self.width, self.height))

        self.textBox = TextInputBox(self.screen, Vector(self.pos.x + 5, self.pos.y + self.height / 2 - 20), self.width - 10, 18, (230, 120, 140))
        self.slider = Slider(self.screen, Vector(self.pos.x + 5, self.pos.y + self.height / 2 - 3), self.width - 10, 6)

        self.hidden = True
        self.type = ""

        self.typeButtonDropdown = DropdownButton(self.screen, Vector(self.pos.x + 5, self.pos.y + 5), 'Type', 50, 20, (255, 255, 255))
        self.setTypeButtons = []
        self.createButtons()
        self.objectValues = {}
        

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
                    self.type = button.text
    
    def update(self, objectValues: dict[str, int] = {}):
        if self.hidden:
            self.typeButtonDropdown.isSelected = False
            return
        self.objectValues = objectValues
        
        self.textBox.update()
        self.slider.update()

    def draw(self, printValues: str = ""):
        if self.hidden:
            return

        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)

        valuesText = Text(self.screen, Vector(self.pos.x + 5, self.pos.y + 105), self.width - 10, 20, printValues)
        valuesText.draw()

        self.textBox.draw()
        self.slider.draw()
        self.typeButtonDropdown.draw()
        if self.typeButtonDropdown.isSelected:
            for button in self.setTypeButtons:
                button.draw()

    def getType(self) -> str:
        return self.type
        