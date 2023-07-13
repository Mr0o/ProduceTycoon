import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.UserInterface.objectButton import ObjectButton

class DropdownButton(Button):
    def __init__(self, screen: pygame.Surface, pos: Vector, text: str):
        super().__init__(screen, pos, text)

        self.buttons: list[ObjectButton] = []

    def events(self, mouseClicked: bool = False):
        if self.isOn:
            for button in self.buttons:
                button.events(mouseClicked)
        super().events(mouseClicked)
    
    def update(self):
        super().update()

        for button in self.buttons:
            button.update()

    def draw(self):
        if self.isOn:
            for button in self.buttons:
                button.draw()
        super().draw()