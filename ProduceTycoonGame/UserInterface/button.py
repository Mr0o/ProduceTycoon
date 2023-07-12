import pygame

from ProduceTycoonGame.vectors import Vector
from ProduceTycoonGame.tileMap import TileMap, createStaticTileSurface
from ProduceTycoonGame.tile import Type
from ProduceTycoonGame.UserInterface.elements import Element


class Button(Element):
    def __init__(self, screen: pygame.Surface, pos: Vector, tileMap: TileMap, isSelected: bool, text = "3x3"):
        super().__init__(screen, pos, tileMap, isSelected)
        self.text = text
        self.color = (0, 0, 255)
        self.showRect = False
        self.posBut = Vector(0, 0)

        
        self.interactableRect = pygame.Rect(0, 0, screen.get_height() // 25 * 3, screen.get_height() // 25 * 3)
    
    def events(self, mouseClicked: bool):
        if self.showRect:
            for tile in self.tileMap.tileMapGrid:
                if tile.rect.collidepoint(pygame.mouse.get_pos()):
                    self.posBut.x = tile.pos.x + tile.size / 2 
                    self.posBut.y = tile.pos.y + tile.size / 2
                if self.interactableRect.colliderect(tile.rect) and mouseClicked:
                    tile.type = Type.INTERACTABLE
                    self.tileMap.staticSurface = createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)
                    self.showRect = False
        if self.rect.collidepoint(pygame.mouse.get_pos()) and mouseClicked:
            self.color = (0, 123, 255)
            self.showRect = True
        else:
            self.color = (100, 123, 0)
        


    def update(self):
        self.interactableRect.center = (self.posInteractable.x, self.posInteractable.y)
        createStaticTileSurface(self.tileMap.tileMapGrid, self.tileMap.width, self.tileMap.height)
        

    def draw(self):
        objectSize = pygame.font.SysFont('Arial', 15, bold=True)
        text = objectSize.render(self.text, True, (0, 0, 0))

        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(text, (self.pos.x, self.pos.y))

        if self.showRect:
            pygame.draw.rect(self.screen, self.color, self.interactableRect)