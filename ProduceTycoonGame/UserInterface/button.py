import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type
from ProduceTycoonGame.UserInterface.elements import Element


class Button(Element):
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, isSelected = False, text = "3x3"):
        super().__init__(screen, pos, tileMap)
        self.isSelected = isSelected
        self.text = text
        self.color = (40, 120, 180)
        self.showRect = False
        self.posBut = Vector(0, 0)

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
        self.interactableRect = pygame.Rect(0, 0, self.screen.get_height() // 25 * 3, self.screen.get_height() // 25 * 3)
    
    def events(self, mouseClicked: bool):
        if self.showRect:
            for tile in self.tileMap.tileMapGrid:
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    self.posBut.x = tile.pos.x + tile.size / 2 
                    self.posBut.y = tile.pos.y + tile.size / 2
                if self.interactableRect.colliderect(tile.rect) and mouseClicked and not(self.rect.collidepoint(pygame.mouse.get_pos())):
                    tile.type = Type.INTERACTABLE
                    self.tileMap.staticSurface = createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)
                    self.showRect = False

        if self.rect.collidepoint(pygame.mouse.get_pos()) and mouseClicked:
            self.isSelected != self.isSelected
            self.showRect = True
        
        if self.isSelected:
            self.color = (200, 120, 180)
        


    def update(self):
        self.interactableRect.center = (self.posBut.x, self.posBut.y)
        createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)
        

    def draw(self):
        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        text = objectSize.render(self.text, True, (0, 0, 0))

        if self.showRect:
            pygame.draw.rect(self.screen, self.color, self.interactableRect)

        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
        self.screen.blit(text, (self.pos.x, self.pos.y))

        