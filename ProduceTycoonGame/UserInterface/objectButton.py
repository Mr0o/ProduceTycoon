import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.tileMap import TileMap
from ProduceTycoonGame.placableObject import PlacableObject

class ObjectButton(Button):
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, text: str):
        super().__init__(screen, pos, text, False)

        width = self.screen.get_height() // 25 * 3
        height = self.screen.get_height() // 25 * 3
        self.object = PlacableObject(self.screen, Vector(0, 0), tileMap, width, height)
        self.showRect = False
    
    def events(self, mouseClicked: bool = False):
        collideBut = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.showRect:
            self.object.events(mouseClicked, collideBut)
        super().events(mouseClicked)
        if self.isSelected:
            self.object.showRect = True
            self.isSelected = False

    def update(self):
        super().update()
        self.showRect = self.object.showRect
        if self.showRect:
            self.object.update()
        

    def draw(self):
        if self.showRect:
            self.object.draw()
        super().draw()
