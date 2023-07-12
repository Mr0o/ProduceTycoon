import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.placableObject import PlacableObject
from ProduceTycoonGame.tileMap import TileMap

class ObjectButton(Button):
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, text: str, objectWidth: int, objectHeight: int):
        super().__init__(screen, pos, text)
        self.tileMap = tileMap
        self.widthObject = objectWidth
        self.heightObject = objectHeight

        self.widthObject = self.screen.get_height() // 25 * objectWidth
        self.heightObject = self.screen.get_height() // 25 * objectHeight
        self.posObject = Vector(0, 0)

        self.objects: list[PlacableObject] = []
        self.objects.append(PlacableObject(self.screen, self.posObject, self.tileMap, self.widthObject, self.heightObject))

        self.lastObject = self.objects[0]
    
    def newObject(self):
        if self.create:
            self.objects.append(PlacableObject(self.screen, self.posObject, self.tileMap, self.widthObject, self.heightObject))
            self.lastObject = self.objects[len(self.objects) - 1]
            self.create = False
    
    def events(self, mouseClicked: bool = False):
        collideBut = self.rect.collidepoint(pygame.mouse.get_pos())

        if self.isOn:
            if self.lastObject.isPlaced:
                self.isOn = False
            else:
                self.lastObject.showRect = True
                self.lastObject.events(mouseClicked, collideBut)
        super().events(mouseClicked)
        self.newObject()
            

    def update(self):
        super().update()

        if len(self.objects) == 1:
            self.objects[0] = self.lastObject
        else:
            self.objects[len(self.objects) - 1] = self.lastObject

        for placableObject in self.objects:
            placableObject.update()
        
        

    def draw(self):
        for placableObject in self.objects:
            placableObject.draw()
        super().draw()
