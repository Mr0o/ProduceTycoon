import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.UserInterface.button import Button
from ProduceTycoonGame.placableObject import PlacableObject
from ProduceTycoonGame.tileMap import TileMap

class ObjectButton(Button):
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, text: str):
        super().__init__(screen, pos, text)
        self.tileMap = tileMap

        self.widthObject = self.screen.get_height() // 25 * 3
        self.heightObject = self.screen.get_height() // 25 * 3
        self.posObject = Vector(0, 0)

        self.objects: list[PlacableObject] = []
        self.objects.append(PlacableObject(self.screen, self.posObject, self.tileMap, self.widthObject, self.heightObject))

        self.lastObject = self.objects[0]
    
    def newObject(self):
        self.objects.append(PlacableObject(self.screen, self.posObject, self.tileMap, self.widthObject, self.heightObject))

        self.lastObject = self.objects[len(self.objects) - 1]
    
    def events(self, mouseClicked: bool = False):
        collideBut = self.rect.collidepoint(pygame.mouse.get_pos())

        if self.isOn:
            if self.lastObject.isPlaced:
                self.isOn = False
                self.newObject()
            else:
                self.lastObject.showRect = True
                self.lastObject.events(mouseClicked, collideBut)
        super().events(mouseClicked)
            

    def update(self):
        super().update()

        if len(self.objects) == 1:
            self.objects[0] = self.lastObject
        else:
            self.objects[len(self.objects) - 1] = self.lastObject

        for placableObject in self.objects:
            placableObject.update()
        
        

    def draw(self):
        i = 0
        for placableObject in self.objects:
            i += 1
            print(i)
            placableObject.draw()
        super().draw()
